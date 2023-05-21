
#Class for representing a climbs features instead of a JSON file
class Climb:
    def __init__(self, JSONfile):
        pass

#Class for representing hold specific information
class Hold:
    def __init__(self, holdID, x, y, rot):
        self.holdID = holdID
        self.x = x
        self.y = y
        self.rot = rot