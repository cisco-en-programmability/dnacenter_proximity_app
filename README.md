
# Cisco DNA Center Proximity App


This repo is for an application that will call the new Cisco DNA Center Client Proximity API.
The repo includes also sample software to build a Webhook Receiver that will receive the Client Proximity data
 and generate reports.
 
This app is to be used only in demo or lab environments, it is not written for production. Please follow these
 recommendations for production Flask deployments: https://flask.palletsprojects.com/en/1.1.x/deploying/.




**Cisco Products & Services:**

- Cisco DNA Center

**Tools & Frameworks:**

- Python environment to run the Flask App as a Webhook Receiver

**Usage**

 The "flask_receiver.py" will save the notification to a file for records retention, parse the data and create reports.
 - Create a new Flask App to receive Cisco DNA Center notifications
 
 This sample code is for proof of concepts and labs

**License**

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).


