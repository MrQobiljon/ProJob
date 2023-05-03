import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data


    def create_user_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            phone_number VARCHAR(18),
            full_name VARCHAR(150),
            employer BOOLEAN,
            freelancer BOOLEAN
        )'''
        self.execute(sql, commit=True)

    def insert_telegram_id_users(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES (?) ON CONFLICT DO NOTHING'''
        self.execute(sql, parameters=(telegram_id,), commit=True)

    def update_insert_employer(self, employer: bool, telegram_id):
        sql = '''UPDATE users SET employer = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(employer, telegram_id), commit=True)

    def update_insert_freelancer(self, freelancer: bool, telegram_id):
        sql = '''UPDATE users SET freelancer = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(freelancer, telegram_id), commit=True)

    def select_phone_number(self, telegram_id):
        sql = '''SELECT phone_number FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def update_phone_number(self,  phone_number, telegram_id):
        sql = '''UPDATE users SET phone_number = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(phone_number, telegram_id), commit=True)

    def update_full_name(self, full_name, telegram_id):
        sql = '''UPDATE users SET full_name = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(full_name, telegram_id), commit=True)


    def create_table_works(self):
        sql = '''CREATE TABLE IF NOT EXISTS works(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            price INTEGER,
            work_type VARCHAR(30),
            telegram_id BIGINT REFERENCES users(telegram_id)
        )'''
        self.execute(sql, commit=True)


    def insert_work(self, telegram_id, title, content, price, work_type):
        sql = '''INSERT INTO works(telegram_id, title, content, price, work_type)
        VALUES (?, ?, ?, ?, ?)'''
        self.execute(sql, parameters=(telegram_id, title, content, price, work_type), commit=True)

    def select_works_users_by_telegram_id(self, telegram_id):
        sql = '''SELECT * FROM works WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchall=True)



    def create_table_directions(self):
        sql = '''CREATE TABLE IF NOT EXISTS directions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            direction TEXT
        )'''
        self.execute(sql, commit=True)

    def insert_value_to_directions(self, direction):
        sql = '''INSERT INTO directions(direction) VALUES (?)'''
        self.execute(sql, parameters=(direction,), commit=True)

    def select_value_in_directions(self):
        sql = '''SELECT direction FROM directions'''
        return self.execute(sql, fetchall=True)

    def delete_value_in_directions(self, direction):
        sql = '''DELETE FROM directions WHERE direction = ?'''
        self.execute(sql, parameters=(direction,), commit=True)


    def create_table_admins(self):
        sql = '''CREATE TABLE IF NOT EXISTS admins(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id BIGINT,
            full_name VARCHAR(255)
        )'''
        self.execute(sql, commit=True)

    def insert_admin(self, telegram_id, full_name):
        sql = """INSERT INTO admins(telegram_id, full_name) VALUES (?, ?)"""
        self.execute(sql, parameters=(telegram_id, full_name), commit=True)

    def select_admins(self):
        sql = """SELECT full_name FROM admins"""
        return self.execute(sql, fetchall=True)

    def delete_admin(self, admin_name):
        sql = '''DELETE FROM admins WHERE full_name = ?'''
        self.execute(sql, parameters=(admin_name,), commit=True)