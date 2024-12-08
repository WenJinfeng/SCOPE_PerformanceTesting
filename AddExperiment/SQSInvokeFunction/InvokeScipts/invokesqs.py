import boto3
import json
import time

sqs = boto3.client(
        'sqs',
        region_name='us-west-1'
)
queue_url = 'url of your queue'




for i in range(500):

    messages = {"execTime": 1000,"loopTime": 100}
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(messages)
    )

    print(f"Iteration {i} completed")
    time.sleep(5)

