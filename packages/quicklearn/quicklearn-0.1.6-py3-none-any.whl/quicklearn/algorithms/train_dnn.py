#!/usr/bin/env python

import os
import traceback
import json
import argparse
import sys
import logging

import time
import datetime
import math
import numpy as np

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import mean_squared_error
from tensorflow import keras

import tensorflow as tf

from quicklearn.algorithms.dnn_logger import DNNLogger


def train_dnn(x_train, y_train, x_val, y_val, x_test, y_test, batch_size=64, epochs=1000, filename=None, log_dir='./logs', search_space=None, extra_attributes={},**kwargs):
    attributes = {}
    attributes['feature_dimension'] = x_train.shape[1]
    attributes['train_size'] = x_train.shape[0]
    attributes['test_size'] = x_test.shape[0]
    attributes['epochs'] = epochs
    attributes['batch_size'] = batch_size

    logger = DNNLogger(attributes, filename=filename, log_dir=log_dir, extra_attributes=extra_attributes)
    model = keras.Sequential([
         keras.layers.Input(shape=attributes['feature_dimension']),
         #keras.layers.Dense(args.nqubits, activation='relu',),
         keras.layers.Dense(64, activation='relu'),
         keras.layers.Dense(16, activation='relu'),
         keras.layers.Dropout(0.1),
         keras.layers.Dense(1, activation='sigmoid'),
    ])


    print(model.summary())

    model.compile(
        loss='mse',
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
        metrics=['accuracy',tf.keras.metrics.AUC()])


    logging.info(model.summary())

    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
 
    model.fit(
            x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=1,
            validation_data=(x_val, y_val),
            callbacks=[callback])

    logger.on_train_end(model, x_test, y_test)

    return model
