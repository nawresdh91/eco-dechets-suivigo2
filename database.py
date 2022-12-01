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
        self.connect = mydb
        self.migrate()

    def migrate(self):
        self.__create_table_users()
        self.__create_table_go()

    def __create_table_go(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS fournisseur (id INT AUTO_INCREMENT PRIMARY KEY, carte VARCHAR(255), vehicule VARCHAR(255), date VARCHAR(255), produit VARCHAR(255), quantite VARCHAR(255), tarif_ht FLOAT, tarif_ttc FLOAT, montant FLOAT ,fournisseur VARCHAR(255), km VARCHAR(255))")
        mydb.commit()
        print('Table goods created')

    def __create_table_users(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, password VARCHAR(255), email VARCHAR(255) UNIQUE, name VARCHAR(255))")
        mydb.commit()
        print('Table users created')

    def insert_go(self, carte, vehicule, date, produit, quantite, tarif_ht, tarif_ttc, montant, fournisseur, km):
        self.cursor.execute("INSERT INTO fournisseur (carte, vehicule, date, produit, quantite, tarif_ht, tarif_ttc, montant, fournisseur, km) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (carte, vehicule, date, produit, quantite, tarif_ht, tarif_ttc, montant, fournisseur, km))
        mydb.commit()
        print('Fournisseur inserted')

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

    def get_go(self):
        self.cursor.execute("SELECT * FROM fournisseur")
        return self.cursor.fetchall()

    def login(self, email, password):
        try:
            hashed_password = stauth.Hasher([password]).generate()
            self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password[0]))
            return self.cursor.fetchone()
        except:
            return None
