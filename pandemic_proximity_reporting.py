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


import urllib3
import json
import os
import time
import datetime

from fpdf import FPDF  # for creating pdf files

from flask import Flask, request, abort, send_from_directory
from flask_basicauth import BasicAuth

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings


os.environ['TZ'] = 'America/Los_Angeles'  # define the timezone for PST
time.tzset()  # adjust the timezone, more info https://help.pythonanywhere.com/pages/SettingTheTimezone/

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

from config import WEBHOOK_URL, WEBHOOK_USERNAME, WEBHOOK_PASSWORD


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = WEBHOOK_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = WEBHOOK_PASSWORD
# app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


@app.route('/')  # create a page for testing the flask framework
# @basic_auth.required
def index():
    return '<h1>Flask Receiver App is Up!</h1>', 200


@app.route('/client_proximity_data', methods=['GET'])  # create a return detailed logs file
@basic_auth.required
def detailed_logs():
    print('File client_proximity_data.log requested, transfer started')
    return send_from_directory('', 'client_proximity_data.log', as_attachment=True)


@app.route('/proximity', methods=['POST'])  # create a route for /proximity, method POST, to receive the webhook with
@basic_auth.required
def proximity_webhook():
    if request.method == 'POST':
        print('Proximity Webhook Received')
        webhook_json = request.json

        # save as a file, create new file if not existing, append to existing file, full details of each notification
        with open('client_proximity_data.log', 'a') as filehandle:
            filehandle.write('%s\n' % json.dumps(webhook_json))

        # print the received notification
        print('Payload: ')
        print(webhook_json)

        # create reports with the data received
        proximity_details = webhook_json['details']
        username = proximity_details['user_name']
        time_resolution = proximity_details['time_resolution']
        number_days = proximity_details['number_days']
        start_time_epoch = int(proximity_details['start_time'])
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(start_time_epoch/1000)))
        end_time_epoch = int(proximity_details['end_time'])
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(end_time_epoch/1000)))
        proximity_data = proximity_details['client_proximity']

        # create reports for each wireless client in the list of devices
        for data_set in proximity_data:
            wireless_mac_address = data_set['mac_address']
            client_info = data_set['client_info']

            # create report for proximity time for each client
            # data structure
            # user_info: client_mac, username, device type, total time in proximity of pandemic positive employee
            users_list_time = []
            users_unique_list = set()
            # loop through all time intervals, collect all wireless clients and length of time in proximity
            for event in client_info:
                time_length = int(event['end_time']) - int(event['start_time'])
                # loop through all users in each time interval
                for user in event['users_info']:
                    user_updated_with_time = {**user, **{'time_length': time_length}}
                    users_list_time.append(user_updated_with_time)
                    users_unique_list.add(user['client_mac'])

            # add all time intervals
            users_list_total_time = []
            for unique_user in users_unique_list:
                total_time = 0
                for user in users_list_time:
                    if unique_user == user['client_mac']:
                        total_time += user['time_length']
                        user_details = {
                            'client_mac': user['client_mac'], 'client_user': user['client_user'],
                            'client_type': user['client_type']
                        }
                total_time_dhms = str(datetime.timedelta(seconds=int(total_time/1000)))
                user_details.update({'total_time': total_time_dhms})
                users_list_total_time.append(user_details)

        print(users_list_total_time)

        # send the response message
        return 'Webhook Received', 202
    else:
        return 'POST Method not supported', 405


if __name__ == '__main__':
    app.run(debug=True)
