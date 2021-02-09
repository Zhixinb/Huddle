
#Keeps track of the state of a room
class StateManager(object):
    
    """Object for tracking stored data"""
    def __init__(self):
        self.storedData = [{ "id": 0, "components": {} }]

    def update_state(self, new_state):
        self.storedData = new_state

    def getSingleData(self, key):
        for item in self.storedData:
            if item["id"] == key:
                return item
        return None

    def getAllData(self):
        return self.storedData
        
    def add_new_widget(self, component):
        sid = component["s_id"]
        cid = component["c_id"]
        for item in self.storedData:
            if item["id"] == sid:
                item["components"][cid] = component
                return True
        return False

    def update_component(self, component):
        sid = component["s_id"]
        cid = component["c_id"]
        for item in self.storedData:
            if item["id"] == sid and cid in item["components"]:
                item["components"][cid] = component
                return True
        return False
    
    def update_component_id(self, sid, cid, changes):
        for item in self.storedData:
            if item["id"] == sid and cid in item["components"]:
                component = item["components"][cid]
                for k in changes:
                    component[k] = changes[k]
                return True
        return False

    def add_new_slide(self, sid):
        self.storedData.append({ "id": sid, "components": {} })
