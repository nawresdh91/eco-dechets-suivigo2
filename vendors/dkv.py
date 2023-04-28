import numpy as np

import streamlit as st
import pandas as pd

from database2 import Database2


class DKV:

    def __init__(self, file, vendor='DKV'):
        # try to read file as csv
        try:
            #self.df = pd.read_excel(file, index_col=False, dtype=str)
            self.df = pd.read_csv(file, sep=';', index_col=False)
        except:
            st.error('Ce fichier n\'est pas un fichier csv')
            # stop execution
            st.stop()
        self.vendor = vendor
        self.__is_dkv()

    def split_date_heure(self):
        self.df[['date', 'heure']] = self.df['Temps de transaction'].str.split(
            '-', 1, expand=True)
        self.df.drop(columns=["Temps de transaction"], inplace=True)


    def show_data(self):
        self.split_date_heure()
        # remove unnamed columns
        self.df = self.df.loc[:, ~self.df.columns.str.contains('^Unnamed')]
        # df = self.df.drop(self.df.columns[self.df.columns.str.contains('unnamed',case = False)],axis = 1)
        return st.write(self.df)

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

    def __insert_data(self):
        # insert all data into the database
        for i in range(len(self.df)):
            # get the data
            # get the data from table fournisseur
            vendor = self.vendor
            partner_code  = None
            partner=None
            # get the data from table carte
            card_number = int(self.df.iloc[i]['Numéro de l\'objet de décompte (PAN, carte, boîtier)'])
            card_name = None
            extra_name = None
            nature = None
            rangee = None
            additive_text = None
            # get the data from table client
            client_number = int(self.df.iloc[i]['Numéro client'])
            client_name = None
            client_message = None 
        
            # get the data from table conducteur 
            driver_name = None
            driver_code = None
            #get the data from table produit 
            code_product = self.df.iloc[i]['Code de marchandise']
            product_name = self.df.iloc[i]['Type de marchandise']
            group_product = self.df.iloc[i]['Groupe de produits']
            
            #get the data from table site 
            site_number = None
            site_name = None
            #get the data from table station
            station_number = self.df.iloc[i]['Numéro de la gare de péage']
            station_name =  self.df.iloc[i]['Nom de la gare de péage']
            station_reference = None
            #get the data from table vehicle
            vehicle =np.str(self.df.iloc[i]['N° d\'immatriculation']).replace("-", "")
            #get the data from table ville
            city = self.df.iloc[i]['Localité']
            post_code = self.df.iloc[i]['CP']
            departement = None
            country = "France" 
            #get the data from table transaction_carburant
            transaction_number = None
            transaction_code = None 
           # date = self.df.iloc[i]['date']
            #hour = self.df.iloc[i]['heure'] 
            invoice_number = self.df.iloc[i]['Numéro de facture']

            invoice_date = self.df.iloc[i]['Date de décompte']
            unity = self.df.iloc[i]['Unité']
            quantity = np.float(self.df.iloc[i]['Paragraphe'])
            unit_price_ht = np.float(self.df.iloc[i]['Prix à l\'unité'])
            unit_price_ttc = None
            amount_ttc = np.float(self.df.iloc[i]['Valeur totale nette'])
            amount_ht = np.float(self.df.iloc[i]['Valeur totale brute'])
            service_cost_ht = None
            service_cost_ttc =  np.float(self.df.iloc[i]['Service Fee net'])

            km = int(self.df.iloc[i]['Kilométrage'])
            consumption = None
            tva_rate = None
            tva_amount = np.float(self.df.iloc[i]['TVA']) 
            discount_rate = None
            discout_amount = None   



            carte_id =Database2().insert_carte(num=card_number,nom=card_name, nature=nature, extra_nom=extra_name, rang=rangee, texte_additif=additive_text)

            client_id = Database2().insert_client(num=client_number,nom=client_name,message=client_message)

            product_id = Database2().insert_produit(code_article=code_product,libelle_article=product_name, groupe_produit=group_product)

           
           
            station_id = Database2().insert_station(num=station_number,nom=station_name,ref_saisie=station_reference,bon_enlevement=None) 
            site_id = Database2().insert_site(num=site_number, nom=site_name)
            
            vehicule_id = Database2().insert_vehicule(immatriculation=vehicle)
            fournisseur_id =Database2().insert_fournisseurs(nom=vendor, code_partenaire=partner_code, partenaire=partner)

            Database2().insert_transaction_carburant(id_carte=carte_id,id_client=client_id, id_produit=product_id,id_station=station_id, id_site=site_id, id_vehicule=vehicule_id,id_fournisseurs=fournisseur_id,unite=unity, quantite=quantity,montant_ttc=amount_ttc,montant_ht=amount_ht,kilometrage=km,consoL_au100=consumption,montant_tva=tva_amount,num_facture=invoice_number)
              
#date_transaction=date,heure_transaction=hour,



    def __is_dkv(self):
        # verify df column exist
        if "N° d'immatriculation" in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier DKV')
            # stop execution
            st.stop()
