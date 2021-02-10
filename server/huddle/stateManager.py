
#Keeps track of the state of a room
class StateManager(object):
    
    """Object for tracking stored data"""
    def __init__(self):
        self.storedData = {0: {"id": 0, "components": {}, "connections": {}}}

    def update_state(self, new_state):
        self.storedData = new_state

    def getSingleData(self, key):
        if key in self.storedData:
            return self.storedData[key]
        return None

    def getAllData(self):
        return self.storedData
        
    def add_new_widget(self, component):
        sid = component["s_id"]
        cid = component["c_id"]
        if sid in self.storedData:
            self.storedData[sid]["components"][cid] = component
            return True
        return False

    def update_component(self, component):
        sid = component["s_id"]
        cid = component["c_id"]
        if sid in self.storedData:
            components = self.storedData[sid][["components"]]
            if cid in components:
                components[cid] = component
                return True
        return False
    
    def update_component_id(self, sid, cid, changes):
        if sid in self.storedData:
            components = self.storedData[sid]["components"]
            if cid in components:
                component = components[cid]
                for k in changes:
                    component[k] = changes[k]
                return True
        return False

    def add_new_slide(self, sid):
        if sid not in self.storedData:
            self.storedData[sid] = {"id": sid, "components": {}, "connections": {}}
            return True
        return False
