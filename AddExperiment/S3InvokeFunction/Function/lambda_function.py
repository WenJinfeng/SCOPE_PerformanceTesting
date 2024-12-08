import urllib.parse
import boto3
import ops
import uuid
from time import time
from datetime import datetime
from PIL import Image

s3_client = boto3.client('s3')
FILE_NAME_INDEX = 2


def image_processing(file_name, image_path):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += ops.flip(image, file_name)
        path_list += ops.rotate(image, file_name)
        path_list += ops.filter(image, file_name)
        path_list += ops.gray_scale(image, file_name)
        path_list += ops.resize(image, file_name)

    latency = time() - start
    return latency, path_list

def lambda_handler(event, context):

    event_time = event['Records'][0]['eventTime']
    dt = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = dt.timestamp()

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    output_bucket = "imageoutput-bucket"
    
    response = s3_client.get_object(Bucket=bucket, Key=object_key)



    download_path = '/tmp/{}{}'.format(uuid.uuid4(), object_key)

    s3_client.download_file(bucket, object_key, download_path)

    latency, path_list = image_processing(object_key, download_path)

    for upload_path in path_list:
        s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_NAME_INDEX])
    
    time_diff = time() * 1000 - timestamp * 1000
    print(f"TIME: {time_diff} ms")
    return latency
