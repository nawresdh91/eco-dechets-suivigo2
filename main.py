from views import home, statistics

import streamlit as st
import streamlit_authenticator as stauth

from database import Database


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.set_page_config(page_title='Gestion des carburants', page_icon=':fuelpump:', layout='wide')

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
        st.title('Suivie fournisssseurs GO')
        tab1, tab2 = st.tabs(["Home", "Statistics"])
        with tab1:
            st.header('Home')
            home.main()

        with tab2:
            st.header('Statistics')
            statistics.main()
