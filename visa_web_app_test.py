import streamlit as st

"""
# Code for Charlottesville
Visa API Test
Submit Transactions

"""

customer_acct = st.text_input("Customer Account: ")

vendor_acct = st.text_input("Vendor Account: ")

amount = st.text_input("Amount: ", 0.00)

if(st.button("Submit")):
    st.text('Customer ' + customer_acct + ' paid Vendor ' + vendor_acct + ' $' + amount)



