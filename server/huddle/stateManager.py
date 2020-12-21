
#Keeps track of the state of a room
class StateManager(object):
    
    """Object for tracking stored data"""
    def __init__(self):
        self.storedData = [{ "id": 0, "components": [] }]

    def update_state(self, new_state):
        self.storedData = new_state

    def getSingleData(self, key):
        for item in self.storedData:
            if item.id == key:
                return item
        return None

    def getAllData(self):
        return self.storedData

    def update_circle_rad(self, sid, cid, value):
        for item in self.storedData:
            for component in item["components"]:
                if component["c_id"] == cid and component["s_id"] == sid:
                    
                    component["r"] = value
                    return component
        return None

    def update_rect_sides(self, sid, cid, w, l):
        for item in self.storedData:
            for component in item["components"]:
                if component["c_id"] == cid and component["s_id"] == sid: 
                    component["w"] = w
                    component["l"] = l
                    return component
        return None