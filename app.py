import streamlit as st
import os
from dotenv import load_dotenv
import streamlit_google_oauth as oauth
import pharmacyAssistant
import pandas as pd


load_dotenv()
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]


if __name__ == "__main__":
    login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        login_button_text="Continue with Google",
        logout_button_text="Logout",
    )
    if login_info:
        
        user_id, user_email = login_info
        container = st.container()
        with container:
            st.write(f"Welcome {user_email}")
            Excel_file = 'Source.xlsx'
            sheet_name = 'DATA'
            df = pd.read_excel(Excel_file,engine='openpyxl',sheet_name=sheet_name,usecols='A:C',header=0)
            st.dataframe(pharmacyAssistant.filter_dataframe(df))
    else:
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with right_column:
                    st.write("Please login")
# streamlit run app.py --server.port 8080
