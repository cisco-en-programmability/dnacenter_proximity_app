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


def get_destination_details(dnac_auth):
    """
    The function will retrieve all REST based (webhooks) destinations configured
    :param dnac_auth: Cisco DNA Center auth token
    :return: list with all the configured webhooks
    """
    url = DNAC_URL + '/dna/intent/api/v1/event/subscription-details?connectorType=REST'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_auth}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    return response_json


def create_event_subscription(subscription_info, dnac_auth):
    """
    This function will create a new event subscription
    :param subscription_info: subscription info required for the subscription
    :param dnac_auth: Cisco DNA Center auth token
    :return:
    """
    url = DNAC_URL + '/dna/intent/api/v1/event/subscription'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_auth}
    response = requests.post(url, headers=header, data=json.dumps(subscription_info), verify=False)
    response_json = response.json()
    return response_json


def main():
    """
    This application will:
    - retrieve existing REST destinations (webhooks) configured on Cisco DNA Center
    - the webhook destination needs to be configured using the Cisco DNA Center user interface (if not existing)
        System --> Settings --> Destinations
    - will find existing subscriptions for the event with the id {EVENT_ID}
    - create new event subscription (if not existing) for the destination {WEBHOOK_URL}
    """

    # logging, debug level, to file {application_run.log}
    logging.basicConfig(
        filename='application_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"pandemic_proximity_subscription.py" App Run Start, ', current_time)

    # obtain a Cisco DNA Center auth token
    dnac_auth = get_dnac_jwt_token(DNAC_AUTH)

    # get all the configured webhooks destinations
    destinations_list = get_destination_details(dnac_auth)

    # identify the one matching the desired url
    destination_id = ''
    for destination in destinations_list:
        if destination['url'] == WEBHOOK_URL:
            destination_id = destination['instanceId']

    if destination_id is '':
        print('\nDestination for the url ' + WEBHOOK_URL + ' not found')
        print('\nPlease configure the new destination using the Cisco DNA Center UI: ')
        print('System --> Settings --> Destinations')
        current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('\n"pandemic_proximity_subscription.py" App Run End, ', current_time)
        return
    else:
        print('\nDestination for the url ' + WEBHOOK_URL + ' found')

    # verify if existing destination is configured for event
    event_subscriptions = get_event_subscriptions(EVENT_ID, dnac_auth)

    existing_subscription = None
    for subscription in event_subscriptions:
        subscription_id = subscription['subscriptionEndpoints'][0]['instanceId']
        if subscription_id == destination_id:
            existing_subscription = True
            print('\nExisting subscription: ', existing_subscription, ', will not add new subscription')
            current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('\n"pandemic_proximity_subscription.py" App Run End, ', current_time)
            return

    print('\nExisting subscription: ', existing_subscription, ', will add new subscription')

    subscription_info = [
        {
            'name': SUBSCRIPTION_NAME,
            'subscriptionEndpoints': [
                {
                    'instanceId': destination_id,
                    'subscriptionDetails': {
                        'connectorType': 'REST'
                    }
                }
            ],
            'filter': {
                'eventIds': [
                     EVENT_ID
                ]
            }
        }
    ]

    new_subscription = create_event_subscription(subscription_info, dnac_auth)
    print('\nNew subscription API call result:', new_subscription)

    current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"pandemic_proximity_subscription.py" App Run End, ', current_time)


if __name__ == '__main__':
    main()
