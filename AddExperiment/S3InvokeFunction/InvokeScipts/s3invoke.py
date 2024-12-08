import boto3
import time

s3 = boto3.client('s3')

local_file_path = 'data/animal-dog.jpg'

bucket_name = 'your bucket name'

for i in range(500):

    new_file_name = f'animal-dog{i}.jpg'
    
    s3.upload_file(local_file_path, bucket_name, new_file_name)
    print(f'Uploaded file: {new_file_name} completed')
    time.sleep(20)

