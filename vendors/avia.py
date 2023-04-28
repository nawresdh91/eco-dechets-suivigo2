import numpy as np
import streamlit as st
import pandas as pd
from database2 import Database2


class Avia:

    def __init__(self, file, vendor='Avia'):
        # try to read file as csv
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False,dtype=str)
            #, dtype={'NUM SITE': int})
            self.back_up = self.df.copy()
        except:
            st.error('Ce fichier n\'est pas un fichier CSV')
            # stop execution
            st.stop()
        self.vendor = vendor
        self.__is_avia()
    # diviser la colonne CP Ville en CP et Ville

    def split_CP_VILLE(self):
        self.df[['CP', 'VILLE']] = self.df['CP VILLE'].str.split(
            ' ', 1, expand=True)
        self.df.drop(columns=["CP VILLE"], inplace=True)

    def __is_avia(self):
        # verify df column exist
        if 'NUM CARTE' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Avia')
            # stop execution
            st.stop()

    def show_data(self):
        self.split_CP_VILLE() # appel de la fonction split_CP_VILLE
        pd.set_option('display.float_format', lambda x: '{:.0f}'.format(x))
        if self.vendor == 'Avia':
            return st.write(self.df)
        else:
            return st.write('Le fichier n\'est pas un fichier Avia')

    def show_upload_btn(self):

        if st.button('upload data'):
            with st.spinner('Wait for it...'):
                try:
                    self.__insert_data()
                    st.success('Data uploaded')
                except Exception as e:
                    print(e)
                    st.error(e)
                    st.stop()

    def test(self):
       # insert all data into the database
        try:

            print(np.str_(self.df.iloc[0]['IMMATRICULATION'].replace(" ", "")))
        except Exception as e:
            print(e)

        print('done')

    def __insert_data(self):
        #self.split_CP_VILLE()
        # insert all data into the database
        unique_immatriculation= set()
        immatriculation_ids = {}
        for i in range(len(self.df)):
            # insert the data into table fournisseur
            vendor = self.vendor
            partner_code = None
            partner = None
            # get the data from table carte
            card_number = int(self.df.iloc[i]['NUM CARTE'].replace("'", ""))
            card_name = None
            extra_name = None
            nature = None
            rangee = None
            additive_text = None
            # get the data from table client
            client_number = None
            client_name = None
            client_message = None
            # get the data from table conducteur
            driver_name = None
            #driver_code = self.df.iloc[i]['CODE CHAUFFEUR']
            # get the data from table produit
            code_product = None
            product_name =self.df.iloc[i]['PRODUIT']

            group_product = None

            # get the data from table site
            site_number = self.df.iloc[i]['NUM SITE']
            site_name = None
            # get the data from table station
            station_number = None
            station_name = None
            station_reference = None
            # get the data from table vehicle
            vehicle = self.df.iloc[i]['IMMATRICULATION'].replace(" ", "")
            if vehicle not in unique_immatriculation:
                # insert a new row into the vehicle table and retrieve the auto-incremented ID
                query = "INSERT INTO vehicule (IMMATRICULATION) VALUES ('{}')".format(vehicle)
                self.cursor.execute(query)
                vehicle_id = self.cursor.lastrowid
                # store the unique immatriculation value and its corresponding ID
                unique_immatriculation.add(vehicle)
                immatriculation_ids[vehicle] = vehicle_id
            else:
                # retrieve the ID for the existing immatriculation value
                vehicle_id = immatriculation_ids[vehicle]

            # get the data from table ville
            #city = self.df.iloc[i]['VILLE']
            #post_code = self.df.iloc[i]['CP']
            departement = None
            country = None
            # get the data from table transaction_carburant
            transaction_number = None
            transaction_code = None
            datee = self.df.iloc[i]['DATE']
            hour = None
            invoice_number = None
            invoice_date = None
            unity = None
            quantity = np.float(self.df.iloc[i]['QUANTITE'].replace(",", "."))
            unit_price_ht = None
            unit_price_ttc = np.float(self.df.iloc[i]['PU'].replace(",", "."))
            amount_ttc = np.float(self.df.iloc[i]['MONTANT'].replace(",", "."))
            amount_ht = None
            service_cost_ht = None
            service_cost_ttc = None
            km =int(self.df.iloc[i]['KM'])
            consumption = None
            tva_rate = None
            tva_amount = None
            discount_rate = None
            discout_amount = None

            carte_id =Database2().insert_carte(num=card_number, nom=card_name, nature=nature, extra_nom=extra_name, rang=rangee, texte_additif=additive_text)

            conducteur_id = Database2().insert_conducteur(nom=driver_name,code=None)


            product_id = Database2().insert_produit(code_article=code_product,libelle_article=product_name, groupe_produit=group_product)
           
           
            site_id = Database2().insert_site(num=site_number, nom=site_name)
            
            ville_id =Database2().insert_ville(nom=None,code_postal=None departement=departement)
            
            vehicule_id = Database2().insert_vehicule(immatriculation=vehicle)
            fournisseur_id =Database2().insert_fournisseurs(nom=vendor, code_partenaire=partner_code, partenaire=partner)
            Database2().insert_transaction_carburant(id_carte=carte_id,id_conducteur=conducteur_id,id_produit=product_id,id_site=site_id,id_ville=ville_id,id_vehicule=vehicule_id,id_fournisseurs=fournisseur_id, quantite=quantity, kilometrage=km, pu_ttc=unit_price_ttc,montant_ttc=amount_ttc )

    def bar_chart(self):
        # bar chart with the total amount of immatriulation
        chart_data = self.df.groupby('MONTANT').sum()

        return st.bar_chart(chart_data)

    def show_filter(self):
        # select box to choose immatriculation
        immatriculation = st.selectbox(
            'Select immatriculation', self.df['IMMATRICULATION'].unique())
        # filter the data with the immatriculation
        self.df = self.df[self.df['IMMATRICULATION'] == immatriculation]
        # self.df['CONSO L au 100'] = pd.to_numeric(self.df['CONSO L au 100'])

        # print mean consommation
        # st.write(f"Mean consommation: {self.df['CONSO L au 100'].mean()}")  


