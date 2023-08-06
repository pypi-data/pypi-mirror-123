import os
import glob
import numpy as np
from sklearn.metrics import auc
from sklearn.metrics import roc_curve

algorithms = ['xgboost', 'svm','dnn']
indir = 'logs'
outdir = 'output'

def combine_auc(data):
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    for d in data:
        fpr = d['fpr']
        tpr = d['tpr']
        aucs.append(auc(fpr, tpr))
        interp_tpr = np.interp(mean_fpr, fpr, tpr)
        interp_tpr[0] = 0.0
        tprs.append(interp_tpr)
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    return {'fpr':mean_fpr, 'tpr':mean_tpr, 'auc': mean_auc,'std_auc':std_auc}


data = {}
for algo in algorithms:
    data[algo] = {}
    temp = [dict(np.load(f, allow_pickle=True)) for f in glob.glob(os.path.join(indir, algo+'_*.npz'))]
    for t in temp:
        n_feature = int(t['feature_dimension'])
        n_event = int(t['train_size']) 
        if (n_feature, n_event) not in data[algo]:
            data[algo][(n_feature, n_event)] = {'raw': []}
        fpr, tpr, _ = roc_curve(t['y_test'], t['score'])
        data[algo][(n_feature, n_event)]['raw'].append({'fpr':fpr,'tpr':tpr})
    for key in data[algo]:
        data[algo][key].update(combine_auc(data[algo][key]['raw']))

if not os.path.exists(outdir):
    os.makedirs(outdir, exist_ok=True)

    
np.savez(os.path.join(outdir, 'combined_result.npz'), **data)
