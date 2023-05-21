
#Class for representing a climbs features instead of a JSON file
class Climb:
    def __init__(self, dict):
        self.name = dict['name']
        self.width = dict['width']
        self.height = dict['height']
        self.angle = dict['angle']
        self.difficulty = dict['difficulty']
        self.author = dict['author']
        self.region = dict['region'] 
        self.hold_theme = dict['hold_theme']
        self.hold = []

        for item in dict['holds']:
            newHold = Hold(item['id'], item['x'], item['y'], item['rotation'])
            self.hold.append(newHold)
            
#Class for representing hold specific information
class Hold:
    def __init__(self, holdID, x, y, rot):
        self.holdID = holdID
        self.x = x
        self.y = y
        self.rot = rot