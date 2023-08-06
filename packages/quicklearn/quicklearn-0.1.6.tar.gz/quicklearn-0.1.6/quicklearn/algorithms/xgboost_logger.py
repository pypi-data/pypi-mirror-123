import os
import time
import datetime
import logging

import numpy as np
import quple

from sklearn.metrics import accuracy_score,roc_auc_score, auc, roc_curve

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DefaultDict(dict):
    def __missing__(self, key):
        return key
    
class XGBoostLogger():
    """Logger for the quantum support vector machine classifer (QSVM)
    
    """
    DEFAULT_FILENAME = 'xgboost_feature_dimension_{feature_dimension}_'+\
                 'train_{train_size}_'+\
                 'test_{test_size}_{time}'
    def __init__(self, attributes,
                 log_dir='./logs', 
                 filename=None,
                 keys=None,
                 stream_level=logging.INFO,
                 file_level=logging.DEBUG,
                 formatter=None,
                 save_npz=True,
                 extra_attributes={}):
        if filename == None:
          filename = self.DEFAULT_FILENAME
        self.log_dir = log_dir
        self.filename = filename
        self.keys = keys
        self.stream_level = stream_level
        self.file_level = file_level
        self.stream_handler = None
        self.file_handler = None
        self.formatter = formatter or logging.Formatter('%(asctime)s [%(threadName)-12.12s]'
                                                         '[%(levelname)-5.5s]  %(message)s')
        self.time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S-%f')
        self.logger_is_set = False
        self.save_npz = save_npz
        self.attributes = extra_attributes
        self.attributes.update(attributes)
        self.start_time = time.time()
        self.setup_logger()
        
    def reset_logger(self):
        self.file_handler.close()
        logger.removeHandler(self.stream_handler)
        logger.removeHandler(self.file_handler)
        self.logger_is_set = False
        
    def setup_logger(self):
        if self.logger_is_set:
            return
        # setup stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.stream_level)
        stream_handler.setFormatter(self.formatter)
        
        self.attributes['time'] = self.time
        self.attributes = DefaultDict(self.attributes)
        self.formatted_filename = os.path.join(self.log_dir, self.filename.format(**self.attributes))
        log_filename = self.formatted_filename + '.log'
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(self.file_level)
        file_handler.setFormatter(self.formatter)
        self.stream_handler = stream_handler
        self.file_handler = file_handler
        
        #setup logger
        logger.addHandler(self.stream_handler)
        logger.addHandler(self.file_handler)
        self.logger_is_set = True
        self.print_attributes()
        
    def print_attributes(self):
        attrib = self.attributes.copy()
        logger.info('######## Executing XGBoost with the following attributes ########')
        logger.info('Feature Dimension: {}'.format(attrib.pop('feature_dimension','')))                           
        logger.info('Train Size: {}'.format(attrib.pop('train_size','')))
        logger.info('Test Size: {}'.format(attrib.pop('test_size','')))  
        for k,v in attrib.items():
            logger.info('{}: {}'.format(k.replace('_',' ').title(),v)) 
        logger.info('#################################################################')
        
    def info(self, text):
        logger.info(text)
        
    def on_train_end(self, clf, x_test, y_test):
        logger.info('######################## Training Ends ##########################')
            
        score = clf.predict_proba(x_test)[:,1]
        predictions = [round(value) for value in score]
        accuracy = accuracy_score(y_test, predictions)
        fpr, tpr, _ = roc_curve(y_test, score)
        roc_auc = auc(fpr, tpr)

        print("Test AUC:", roc_auc)
        print("Accuracy:", accuracy)

        result = {'score': score,
                  'y_test': y_test,
                  'auc': roc_auc,
                  'accuracy':accuracy}

        self.end_time = time.time()
        
        self.attributes['time_taken'] = self.end_time - self.start_time
        
        logger.info("Time taken: %s" % self.attributes['time_taken'])

        if self.save_npz:
            np.savez(self.formatted_filename +'.npz', 
                    result=result,
                    **self.attributes)
        
        self.reset_logger()    
