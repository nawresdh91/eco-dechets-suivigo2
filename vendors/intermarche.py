import numpy as np
import pandas as pd
import streamlit as st

from database2 import Database2


class Intermarche:
    def __init__(self, file, vendor='Intermarche'):
        try:
            # verify if file is csv or excel
            if file.name.endswith('.csv'):
                self.df = pd.read_csv(file, sep=';', index_col=False, dtype=str)
            elif file.name.endswith('.xlsx'):
                self.df = pd.read_excel(file, index_col=False, dtype=str)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        #self.__is_intermarche()
    #renommer les deux colonnes Date et heure en Date et heure 
    def rename_columns(self, old_names=['Date et heure','Date et heure'], new_names=['date','heure']):
        
        try:
            mapping = dict(zip(old_names, new_names))
            self.df = self.df.rename(columns=mapping)
            # renommer la deuxième colonne si elle a le même nom que la première
            if len(set(new_names)) < 2:
                self.df = self.df.rename(columns={new_names[1]: f"{new_names[1]}.1"})
        
        except KeyError as e:
            st.error(f"Les colonnes {e} ne sont pas dans le dataframe.")
            st.stop()

        return self.df 
        


    def show_data(self):
        self.rename_columns()
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
            partner=None
            # get the data from table carte
            card_number = self.df.iloc[i]['Numéro de carte']
            card_name = None
            extra_name = None
            nature = None
            rangee = None
            additive_text = None
            # get the data from table client
            client_number = self.df.iloc[i]['Numéro de client']
            client_name = self.df.iloc[i]['Nom ou raison sociale']
            client_message = None 
        
            # get the data from table conducteur 
            driver_name = None
            driver_code = self.df.iloc[i]['Code du chauffeur']
            #get the data from table produit 
            code_product = self.df.iloc[i]['Code article']
            product_name = self.df.iloc[i]['Libellé article']
            group_product = None
            
            #get the data from table site 
            site_number = self.df.iloc[i]['Numéro de site']
            site_name = self.df.iloc[i]['Nom du site']
            #get the data from table station
            station_number = None
            station_name =  None
            station_reference = None
            #get the data from table vehicle
            vehicle =np.str(self.df.iloc[i]['Immatriculation']).replace("-", "")
            #get the data from table ville
            city = None
            post_code = None
            departement = None
            country = None
            #get the data from table transaction_carburant
            transaction_number = self.df.iloc[i]['Numéro de transaction']
            transaction_code = None 
            #date = self.df.iloc[i]['date']
            #hour = self.df.iloc[i]['heure']
            #invoice_number = self.df.iloc[i]['Numéro de facture']
            #invoice_date = self.df.iloc[i]['Date de facturation']
            unity = None
            quantity = self.df.iloc[i]['Quantité']
            unit_price_ht = None
            unit_price_ttc = None
            amount_ttc = self.df.iloc[i]['Montant TTC']
            amount_ht = self.df.iloc[i]['Montant HT']
            service_cost_ht =  None
            service_cost_ttc =  None

            km = self.df.iloc[i]['Kilométrage']
            consumption = None
            tva_rate = None
            tva_amount = None
            discount_rate = None
            discout_amount = None   
            currency = None
            status = None   



            carte_id =Database2().insert_carte(num=card_number,nom=card_name, nature=nature, extra_nom=extra_name, rang=rangee, texte_additif=additive_text)

            client_id = Database2().insert_client(num=client_number,nom=client_name,message=client_message)
            conducteur_id = Database2().insert_conducteur(nom=driver_name,code=driver_code)


            product_id = Database2().insert_produit(code_article=code_product,libelle_article=product_name, groupe_produit=group_product)

           
           
            #station_id = Database2().insert_station(num=station_number,nom=station_name,ref_saisie=station_reference,bon_enlevement=None) 
            site_id = Database2().insert_site(num=site_number, nom=site_name)
            
            vehicule_id = Database2().insert_vehicule(immatriculation=vehicle)
            fournisseur_id =Database2().insert_fournisseurs(nom=vendor, code_partenaire=partner_code, partenaire=partner)

            Database2().insert_transaction_carburant(id_carte=carte_id,id_client=client_id,id_conducteur=conducteur_id, id_produit=product_id, id_site=site_id, id_vehicule=vehicule_id,id_fournisseurs=fournisseur_id,num_transaction=transaction_number,code_transaction=transaction_code,unite=unity,pu_ht=unit_price_ht,pu_ttc=unit_price_ttc ,frais_service_ht=service_cost_ht,frais_service_ttc=service_cost_ttc, consoL_au100=consumption,taux_tva=tva_rate,montant_tva=tva_amount,taux_remise=discount_rate,montant_remise=discout_amount,devise=currency,etat=status)
            
            
    def __is_intermarche(self):
        # verify df column exist
        if "Immatriculation" in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Intermarche')
            # stop execution
            st.stop()  



































