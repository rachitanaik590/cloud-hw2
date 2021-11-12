import json
import os
import math
import dateutil.parser
import datetime
import time
import logging
import boto3
from botocore.vendored import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    
    return response

    
def lambda_handler(event, context):

    client = boto3.client('lex-runtime',aws_access_key_id='AKIAQXUD5BGIINAUG6UO',
    aws_secret_access_key='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')

    resp = client.post_text(
    botName='PhotoSearch',
    botAlias="photobot",
    userId="test",
    inputText= event["queryStringParameters"]['q'])
    
    response = [resp['slots']['label_a'], resp['slots']['label_b']]
    ans = []
    URL = 'https://search-photos-mmvydcxhqxq4qhnhcwgkkjb7vi.us-east-1.es.amazonaws.com/photos/_search'
    for label in response:
        print(label)
        if (label is None):
            continue
        query = {"size":1000 ,"query": {"match": {"labels":label}}}
        temp = requests.post(URL, data = json.dumps(query), auth = ('ccbdhw2', 'Ccbd2021#'), headers = {'Content-Type': 'application/json'})
        print(temp.json())
        ans.append(temp.json())

    output = []
    for data in ans:
        for item in data['hits']['hits']:
            objectKey = item['_source']['objectKey']
            img_url = "https://s3.amazonaws.com/photos-ccbdhw2/" + objectKey
            output.append(img_url)
    print(output)
    
    if output:
        return{
			'statusCode': 200,
			'headers': {
				"Access-Control-Allow-Origin": "*",
				'Content-Type': 'application/json'
			},
			'body': json.dumps(output)
		}

    return{
        'statusCode': 200,
		'headers': {
			"Access-Control-Allow-Origin": "*",
			'Content-Type': 'application/json'
		},
		'body': json.dumps("No such photos.")
    }