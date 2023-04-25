import config
import psycopg2
import base64

class Database:
    @property
    def cursor(self):
        return self._cur

    def __init__(self) -> None:
        self.connect()

    def connect(self):
        print("connecting to database...")
        self.connection = psycopg2.connect(config.Database.connection_string)
        self._cur = self.connection.cursor()
        print("database connection establised: ", self.connect)

    def executevars(self, query:str, vars):
        try:
            self.cursor.execute(query, vars)
        
        except psycopg2.ProgrammingError as e:
            self.connection.rollback()
        
        except psycopg2.InterfaceError as e:
            self.connect()
            self.cursor.execute(query, vars)

        except psycopg2.OperationalError as e:
            self.connect()
            self.cursor.execute(query, vars)

    def execute(self, query:str):
        try:
            self.cursor.execute(query)
        
        except psycopg2.ProgrammingError as e:
            self.connection.rollback()
        
        except psycopg2.InterfaceError as e:
            self.connect()
            self.cursor.execute(query)

        except psycopg2.OperationalError as e:
            self.connect()
            self.cursor.execute(query)

    def insert(self, img, plate):
        self.executevars(
            "INSERT INTO Captured (PlateNumber, Image, Location, DateTimeCaptured, IsActive) VALUES (%s, %s, %s, %s, %s)",
            (plate, img, config.Map.location, 'now()', True)
        )
        self.connection.commit()

    def get_by_id(self, id:int):
        self.execute(f"SELECT * FROM Captured WHERE Id = {id}")
        return self.cursor.fetchone()