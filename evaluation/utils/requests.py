
from mission_control.data_model.restrictions import Request


def create_from_str(input_str: str):
    pairs = input_str.split(';')
    for pair in pairs:
        parameters = pair.split(',')
        yield Request(*parameters)

        
        
