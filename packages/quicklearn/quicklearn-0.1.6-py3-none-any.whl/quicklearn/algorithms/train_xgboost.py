#!/usr/bin/env python

import os
import logging
import time
import datetime
import numpy as np
import xgboost as xgb
from sklearn.model_selection import GridSearchCV

from quicklearn.algorithms.xgboost_logger import XGBoostLogger
from sklearn.model_selection import PredefinedSplit

_DEFAULT_BDT_SPACE_ = {'nthread':[4], #when use hyperthread, xgboost may become slower
              'objective':['binary:logistic'],
              'booster': ['gbtree'],
              'eval_metric': ['auc'],
              'learning_rate': [0.01,0.1,0.3], #so called `eta` value
              'max_depth': [3,6,8,11]}

def train_xgboost(x_train, y_train,  x_val, y_val, x_test, y_test, filename=None, log_dir='./logs', search_space=None, extra_attributes={}, cv=3, **kwargs):
    attributes = {}
    attributes['feature_dimension'] = x_train.shape[1]
    attributes['train_size'] = x_train.shape[0]
    attributes['test_size'] = x_test.shape[0]

    logger = XGBoostLogger(attributes, filename=filename, log_dir=log_dir, extra_attributes=extra_attributes)

    search_space = search_space or _DEFAULT_BDT_SPACE_

    if (x_val is None) and (y_val is None):
        X = x_train
        Y = y_train
        pds = cv
    else:
        X = np.concatenate((x_train, x_val), axis=0)
        Y = np.concatenate((y_train, y_val), axis=0)
        test_fold = [-1]*len(x_train)+[0]*len(x_val)
        pds = PredefinedSplit(test_fold=test_fold)

    xgb_model = xgb.XGBClassifier()

    clf = GridSearchCV(xgb_model, param_grid=search_space, n_jobs=-1, cv=pds, refit=False, scoring='roc_auc')

    clf.fit(X, Y)

    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']

    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        if mean == max(means):
            best_params_ = params

        logger.info("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

    logger.info("best parameters: %s" % best_params_)
    
    clf_best = xgb.XGBClassifier(**best_params_)
    clf_best.fit(x_train, y_train)

    logger.on_train_end(clf_best, x_test, y_test)    

    return clf
