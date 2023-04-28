import numpy as np
import streamlit as st
import pandas as pd

from database2 import Database2


class DATS:

    def __init__(self, file, vendor='DATS'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False)
            self.back_up = self.df.copy()
        except:
            st.error('Ce fichier n\'est pas un fichier CSV')
            # stop execution
            st.stop()
        self.vendor = vendor
        self.__is_dats()

    def show_data(self):
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
            partner_code = None
            partner = None
            # get the data from table carte
            card_number = int(self.df.iloc[i]['CARTE NO'])
            card_name = self.df.iloc[i]['CARTE NOM']
            extra_name = self.df.iloc[i]['EXTRA NOM CARTE']
            nature = None
            rangee = None
            additive_text = None
            # get the data from table client
            client_number = int(self.df.iloc[i]['CLIENT NO'])
            client_name = None
            client_message = None 
        
            # get the data from table conducteur 
            driver_name = None
            driver_code = None
            #get the data from table produit 
            code_product = None
            product_name = self.df.iloc[i]['PRODUIT']
            group_product = None
            
            #get the data from table site 
            site_number = None
            site_name = None 
            #get the data from table station
            station_number = int(self.df.iloc[i]['STATION NO'])
            station_name =  self.df.iloc[i]['NOM STATION']
            station_reference = None
            #get the data from table vehicle
            vehicle =str(self.df.iloc[i]['NO DE PLAQUE'])
            #get the data from table ville
            city = None
            post_code = None
            departement = None
            country = None 
            #get the data from table transaction_carburant
            transaction_number = None
            transaction_code = None 
            date = self.df.iloc[i]['DATE']
            hour = self.df.iloc[i]['HEURE']
            invoice_number = None
            invoice_date = None
            unity = self.df.iloc[i]['UNIT']
            quantity = np.float(self.df.iloc[i]['QUANT'].replace(',', '.'))
            unit_price_ht = None
            unit_price_ttc = None
            amount_ttc = np.float(self.df.iloc[i]['MONTANT TVA INCL'].replace(",", "."))
            amount_ht = np.float(self.df.iloc[i]['MONTANT TVA EXCL'].replace(",", "."))
            service_cost_ht = None
            service_cost_ttc = None

            km = int(self.df.iloc[i]['KILOMETRAGE'])
            consumption = self.df.iloc[i]['CONSOMMATION (L/100KM)']
            tva_rate = None
            tva_amount = np.float(self.df.iloc[i]['MONTANT TVA'].replace(",", ".")) 
            discount_rate = None
            discout_amount = None      



            carte_id =Database2().insert_carte(num=card_number,nom=card_name, nature=nature, extra_nom=extra_name, rang=rangee, texte_additif=additive_text)

            client_id = Database2().insert_client(num=client_number,nom=client_name,message=client_message)

            product_id = Database2().insert_produit(code_article=code_product,libelle_article=product_name, groupe_produit=group_product)

           
           
            station_id = Database2().insert_station(num=station_number,nom=station_name,ref_saisie=station_reference,bon_enlevement=None) 
            
            vehicule_id = Database2().insert_vehicule(immatriculation=vehicle)
            fournisseur_id =Database2().insert_fournisseurs(nom=vendor, code_partenaire=partner_code, partenaire=partner)

            Database2().insert_transaction_carburant(id_carte=carte_id,id_client=client_id, id_produit=product_id,id_station=station_id,id_vehicule=vehicule_id,id_fournisseurs=fournisseur_id,date_transaction=date,heure_transaction=hour,unite=unity, quantite=quantity,montant_ttc=amount_ttc,montant_ht=amount_ht,kilometrage=km,consoL_au100=consumption,montant_tva=tva_amount )
           



    def __is_dats(self):
        # verify df column exist
        if 'CLIENT NO' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier DATS')
            # stop execution
            st.stop()




    



