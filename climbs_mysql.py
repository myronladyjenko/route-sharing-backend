import mysql.connector
import ClimbWrapper
import sqlite3
import os

class Database:
    # def __init__(self):
    #     self.connection = mysql.connector.connect(
    #         host='localhost',
    #         user='root',
    #         password='password',
    #         database='climb_db'
    #     )

    #     self.connection = self.connection.connection()


    #     self.dropTables()
    #     self.createTables()
    
    def __init__(self, reset=False):
        if reset == True:
            if (os.path.exists('molecules.db')):
                os.remove('molecules.db')
            
        self.connection = sqlite3.connect("molecules.db");
        # self.connection = self.connection.connection()

    def __del__(self):
        self.connection.close()

    def __setitem__(self, table, values):
        questionMarkStr = ", ".join(('?',)*len(values)) 
        insertStr = f"INSERT OR IGNORE INTO {table} VALUES (" + questionMarkStr + ")";
        print(insertStr)
        print(values)

        self.connection.execute(insertStr, values)

    def dropTables(self):
        dropQuery = 'DROP TABLE Climbs, Holds;'
        self.connection.execute(dropQuery);
        self.connection.commit()

    #Create Tables
    def createTables(self):
        climbs = """CREATE TABLE IF NOT EXISTS Climbs (
                        NAME        TEXT        NOT NULL,
                        WIDTH       INTEGER         NOT NULL,
                        HEIGHT      INTEGER         NOT NULL,
                        ANGLE       INTEGER         NOT NULL,
                        DIFFICULTY  TEXT        NOT NULL,
                        AUTHOR      TEXT        NOT NULL,
                        REGION      TEXT        NOT NULL,
                        HOLDS_SET   TEXT        NOT NULL,
                        CLIMB_ID    INTEGER         NOT NULL PRIMARY KEY AUTOINCREMENT
                    );"""

        holds = """ CREATE TABLE IF NOT EXISTS Holds (
                        HOLD_ID         INTEGER         NOT NULL,
                        X               INTEGER         NOT NULL,
                        Y               INTEGER         NOT NULL,
                        ROT             INTEGER         NOT NULL,
                        CLIMB_ID        INTEGER         NOT NULL,
                        PRIMARY KEY (CLIMB_ID),
                        FOREIGN KEY (CLIMB_ID) REFERENCES Climbs (CLIMB_ID)
                    );"""
        
        self.connection.execute(climbs);
        self.connection.execute(holds)
        self.connection.commit()

    #Add a new climb to the db
    def createClimb(self, climbData):
        climb = ClimbWrapper.Climb(climbData)
        print(climbData)

        self['Climbs'] = (climb.name, climb.width, climb.height, climb.angle, climb.difficulty, climb.author, climb.region, climb.hold_theme, None)

        climbID = self.connection.execute(self.lastID)

        for hold in climb.holds:
            self['Holds'] = (hold.holdID, hold.x, hold.y, hold.rot, climbID)

    #Retrieves all the climb previews for di
    def loadClimbPreviews(self):
        climbPreviewQuery = 'SELECT * FROM Climbs;'
        climbPreviews = self.connection.execute(climbPreviewQuery)
        return climbPreviews.fetchall()

    #Retrieves the full climb data for when the user purchased a climb
    def loadFullClimb(self, climbID):
        climbQuery = 'SELECT * FROM Climbs WHERE CLIMB_ID = ?;'
        holdsQuery = 'SELECT * FROM Holds WHERE CLIMB_ID = ?;'

        climbInfo = self.connection.execute(climbQuery, (climbID,))
        climbInfo = climbInfo.fetchone()

        holdsInfo = self.connection.execute(holdsQuery, (climbID,))
        holdsInfo = holdsInfo.fetchall()

        climb = ClimbWrapper(climbInfo, holdsInfo)
        return climb
    
if __name__ == '__main__':
    db = Database() 
