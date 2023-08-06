from projectaile.utils.exceptions import _EXCEPTION_LIST_

# Generates all exceptions in projectaile, used for logging.
class EXCEPTION_HANDLER:
    def __init__(self):
        pass
    
    # Generate Exception Strings
    def generate_exception(
            self, 
            exception_source: str='default', 
            exception_name: str='base_exception', 
            params: dict={'params_name' : {}}
        )-> str:
        
        exception_source_exists = exception_source in _EXCEPTION_LIST_.keys()
        
        exception_source = exception_source if exception_source_exists else 'default'
        
        exception_exists = exception_name in _EXCEPTION_LIST_[exception_source].keys()
        
        exception_name = exception_name if exception_exists else 'base_exception'
        
        base_exception_string = _EXCEPTION_LIST_[exception_source][exception_name] 
        
        exception = base_exception_string.format_map(params)
        
        return exception