import boto3
import json
import time

arn = "arn of step functions" # concrete arn of state_machine
input = json.dumps({"inputCaseID": "001"})
file_name = "/your/filename"


class StateMachine:
    """Encapsulates Step Functions state machine actions."""

    def __init__(self, stepfunctions_client):
        """
        :param stepfunctions_client: A Boto3 Step Functions client.
        """
        self.stepfunctions_client = stepfunctions_client


    def start(self, state_machine_arn, run_input):
        """
        Start a run of a state machine with a specified input. A run is also known
        as an "execution" in Step Functions.

        :param state_machine_arn: The ARN of the state machine to run.
        :param run_input: The input to the state machine, in JSON format.
        :return: The ARN of the run. This can be used to get information about the run,
                 including its current status and final output.
        """
        response = self.stepfunctions_client.start_execution(
            stateMachineArn=state_machine_arn, input=run_input
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            execution_arn = response['executionArn']
            while True:
                status_response = self.stepfunctions_client.describe_execution(
                    executionArn=execution_arn
                )
                status = status_response['status']
                if status in ['SUCCEEDED', 'FAILED', 'TIMED_OUT', 'CANCELLED']:

                    if status == 'SUCCEEDED':
                        return True
                    else:
                        return False

if __name__ == "__main__":

    step_client = boto3.client(
        'stepfunctions',
        region_name='us-west-1',
    )


    state_machine_instance = StateMachine(step_client)


    for i in range(500):
        time1 = time.time()
        if not state_machine_instance.start(state_machine_arn = arn,run_input = input):
            time.sleep(5)
            continue
        time2 = time.time()


        time.sleep(5)

        time3 = time.time()
        if not state_machine_instance.start(state_machine_arn = arn,run_input = input):
            time.sleep(5)
            continue
        time4 = time.time()

        cold_time = (time2 - time1) * 1000
        warm_time = (time4 - time3) * 1000
        line = f"Function-Name:awsapp, status:cold, End-to-end-Time:{cold_time}, status:warm, End-to-end-Time:{warm_time}\n"

        with open(file_name, "a") as file:
            file.write(line)

        print(f"Iteration {i+1}: Data written to {file_name}")
        print(line)

        time.sleep(420)

