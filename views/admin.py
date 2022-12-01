from database import Database
import pandas as pd
import streamlit as st


def main():
    col1, col2 = st.columns(2)
    user = Database().get_user(st.session_state["username"])
    user_email = user[2]

    if user_email in st.secrets["ADMIN"]:
        st.header('Admin')
        with st.form(key='my_form', clear_on_submit=True):
            email = st.text_input('Email')
            name = st.text_input('Name')
            password = st.text_input(value=Database.generate_password(), label="Mot de passe")

            submitted = st.form_submit_button("Save")

            if submitted:
                with st.spinner('Wait for it...'):
                    try:
                        Database().insert_user(password=password, email=email, name=name)
                        st.success('User added')
                    except Exception as e:
                        print(e)
                        st.error(e)
                        st.stop()

    else:
        st.title('You are not allowed to access this page')