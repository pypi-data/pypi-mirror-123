import pandas as pd

'''
    extract features and targets list from the csv
'''
def csv_extractor(config):
    train_config = config.data.dataset.train
    
    if 'valid' in config.data.dataset.keys():
        valid_config = config.data.dataset.valid
    else:
        valid_config = None
    
    train_features, train_targets, valid_features, valid_targets = [], [], [], []
    
    return train_features, valid_features, train_targets, valid_targets