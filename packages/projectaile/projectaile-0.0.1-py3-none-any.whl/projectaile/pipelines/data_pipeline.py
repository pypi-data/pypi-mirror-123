'''
    ProjectAile data pipeline module

'''

# imports
from functools import wraps
from projectaile.loggers import LOGGER
from .pipeline import PIPELINE

'''
    Pipeline Base Class. Create a pipeline with callables that are called and
    intermediate states can be logged or altered.
'''
class DATA_PIPELINE(PIPELINE):
    def __init__(self, config=None):
        super(DATA_PIPELINE, self).__init__(config, 'data_pipeline')
        
        self.callables = {}  
        
    # Used to fetch prebuilt pipelines
    def _create_pipeline_from_config_(self, config):
        return
    
    def _init_callable_(self, callable_method):
        self.callables[callable_method.__name__] = callable_method
        callable_method.__pipeline_order__ = len(self.callables.keys()) + 1
        callable_method.__pipeline_def__ = self.pipeline_type
        callable_method.__log__ = True
        callable_method.__logger__ = self.logger
        callable_method.__return_state__ = True
            
    '''
        callable : decorator to make a function into a pipeline callable component and
                associate important properties like the logger to it.
        
    '''
    def callable(self, callable_method):
        self._init_callable_(callable_method)
        @wraps(callable_method)
        def wrapper(*args, **kwargs):
            self.logger.log(f'Adding Callable : {callable_method.__name__} to {self.pipeline_type}')
            return callable_method(*args, **kwargs)
        
        return wrapper
    
    def run(self, x, y):
        for callable in self.callables:
            x, y = self.callables(x, y)
            
        return x, y