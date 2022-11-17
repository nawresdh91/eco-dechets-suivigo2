import pandas as pd
import streamlit as st


class Leclerc:
    def __init__(self, file, vendor='Leclerc'):
        try:
            self.df = pd.read_csv(file, sep=';', index_col=False, encoding='latin-1')
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            # stop execution
            st.stop()
        self.vendor = vendor
        #self.__is_leclerc()

    def show_data(self):
        return st.write(self.df)

    def __is_leclerc(self):
        # verify df column exist
        if 'Conducteur' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Leclerc')
            # stop execution
            st.stop()