
#Keeps track of the state of a room
class StateManager(object):
    
    """Object for tracking stored data"""
    def __init__(self):
        self.storedData = {"0": {"id": "0", "components": {}, "connections": {}, "backward_connections": {}, "next_c_id": 0}}
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
            cid = str(slide["next_c_id"])
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
        self.storedData[str(len(self.storedData))] = {"id": str(len(self.storedData)), "components": {}, "connections": {}, "backward_connections": {}, "next_c_id": 0}
        self.next_sid += 1

    def add_new_connection(self, sid, cid0, cid1, signal, slot, expression):
        if sid in self.storedData:
            components = self.storedData[sid]["components"]
            if cid0 in components and cid1 in components:
                d = self.storedData[sid]["connections"]
                if cid0 not in d:
                    d[cid0] = {}
                d = d[cid0]
                if signal not in d:
                    d[signal] = {}
                d = d[signal]
                if cid1 not in d:
                    d[cid1] = {}
                d[cid1][slot] = expression
                d = self.storedData[sid]["backward_connections"]
                if cid1 not in d:
                    d[cid1] = {}
                d = d[cid1]
                d[slot] = [cid0, signal]
                return True
        return False

    def remove_connection(self, sid, cid0, cid1, signal, slot):
        if sid in self.storedData:
            connections = self.storedData[sid]["connections"]
            backward_connections = self.storedData[sid]["backward_connections"]
            if cid0 in connections and signal in connections[cid0] and cid1 in connections[cid0][signal] and slot in connections[cid0][signal][cid1]:
                del connections[cid0][signal][cid1][slot]
                del backward_connections[cid1][slot]
                return True
        return False
    
    def remove_component(self, sid, cid):
        if sid in self.storedData:
            components = self.storedData[sid]["components"]
            connections = self.storedData[sid]["connections"]
            backward_connections = self.storedData[sid]["backward_connections"]
            if cid in components:
                del components[cid]
                if cid in connections:
                    for signal in connections[cid]:
                        for cid1 in connections[cid][signal]:
                            for slot in connections[cid][signal][cid1]:
                                del backward_connections[cid1][slot]
                    del connections[cid]
                if cid in backward_connections:
                    for slot in backward_connections[cid]:
                        cid1, signal = backward_connections[cid][slot]
                        del connections[cid1][signal][cid][slot]
                    del backward_connections[cid]
                return True
        return False
