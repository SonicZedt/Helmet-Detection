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
        self.connection = psycopg2.connect(config.Database.connection_string)
        self._cur = self.connection.cursor()

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

    def send(self, img, plate):
        # encode img to base64
        encoded_string = base64.b64encode(img)
        

    # def get_all_sheetmaps(self) -> list[model.SheetMap]:
    #     self.execute(queries.SheetMap.get_all_sheetmaps())
    #     result = self.cursor.fetchall()

    #     return list(map(lambda sheetmap: model.SheetMap(
    #         sheetmap_id=sheetmap[0],
    #         name=sheetmap[1],
    #         server_id=sheetmap[2],
    #         response_sheet_id=sheetmap[3],
    #         is_active=sheetmap[4],
    #         datetime_created=sheetmap[5],
    #         datetime_updated=sheetmap[6]
    #     ), result))