import os
from typing import List, Dict, Union, Optional
from itertools import combinations, combinations_with_replacement
import json

import numpy as np
import pandas as pd
from numba import jit

import xgboost as xgb

class EventCategorization:
    def __init__(self, input_dir:str, channel:str, processes:List, 
                 configuration:Union[str, Dict], fold:int=2,
                 n_bins:int=200, n_boundaries:int=2, min_yy_yield:float=2.,
                 data_preprocessor=None):
        self.input_dir = input_dir
        self.channel = channel
        self.processes = processes
        self.n_bins = n_bins
        self.n_boundaries = n_boundaries
        self.min_yy_yield = min_yy_yield
        self.fold = fold        
        self.load_configuration(configuration)
        self.load_inputs(input_dir)
        self.data_preprocessor = data_preprocessor
        
        self.data_hists = {}
        self.signal_hist = None
        self.background_hist = None
        self.summary = None
    
    def load_inputs(self, input_dir:str):
        df = {}
        weight_variable = self.variables['weight']
        fold_variable    = self.variables['fold']
        for process in self.processes:
            csv_path = os.path.join(input_dir, self.channel, f"{process}.csv")
            print(f"INFO: Loading inputs for the process `{process}` from `{csv_path}`")
            df[process] = pd.read_csv(csv_path)
            weight_expr = f"{weight_variable} * {self.selection[process]}"
            if (self.fold is not None) and (process in self.train_processes):
                weight_expr += f" * 4. * ({fold_variable} % 4 == {self.fold})"
            weight_expr = weight_expr.replace("&&", "&")
            weight_expr = weight_expr.replace("!", "not")
            df[process]['weight_total'] = df[process].eval(weight_expr)
        self.df = df
        
    def apply_scores(self, model):
        score_variable = self.variables['score']
        for process in self.processes:
            proc_train_data = self.df[process][self.train_variables]
            if isinstance(model, xgb.core.Booster):
                proc_train_data = xgb.DMatrix(proc_train_data)
            if self.data_preprocessor is not None:
                proc_train_data = self.data_preprocessor(proc_train_data)
            score = model.predict(proc_train_data)
            self.df[process][score_variable] = score
        self.load_data_hists()
        
    def load_configuration(self, configuration:Union[str, Dict]):
        if isinstance(configuration, str):
            with open(configuration, 'r') as f:
                self.configuration = json.load(f)
        elif isinstance(configuration, dict):
            self.configuration = configuration
        else:
            raise ValueError("unsupported config format")
        self.sig_processes = self.configuration['processes']['signal']
        self.bkg_processes = self.configuration['processes']['background']
        self.train_processes = self.configuration['processes']['train']
        self.train_variables = self.configuration['train_variables']
        self.selection = self.configuration['selection']
        self.variables = self.configuration['variables']
        
    def load_data_hists(self):
        score_variable = self.variables['score']
        bins = np.arange(0, 1, 1/self.n_bins)
        data_hists = {}
        for process in self.processes:
            if score_variable not in self.df[process]:
                raise RuntimeError("model scores are not initialized")
            digits = np.digitize(self.df[process][score_variable], bins)
            group  = self.df[process].groupby(digits)
            bin_values = group['weight_total'].sum().values
            bin_indices = group['weight_total'].sum().index.values - 1
            data_hists[process] = np.zeros(self.n_bins)
            data_hists[process][bin_indices] = bin_values
        signal_hist = np.zeros(self.n_bins)
        background_hist = np.zeros(self.n_bins)
        for process in data_hists:
            if process in self.sig_processes:
                signal_hist += data_hists[process]
            elif process in self.bkg_processes:
                background_hist += data_hists[process]
        self.data_hists = data_hists
        self.signal_hist = signal_hist
        self.background_hist = background_hist
    
    @staticmethod
    def get_significance(yield_s, yield_b):
        yield_tot = yield_s + yield_b
        return math.sqrt(2*((yield_tot*math.log(yield_tot/yield_b)) - yield_s))
    
    @staticmethod
    def get_boundary_indices(n_bins:int, n_cut=2):
        return np.array(list(combinations_with_replacement(range(n_bins), n_cut)))

    @staticmethod
    @jit(nopython=True)
    def _get_region_yields(data:np.ndarray, boundary_indices:np.ndarray):
        return [[np.sum(region) for region in np.split(data, indices)] for indices in boundary_indices]
    
    @staticmethod
    def get_region_yields(data:np.ndarray, boundary_indices:np.ndarray):
        # remove the first region
        return np.array(EventCategorization._get_region_yields(data, boundary_indices))[:, 1:]
    
    @staticmethod
    def get_combined_significance(yield_s:np.ndarray, yield_b:np.ndarray):
        yield_tot = yield_s + yield_b
        Z2 = 2*((yield_tot*np.log(yield_tot/yield_b)) - yield_s)
        combined_Z = np.sqrt(np.sum(Z2, axis=1))
        return combined_Z    
    
    def scan_bounds(self):
        if not self.data_hists:
            raise RuntimeError("data histograms are not initialized")
        boundary_indices = self.get_boundary_indices(self.n_bins, self.n_boundaries)
        yy_yields = self.get_region_yields(self.data_hists['yy'], boundary_indices)
        signal_yields = self.get_region_yields(self.signal_hist, boundary_indices)
        background_yields = self.get_region_yields(self.background_hist, boundary_indices)
        # filter boundaries which the regions contain no signal or background yields
        valid_boundaries = np.all(background_yields != 0., axis=1) & np.all(signal_yields != 0., axis=1) 
        # filter boundaries which the regions contain yy backgrounds less than the minimum required yields
        valid_boundaries &= np.all(yy_yields > self.min_yy_yield, axis=1)
        combined_significances = self.get_combined_significance(signal_yields[valid_boundaries], 
                                                                background_yields[valid_boundaries])
        bins = np.arange(0, 1, 1/self.n_bins)
        max_boundary_idx = np.argmax(combined_significances)
        max_significance = combined_significances[max_boundary_idx]
        max_bins         = boundary_indices[valid_boundaries][max_boundary_idx]
        max_boundary     = [bins[i] for i in max_bins]
        
        result = {
            'boundaries'  : max_boundary,
            'significance': max_significance 
        }
        self.summary = result
        return result