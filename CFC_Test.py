# !/usr/bin/python

import datetime
import json
import unittest

from helpers.response_recorder import ResponseRecorder
from helpers.visa_api_client import VisaAPIClient


class TestFundsTransfer():

    def setUp(self):
        #super(TestFundsTransfer, self).setUp()
        self.visa_api_client = VisaAPIClient()
        self.response_recorder = ResponseRecorder()
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        with open("request_payloads/pull_funds_transaction_request.json", 'r') as file:
            self.pull_funds_request = json.load(file)
            self.pull_funds_request['localTransactionDateTime'] = date
        self.push_funds_request_post = json.loads('''{
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
        self.push_funds_request_get = json.loads('''{
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

    def test_pull_funds_transactions(self):
        base_uri = 'visadirect/'
        resource_path = 'fundstransfer/v1/pullfundstransactions'
        response = self.visa_api_client.do_mutual_auth_request(base_uri + resource_path, self.pull_funds_request,
                                                               'CFC Push Funds Transaction Test', 'post')
        self.response_recorder.record_json_data("pull_funds_transaction_post_response.json",
                                                response.json(encoding='utf-8'))
        #self.assertEqual(str(response.status_code), "200", "Pull Funds Transaction test failed")
    
    def test_push_funds_transactions(self):
        base_uri = 'visadirect/'
        resource_path = 'fundstransfer/v1/pushfundstransactions'
        response = self.visa_api_client.do_mutual_auth_request(base_uri + resource_path, self.push_funds_request_post,
                                                               'CFC Push Funds Transaction Test', 'post')
        #self.assertEqual(str(response.status_code), "200", "Push Funds Transaction test failed")
        
   
    
    def test_pull_fund_transaction_get(self):
        resource_path_get_pull_funds = 'visadirect/fundstransfer/v1/pullfundstransactions/'

        timeout_response = self.simulate_pull_transaction_timeout_pull(self)
        status_identifier = timeout_response.content
        
        get_pull_funds_transaction_response = self.visa_api_client.do_mutual_auth_request(
            resource_path_get_pull_funds + (status_identifier.decode()),
            None,
            'Pull Funds Transaction Test Get',
            'get')
        response_code = get_pull_funds_transaction_response.status_code
               

    def simulate_pull_transaction_timeout_pull(self):
        base_uri = 'visadirect/'
        resource_path = 'fundstransfer/v1/pullfundstransactions'
        timeout_response = self.visa_api_client.do_mutual_auth_request(base_uri + resource_path,
                                                                       self.pull_funds_request,
                                                                       'Pull Funds Transaction Test', 'post',
                                                                       {'x-transaction-timeout-ms': "1"})
       
        return timeout_response

    def test_push_fund_transaction_get(self):
        resource_path_get_push_funds = 'visadirect/fundstransfer/v1/pushfundstransactions/'
        

        timeout_response = self.simulate_push_transaction_timeout_push(self)
        status_identifier = timeout_response.content
        get_push_funds_transaction_response = self.visa_api_client.do_mutual_auth_request(
            resource_path_get_push_funds + (status_identifier.decode()),
            None,
            'Push Funds Transaction Test Get',
            'get')
        
        
        response_code = get_push_funds_transaction_response.status_code
        

    def simulate_push_transaction_timeout_push(self):
        base_uri = 'visadirect/'
        resource_path = 'fundstransfer/v1/pushfundstransactions'
        timeout_response = self.visa_api_client.do_mutual_auth_request(base_uri + resource_path,
                                                                       self.push_funds_request_get,
                                                                       'Push Funds Transaction Test', 'post',
                                                                       {'x-transaction-timeout-ms': "1"})
        
        return timeout_response



# ###############################################################


    # END
