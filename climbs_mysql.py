import mysql.connector
import ClimbWrapper

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='climb_db'
        )

        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()

    def __setitem__(self, table, values):
        questionMarkStr = ", ".join(('?',)*len(values)) 
        insertStr = f"INSERT OR IGNORE INTO {table} VALUES (" + questionMarkStr + ");";

        self.cursor.execute(insertStr, values)

    #Create Tables
    def createTables(self):
        climbs = """CREATE TABLE IF NOT EXISTS Climbs (
                        NAME        TEXT        NOT NULL,
                        WIDTH       INT         NOT NULL,
                        HEIGHT      INT         NOT NULL,
                        ANGLE       INT         NOT NULL,
                        DIFFICULTY  TEXT        NOT NULL,
                        AUTHOR      TEXT        NOT NULL,
                        REGION      TEXT        NOT NULL,
                        HOLDS_SET   TEXT        NOT NULL,
                        CLIMB_ID    INT         NOT NULL AUTO_INCREMENT,
                        PRIMARY KEY (CLIMB_ID)
                    );"""

        holds = """ CREATE TABLE IF NOT EXISTS Holds (
                        HOLD_ID         INT         NOT NULL,
                        X               INT         NOT NULL,
                        Y               INT         NOT NULL,
                        ROT             INT         NOT NULL,
                        CLIMB_ID        INT         NOT NULL,
                        PRIMARY KEY (CLIMB_ID),
                        FOREIGN KEY (CLIMB_ID) REFERENCES Climbs (CLIMB_ID)
                    );"""
        
        self.cursor.execute(climbs);
        self.cursor.execute(holds)
        self.connection.commit()

    #Add a new climb to the db
    def createClimb(self, climbData):
        climb = ClimbWrapper.Climb(climbData)
        print(climbData)

        self['Climbs'] = (climb.name, climb.width, climb.height, climb.angle, climb.difficulty, climb.author, climb.region, climb.hold_theme, None)

        climbID = self.cursor.execute(self.lastID)

        for hold in climb.holds:
            self['Holds'] = (hold.holdID, hold.x, hold.y, hold.rot, climbID)

    #Retrieves all the climb previews for di
    def loadClimbPreviews(self):
        climbPreviewQuery = 'SELECT * FROM Climbs;'
        climbPreviews = self.cursor.execute(climbPreviewQuery)
        return climbPreviews.fetchall()

    #Retrieves the full climb data for when the user purchased a climb
    def loadFullClimb(self, climbID):
        climbQuery = 'SELECT * FROM Climbs WHERE CLIMB_ID = ?;'
        holdsQuery = 'SELECT * FROM Holds WHERE CLIMB_ID = ?;'

        climbInfo = self.cursor.execute(climbQuery, (climbID,))
        climbInfo = climbInfo.fetchone()

        holdsInfo = self.cursor.execute(holdsQuery, (climbID,))
        holdsInfo = holdsInfo.fetchall()

        climb = ClimbWrapper(climbInfo, holdsInfo)
        return climb
    
if __name__ == '__main__':
    db = Database() 
