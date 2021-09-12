# -*- coding: utf-8 -*-

#  **© Copyright 2018 - 2020 Visa. All Rights Reserved.**
#
#  *NOTICE: The software and accompanying information and documentation (together, the “Software”) remain the property of and are proprietary to Visa and its suppliers and affiliates. The Software remains protected by intellectual property rights and may be covered by U.S. and foreign patents or patent applications. The Software is licensed and not sold.*
#
#  * By accessing the Software you are agreeing to Visa's terms of use (developer.visa.com/terms) and privacy policy (developer.visa.com/privacy).In addition, all permissible uses of the Software must be in support of Visa products, programs and services provided through the Visa Developer Program (VDP) platform only (developer.visa.com). **THE SOFTWARE AND ANY ASSOCIATED INFORMATION OR DOCUMENTATION IS PROVIDED ON AN “AS IS,” “AS AVAILABLE,” “WITH ALL FAULTS” BASIS WITHOUT WARRANTY OR  CONDITION OF ANY KIND. YOUR USE IS AT YOUR OWN RISK.** All brand names are the property of their respective owners, used for identification purposes only, and do not imply product endorsement or affiliation with Visa. Any links to third party sites are for your information only and equally  do not constitute a Visa endorsement. Visa has no insight into and control over third party content and code and disclaims all liability for any such components, including continued availability and functionality. Benefits depend on implementation details and business factors and coding steps shown are exemplary only and do not reflect all necessary elements for the described capabilities. Capabilities and features are subject to Visa’s terms and conditions and may require development,implementation and resources by you based on your business and operational details. Please refer to the specific API documentation for details on the requirements, eligibility and geographic availability.*
#
#  *This Software includes programs, concepts and details under continuing development by Visa. Any Visa features,functionality, implementation, branding, and schedules may be amended, updated or canceled at Visa’s discretion.The timing of widespread availability of programs and functionality is also subject to a number of factors outside Visa’s control,including but not limited to deployment of necessary infrastructure by issuers, acquirers, merchants and mobile device manufacturers.*
#

# !/usr/bin/python

import datetime
import json
import logging
import sys
import unittest

from funds_transfer_api.helpers.response_recorder import ResponseRecorder
from funds_transfer_api.test.base_test import BaseTest
from funds_transfer_api.helpers.visa_api_client import VisaAPIClient

DEBUG = False

if DEBUG:

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

if sys.version_info < (3, 0):
    pass
else:
    pass
'''
@author: visa
'''


class TestPushFundsTransactionGet(BaseTest):
    def setUp(self):
        super(TestPushFundsTransactionGet, self).setUp()
        self.visa_api_client = VisaAPIClient()
        self.response_recorder = ResponseRecorder()
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        self.push_funds_request = json.loads('''{
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

    def test_push_funds_transactions(self):
        base_uri = 'visadirect/'
        resource_path = 'fundstransfer/v1/pushfundstransactions'
        response = self.visa_api_client.do_mutual_auth_request(base_uri + resource_path, self.push_funds_request,
                                                               'Push Funds Transaction Test', 'post')
        self.assertEqual(str(response.status_code), "200", "Push Funds Transaction test failed")
        pass

    def test_pull_fund_transaction_get(self):
        resource_path_get_pull_funds = 'visadirect/fundstransfer/v1/pushfundstransactions/'

        timeout_response = self.simulate_push_transaction_timeout()
        status_identifier = timeout_response.content
        get_pull_funds_transaction_response = self.visa_api_client.do_mutual_auth_request(
            resource_path_get_pull_funds + (status_identifier.decode()),
            None,
            'Push Funds Transaction Test Get',
            'get')
        response_code = get_pull_funds_transaction_response.status_code
        self.assertTrue(response_code >= 200 and response_code <= 299,
                         "Get Push funds transaction test failed")

    pass

    def simulate_push_transaction_timeout(self):
        base_uri = 'visadirect/'
        resource_path = 'fundstransfer/v1/pushfundstransactions'
        timeout_response = self.visa_api_client.do_mutual_auth_request(base_uri + resource_path,
                                                                       self.push_funds_request,
                                                                       'Push Funds Transaction Test', 'post',
                                                                       {'x-transaction-timeout-ms': "1"},
                                                                       stream=True)
        self.assertEqual(str(timeout_response.status_code), "202", "Pull Funds Transaction didnot time out")
        self.assertIsNotNone(timeout_response.content)
        return timeout_response


# ###############################################################

if __name__ == '__main__':
    unittest.main()
    # END
