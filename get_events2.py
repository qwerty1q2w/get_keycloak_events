#!/usr/bin/env python3
import os
import json
import requests
import configparser
from datetime import datetime, timezone
config = configparser.ConfigParser()
config.read('keycloak_config')

data = {
        'client_secret': config['creds']['client_secret'],
        'grant_type': 'client_credentials',
        'client_id': 'logging'
    }

def get_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(config['prod_urls']['token_url'], headers=headers, data=data)
    token = response.json()['access_token']
    return token

def get_keycloak_events(token):
    token = token
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + str(token),
    }

    response = requests.get(config['prod_urls']['events_url'], headers=headers)
    if response.status_code == 200:
#        print(response.json())
        events = response.json()
        newlist = sorted(events, key=lambda k: k['time'])
        f = open("counter.txt", "r")
        last_count = f.read()
        f.close()
        log = open('/var/log/keycloak.log', 'a')
        for message in newlist:
            if int(message['time']) > int(last_count):
                f = open("counter.txt", "w")
                temp_time = int(message['time']) / 1000.0
                message['timestamp'] = datetime.fromtimestamp(temp_time, tz=timezone.utc).isoformat()
                f.write(str(message['time']))
                del message['time']
                log.write(str(json.dumps(message)) + '\n')
                f.close()
        log.close()
get_keycloak_events(get_token())

#token_url = https://1q2w3e/auth/realms/master/protocol/openid-connect/token
#events_url = https://1q2w3e/auth/admin/realms/test/events?max=1000
#admin_events_url =  https://1q2w3e/auth/admin/realms/test/admin-events?max=1000
