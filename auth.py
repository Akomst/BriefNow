# auth.py
import streamlit as st
from streamlit_auth0 import Auth0

def authenticate():
    auth0 = Auth0(
        domain="dev-btdcd2ttscxcsa6a.us.auth0.com",
        client_id="Z9cEMfO3ejpW966IB6ISKlHDWAU3aKA5",
        client_secret="DuuYGVoVRPR6Skkg-tB3BVF1bDlADs7jXvze4tshYMbn3tFigRPG9fEUoRukZQMl",
        redirect_uri="https://briefnow.streamlit.app/",
    )

    user_info = auth0.authorize()
    if user_info:
        st.session_state['user'] = user_info
    return user_info

def logout():
    if 'user' in st.session_state:
        del st.session_state['user']
