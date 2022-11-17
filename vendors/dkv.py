import streamlit as st
import pandas as pd


class DKV:

    def __init__(self, file, vendor='DKV'):
        # try to read file as csv
        try:
            self.df = pd.read_excel(file, index_col=False)
        except:
            st.error('Ce fichier n\'est pas un fichier Excel')
            #stop execution
            st.stop()
        self.vendor = vendor
        self.__is_dkv()

    def show_data(self):
        # remove unnamed columns
        self.df = self.df.loc[:, ~self.df.columns.str.contains('^Unnamed')]
        # df = self.df.drop(self.df.columns[self.df.columns.str.contains('unnamed',case = False)],axis = 1)
        return st.write(self.df)

    def __is_dkv(self):
        # verify df column exist
        if "N° d'immatriculation" in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier DKV')
            # stop execution
            st.stop()
