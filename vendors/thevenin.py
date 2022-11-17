import pandas as pd
import streamlit as st


class Thevenin:
    def __init__(self, file, vendor='Thevenin'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False, encoding='latin-1')
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        self.__is_thevenin()

    def show_data(self):
        return st.write(self.df)

    def __is_thevenin(self):
        # verify df column exist
        if 'CODE CHAUFFEUR' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Thevenin')
            # stop execution
            st.stop()
