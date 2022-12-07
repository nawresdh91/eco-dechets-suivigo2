import streamlit as st
from vendors.avia import Avia
from vendors.carrefour import Carrefour
from vendors.dats import DATS
from vendors.dkv import DKV
from vendors.intermarche import Intermarche
from vendors.leclerc import Leclerc
from vendors.thevenin import Thevenin
from vendors.total import Total


def main():
    # authenticator.logout('Se déconnecter', 'main')
    # st.sidebar.title(f"Welcome {name}")
    vendor = st.selectbox('Selectionner un fournisseur',
                          ('Avia', 'DATS', 'DKV', 'Intermarche', 'Leclerc', 'Thevenin', 'Total', 'Carrefour', 'Petrol and Co', 'Soufflet'))

    if vendor is not None:
        csv = st.file_uploader('Selectionner un fichier CSV ou Excel', type=['csv', 'xlsx', 'xls'])
        if csv is not None:
            # check if file is csv or excel
            if vendor == 'Avia':
                data = Avia(file=csv, vendor=vendor)
            elif vendor == 'DATS':
                data = DATS(file=csv, vendor=vendor)
            elif vendor == 'DKV':
                data = DKV(file=csv, vendor=vendor)
            elif vendor == 'Intermarche':
                data = Intermarche(file=csv, vendor=vendor)
            elif vendor == 'Leclerc':
                data = Leclerc(file=csv, vendor=vendor)
            elif vendor == 'Thevenin':
                data = Thevenin(file=csv, vendor=vendor)
            elif vendor == 'Total':
                data = Total(file=csv, vendor=vendor)
            elif vendor == 'Carrefour':
                data = Carrefour(file=csv, vendor=vendor)
            elif vendor == 'Petrol and Co':
                data = Carrefour(file=csv, vendor=vendor)
            elif vendor == 'Soufflet':
                data = Carrefour(file=csv, vendor=vendor)

        if vendor in ('Carrefour', 'Petrol And Co', 'Soufflet'):
            Carrefour.show_download_btn(csv)

        if csv is not None:
            # data.show_filter()
            data.show_upload_btn()
            data.show_data()
