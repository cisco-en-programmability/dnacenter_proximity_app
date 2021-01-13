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


# This file contains:
# Webhook URL
WEBHOOK_URL = 'https://webhook_url'

# Cisco DNA Center dnalive
DNAC_URL = 'https://dnac_url'
DNAC_USER = 'username'
DNAC_PASS = 'password'

# Proximity API config params
DAYS = 14  # number of days to search for contact tracing
TIME_RESOLUTION = 5  # 15 minutes time resolution

username = 'gabiz'

# Proximity API event and subscription
EVENT_ID = 'NETWORK-CLIENTS-3-506'
SUBSCRIPTION_NAME = 'Proximity Event Subscription'


