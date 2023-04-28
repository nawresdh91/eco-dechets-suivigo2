import pandas as pd
import numpy as np 
import streamlit as st

from database2 import Database2


class Leclerc:
    def __init__(self, file, vendor='Leclerc'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False, encoding='latin-1', dtype=str)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            # stop execution
            st.stop()
        self.vendor = vendor
        #self.__is_leclerc()

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
            for i in range(len(self.df)):
            # get the data
             # get the data from table fournisseur
                vendor = self.vendor
                partner_code=None
                partner = None
                # get the data from table carte
                card_number = int(self.df.iloc[i]['Carte'].replace(" ", ""))
                card_name = None
                extra_name = None
                nature = None
                rangee = None
                additive_text = None
                # get the data from table client
                client_number = self.df.iloc[i]['Numéro client']
                client_name = self.df.iloc[i]['Nom client']
                client_message = None 
            
                # get the data from table conducteur 
                #driver_name = self.df.iloc[i]['Conducteur']    
                driver_code = None
                #get the data from table produit 
                code_product = None
                product_name = self.df.iloc[i]['Produit']
                group_product = None
                
                #get the data from table site 
                site_number = None
                site_name = None
                #get the data from table station
                station_number = self.df.iloc[i]['Point de vente']
                station_name =  None
                station_reference = None
                #get the data from table vehicle
                vehicle =np.str(self.df.iloc[i]['Immatriculation']).replace("-", "")     
                #get the data from table ville
                city = self.df.iloc[i]['Ville']
                post_code = self.df.iloc[i]['Code postal']
                departement = None
                country = None
                #get the data from table transaction_carburant
                transaction_number = self.df.iloc[i]['Numéro de transaction']
                transaction_code = None 
                date = self.df.iloc[i]['Date']
                hour = self.df.iloc[i]['Heure']
                invoice_number = self.df.iloc[i]['Numéro de facture']
                invoice_date = self.df.iloc[i]['Date de facture']
                unity = None
                quantity = np.float(self.df.iloc[i]['Quantité'].replace(',', '.'))
                unit_price_ht = None
                unit_price_ttc = np.float(self.df.iloc[i]['PU TTC'].replace(',', '.'))
                amount_ttc = np.float(self.df.iloc[i]['Montant TTC'].replace(",", "."))
                amount_ht = np.float(self.df.iloc[i]['Montant HT'].replace(",", "."))
                service_cost_ht =  None
                service_cost_ttc =  None

                km = np.int(self.df.iloc[i]['Kilométrage'])
                consumption = None
                tva_rate = np.int(self.df.iloc[i]['Taux TVA'])
                tva_amount = np.float(self.df.iloc[i]['Montant TVA'].replace(",", "."))
                discount_rate = None
                discout_amount = None     
                currency = np.str(self.df.iloc[i]['Devise'])
                status = np.str(self.df.iloc[i]['Statut'])


            

                carte_id =Database2().insert_carte(num=card_number,nom=card_name, nature=nature, extra_nom=extra_name, rang=rangee, texte_additif=additive_text)

                client_id = Database2().insert_client(num=client_number,nom=client_name,message=client_message)
                conducteur_id = Database2().insert_conducteur(nom=None,code=driver_code)


                product_id = Database2().insert_produit(code_article=code_product,libelle_article=product_name, groupe_produit=group_product)

                station_id = Database2().insert_station(num=station_number,nom=station_name,ref_saisie=station_reference,bon_enlevement=None) 
              
                vehicule_id = Database2().insert_vehicule(immatriculation=vehicle)

                fournisseur_id =Database2().insert_fournisseurs(nom=vendor, code_partenaire=partner_code, partenaire=partner)  
               
                Database2().insert_transaction_carburant (id_carte=carte_id,id_client=client_id,id_conducteur=conducteur_id,id_fournisseurs=fournisseur_id, id_station=station_id, id_produit=product_id, id_vehicule=vehicule_id,num_transaction=transaction_number,code_transaction=transaction_code,date_transaction=date,heure_transaction=hour,num_facture=invoice_number,date_facture=invoice_date,unite=unity,quantite=quantity,pu_ht=unit_price_ht,pu_ttc=unit_price_ttc ,montant_ttc=amount_ttc,montant_ht=amount_ht,frais_service_ht=service_cost_ht,frais_service_ttc=service_cost_ttc, kilometrage=km,consoL_au100=consumption,taux_tva=tva_rate,montant_tva=tva_amount,taux_remise=discount_rate,montant_remise=discout_amount,devise=currency,etat=status)
                
                
    def __is_leclerc(self):
        # verify df column exist
        if 'Conducteur' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Leclerc')
            # stop execution
            st.stop()