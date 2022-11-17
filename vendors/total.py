import pandas as pd
import streamlit as st


class Total:
    def __init__(self, file, vendor='Total'):
        try:
            self.df = pd.read_excel(file, index_col=False)
            self.back_up = self.df.copy()
        except Exception as e:
            st.error(e)
            st.stop()
        self.vendor = vendor
        self.__is_total()

    def show_data(self):
        return st.write(self.df)

    def __is_total(self):
        # verify df column exist
        if 'Référence interne' in self.df.columns:
            return True
        else:
            st.error('Ce fichier n\'est pas un fichier Total')
            # stop execution
            st.stop()
