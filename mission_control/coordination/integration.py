
from abc import abstractmethod

from ..data_model import MissionContext


class MissionError(Exception):
    def __init__(self, orignal_error, message):
        pass

class MissionUnnexpectedError(Exception):
    def __init__(self, orignal_error, message):
        pass

class MissionHandler:
    """
    Interface provided by the Ensemble Layer for the Mission Management 
    Processses of the Coordinator 
    """
    @abstractmethod
    def start_mission(self, mission_context):
        pass

    @abstractmethod
    def no_coalition_available(self, mission_context: MissionContext):
        pass
    
    @abstractmethod
    def update_assigments(self, mission_context: MissionContext):
        pass
        
    @abstractmethod
    def end_mission():
        pass
    
    @abstractmethod
    def completed_assignment():
        pass
    
    @abstractmethod
    def notify_operator():
        pass

    @abstractmethod
    def status_update_to_user():
        pass

    @abstractmethod
    def queue_request():
        pass

    @abstractmethod
    def handle_unnexpected_error(self, error: MissionUnnexpectedError):
        """ 
            Should handle internal error in the mission management process
        """
        print(error.message)
        print(error.orignal_error)
