#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import requests
import urllib3
import datetime
import json
import time
import logging

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth
from datetime import datetime

from config import DNAC_URL, DNAC_PASS, DNAC_USER
from config import EVENT_ID
from config import SUBSCRIPTION_NAME
from config import WEBHOOK_URL

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)



def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data: data to pretty print
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_epoch_time(timestamp):
    """
    This function will return the epoch time for the {timestamp}, UTC time format, for current time
    :param timestamp: timestamp in UTC format or none
    :return: epoch time including msec
    """
    epoch = time.time()*1000
    return int(epoch)


def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access DNA C
    Call to Cisco DNA Center - /api/system/v1/auth/login
    :param dnac_auth - Cisco DNA Center Basic Auth string
    :return: Cisco DNA Center JWT token
    """
    url = DNAC_URL + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    dnac_jwt_token = response.json()['Token']
    return dnac_jwt_token


def get_event_subscriptions(event_id, dnac_auth):
    """
    This function will find the event subscription for the {event_id}
    :param event_id: Cisco DNA Center event id, example {NETWORK-CLIENTS-3-506}
    :param dnac_auth: Cisco DNA Center auth token
    :return: existing subscriptions info, or [] if none
    """
    url = DNAC_URL + '/dna/intent/api/v1/event/subscription?eventIds=' + event_id + '&limit=100'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_auth}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    return response_json


def main():
    """

    """

    # logging, debug level, to file {application_run.log}
    logging.basicConfig(
        filename='application_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"pandemic_proximity_call.py" App Run Start, ', current_time)

    # obtain a Cisco DNA Center auth token
    dnac_auth = get_dnac_jwt_token(DNAC_AUTH)

    # verify we have existing event subscriptions
    subscription_list = []
    event_subscriptions = get_event_subscriptions(EVENT_ID, dnac_auth)

    for sub in event_subscriptions:
        details = sub['subscriptionEndpoints'][0]['subscriptionDetails']
        subscription_list.append({'url': details['url'], 'name': details['name']})

    print('\nExisting event "' + EVENT_ID + '" subscriptions found:')
    print('{0:40} {1:80}'.format('Name', 'Destination URL'))
    for sub in subscription_list:
        print('{0:40} {1:80}'.format(sub['name'], sub['url']))

    print('\nSubmitting a new pandemic proximity request will send the data to all of these destinations')

    user_input = input('Do you want to continue? (y/n) ')
    if user_input == 'n':
        print('\nNo new pandemic proximity report has been requested')
        return



    current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"pandemic_proximity_call.py" App Run End, ', current_time)


if __name__ == '__main__':
    main()
