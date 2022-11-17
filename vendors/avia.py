import streamlit as st
import pandas as pd


class Avia:

    def __init__(self, file, vendor='Avia'):
        # try to read file as csv
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False)
            self.back_up = self.df.copy()
        except:
            st.error('Ce fichier n\'est pas un fichier CSV')
            # stop execution
            st.stop()
        self.vendor = vendor
        self.__is_avia()

    def show_data(self):
        if self.vendor == 'Avia':
            return st.write(self.df)
        else:
            return st.write('Le fichier n\'est pas un fichier Avia')

    def __is_avia(self):
        # verify df column exist
        if 'NUM CARTE' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Avia')
            # stop execution
            st.stop()

    def bar_chart(self):
        # bar chart with the total amount of immatriulation
        chart_data = self.df.groupby('MONTANT').sum()

        return st.bar_chart(chart_data)

    def show_filter(self):
        # select box to choose immatriculation
        immatriculation = st.selectbox('Select immatriculation', self.df['IMMATRICULATION'].unique())
        # filter the data with the immatriculation
        self.df = self.df[self.df['IMMATRICULATION'] == immatriculation]
        # self.df['CONSO L au 100'] = pd.to_numeric(self.df['CONSO L au 100'])

        # print mean consommation
        # st.write(f"Mean consommation: {self.df['CONSO L au 100'].mean()}")
