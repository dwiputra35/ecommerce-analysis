import streamlit as st
import eda
import dashboard

st.set_page_config(page_title='Ecommerce Analysis', layout='wide', initial_sidebar_state='expanded')

navigation = st.sidebar.selectbox('Pilih Halaman:', ('Exploratory Data Analysis', 'Dashboard'))

if navigation == 'Exploratory Data Analysis':
    eda.run()
elif navigation == 'Dashboard': 
    dashboard.run()
