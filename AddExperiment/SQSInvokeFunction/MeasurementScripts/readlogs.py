import boto3
import re

client = boto3.client('logs', region_name='us-west-1')


file_name = "/your/filename"
logs = []
data = []

def list_log_streams(log_group_name):
    response = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True,
    )
    for log_stream in response['logStreams']:
        logs.append(log_stream['logStreamName'])


def get_log_events(log_group_name, log_stream_name):
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startFromHead= True,
    )

    duration_pattern = r"TIME:\s*(\d+\.\d+|\d+)\s*ms"
    for event in response['events']:

        message = event['message']
        match = re.search(duration_pattern, message)
        if match:
            duration = match.group(1)
            data.append(float(duration))


if __name__ == '__main__':
    log_group_name = 'your log group name'
    list_log_streams(log_group_name)
    for i in range(1): # range number depends on actual count of log streams
        print(logs[i])
        cold_start_location = len(data)
        get_log_events(log_group_name, logs[i])
        data.pop(cold_start_location)

    data = data[:500]

    for i in range(len(data)):
        line = f"Function-Name:sqstrigger, End-to-end-Time:{data[i]}\n"

        with open(file_name, "a") as file:
            file.write(line)

        print(f"Iteration {i+1}: Data written to {file_name}")
        print(line)
