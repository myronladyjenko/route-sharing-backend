import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='climb_db'
        )

        self.cursor = self.connection.cursor()
        self.lastID = 'SELECT LAST_INSERT_ID();'
    
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def __setitem__(self, table, values):
        questionMarkStr = ", ".join(('?',)*len(values)) 
        insertStr = f"INSERT OR IGNORE INTO {table} VALUES (" + questionMarkStr + ")";

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
                HOLD_LIST   INT         NOT NULL AUTO_INCREMENT,
                PRIMARY KEY (HOLD_LIST)
            );"""

        holds = """CREATE TABLE IF NOT EXISTS Holds (
                    HOLD_ID         INT         NOT NULL,
                    X               INT         NOT NULL,
                    Y               INT         NOT NULL,
                    ROT             INT         NOT NULL,
                    HOLD_LIST       INT         NOT NULL,
                    PRIMARY KEY (HOLD_LIST),
                    FOREIGN KEY (HOLD_LIST) REFERENCES Climbs (HOLD_LIST)
                );"""
        
        self.cursor.execute(climbs);
        self.cursor.execute(holds)
        self.connection.commit()

    #Add a new climb to the db
    def createClimb(self, climb):
        self['Climbs'] = (climb.name, climb.width, climb.height, climb.angle, climb.difficulty, climb.author, \
                            climb.region, climb.set, None)
        
        holdListID = self.cursor.execute(self.lastID)

        for hold in climb.holds:
            self['Holds'] = (hold.holdID, hold.x, hold.y, hold.rot, holdListID)

