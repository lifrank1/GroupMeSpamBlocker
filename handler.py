import sys
sys.path.insert(0, 'vendor')
import os
import requests
import random
import urllib3
import json

# This should be an AWS Lambda function
API_ROOT = 'https://api.groupme.com/v3/'
FLAGGED_PHRASES = (
    'selling',
    'sex',
    'tickets',
    'ticket',
    'nudes',
    'donate',
    'removemetest',
    'insert phrases you want removed here'
)


def get_memberships(group_id, token):
    response = requests.get(f'{API_ROOT}groups/{group_id}', params={'token': token}).json()['response']['members']
    return response


def get_membership_id(group_id, user_id, token):
    memberships = get_memberships(group_id, token)
    for membership in memberships:
        if membership['user_id'] == user_id:
            return membership['id']


def remove_member(group_id, membership_id, token):
    response = requests.post(f'{API_ROOT}groups/{group_id}/members/{membership_id}/remove', params={'token': token})
    # print('Tried to kick user, got response:')
    # print(response.text)
    return response.ok


def delete_message(group_id, message_id, token):
    response = requests.delete(f'{API_ROOT}conversations/{group_id}/messages/{message_id}', params={'token': token})
    return response.ok


def kick_user(group_id, user_id, token):
    membership_id = get_membership_id(group_id, user_id, token)
    remove_member(group_id, membership_id, token)


def receive(event, context):
    message = json.loads(event['body'])

    # In AWS use secrets to set the token and bot ID
    message['token'] = 'YOUR_TOKEN_HERE'
    bot_id = 'YOUR_BOT_ID_HERE'
    
    # Do not run check if the message is from this bot
    if not('Antispam' in message['name']):
        for phrase in FLAGGED_PHRASES:
            if phrase in message['text'].lower():
                delete_message(message['group_id'], message['id'], message['token'])
                send('Deleted message: "' + message['text'] + '"\nUser: "' + message['name'] + '"\nPhrase: "' + phrase + '"', bot_id)
                break

    return {
        'statusCode': 200,
        'body': 'ok'
    }


def send(text, bot_id):
    url = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)