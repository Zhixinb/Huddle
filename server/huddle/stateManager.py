
#Keeps track of the state of a room
class StateManager(object):
    
    """Object for tracking stored data"""
    def __init__(self):
        self.storedData = {0 : "hello"}

    def insertData(self, value):
        self.storedData[value.key] = value.data

    def getSingleData(self, key):
        return self.storedData[key]

    def getAllData(self):
        return self.storedData

