from huddle.stateManager import StateManager

#Communicates between clients and state/widget manager
class Router(object):
    workspace_ids = set()

    """Object for tracking game stats"""
    def __init__(self):
        self.state_manager = StateManager()

    def getState(self):
        return self.state_manager.getAllData()

