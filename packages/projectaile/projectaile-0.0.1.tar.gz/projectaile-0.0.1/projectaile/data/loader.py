import numpy as np
from functools import wraps
from projectaile.utils.base_class import BASE
from projectaile.data.extractors import extractors


'''
    LOADER class, acts as a base class for different types of loaders.
    different loaders like image, audio, text etc. can be decorated to act
    as loader functions and can be called from this class to generate batches
    and feed to the feeder, which then feeds to the data pipeline,
    where preprocessing an augmentations can be applied.
'''
class LOADER(BASE):
    def __init__(self, loader_function):
        self._loader = loader_function
        
    def init_loader(self):
        super(LOADER, self).__init__('loader')
        
    '''
    get_data_info : extracts base information about the data for generating batches and using
                    it for getting batches of data from the feeders.
                
    '''    
    # Getting indices and features and targets for the dataset.
    def get_data_info(self):
        if self._config.data.split == 0.0:
            interface_type = self._config.data.dataset.train.interface_type
        else:
            interface_type = self._config.data.dataset.interface_type
                
        if interface_type in extractors.keys():
            train_features, valid_features, train_targets, valid_targets = extractors[interface_type](self._config)
        else:
            params = {'interface_type': interface_type}
            self.exception('no_extractor', params)
            exit(0)

        self.train_features = train_features
        self.train_targets = train_targets
        self.train_indices = np.arange(0, len(train_features))
        self.valid_features = valid_features
        self.valid_targets = valid_targets
        self.valid_indices = np.arange(0, len(valid_features))
    
    '''
        load a single example using the feature and target
        value at current index.
    '''
    def load(self, feature, target):
        if self._config.data.data_type == 'structured':
            return feature, target
        else:
            if self._loader:
                return self._loader(feature, target)
            else:
                params = {'data_type' : self._config.data.data_type}
                raise self.exception('no_loader', params)
    
    '''
        load a batch of size batch_size and update the iterator 
        for next batch
    '''
    def load_batch(self, mode='train', itertator=0, batch_size=1, shuffle=False):
        if mode == 'train':
            indices = self.train_indices
            features = self.train_features
            targets = self.train_targets
            
        elif mode == 'valid':
            indices = self.valid_indices
            features = self.valid_features
            targets = self.valid_targets
            
        if shuffle:
            indices = np.random.shuffle(indices)
        
        indices = indices[iterator*batch_size:(iterator+1)*batch_size]
        
        x, y = [], []
        
        for idx in indices:
            try:
                feature, target = self.load(features[idx], targets[idx])
                x.append(feature)
                y.append(target)
            except Exception as e:
                self.exception('load_failed', e)
                return None, None, iterator
        
        iterator += 1
        
        if iterator > len(indices)//batch_size:
            iterator = 0
            
        return np.array(x), np.array(y), iterator