import pandas as pd
import streamlit as st


class Intermarche:
    def __init__(self, file, vendor='Intermarche'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        self.__is_intermarche()

    def show_data(self):
        return st.write(self.df)

    def __is_intermarche(self):
        # verify df column exist
        if "Carte" in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Intermarche')
            # stop execution
            st.stop()
