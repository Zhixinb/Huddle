
#Keeps track of the state of a room
class StateManager(object):
    
    """Object for tracking stored data"""
    def __init__(self):
        self.storedData = {0: {"id": 0, "components": {}, "connections": {}, "next_c_id": 0}}
        self.next_sid = 1

    def update_state(self, new_state):
        self.storedData = new_state
        #to-do: make sure next_sid stays updated

    def getSingleData(self, key):
        if key in self.storedData:
            return self.storedData[key]
        return None

    def getAllData(self):
        return self.storedData
        
    def add_new_component(self, component):
        sid = component["s_id"]
        if sid in self.storedData:
            slide = self.storedData[sid]
            cid = slide["next_c_id"]
            component["c_id"] = cid
            slide["next_c_id"] += 1
            slide["components"][cid] = component
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

    def add_new_slide(self):
        #self.storedData[self.next_sid] = {"id": self.next_sid, "components": {}, "connections": {}, "next_c_id": 0}
        self.storedData[len(self.storedData)] = {"id": self.next_sid, "components": {}, "connections": {}, "next_c_id": 0}
        self.next_sid += 1

    def add_new_connection(self, sid, cid0, cid1, signal, slot):
        if sid in self.storedData:
            components = self.storedData[sid]["components"]
            if cid0 in components and cid1 in components:
                connections = self.storedData[sid]["connections"]
                if (cid0 not in connections):
                    connections[cid0] = {}
                if (signal not in connections[cid0]):
                    connections[cid0][signal] = []
                connections[cid0][signal].append((cid1, slot))
                return True
        return False
