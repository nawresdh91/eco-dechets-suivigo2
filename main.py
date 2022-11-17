import pickle
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader

from database import Database
from vendors.avia import Avia
from vendors.dats import DATS
from vendors.dkv import DKV
from vendors.intermarche import Intermarche
from vendors.leclerc import Leclerc
from vendors.thevenin import Thevenin
from vendors.total import Total

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    users = Database().get_users()

    usernames = [user[2] for user in users]
    names = [user[3] for user in users]
    passwords = [user[1] for user in users]

    users_dict = {}
    for i in range(len(users)):
        users_dict[usernames[i]] = {'email': usernames[i], 'name': names[i], 'password': passwords[i]}

    users_dict = {'usernames': users_dict}

    authenticator = stauth.Authenticate(
        users_dict,
        "eco-dechets",
        "HYZg6Z7X627dhb2ey0khe",
    )
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status == False:
        st.error('Authentication failed')
    if authentication_status == None:
        st.info('Authentication required')

    if authentication_status:
        st.title('Import data')
        col1, col2 = st.columns([2, 3])

        authenticator.logout('Se déconnecter', 'sidebar')
        st.sidebar.title(f"Welcome {name}")
        vendor = st.sidebar.selectbox('Selectionner un fournisseur', ('Avia', 'DATS', 'DKV', 'Intermarche', 'Leclerc', 'Thevenin', 'Total'))
        if vendor is not None:
            csv = st.sidebar.file_uploader('Selectionner un fichier CSV ou Excel', type=['csv', 'xlsx', 'xls'])
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

            if csv is not None:
                #data.show_filter()
                data.show_data()

