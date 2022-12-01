import random
import string

import mysql.connector
import streamlit as st

import streamlit_authenticator as stauth

mydb = mysql.connector.connect(
    host=st.secrets['DB_HOST'],
    user=st.secrets['DB_USER'],
    password=st.secrets['DB_PASSWORD'],
    database=st.secrets['DB_DATABASE']
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
        self.cursor.execute(
            "INSERT INTO fournisseur (carte, vehicule, date, produit, quantite, tarif_ht, tarif_ttc, montant, fournisseur, km) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (carte, vehicule, date, produit, quantite, tarif_ht, tarif_ttc, montant, fournisseur, km))
        mydb.commit()
        print('Fournisseur inserted')

    def insert_user(self, password, email, name):
        hashed_password = stauth.Hasher([password]).generate()[0]
        print(hashed_password)
        self.cursor.execute("INSERT INTO users (password, email, name) VALUES (%s, %s, %s)",
                            (hashed_password, email, name))
        mydb.commit()
        print('User inserted')

    def get_user(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return self.cursor.fetchone()

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def reset_password(self, email, password):
        hashed_password = stauth.Hasher([password]).generate()[0]
        self.cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
        mydb.commit()
        return password

    def delete_user(self, email):
        self.cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        mydb.commit()

    def get_go(self):
        self.cursor.execute("SELECT * FROM fournisseur")
        return self.cursor.fetchall()

    def add_role_to_users(self):
        self.cursor.execute("ALTER TABLE users ADD role VARCHAR(255) DEFAULT 'user'")
        mydb.commit()
        print('Role added to users')

    @staticmethod
    def generate_password(length=8):
        password = ''
        for i in range(length):
            password += random.choice(string.ascii_letters + string.digits)
        return password

    def login(self, email, password):
        try:
            hashed_password = stauth.Hasher([password]).generate()
            self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password[0]))
            return self.cursor.fetchone()
        except:
            return None
