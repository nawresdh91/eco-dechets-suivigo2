import numpy as np

import streamlit as st
import pandas as pd

from database import Database


class DKV:

    def __init__(self, file, vendor='DKV'):
        # try to read file as csv
        try:
            self.df = pd.read_excel(file, index_col=False, dtype=str)
        except:
            st.error('Ce fichier n\'est pas un fichier Excel')
            # stop execution
            st.stop()
        self.vendor = vendor
        self.__is_dkv()

    def show_data(self):
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
            card_number = self.df.iloc[i]['Numéro de carte ou boîtier']
            vehicle = np.str(self.df.iloc[i]['N° d\'immatriculation']).replace("-", "")
            date = self.df.iloc[i]['Date de facturation']
            product = "GO"  # self.df.iloc[i]['Produit']
            quantity = None
            amount_ht = self.df.iloc[i]["Prix d'achat HT"]
            amount_ttc = self.df.iloc[i]["Prix d'achat TTC"]
            amount = self.df.iloc[i]["Prix d'achat TTC"]
            vendor = self.vendor
            km = np.int(self.df.iloc[i]['Kilométrage'])
            Database().insert_go(carte=card_number, vehicule=vehicle, date=date, produit=product, quantite=quantity,
                                 tarif_ht=amount_ht, tarif_ttc=amount_ttc, montant=amount, fournisseur=vendor, km=km)

    def __is_dkv(self):
        # verify df column exist
        if "N° d'immatriculation" in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier DKV')
            # stop execution
            st.stop()
