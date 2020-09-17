#!/usr/bin/env python3

import requests
import json
import re
import argparse
import uuid
import base64
from datetime import datetime, timedelta

import config
from todoist import addTask


def createAuth():
    # Create base 64 header auth
    userpass = config.shipstation["API_Key"] + ":" + config.shipstation["API_Secret"]
    encoded_u = base64.b64encode(userpass.encode()).decode()

    return encoded_u


def getOrders():
    headers = {"Authorization": "Basic %s" % createAuth()}
    payload = {}

    # Get unshipped orders from shipstation
    response = requests.request(
        "GET", config.shipstation["orders_endpoint"], headers=headers, data=payload
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
                timeframe = timedelta(hours=config.shipstation["ship_timeframe"])
                if difference > timeframe:
                    # Add urgent tag in shipstation
                    tagUrgent(orders["orders"][index]["orderId"])
                    # Create task in todoist
                    addTask(orders["orders"][index]["orderNumber"])
    else:
        print("No Orders")


def tagUrgent(orderId):
    headers = {"Authorization": "Basic %s" % createAuth()}
    payload = {"orderId": orderId, "tagId": config.shipstation["tag_id"]}

    # Get unshipped orders from shipstation
    response = requests.request(
        "POST", config.shipstation["tag_endpoint"], headers=headers, data=payload
    )

    if response.status_code == 200:
        print("Order " + str(orderId) + " tagged as urgent")
    else:
        print("Error code: ")
        print(response.status_code)
        print(response.raise_for_status())

