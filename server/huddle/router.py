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

    def update_circle_rad(self, sid, cid, value):
        self.state_manager.update_circle_rad(sid, cid, value)

    def update_rect_sides(self, sid, cid, w, l):
        self.state_manager.update_rect_sides(sid, cid, w, l)

