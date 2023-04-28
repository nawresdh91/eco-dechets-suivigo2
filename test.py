import os
from dotenv import load_dotenv
# charger les variables d'environnement à partir d'un fichier .env
load_dotenv()


import mysql.connector
from sqlalchemy import create_engine


import streamlit_authenticator as stauth

# load env variables


# get env variables
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_DATABASE')


# connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

#mydb.connect()

class Database:
    #initialiser les variables de connexion à la base de données
    def __init__(self):
        self.cursor = mydb.cursor()
        self.connect = mydb
        self.migrate()
    #créer la  table users
    def migrate(self):
        self.__create_table_users()
        #self.__create_table_go()
    
    #def __create_table_go(self):
     #   self.cursor.execute(
      #     "CREATE TABLE IF NOT EXISTS fournisseur (id INT AUTO_INCREMENT PRIMARY KEY, carte VARCHAR(255), vehicule VARCHAR(255), date VARCHAR(255), produit VARCHAR(255), quantite VARCHAR(255), tarif_ht FLOAT, tarif_ttc FLOAT, montant FLOAT ,fournisseur VARCHAR(255), km VARCHAR(255))")
       # mydb.commit()
        #print('Table goods created')

    def __create_table_users(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, password VARCHAR(255), email VARCHAR(255) UNIQUE, name VARCHAR(255))")
        mydb.commit()
        print('Table users created')
    

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


    def add_role_to_users(self):
        self.cursor.execute("ALTER TABLE users ADD role VARCHAR(255) DEFAULT 'user'")
        mydb.commit()
        print('Role added to users')

    def insert_fournisseurs(self,id,nom,code_partenaire,partenaire):
        self.cursor.execute(
            "INSERT INTO fournisseurs (id,nom,code_partenaire,partenaire) VALUES (%s, %s, %s, %s)",
            (id,nom,code_partenaire,partenaire))
        mydb.commit()
        print('Fournisseur inserted')

    def get_go(self):
        self.cursor.execute("SELECT * FROM fournisseurs")
        return self.cursor.fetchall()


    def insert_carte(self, id, num,nom,extra_nom,nature,rang,texte_additif):
        self.cursor.execute("INSERT INTO carte (id, num,nom,extra_nom,nature,rang,texte_additif) VALUES (%s, %s,%s, %s,%s, %s,%s)", (id, num,nom,extra_nom,nature,rang,texte_additif))
        mydb.commit()
        print('Carte inserted')


    def insert_client(self, id, num, nom,message):
        self.cursor.execute("INSERT INTO client (id, num, nom,message) VALUES (%s, %s, %s, %s)", (id, num, nom,message))
        mydb.commit()
        print('Client inserted')

    def insert_conducteur(self, id, nom ,code):
        self.cursor.execute("INSERT INTO conducteur (id, nom ,code) VALUES (%s, %s, %s)", (id, nom ,code))
        mydb.commit()
        print('conducteur inserted')

    def insert_produit(self, id,code_article,libelle_article,groupe_produit):
        self.cursor.execute("INSERT INTO produit (id,code_article,libelle_article,groupe_produit) VALUES (%s, %s, %s,%s)", (id,code_article,libelle_article,groupe_produit))
        mydb.commit()
        print('produit inserted')    

    def insert_site(self, id,num,nom):
        self.cursor.execute("INSERT INTO site (id,num,nom) VALUES (%s, %s, %s)", (id,num,nom))
        mydb.commit()
        print('site inserted')    

    
    def insert_station(self, id,num,nom,ref_saisie):
        self.cursor.execute("INSERT INTO station (id,num,nom,ref_saisie) VALUES (%s, %s, %s,%s)", (id,num,nom,ref_saisie))
        mydb.commit()
        print('station inserted')   


    def insert_vehicule(self, id,immatriculation):
        self.cursor.execute("INSERT INTO vehicule(id,immatriculation) VALUES (%s, %s)", (id,immatriculation))
        mydb.commit()
        print('vehicule inserted')   

    def insert_ville(self, id,nom,code_postal,departement):
        self.cursor.execute("INSERT INTO ville (id,nom,code_postal,departement) VALUES (%s, %s,%s, %s))", (id,nom,code_postal,departement))
        mydb.commit()
        print('ville inserted')   

    

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
        


    


