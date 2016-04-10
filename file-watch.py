__author__ = 'Jan Povala'


import boto3
import urllib2
import hashlib
import time

from botocore.exceptions import ClientError

# URL for the remote file
FILE_URL = "https://www.example.com/some-interesting-spreadsheet.xls"

# Name of the bucket used for
S3_BUCKET_NAME = 's3-bucket-name'
# Key to the file which contains hash of the most recent file version
S3_FILE_KEY = 's3-bucket-file-key'

# This is the identifier for a SNS topic into which updates will be published
SNS_TOPIC_ARN = 'arn:aws:sns:...:...'

# This is SUBJECT and BODY of the notifications published to the SNS topic. Note that if the events are published
# using email notification, it will form the subject and body of the notification email.
EMAIL_SUBJECT = "[File Update] " + time.strftime("%d/%m/%Y") + " - " + time.strftime("%H:%M:%S")
EMAIL_BODY = "The file has just been updated"


def get_hash(data):
    hash_function_instance = hashlib.md5()
    hash_function_instance.update(data)
    return hash_function_instance.digest()

def download_latest_hash_from_s3():
    client = boto3.client('s3')
    response = client.get_object(Bucket=S3_BUCKET_NAME,
                                 Key=S3_FILE_KEY)['Body']
    s3_hash = response.read()
    return s3_hash

def update_latest_hash_in_s3(hash_str):
    client = boto3.client('s3')
    client.put_object(Bucket=S3_BUCKET_NAME,
                      Key=S3_FILE_KEY,
                      Body=hash_str)

def download_latest_hash_from_remote_server():
    f = urllib2.urlopen(FILE_URL)
    remote_data = f.read()
    get_hash(remote_data)

def send_sns_notification():
    client = boto3.client('sns')
    client.publish(TopicArn=SNS_TOPIC_ARN,
                   MessageStructure='string',
                   Message=EMAIL_BODY,
                   Subject=EMAIL_SUBJECT)

def execute():
    remote_server_hash = download_latest_hash_from_remote_server()
    try:
        s3_version_hash = download_latest_hash_from_s3()
    except ClientError:
        update_latest_hash_in_s3(remote_server_hash)
        return "INITIAL HASH HAS BEEN DOWNLOADED"

    if remote_server_hash != s3_version_hash:
        update_latest_hash_in_s3(remote_server_hash)
        return "UPDATE SENT VIA SNS."

    return "NO UPDATE"
execute()



