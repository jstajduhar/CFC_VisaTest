import streamlit as st
import datetime
import json

#from helpers.response_recorder import ResponseRecorder
from helpers.visa_api_client import VisaAPIClient

pull_funds_request = ""
push_funds_request_post = ""
visa_api_client

def submitTest(cust,vendor,amt):
    st.text('Payment submitted')
	
    test_pull_funds_transactions(cust,vendor,amt)
    test_push_funds_transactions(cust,vendor,amt)
	
    st.text('Payment completed')
    st.text('Customer ${cust} paid Vendor ${vendor} $${amt}')
	
    return
	
def test_pull_funds_transactions(cust,vendor,amt):
    base_uri = 'visadirect/'
    resource_path = 'fundstransfer/v1/pullfundstransactions'
	
    pull_funds_request['senderAccountNumber'] = cust
    pull_funds_request['amount'] = amt
    
    response = visa_api_client.do_mutual_auth_request(base_uri + resource_path, pull_funds_request,
                                                               'CFC Push Funds Transaction Test', 'post')
    #self.response_recorder.record_json_data("pull_funds_transaction_post_response.json",
     #                                       response.json(encoding='utf-8'))
    
def test_push_funds_transactions(cust,vendor,amt):
    base_uri = 'visadirect/'
    resource_path = 'fundstransfer/v1/pushfundstransactions'
	
    push_funds_request_post['senderAccountNumber'] = cust
    push_funds_request_post['recipientPrimaryAccountNumber'] = vendor
    push_funds_request_post['amount'] = amt
    
    response = visa_api_client.do_mutual_auth_request(base_uri + resource_path, push_funds_request_post,
                                                               'CFC Push Funds Transaction Test', 'post')
															   
def setUpTest():
    st.text('Successfully called function')
	
def setUp():
    global pull_funds_request
    global push_funds_request_post
    global visa_api_client
    
    #super(TestFundsTransfer, self).setUp()
    visa_api_client = VisaAPIClient()
    #self.response_recorder = ResponseRecorder()
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open("request_payloads/pull_funds_transaction_request.json", 'r') as file:
        pull_funds_request = json.load(file)
        pull_funds_request['localTransactionDateTime'] = date
        push_funds_request_post = json.loads('''{
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "amount": "124.05",
            "businessApplicationId": "AA",
            "cardAcceptor": {
            "address": {
            "country": "USA",
            "county": "San Mateo",
            "state": "CA",
            "zipCode": "94404"
            },
            "idCode": "CA-IDCode-77765",
            "name": "Visa Inc. USA-Foster City",
            "terminalId": "TID-9999"
            },
            "localTransactionDateTime": "''' + date + '''",
            "merchantCategoryCode": "6012",
            "pointOfServiceData": {
            "motoECIIndicator": "0",
            "panEntryMode": "90",
            "posConditionCode": "00"
            },
            "recipientName": "rohan",
            "recipientPrimaryAccountNumber": "4957030420210462",
            "retrievalReferenceNumber": "412770451018",
            "senderAccountNumber": "4957030420210454",
            "senderAddress": "901 Metro Center Blvd",
            "senderCity": "Foster City",
            "senderCountryCode": "124",
            "senderName": "Mohammed Qasim",
            "senderReference": "",
            "senderStateCode": "CA",
            "sourceOfFundsCode": "05",
            "systemsTraceAuditNumber": "451018",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "381228649430015"
        }''')
    

"""
# Code for Charlottesville
Visa API Test
Submit Transactions

"""

setUp()

customer_acct = st.text_input("Customer Account: ", 4957030420210454)

vendor_acct = st.text_input("Vendor Account: ", 4957030420210462)

amount = st.text_input("Amount: ", 90.14)

if(st.button("Submit")):
    submitTest(customer_acct, vendor_acct, amount)
	



