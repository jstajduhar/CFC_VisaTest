# -*- coding: utf-8 -*-
#  **© Copyright 2018 - 2020 Visa. All Rights Reserved.**
# 
#  *NOTICE: The software and accompanying information and documentation (together, the “Software”) remain the property of and are proprietary to Visa and its suppliers and affiliates. The Software remains protected by intellectual property rights and may be covered by U.S. and foreign patents or patent applications. The Software is licensed and not sold.*
# 
#  * By accessing the Software you are agreeing to Visa's terms of use (developer.visa.com/terms) and privacy policy (developer.visa.com/privacy).In addition, all permissible uses of the Software must be in support of Visa products, programs and services provided through the Visa Developer Program (VDP) platform only (developer.visa.com). **THE SOFTWARE AND ANY ASSOCIATED INFORMATION OR DOCUMENTATION IS PROVIDED ON AN “AS IS,” “AS AVAILABLE,” “WITH ALL FAULTS” BASIS WITHOUT WARRANTY OR  CONDITION OF ANY KIND. YOUR USE IS AT YOUR OWN RISK.** All brand names are the property of their respective owners, used for identification purposes only, and do not imply product endorsement or affiliation with Visa. Any links to third party sites are for your information only and equally  do not constitute a Visa endorsement. Visa has no insight into and control over third party content and code and disclaims all liability for any such components, including continued availability and functionality. Benefits depend on implementation details and business factors and coding steps shown are exemplary only and do not reflect all necessary elements for the described capabilities. Capabilities and features are subject to Visa’s terms and conditions and may require development,implementation and resources by you based on your business and operational details. Please refer to the specific API documentation for details on the requirements, eligibility and geographic availability.*
# 
#  *This Software includes programs, concepts and details under continuing development by Visa. Any Visa features,functionality, implementation, branding, and schedules may be amended, updated or canceled at Visa’s discretion.The timing of widespread availability of programs and functionality is also subject to a number of factors outside Visa’s control,including but not limited to deployment of necessary infrastructure by issuers, acquirers, merchants and mobile device manufacturers.*import json
import json
import logging
import os.path
import random
import string
import sys

import streamlit as st

import requests

if sys.version_info < (3, 0):
    import ConfigParser as parser
else:
    import configparser as parser

import hmac
import datetime
import time
import os
from hashlib import sha256
from jwcrypto import jwk, jwe

import calendar

'''
@author: visa
'''


class VisaAPIClient:
    config = parser.ConfigParser()
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), os.getenv("CONFIG_FILE", "configuration.ini")))
    config.read(config_path)

    logging.getLogger('').addHandler(logging.StreamHandler())
    log = logging.getLogger('VisaAPIClient')
    log.propagate = True

    def _get_x_pay_session(self, shared_secret, resource_path, query_string, body):
        return XSession(shared_secret, resource_path, query_string, body)

    def _get_mutual_auth_session(self, user_name, password, cert, key):
        return MSession(user_name, password, cert, key)

    """
       Correlation Id ( ex-correlation-id ) is an optional header while making an API call. You can skip passing the header while calling the API's.
    """

    def _get_correlation_id(self):
        size = 12
        chars = string.digits
        correlationId = ''.join(random.choice(chars) for _ in range(size)) + '_SC'
        return correlationId

    def _logging_helper(self, url, response, test_info, body):

        # self.log.info("\n\n###############################################")
        self.log.info(test_info)
        self.log.info(url)
        if body != '':
            self.log.info(json.dumps(body, indent=4, sort_keys=True))
        self.log.info("Response Code : " + str(response.status_code))
        self.log.info("Response Headers : ")
        for header in response.headers:
            self.log.info(header + ":" + response.headers[header])
        self.log.info("Response Body : ")
        if response.text != '':
            # it might not be JSON
            try:
                print(response.content)
                self.log.info(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
            except:
                print("Unable to serialize the object")
            finally:
                print(response.content)

        
    def do_mutual_auth_request(self, path, body, test_info, method_type, input_headers={}, stream=False, timeout = 10, mle=False):
        #user_name = self.config.get('VDP','userId')
        #password= self.config.get('VDP','password')
        user_name = st.secrets["VISA_USER_ID"]
        password= st.secrets["VISA_PASSWORD"]
        cert = self.config.get('VDP','cert')
        key = self.config.get('VDP','key')
        if not os.path.isfile(cert):
            cert = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/" + cert
        if not os.path.isfile(key):
            key = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + "/" + key
        end_point = self.config.get('VDP','visaUrl')
        url = end_point + path
        response = {}
        self.session = self._get_mutual_auth_session(user_name, password, cert, key)
        self.log.info(self.session.headers)

        # self.session.headers = self.headers
        if input_headers:
            for key in input_headers.keys():
                self.session.headers[key] = input_headers[key]
        if method_type == 'post' or method_type == 'put':
            self.session.headers.update({'content-type': 'application/json',
                                         'accept': 'application/json',
                                         'x-correlation-id': self._get_correlation_id()})
            if method_type == 'post':
                response = self.session.post(url, json=body, timeout=10)
            if method_type == 'put':
                response = self.session.put(url, json=body, timeout=10)
            self._logging_helper(url, response, test_info, body)
        elif method_type == 'get':
            if 'content-type' in input_headers:
                content_type = input_headers['content_type']
            else:
                content_type = 'application/json'
            self.session.headers.update({'accept': content_type, 'ex-correlation-id': self._get_correlation_id(),
                                         'content-type': 'application/json'})
            response = self.session.get(url, stream=stream, timeout=timeout)
            self._logging_helper(url, response, test_info, '')
        return response

    def do_x_pay_request(self, base_uri, resource_path, query_string, body, test_info, method_type, input_headers={}):
        shared_secret = self.config.get('VDP', 'sharedSecret')
        end_point = self.config.get('VDP', 'visaUrl')
        url = end_point + base_uri + resource_path + '?' + query_string
        self.log.info(url)
        response = {}
        if method_type == 'get':
            self.session = self._get_x_pay_session(shared_secret, resource_path, query_string, '')
        else:
            self.session = self._get_x_pay_session(shared_secret, resource_path, query_string, json.dumps(body))
        if input_headers:
            self.log.info(input_headers)
            for key in input_headers.keys():
                self.session.headers[key] = input_headers[key]
        if method_type == 'post' or method_type == 'put':
            self.session.headers.update({'content-type': 'application/json',
                                         'accept': 'application/json',
                                         'x-pay-token': self.session.x_pay_token,
                                         'ex-correlation-id': self._get_correlation_id()})
            if method_type == 'post':
                response = self.session.post(url, json=body, timeout=10)
            if method_type == 'put':
                response = self.session.put(url, json=body, timeout=10)
            self._logging_helper(url, response, test_info, body)
        elif method_type == 'get':
            self.session.headers.update({
                'x-pay-token': self.session.x_pay_token,
                'x-correlation-id': self._get_correlation_id()})
            response = self.session.get(url, timeout=10)
            self._logging_helper(url, response, test_info, '')
        return response

    def import_key(self, pem_file_location):
        with open(pem_file_location, "rb") as pemfile:
            key = jwk.JWK.from_pem(pemfile.read())
        return key

    def encrypt_payload(self, payload, kid, key):
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A128GCM",
            "typ": "JWE",
            "kid": kid,
            "iat": int(round(time.time() * 1000))
        }
        jwetoken = jwe.JWE(json.dumps(payload).encode('utf-8'),
                           recipient=key,
                           protected=protected_header)

        return {"encData": jwetoken.serialize(compact=True)}

    def log_decrypted_response(self, response):
        decryption_key = self.import_key(self.config.get('VDP', 'mlePrivateKey'))
        print(self.decrypt_response(json.loads(response.text)['encData'], decryption_key))

    def decrypt_response(self, encrypted_payload, decryption_key):
        jwe_token = jwe.JWE()
        jwe_token.deserialize(encrypted_payload, decryption_key)
        return jwe_token.payload


class XSession(requests.Session):
    """ Requests Session for xpaytoken apis
        Construct as XSession(apikey, shared_secret), usage same as
        requests.Session
    """

    def _get_timestamp(self):
        d = datetime.datetime.utcnow()
        timestamp = calendar.timegm(d.timetuple())
        return str(timestamp)

    def _get_x_pay_token(self, shared_secret, resource_path, query_string, body):
        timestamp = self._get_timestamp()
        pre_hash_string = timestamp + resource_path + query_string + body
        if sys.version_info < (3, 0):
            hash_string = hmac.new(shared_secret, msg=pre_hash_string.rstrip(), digestmod=sha256).hexdigest()
        else:
            hash_string = hmac.new(str.encode(shared_secret), msg=pre_hash_string.rstrip().encode('utf-8'),
                                   digestmod=sha256).hexdigest()
        return 'xv2:' + timestamp + ':' + hash_string

    def __init__(self, shared_secret, resource_path, query_string, body):
        super(XSession, self).__init__()
        self.x_pay_token = self._get_x_pay_token(shared_secret, resource_path, query_string, body)


class MSession(requests.Session):
    """Requests Session for mutualauth(2-way SSL) apis
    username, password: App credentials
    cert: path to app's client certificate
    key: path to app's private key
    """

    def __init__(self, username, password, cert, key):
        super(MSession, self).__init__()
        self.cert = (cert, key)
        self.auth = (username, password)
