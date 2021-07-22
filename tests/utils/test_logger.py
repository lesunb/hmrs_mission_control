
import os
import pytest
from lagom import Container

from utils.logger import Logger, LogWriter, ContextualLogger, LogDir


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    #pass
    files_to_clear = ['tmp/test_logger.log', 'tmp/fib1.log', 'tmp/fib2.log']

    for file in files_to_clear:
        if os.path.isfile(file):
            os.remove(file)


def fib(l: Logger, end = 100):
    fib1 =0
    fib2 =1
    for _ in range(0, end):
        l.log(f'fib: {fib2}')
        fib1, fib2 = fib2,  fib1 + fib2



def test_logger():
    container = Container()
    container[LogWriter] = LogWriter('tmp/test_logger.log')
    l = container[Logger]
    fib(l) # logs 100 first fib numbers
    l.log('end!')
    # check file creating was delayed
    assert not os.path.isfile('tmp/test_logger.log')
    
    l.flush() # force a flush
    # assert file was created
    assert os.path.isfile('tmp/test_logger.log')


def test_contextual_logger():
    container = Container()
    cl = container[ContextualLogger]
    LogDir.default_path = 'tmp'

    FIB1_FILE_PATH = os.path.join('tmp', 'fib1.log')
    FIB2_FILE_PATH = os.path.join('tmp', 'fib2.log')

    lfib1 = cl.get_logger('fib1', 'init context!')
    fib(lfib1)
    lfib1 = cl.get_logger('fib1', 'init context!')
    fib(lfib1)
    
    assert not os.path.isfile(FIB1_FILE_PATH)
    cl.end_logger_context('fib1')
    assert os.path.isfile(FIB1_FILE_PATH)

    lfib2 = cl.get_logger('fib2')
    fib(lfib2)
    cl.end_logger_context('fib2')
    assert os.path.isfile(FIB2_FILE_PATH)

    