import os
import atexit
from enum import Enum
from collections import namedtuple
from typing import Callable
from .timer import Timer
from .to_string import obj_to_string

class LogLevel(Enum):
    TRACE='[TRACE]'
    DEBUG='[DEBUG]'
    INFO='[INFO]'
    WARN='[WARN]'
    ERROR='[ERROR]'

LogEntry = namedtuple("LogEntry", "time log_level entity content")

class LogDir:
    default_path = 'logs'
    def get_path(file_name, *dirs):
        path_args = [ LogDir.default_path ]
        dirs = [ _dir for _dir in dirs if _dir] # remove None
        if dirs:
            path_args.extend(dirs)
        path_args.append(file_name)
        path = os.path.join(*path_args)
        return path

class LogWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        
    def write(self, log_entry: LogEntry):
        # format log
        text = f'{log_entry.time}, {log_entry.log_level.value}, {log_entry.entity}, {log_entry.content}\n'
        self.file.write(text)
            
    def __enter__(self):
        if not self.file:
            dir_path = '/'.join(self.file_path.split('/')[0:-1])
            os.makedirs(dir_path, exist_ok=True)

        self.file = open(self.file_path, 'w')
        return self
  
    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()
        if exception_type:
            print(exception_type, exception_value, traceback)


class LogFormatterManager:
    def __init__(self):
        self.formatters = {}

    def register_formatter(self, entity, formatter):
        self.formatters[entity] = formatter

    def get(self, entity) -> Callable:
        f = self.formatters.get(entity)
        return f if f else obj_to_string

class Logger:
    '''  
    In memory logger, writes file when logger is destroyed. 
    Used together with ContextualLogger for control in where to write logs.
    Uses a custom timer for getting the time of log entries
    '''
    
    default_level = LogLevel.DEBUG

    def __init__(self, log_writer: LogWriter, timer: Timer, lfm: LogFormatterManager, default_level = LogLevel.DEBUG):
        self.log_queue = []
        self.timer, self.log_writer, self.lfm, self.default_level = timer, log_writer, lfm, default_level
        
    def log(self, content, entity = None, level=None, **other_params):
        level = level if level else self.default_level
        time = self.timer.now()
        formatter = self.lfm.get(entity)
        content = formatter(content, **other_params)
        self.log_queue.append(LogEntry(time, level, entity, content))

    def log_each_in_map(self, map_content:dict, **other_params):
        for key, content in map_content.items():
            self.log(content, key=key, **other_params)

    def flush(self):
        if not self.log_queue:
            return

        with self.log_writer as lw:
            for item in self.log_queue:
                lw.write(item)
            self.log_queue.clear()
    
    def __del__(self):
        if self.log_queue:
            print('logger is being destroied without being flushed')
            try:
                self.flush()
            except Exception as e:
                print('log was lost')
                print(self.log_queue)
                raise Exception('not flushed log')


class ContextualLogger:
    def __init__(self, timer: Timer, lfm: LogFormatterManager, default_level = LogLevel.DEBUG):
        self.timer, self.lfm = timer, lfm
        self.default_level = default_level
        self.loggers_map: dict[str, Logger] = {}
        self.group_context = None
        atexit.register(self.end_all_contexts) # flush before exit
        
    def get_logger(self, context_name, init_message=None) -> Logger:
        
        if not self.loggers_map.get(context_name):
            file_path = LogDir.get_path(f'{context_name}.log', self.group_context)
            logger = Logger(log_writer=LogWriter(file_path), timer=self.timer, lfm=self.lfm)
            self.loggers_map[context_name] = logger
            if init_message:
                logger.log(init_message, level=LogLevel.INFO)

        return self.loggers_map[context_name]

    def start_group_context(self, group_context):
        self.group_context = group_context

    def end_logger_context(self, context_name):
        self.loggers_map[context_name].flush()
        self.loggers_map[context_name] = None
    
    def end_all_contexts(self):
        for context, logger in self.loggers_map.items():
            if logger:
                logger.flush()
            else:
                print(f'log context "{context}"" can`t be closed' )
        self.loggers_map.clear()