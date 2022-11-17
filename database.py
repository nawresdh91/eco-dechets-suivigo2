import os
import mysql.connector

from dotenv import load_dotenv
import streamlit_authenticator as stauth

# load environment variables
load_dotenv('.env')

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE')
)


class Database:
    def __init__(self):
        self.cursor = mydb.cursor()

    def migrate(self):
        self.create_table_users()

    def create_table_users(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, password VARCHAR(255), email VARCHAR(255) UNIQUE, name VARCHAR(255))")
        mydb.commit()
        print('Table users created')

    def insert_user(self, password, email, name):
        self.cursor.execute("INSERT INTO users (password, email, name) VALUES (%s, %s, %s)", (password, email, name))
        mydb.commit()
        print('User inserted')

    def get_user(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return self.cursor.fetchone()

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def delete_user(self, email):
        self.cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        mydb.commit()

    def login(self, email, password):
        try:
            hashed_password = stauth.Hasher([password]).generate()
            self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password[0]))
            return self.cursor.fetchone()
        except:
            return None
