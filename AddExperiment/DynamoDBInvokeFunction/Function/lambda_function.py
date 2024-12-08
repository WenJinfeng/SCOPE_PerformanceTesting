import csv
import time
from util import *

def lambda_handler(event, context):
    # print(event)
    startTime = 1000*time.time()
    with open('data/few_reviews.csv') as csvFile:
        #DictReader -> convert lines of CSV to OrderedDict
        for row in csv.DictReader(csvFile):
            #return just the first loop (row) results!
            body = {}
            for k,v in row.items():
                body[k] = int(v) if k == 'reviewType' else v
    response = {'statusCode':200, 'body':body}
    endTime = 1000*time.time()
 
    time_diff = time.time() * 1000 - 1000 * float(event['Records'][0]['dynamodb']['ApproximateCreationDateTime'])
    print(f"TIME: {time_diff} ms")

    return timestamp(response, event, startTime, endTime, 0)

