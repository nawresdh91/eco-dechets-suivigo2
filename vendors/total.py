import numpy as np
import pandas as pd
import streamlit as st

from database2 import Database2


class Total:
    def __init__(self, file, vendor='Total'):
        try:
            self.df = pd.read_excel(file, index_col=False, dtype=str)
            self.df = self.df.astype(object).where(pd.notnull(self.df),None)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        self.__is_total()

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
        #print columns
        print(self.df.columns)
        for i in range(len(self.df)):
            # get the data
            # get the data from table fournisseur
            vendor = self.vendor
            partner_code = self.df.iloc[i]["Code partenaire"]
            partner = self.df.iloc[i]["Partenaire"]

            # get the data from table carte
            card_number = self.df.iloc[i]['Carte']
            card_name = None
            extra_name = None
            nature = self.df.iloc[i]['Nature Carte']
            range = self.df.iloc[i]['Rang']
            additive_text = None
            # get the data from table client
            client_number = self.df.iloc[i]['Code Client']
            client_name = None
            client_message = self.df.iloc[i]['Message client'] 
            # get the data from table conducteur 
            driver_name = None
            driver_code = self.df.iloc[i]['Code Conducteur']
            #get the data from table produit 
            code_product = self.df.iloc[i]['Code produit']
            product_name = self.df.iloc[i]['Désignation Produit']
            group_product = None
            
            #get the data from table site 
            site_number = self.df.iloc[i]['NUM SITE']
            site_name = None 
            #get the data from table station
            station_number = self.df.iloc[i]['Code lieu enlevement']
            station_name =self.df.iloc[i]['Lieu enlévement']  
            station_reference = self.df.iloc[i]['Reference saisie en station']
            receipt = None

            #get the data from table vehicle
            vehicle = self.df.iloc[i]['Immatriculation'].replace("-", "")
            #get the data from table ville
            city = self.df.iloc[i]['Ville']
            post_code = self.df.iloc[i]['CP']
            departement = None
            country = None 
            #get the data from table transaction_carburant
            transaction_number = None
            transaction_code = None 
            date = self.df.iloc[i]['Date']
            hour = self.df.iloc[i]['Heure']
            invoice_number = self.df.iloc[i]['Element facturation']
            invoice_date = self.df.iloc[i]['Date Reception Transaction']
            unity = None
            quantity = np.float(self.df.iloc[i]['Quantité'].replace(",", "."))
            unit_price_ht = None
            unit_price_ttc = np.float(self.df.iloc[i]['Prix Unitaire'].replace(",", "."))
            amount_ttc = np.float(self.df.iloc[i]['Montant TTC'].replace(",", "."))
            amount_ht = np.float(self.df.iloc[i]['Montant HT'].replace(",", "."))
            service_cost_ht = None
            service_cost_ttc = None
            km = self.df.iloc[i]['Kilométrage']
            consumption = np.float(self.df.iloc[i]['CONSO L au 100'])
            tva_rate = self.df.iloc[i]['Taux de TVA']
            tva_amount = self.df.iloc[i]['Montant de TVA']
            discount_rate = self.df.iloc[i]['Taux remise']
            discout_amount = self.df.iloc[i]['Montant remise']
            currency = self.df.iloc[i]['Devise']
            status = None
            additional_information = self.df.iloc[i]['Mention Complémentaire']




            Database2().insert_carte(num=card_number,nom=card_name, nature=nature , extra_nom=extra_name,rang=range,texte_additif=additive_text)
            Database2().insert_client(num=client_number,nom=client_name,message=client_message)
            Database2().insert_conducteur(nom=driver_name,code=driver_code)
            Database2().insert_produit(code_article=code_product,libelle_article=product_name,groupe_produit=group_product)
            Database2().insert_site(num=site_number,nom=site_name)
            Database2().insert_station(num=station_number,nom=station_name,ref_saisie=station_reference,bon_enlevement=receipt) 
            Database2().insert_ville(nom=city,code_postal=post_code,departement=departement,pays=country)
            Database2().insert_vehicule(immatriculation=vehicle)
            Database2().insert_fournisseurs(nom = vendor,code_partenaire=partner_code,partenaire=partner)
            Database2().insert_fournisseurs(nom=vendor) 
            Database2().insert_transaction_carburant (num_transaction=transaction_number,code_transaction=transaction_code,date_transaction=date,heure_transaction=hour,num_facture=invoice_number,date_facture=invoice_date,unite=unity,quantite=quantity,pu_ht=unit_price_ht,pu_ttc=unit_price_ttc ,montant_ttc=amount_ttc,montant_ht=amount_ht,frais_service_ht=service_cost_ht,frais_service_ttc=service_cost_ttc, kilometrage=km,consoL_au100=consumption,taux_tva=tva_rate,montant_tva=tva_amount,taux_remise=discount_rate,montant_remise=discout_amount,devise=currency,etat=status,mention_complementaire=additional_information)
                

    def __is_total(self):
        # verify df column exist
        if 'Référence interne' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Total')
            # stop execution
            st.stop()
