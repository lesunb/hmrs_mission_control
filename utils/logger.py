import os
from enum import Enum
from collections import namedtuple
from .timer import Timer

class LogLevel(Enum):
    TRACE='[TRACE]'
    DEBUG='[DEBUG]'
    INFO='[INFO]'
    WARN='[WARN]'
    ERROR='[ERROR]'

LogEntry = namedtuple("LogEntry", "time log_level entity content")

class LogDir:
    default_path = 'logs/'
    def get_path(file_name):
        return LogDir.default_path + file_name

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
        

class Logger:
    '''  
    In memory logger, writes file when logger is destroyed. 
    Used together with ContextualLogger for control in where to write logs.
    Uses a custom timer for getting the time of log entries
    '''
    
    default_level = LogLevel.DEBUG

    def __init__(self, log_writer: LogWriter, timer: Timer, default_level = LogLevel.DEBUG):
        self.log_queue = []
        self.timer, self.log_writer, self.default_level = timer, log_writer, default_level

    def log(self, content, entity = None, level=None):
        level = level if level else self.default_level
        time = self.timer.now()
        self.log_queue.append(LogEntry(time, level, entity, content))

    def flush(self):
        if not self.log_queue:
            return

        with self.log_writer as lw:
            for item in self.log_queue:
                lw.write(item)
            self.log_queue.clear()

    def __del__(self):
        self.flush()

class ContextualLogger:
    def __init__(self, timer: Timer, default_level = LogLevel.DEBUG):
        self.timer = timer
        self.default_level = default_level
        self.contexts = {}

    def get_logger(self, context_name, init_message=None):
        
        if not self.contexts.get(context_name):
            file_path = LogDir.get_path(file_name=f'{context_name}.log')

            logger = Logger(log_writer=LogWriter(file_path), timer=self.timer)
            self.contexts[context_name] = logger
            if init_message:
                logger.log(init_message, level=LogLevel.INFO)

        return self.contexts[context_name]


    def end_logger_context(self, context_name):
        self.contexts[context_name].__del__()
        self.contexts[context_name] = None
