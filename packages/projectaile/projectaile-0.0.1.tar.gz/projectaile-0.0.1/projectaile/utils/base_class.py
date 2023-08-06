import rich

from projectaile.loggers import LOGGER
from projectaile.utils.validator import VALIDATOR
from projectaile.utils.container import CONTAINER

'''
    Base Class For Initializing A Logger And A Validator
    Also Register Components and Save Entities To Container
'''
class BASE:
    def __init__(self, source='default'):
        self._source = source
        self.initialize()
    
    '''
        Initializes a component by validating config for that particular component
        and setting log levels and log files path. Also linking the logger and validator
    '''
    def initialize(self, *args, **kwargs):
        # Checking For Existing LOGGER Initialization
        if CONTAINER.is_registered('logger'):
            self._logger = CONTAINER.get_component('logger')
        else:
            self._logger = LOGGER()
            CONTAINER.register_component('logger', self._logger)
        
        # Checking For Existing VALIDATOR Initialization
        if CONTAINER.is_registered('validator'):
            self._validator = CONTAINER.get_component('validator')
        else:
            self._validator = VALIDATOR()
            CONTAINER.register_component('validator', self._validator)
            
        if CONTAINER.is_stored('config'):
            self.log('Found Config In Store')
            self._config = CONTAINER.get_entity('config')
        else:
            if self._config:
                isvalid = self._validate_config()
                if isvalid:
                    logger = CONTAINER.get_component('logger')
                    
                    logger.set_params(
                        logs_path = self._config.config_params.logger.logs_path,
                        log_level = self._config.config_params.logger.log_level
                    )
                    
                    CONTAINER.store_entity('config', self._config)
            else:
                self.warning('No Config Set.')
    
    '''
        Validate Config For The Particular Component
    '''
    def _validate_config(self):
        isvalid, missing_fields = self._validator.validate(self._config, self._source)
        
        if not isvalid:
            self.exception(
                'config', 
                'invalid_config', 
                {
                    'source': self._source,
                    'missing_fields' : [', '.join(missing_fields)]
                })
            
        return isvalid
    
    '''
        Log A Simple Log
    '''
    def log(self, message):
        self._logger.print_log(message)
    
    '''
        Log A Warning
    '''
    def warning(self, warning):
        self._logger.log_warning(warning)
        
    '''
        Log Info
    '''
    def info(self, info):
        self._logger.log_info(info)
    
    '''
        Log an Exception
    '''
    def exception(self, exception, params={}):
        params = params or locals()
        return self._logger.log_exception(self._source, exception, params)
    
    '''
        Run The Operation
    '''
    def run(self):
        pass
    