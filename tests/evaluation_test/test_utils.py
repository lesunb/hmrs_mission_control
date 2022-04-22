

from evaluation.utils.requests import create_from_str



def test_create_requests_from_str():
    requests = list(create_from_str('room1,100;room3,300'))

    assert requests[0].timestamp == '100'
    assert requests[1].timestamp == '300'


