from huddle.stateManager import StateManager

#Communicates between clients and state/widget manager
class Router(object):

    """Object for tracking game stats"""
    def __init__(self):
        self.state_manager = StateManager()

    def get_updated_slide(self, key):
        return self.state_manager.getSingleData(key)

    def get_state(self):
        return self.state_manager.getAllData()

    def update_state(self, new_state):
        self.state_manager.update_state(new_state)

    def add_new_component(self, component):
        self.state_manager.add_new_component(component)
        
    def update_component(self, component):
        self.state_manager.update_component(component)

    def update_component_id(self, sid, cid, changes):
        self.state_manager.update_component_id(sid, cid, changes)

    def add_new_slide(self):
        self.state_manager.add_new_slide()

    def add_new_connection(self, sid, cid0, cid1, signal, slot, expression):
        self.state_manager.add_new_connection(sid, cid0, cid1, signal, slot, expression)
    
    def remove_connection(self, sid, cid0, cid1, signal, slot):
        self.state_manager.remove_connection(sid, cid0, cid1, signal, slot)

