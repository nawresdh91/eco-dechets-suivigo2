import webbrowser

import numpy as np
import pandas as pd
import streamlit as st

from database import Database

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
            st.info(
                'Pour ce founisseur, vous devez télécharger le fichier excel de référence et le completer manuellement.')
            if st.button('Télécharger le fichier'):
                webbrowser.open_new_tab(url)

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
            card_number = np.int(self.df.iloc[i]['carte'])
            vehicle = self.df.iloc[i]['vehicule'].replace("-", "")
            date = self.df.iloc[i]['Date']
            product = "GO"
            quantity = self.df.iloc[i]['Quantité']
            amount_ht = self.df.iloc[i]['Tarif HT']
            amount_ttc = self.df.iloc[i]['Tarif TTC']
            amount = self.df.iloc[i]['Montant TTC']
            vendor = self.vendor
            km = None
            print(card_number, vehicle, date, product, quantity, amount_ht, amount_ttc, amount, vendor, km)
            Database().insert_go(carte=card_number, vehicule=vehicle, date=date, produit=product, quantite=quantity,
                                 tarif_ht=amount_ht, tarif_ttc=amount_ttc, montant=amount, fournisseur=vendor, km=km)
