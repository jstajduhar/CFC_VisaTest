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

import calendar
import datetime
import json
import logging
import unittest

from funds_transfer_api.test.base_test import BaseTest
from funds_transfer_api.helpers.visa_api_client import VisaAPIClient

DEBUG = True

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
'''
@author: visa
'''


class TestMultiPullFundsTransactionGet(BaseTest):

    def setUp(self):
        super(TestMultiPullFundsTransactionGet, self).setUp()
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if DEBUG: print(date)
        self.visa_api_client = VisaAPIClient()
        with open("request_payloads/multi_pull_funds_transaction_get_request.json", 'r') as file:
            self.multi_pull_funds_request = json.load(file)
            self.multi_pull_funds_request['request'][0]['localTransactionDateTime'] = date
            self.multi_pull_funds_request['localTransactionDateTime'] = date

    def test_multi_pull_funds_transactions_get(self):
        status_identifier = self.simulate_multi_pull_timeout()
        base_uri = 'visadirect/'
        resource_path_get_multi_pull = base_uri + 'fundstransfer/v1/multipullfundstransactions/{}'.format(
            status_identifier.decode())
        get_pull_funds_transaction_response = self.visa_api_client.do_mutual_auth_request(
            resource_path_get_multi_pull,
            None,
            'Multi Pull Funds Transaction Test Get',
            'get')

        self.assertEqual(str(get_pull_funds_transaction_response.status_code), "202",
                         "Get Multi Pull funds transaction test failed")
        pass

    def simulate_multi_pull_timeout(self):
        base_uri = 'visadirect/'
        resource_path = 'fundstransfer/v1/multipullfundstransactions'
        # HEADER : X-Client-Transaction-ID
        # Required
        # A unique value for a transaction (unique at the level of the individual service invoker and can
        # be recycled every 24 hours). This identifies the transaction uniquely and can help reference
        # the results of the original transaction.
        # headers = ''
        # generate random number
        d = datetime.datetime.utcnow()
        timestamp = str(calendar.timegm(d.timetuple()))
        headers = {'X-Client-Transaction-ID': timestamp,
                   'x-transaction-timeout-ms': '1'}
        response = self.visa_api_client.do_mutual_auth_request(base_uri + resource_path, self.multi_pull_funds_request,
                                                               'Multi Pull Funds Transaction Test', 'post', headers,
                                                               stream=True)
        self.assertEqual(str(response.status_code), "202", "Multi Pull Funds Transaction test failed")
        self.assertIsNotNone(str(response.content))
        return response.content


# ###############################################################

if __name__ == '__main__':
    unittest.main()
    # END
