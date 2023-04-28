import webbrowser

import numpy as np
import pandas as pd
import streamlit as st

from database2 import Database2

url = 'https://www.dropbox.com/s/8x087om1c9bhuwj/canevas_import.xlsx?dl=0'


class Carrefour:
    def __init__(self, file, vendor='Carrefour'):
        try:
            self.df = pd.read_excel(file, index_col=False, dtype=str)
            # change date format
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Date'] = self.df['Date'].dt.strftime('%d/%m/%Y')
            self.df = self.df.astype(object).where(pd.notnull(self.df), None)
            self.back_up = self.df.copy()
        except Exception as e:
            print(e)
            st.error('Ce fichier n\'est pas un fichier CSV')
            # stop execution
            st.stop()
        self.vendor = vendor
        # self.__is_dats()

    @staticmethod
    def show_download_btn(df):

        if df is None:
            st.write(f'''
                    <p>Pour ce founisseur, vous devez télécharger le fichier excel de référence et le completer manuellement. <a target="_blank" href="https://www.dropbox.com/s/8x087om1c9bhuwj/canevas_import.xlsx?dl=0">
                            Télécharger le fichier excel
                        </a></p>

                        ''',
                     unsafe_allow_html=True
                     )

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
            card_number = np.int(self.df.iloc[i]['carte'])
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
            driver_code = None
            #get the data from table produit 
            code_product = None
            product_name = self.df.iloc[i]['produit']
            group_product = None
            
            #get the data from table site 
            site_number = None
            site_name = None 
            #get the data from table station
            station_number = None
            station_name =  None
            station_reference = None
            #get the data from table vehicle
            vehicle = self.df.iloc[i]['vehicule']
            #get the data from table ville
            city = None
            post_code = None
            departement = None
            country = None 
            #get the data from table transaction_carburant
            transaction_number = None
            transaction_code = None 
            date = self.df.iloc[i]['date']
            hour = None
            invoice_number = None
            invoice_date = None
            unity = None
            quantity = np.float(self.df.iloc[i]['qte'].replace(",", "."))
            unit_price_ht = None
            unit_price_ttc = np.float(self.df.iloc[i]['prix'].replace(",", "."))
            amount_ttc = np.float(self.df.iloc[i]['totalttc'].replace(",", "."))
            amount_ht = None
            service_cost_ht = None
            service_cost_ttc = None
            km = None
            consumption = None
            tva_rate = None
            tva_amount = None
            discount_rate = None
            discout_amount = None

            carte_id =Database2().insert_carte(num=card_number, nom=card_name, nature=nature, extra_nom=extra_name, rang=rangee, texte_additif=additive_text)
            product_id = Database2().insert_produit(code_article=code_product,libelle_article=product_name, groupe_produit=group_product)
            vehicule_id = Database2().insert_vehicule(immatriculation=vehicle)
            fournisseur_id =Database2().insert_fournisseurs(nom=vendor, code_partenaire=partner_code, partenaire=partner)

            Database2().insert_transaction_carburant(id_carte=carte_id,id_produit=product_id,id_vehicule=vehicule_id,id_fournisseurs=fournisseur_id)






           #Database2().insert_client(num=client_number,nom=client_name,message=client_message)
            #Database2().insert_conducteur(nom=driver_name,code=driver_code)
            #Database2().insert_site(num=site_number,nom=site_name)
            #Database2().insert_station(num=station_number,nom=station_name,ref_saisie=station_reference) 
            #Database2().insert_ville(nom=city,code_postal=post_code,departement=departement,pays=country)
            #Database2().insert_vehicule(immatriculation=vehicle)
            #Database2().insert_fournisseurs(nom = vendor)
            #Database2().insert_transaction_carburant (num_transaction=transaction_number,code_transaction=transaction_code,date_transaction=date,heure_transaction=hour,num_facture=invoice_number,date_facture=invoice_date,unite=unity,quantite=quantity,pu_ht=unit_price_ht,pu_ttc=unit_price_ttc ,montant_ttc=amount_ttc,montant_ht=amount_ht,frais_service_ht=service_cost_ht,frais_service_ttc=service_cost_ttc, kilometrage=km,consoL_au100=consumption,taux_tva=tva_rate,montant_tva=tva_amount,taux_remise=discount_rate,montant_remise=discout_amount)
            




            
        
