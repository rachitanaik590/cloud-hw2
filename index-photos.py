import json
import boto3
from botocore.vendored import requests
import datetime

def lambda_handler(event, context):
    
    s3 = boto3.client('s3', aws_access_key_id='AKIAQXUD5BGIINAUG6UO',
    aws_secret_access_key='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')
    rek = boto3.client('rekognition', aws_access_key_id='AKIAQXUD5BGIINAUG6UO',
    aws_secret_access_key='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')
    
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    metadata = s3.head_object(Bucket=bucket, Key=key)
    
    print(bucket, key)
    labels = set()
    print(metadata)
    if 'customlabels' in metadata['Metadata']:
        labels = set(metadata['Metadata']['customlabels'].split(','))
    
    response = rek.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MinConfidence = 95
    )
    
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        labels.add(label['Name'])
    
    print(labels)  
    document = {
        "objectKey" : key,
        "bucket" : bucket,
        "createdTimeStamp" : datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"), #"2020-05-02 17:32:55",
        "labels" : list(labels)
        
    }
   
    print(document)
    url = 'https://search-photos-mmvydcxhqxq4qhnhcwgkkjb7vi.us-east-1.es.amazonaws.com/photos/_doc/'
    headers = { "Content-Type": "application/json" }
    response = requests.post(url, auth = ('ccbdhw2', 'Ccbd2021#'), data = json.dumps(document), headers=headers)
    print(response.text)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
