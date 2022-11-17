import streamlit as st
import pandas as pd


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

    def __is_dats(self):
        # verify df column exist
        if 'CLIENT NO' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier DATS')
            # stop execution
            st.stop()
