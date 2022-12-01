import numpy as np
import streamlit as st
import pandas as pd

from database import Database


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
            card_number = np.int(self.df.iloc[i]['CARTE NO'])
            vehicle = self.df.iloc[i]['NO DE PLAQUE']
            date = self.df.iloc[i]['DATE']
            product = "GO"  # self.df.iloc[i]['PRODUIT']
            quantity = np.float(self.df.iloc[i]['QUANT'].replace(',', '.'))
            amount_ht = np.float(self.df.iloc[i]['MONTANT TVA EXCL'].replace(",", "."))
            amount_ttc = np.float(self.df.iloc[i]['MONTANT TVA INCL'].replace(",", "."))
            amount = np.float(self.df.iloc[i]['MONTANT TVA INCL'].replace(",", "."))
            vendor = self.vendor
            km = np.int(self.df.iloc[i]['KILOMETRAGE'])
            Database().insert_go(carte=card_number, vehicule=vehicle, date=date, produit=product, quantite=quantity,
                                 tarif_ht=amount_ht, tarif_ttc=amount_ttc, montant=amount, fournisseur=vendor, km=km)

    def __is_dats(self):
        # verify df column exist
        if 'CLIENT NO' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier DATS')
            # stop execution
            st.stop()
