# -*- coding: utf-8 -*-
import os
import sys
import time

from typing import List

from alibabacloud_fc20230330.client import Client as FC20230330Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_stream.client import Client as StreamClient
from alibabacloud_fc20230330 import models as fc20230330_models
from alibabacloud_tea_util import models as util_models


file_name = '/your/filename'

class Sample:
    client: FC20230330Client


    def __init__(self):
        pass

    @staticmethod
    def create_client() -> FC20230330Client:

        config = open_api_models.Config(

            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],

            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint
        config.endpoint = "your endpoint"
        return FC20230330Client(config)

    @staticmethod
    def invoke_function():
        runtime = util_models.RuntimeOptions()
        body_stream = StreamClient.read_from_string('{"n": 10}') # input


        invoke_function_headers = fc20230330_models.InvokeFunctionHeaders(
            x_fc_invocation_type='Sync',
            x_fc_log_type='None'
        )
        invoke_function_request = fc20230330_models.InvokeFunctionRequest(
            qualifier='LATEST',
            body=body_stream
        )
        resp = Sample.client.invoke_function_with_options('your function name', invoke_function_request, invoke_function_headers, runtime)
        if 'x-fc-error-type' in resp.headers:
            return False
        else:
            return True

    @staticmethod
    def main(args: List[str],) -> None:
        Sample.client = Sample.create_client()
        for i in range(500):
            time1 = time.time()
            if not Sample.invoke_function():
                time.sleep(5)
                continue
            time2 = time.time()

            time.sleep(5)

            time3 = time.time()
            if not Sample.invoke_function():
                time.sleep(5)
                continue
            time4 = time.time()

            cold_time = (time2 - time1) * 1000
            warm_time = (time4 - time3) * 1000
            line = f"Function-Name:alifunctionlinpack, status:cold, End-to-end-Time:{cold_time}, status:warm, End-to-end-Time:{warm_time}\n"

            with open(file_name, "a") as file:
                file.write(line)

            print(line)
            print(f"Iteration {i+1}: Data written to {file_name}")
            time.sleep(400)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
