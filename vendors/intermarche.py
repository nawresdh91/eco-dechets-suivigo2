import pandas as pd
import streamlit as st

from database import Database


class Intermarche:
    def __init__(self, file, vendor='Intermarche'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False, dtype=str)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        self.__is_intermarche()

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
            card_number = self.df.iloc[i]['Carte']
            vehicle = self.df.iloc[i]['Chauffeur/Véhicule'].replace("-", "")
            date = self.df.iloc[i]['Date']
            product = "GO"
            quantity = self.df.iloc[i]['Quantité']
            amount_ht = self.df.iloc[i]['Montant HT']
            amount_ttc = self.df.iloc[i]['Montant TTC']
            amount = self.df.iloc[i]['Montant TTC']
            vendor = self.vendor
            km = self.df.iloc[i]['Kilométrage']
            Database().insert_go(carte=card_number, vehicule=vehicle, date=date, produit=product, quantite=quantity,
                                 tarif_ht=amount_ht, tarif_ttc=amount_ttc, montant=amount, fournisseur=vendor, km=km)

    def __is_intermarche(self):
        # verify df column exist
        if "Carte" in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Intermarche')
            # stop execution
            st.stop()
