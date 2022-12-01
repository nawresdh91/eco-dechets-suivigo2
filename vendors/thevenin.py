import pandas as pd
import streamlit as st

from database import Database


class Thevenin:
    def __init__(self, file, vendor='Thevenin'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False, encoding='latin-1', dtype=str)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        self.__is_thevenin()

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
            card_number = self.df.iloc[i]['NUM CARTE'].replace("'", "")
            vehicle = self.df.iloc[i]['IMMATRICULATION'].replace(" ", "")
            date = self.df.iloc[i]['DATE']
            product = "GO"
            quantity = self.df.iloc[i]['QUANTITE']
            amount_ht = None
            amount_ttc = self.df.iloc[i]['MONTANT']
            amount = self.df.iloc[i]['MONTANT']
            vendor = self.vendor
            km = self.df.iloc[i]['KM']
            Database().insert_go(carte=card_number, vehicule=vehicle, date=date, produit=product, quantite=quantity,
                                 tarif_ht=amount_ht, tarif_ttc=amount_ttc, montant=amount, fournisseur=vendor, km=km)

    def __is_thevenin(self):
        # verify df column exist
        if 'NUM SITE' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Thevenin')
            # stop execution
            st.stop()
