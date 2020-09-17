#!/usr/bin/env python3

import requests
import json
import re
import argparse
import uuid

import config


def addTask(orderNumber):
    headers = {
        "Authorization": "Bearer %s" % config.todoist["token"],
        "Content-Type": "application/json",
    }

    payload = "{\r\n    \"content\": \"Ship Amazon Order " + str(orderNumber) + " within 24 hours\",\r\n    \"project_id\":" + config.todoist["project_id"] + ",\r\n    \"due_string\": \"now\",\r\n    \"due_lang\": \"en\",\r\n    \"priority\": 4\r\n}"

    # Create task in todoist
    response = requests.request(
        "POST",
        config.todoist["tasks_endpoint"],
        headers=headers,
        data=payload,
    )

    if response.status_code == 200:
        print("Todoist task added for order " + str(orderNumber))
    else:
        print("Error code: ")
        print(response.status_code)
        print(response.raise_for_status())
