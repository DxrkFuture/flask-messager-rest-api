import boto3
from botocore.exceptions import ClientError
from flask import current_app

def get_s3_client():
    return boto3.client('s3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )

def upload_file_to_s3(file_name, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = get_s3_client()
    try:
        s3_client.upload_file(file_name, current_app.config['S3_BUCKET'], object_name)
    except ClientError as e:
        return False
    return True