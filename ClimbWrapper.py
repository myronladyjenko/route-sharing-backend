
#Class for representing a climbs features instead of a JSON file
class Climb:
    def __init__(self, JSONFile):
        self.parseJSONFile(JSONFile)
    
    def parseJSONFile(self, file):
        #TODO: set class variables and initialize hold variables
        pass
        
#Class for representing hold specific information
class Hold:
    def __init__(self, holdID, x, y, rot):
        self.holdID = holdID
        self.x = x
        self.y = y
        self.rot = rot
    
class JSONClass:
    def __init__(self, climbInfo, holdsInfo):
        #TODO: convert data to json file format
        pass