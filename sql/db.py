import os
import sqlite3

class DBConnect:

    def __init__(self):
        self.db_name = os.path.join(os.getcwd(), 'RRS.db')
        self.conn = None
        self.curs = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.curs = self.conn.cursor()

    # CREATE ALL TABLES
    def create_tables(self):
        self.curs.execute(self.create_table_users())
        self.curs.execute(self.create_table_rooms())
        self.curs.execute(self.create_table_rooms_admin())
        self.curs.execute(self.create_table_event())
        self.conn.commit()

    def create_table_users(self):
        return '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            telephone TEXT
        )
        '''

    def create_table_rooms(self):
        return '''
        CREATE TABLE IF NOT EXISTS rooms(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER,
            floor INTEGER,
            description TEXT
        )
        '''

    def create_table_rooms_admin(self):
        return '''
        CREATE TABLE IF NOT EXISTS rooms_admin(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            room_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
        '''

    def create_table_event(self):
        return '''
        CREATE TABLE IF NOT EXISTS event(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_admin INTEGER,
            id_room INTEGER,
            id_user INTEGER,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            description TEXT,
            req_conf INTEGER DEFAULT 0,
            FOREIGN KEY (id_admin) REFERENCES users(id),
            FOREIGN KEY (id_room) REFERENCES rooms(id),
            FOREIGN KEY (id_user) REFERENCES users(id)
        )
        '''

dbConnect = DBConnect()

dbConnect.connect()

dbConnect.create_tables()