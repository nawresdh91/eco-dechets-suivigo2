import pandas as pd
import numpy as np
import streamlit as st

from database2 import Database2


class Thevenin:
    def __init__(self, file, vendor='Thevenin'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False, encoding='latin-1', dtype=str)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        self.__is_thevenin()
    
     #Split CP ville en CP et ville 

    def split_cp_ville(self):
        self.df[['CP', 'Ville']] = self.df['CP VILLE'].str.split(' ', n=1, expand=True)
        self.df.drop('CP VILLE', axis=1, inplace=True)


    def show_data(self):
        self.split_cp_ville()
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
        self.split_cp_ville()
        # insert all data into the database
        for i in range(len(self.df)):
            # get the data
            # get the data from table fournisseur
            vendor = self.vendor
            partner_code = None
            partner=None
            # get the data from table carte
            card_number = np.int(self.df.iloc[i]['NUM CARTE'].replace("'", ""))
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
            driver_code = self.df.iloc[i][' CODE CHAUFFEUR']
            #get the data from table produit 
            code_product = None
            product_name = self.df.iloc[i]['PRODUIT']
            group_product = None
            
            #get the data from table site 
            site_number = self.df.iloc[i]['NUM SITE']
            site_name = None 
            #get the data from table station
            station_number = None
            station_name =  None
            station_reference = None
            #get the data from table vehicle
            vehicle = self.df.iloc[i]['IMMATRICULATION']
            #get the data from table ville
            city = self.df.iloc[i]['Ville']
            post_code = self.df.iloc[i]['CP']
            departement = None
            country = None 
            #get the data from table transaction_carburant
            transaction_number = None
            transaction_code = None 
            date = self.df.iloc[i]['DATE']
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
            km = self.df.iloc[i]['KM']
            consumption = self.df.iloc[i]['CONSO L au 100']
            tva_rate = None
            tva_amount = None
            discount_rate = None
            discout_amount = None
            currency = None
            status = None





            carte_id =Database2().insert_carte(num=card_number,nom=card_name, nature=nature, extra_nom=extra_name, rang=rangee, texte_additif=additive_text)

            client_id = Database2().insert_client(num=client_number,nom=client_name,message=client_message)
            conducteur_id = Database2().insert_conducteur(nom=None,code=driver_code)


            product_id = Database2().insert_produit(code_article=code_product,libelle_article=product_name, groupe_produit=group_product)

            station_id = Database2().insert_station(num=station_number,nom=station_name,ref_saisie=station_reference,bon_enlevement=None) 
              
            vehicule_id = Database2().insert_vehicule(immatriculation=vehicle)

            fournisseur_id =Database2().insert_fournisseurs(nom=vendor, code_partenaire=partner_code, partenaire=partner)  
               
            Database2().insert_transaction_carburant (id_carte=carte_id,id_client=client_id,id_conducteur=conducteur_id, id_fournisseurs=fournisseur_id,  id_station=station_id, id_produit=product_id, id_vehicule=vehicule_id,num_transaction=transaction_number,code_transaction=transaction_code,date_transaction=date,heure_transaction=hour,num_facture=invoice_number,date_facture=invoice_date,unite=unity,quantite=quantity,pu_ht=unit_price_ht,pu_ttc=unit_price_ttc ,montant_ttc=amount_ttc,montant_ht=amount_ht,frais_service_ht=service_cost_ht,frais_service_ttc=service_cost_ttc, kilometrage=km,consoL_au100=consumption,taux_tva=tva_rate,montant_tva=tva_amount,taux_remise=discount_rate,montant_remise=discout_amount,devise=currency,etat=status)

                
    def __is_thevenin(self):
        # verify df column exist
        if 'NUM SITE' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Thevenin')
            # stop execution
            st.stop()
