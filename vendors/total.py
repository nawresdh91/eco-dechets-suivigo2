import numpy as np

import pandas as pd
import streamlit as st

from database import Database


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
            card_number = self.df.iloc[i]['Carte']
            vehicle = self.df.iloc[i]['Immatriculation'].replace("-", "")
            date = self.df.iloc[i]['Date']
            product = "GO"
            quantity = self.df.iloc[i]['Quantité']
            amount_ht = self.df.iloc[i]['Montant HT']
            amount_ttc = self.df.iloc[i]['Montant TTC']
            amount = self.df.iloc[i]['Montant TTC']
            vendor = self.vendor

            # get the km and replace NA by None
            km = self.df.iloc[i]['Kilométrage']

            #print(card_number, vehicle, date, product, quantity, amount_ht, amount_ttc, amount, vendor, km)

            Database().insert_go(carte=card_number, vehicule=vehicle, date=date, produit=product, quantite=quantity,tarif_ht=amount_ht, tarif_ttc=amount_ttc, montant=amount, fournisseur=vendor, km=km)

    def __is_total(self):
        # verify df column exist
        if 'Référence interne' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Total')
            # stop execution
            st.stop()
