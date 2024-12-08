import boto3
import time

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

table = dynamodb.Table('your table name')

def insert_item(item):
    response = table.put_item(Item = item)

    return response


for i in range(500):
    item_example = {"id":str(i),"body": {}}
    resp = insert_item(item_example)
    print(f"Inserted item with id: {item_example['id']}")
    time.sleep(5)
