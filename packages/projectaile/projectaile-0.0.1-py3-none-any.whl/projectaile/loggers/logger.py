'''
    projectaile LOGGER
'''

import os
import atexit
import datetime
from rich.console import Console
from rich.traceback import install
from rich.logging import RichHandler
from projectaile.utils.exception_handler import EXCEPTION_HANDLER
from pyinstrument import Profiler

'''
    LOGGER : logger class for creating a log file.
    
    logs both in the terminal using rich's beautiful logger
    and also saves the logs to a logs file
    
    Used to track exceptions throughout the projectaile engine
    Has some inbuilt exceptions for projectaile specific classes
    and supports graceful error handling for tensorflow, pytorch and sklearn.
'''


class LOGGER:
    '''
        create a LOGGER intance and initialize the exception handler

        the logger instance is global for a projectaile project as it is
        a part of the base class. It automatically captures exceptions and
        errors for different engine components.
    '''

    def __init__(self):
        self.logger_name = 'base logger'
        self.commit = False

    '''
        initializes exception handlers and loggers for 
        python, tensorflow, pytorch, sklearn etc.
    '''
    def initialize(self):
        self.console = Console(record=True)
        self.exception_handler = EXCEPTION_HANDLER()
        self.profiler = Profiler()
        
        self.log_info('Initializing Loggers and Handlers...')
        rich_exception_handler = RichHandler(rich_tracebacks=True, markup=True)

        _possible_loggers = {}
        
        # Set exit commit
        atexit.register(self._exit_commit)
        
        # Set Pythons traceback handler
        install(console=self.console)

        # Set python logging logger
        import logging

        _possible_loggers['python_logging'] = logging.getLogger('')

        # Set tensorflow logger
        try:
            import tensorflow as tf
            from tensorflow.python.platform import tf_logging
            _tf_version = None
            try:
                _tf_version = tf.__version__
            except Exception as e:
                self.log_info('No __version__ property found on tensorflow')

            if _tf_version[0] == '2':
                _possible_loggers['tensorflow'] = tf_logging.get_logger()
            else:
                _possible_loggers['tensorflow'] = tf_logging._get_logger()

        except Exception as e:
            self.log_warning(
                f'Tensorflow not installed or tf_logging not found.\
                Exception Message : {e}'
            )

        # TODO : Set pytorch logger
        try:
            import torch
        except Exception as e:
            self.log_warning(
                f'Pytorch not installed or pytorch_logging not found.\
                Exception Message : {e}'
            )

        # Setting handlers for all loggers
        for logger_name, logger in _possible_loggers.items():
            self.log_info(f'Setting handler for {logger_name}.')
            try:
                logger.setLevel(self._log_level)
            except Exception as e:
                self.log_warning('Couldnt set logging level using setLevel')
                try:
                    logger.set_level(self._log_level)
                except Exception as e:
                    self.log_warning(
                        f'Could not set level for logging in {logger_name} logger, {e}'
                    )
            logger.handlers = [rich_exception_handler]
            self.log_info(f'Setting handler for {logger_name} successful.')        
    
    '''
        set log file path and log level
    '''
    def set_params(self, logs_path='logs/', log_level='DEBUG'):
        self._log_level = log_level
        self.log_file = (os.path.join(os.getcwd(), logs_path))+'/.logs'
        self.commit = True
        self.initialize()

    '''
        prints a log to the terminal and saves text to the logs file.
        
        params : 
            log_message : str : the message to be written to the terminal 
            and to the file
    '''
    def print_log(self, log_message: str):
        self.console.log(log_message)
        if self.commit:
            self._commit()

    '''
        prints a log as info (green text) to the terminal 
        and saves text to the logs file.
        
        params : 
            log_message : str : the message to be written to the terminal 
            and to the file
    '''
    def log_info(self, log_message: str):
        message = f'[green]INFO : {log_message}[/]'
        self.print_log(message)

    '''
        prints a log as warning (red text) to the terminal 
        and saves text to the logs file.
        
        params : 
            log_message : str : the message to be written to the terminal 
            and to the file
    '''
    def log_warning(self, log_message: str):
        message = f'[yellow]WARNING : {log_message}[/]'
        self.print_log(message)

    '''
        prints a log as exception (formatted according to exceptions.py) 
        to the terminal and saves text to the logs file.
        
        params : 
            exception_sources : str : the projectaile component producing the exception
            exception_name : str : type of exception produced
            params : dict : key-val pairs of parameters that were passed to the component
    '''
    def log_exception(self,
                      exception_source: str = 'default',
                      exception_name: str = 'base_exception',
                      params: dict = {'params': {}}
                      ):
        exception = self.exception_handler.generate_exception(
            exception_source, exception_name, params)
        self.print_log(exception)

    '''
        saves the current data buffer to the text file path saved in self.log_file
    '''
    def _commit(self, clear=False):
        self.console.save_text(self.log_file, clear=clear)

    '''
        write the commits to timestamped logs file on exit
    '''
    def _exit_commit(self):
        time_stamp = datetime.datetime.now()
        
        if self.commit:
            file_name = self.log_file+'_'+str(time_stamp)\
                                            .replace(' ', '')\
                                            .replace('.', '_')\
                                            .replace(':', '_')
            self.console.save_text(file_name, clear=True)
            
            if os.path.exists(self.log_file):
                os.remove(self.log_file)

        del self.console

    '''
        deletes the current console instance clearing it's record buffer and creates
        a new console instance
    '''
    def _clear_record(self):
        self._commit()
        del self.console
        self.console = Console(record=True)