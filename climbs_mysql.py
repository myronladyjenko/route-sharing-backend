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

# Connect to the MySQL server


# Create a cursor object to interact with the database

# Close the cursor and the connection
cursor.close()
connection.close()

