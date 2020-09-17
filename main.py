#!/usr/bin/env python3
"""
Amazon Order Alert
"""

__author__ = "Chris Loidolt"
__version__ = "0.1.0"
__license__ = "GNU 3.0"

import requests
import json
import re
import argparse
import uuid
import base64
from datetime import datetime, timedelta

####
## Config
####

shipstation = dict(
    API_Key="",
    API_Secret="",
    orders_endpoint="https://ssapi.shipstation.com/orders?orderStatus=awaiting_shipment",
    tag_endpoint="https://ssapi.shipstation.com/orders/addtag",
    # Safe shipping timeframe in hours
    ship_timeframe=48,
    # Tag ID for the urgent tag
    tag_id="103434",
)

todoist = dict(
    token="", tasks_endpoint="https://api.todoist.com/rest/v1/tasks", project_id="",
)


####
## Shipstation
####


def createAuth():
    # Create base 64 header auth
    userpass = shipstation["API_Key"] + ":" + shipstation["API_Secret"]
    encoded_u = base64.b64encode(userpass.encode()).decode()

    return encoded_u


def getOrders():
    headers = {"Authorization": "Basic %s" % createAuth()}
    payload = {}

    # Get unshipped orders from shipstation
    response = requests.request(
        "GET", shipstation["orders_endpoint"], headers=headers, data=payload
    )

    if response.status_code == 200:
        res_dict = response.json()
        filterOrders(res_dict)
    else:
        print("Error code: ")
        print(response.status_code)
        print(response.raise_for_status())


def filterOrders(orders):
    # Iterate through orders
    if orders != []:
        for index in range(len(orders["orders"])):
            # Check if order notes contain an amazon order ID
            notes = str(orders["orders"][index]["customerNotes"])
            if "Amazon Order ID:" in notes:
                print(orders["orders"][index]["orderNumber"])
                # Get order date and current timestamp
                orderDate = datetime.strptime(
                    str(orders["orders"][index]["orderDate"]), "%Y-%m-%dT%H:%M:%S.%f0"
                )
                currentDate = datetime.now()
                # Check if order creation date is outside shipping timeframe
                difference = currentDate - orderDate
                timeframe = timedelta(hours=shipstation["ship_timeframe"])
                if difference > timeframe:
                    # Add urgent tag in shipstation
                    tagUrgent(orders["orders"][index]["orderId"])
                    # Create task in todoist
                    addTask(orders["orders"][index]["orderNumber"])
    else:
        print("No Orders")


def tagUrgent(orderId):
    headers = {"Authorization": "Basic %s" % createAuth()}
    payload = {"orderId": orderId, "tagId": shipstation["tag_id"]}

    # Get unshipped orders from shipstation
    response = requests.request(
        "POST", shipstation["tag_endpoint"], headers=headers, data=payload
    )

    if response.status_code == 200:
        print("Order " + str(orderId) + " tagged as urgent")
    else:
        print("Error code: ")
        print(response.status_code)
        print(response.raise_for_status())


####
## Todoist
####


def addTask(orderNumber):
    headers = {
        "Authorization": "Bearer %s" % todoist["token"],
        "Content-Type": "application/json",
    }

    payload = (
        '{\r\n    "content": "Ship Amazon Order '
        + str(orderNumber)
        + ' within 24 hours",\r\n    "project_id":'
        + todoist["project_id"]
        + ',\r\n    "due_string": "now",\r\n    "due_lang": "en",\r\n    "priority": 4\r\n}'
    )

    # Create task in todoist
    response = requests.request(
        "POST", todoist["tasks_endpoint"], headers=headers, data=payload,
    )

    if response.status_code == 200:
        print("Todoist task added for order " + str(orderNumber))
    else:
        print("Error code: ")
        print(response.status_code)
        print(response.raise_for_status())


####
## Main
####


def main():
    """ Main entry point of the app """
    getOrders()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
