#!/usr/bin/env python3
import os
import json
import requests
import configparser

config = configparser.ConfigParser()
config.read('keycloak_config')

data = {
        'username': config['creds']['user'],
        'password': config['creds']['password'],
        'grant_type': 'password',
        'client_id': 'admin-cli'
    }

def get_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(config['urls']['token_url'], headers=headers, data=data)
    token = response.json()['access_token']
    return token

def get_keycloak_events(token):
    token = token
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + str(token),
    }

    response = requests.get(config['urls']['events_url'], headers=headers)
    if response.status_code == 200:
        events = response.json()
        newlist = sorted(events, key=lambda k: k['time'])
        f = open("counter.txt", "r")
        last_count = content =f.read()
        f.close()
        log = open('keycloak.log', 'a')
        for message in newlist:
            if int(message['time']) > int(last_count):
                f = open("counter.txt", "w")
                log.write(str(json.dumps(message)) + '\n')
                print(message)
                f.write(str(message['time']))
                f.close()
        log.close()
get_keycloak_events(get_token())

#token_url = https://1q2w3e/auth/realms/master/protocol/openid-connect/token
#events_url = https://1q2w3e/auth/admin/realms/test/events?max=1000
#admin_events_url =  https://1q2w3e/auth/admin/realms/test/admin-events?max=1000
