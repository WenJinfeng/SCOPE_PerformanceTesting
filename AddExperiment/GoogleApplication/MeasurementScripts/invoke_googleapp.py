import subprocess
import time
import yaml


file_name = "/your/filename"

if __name__ == "__main__":

    for i in range(500):
        time1 = time.time()
        result = subprocess.run(['gcloud', 'workflows',  'run',  'service-chaining'], capture_output=True, text=True)
        time2 = time.time()

        output = yaml.safe_load(result.stdout)
        state = output.get('state', None)
        if state != "SUCCEEDED":
            continue

        time.sleep(5)

        time3 = time.time()
        result = subprocess.run(['gcloud', 'workflows',  'run',  'service-chaining'], capture_output=True, text=True)
        time4 = time.time()

        output = yaml.safe_load(result.stdout)
        state = output.get('state', None)
        if state != "SUCCEEDED":
            continue

        cold_time = (time2 - time1) * 1000
        warm_time = (time4 - time3) * 1000
        line = f"Function-Name:googleapp, status:cold, End-to-end-Time:{cold_time}, status:warm, End-to-end-Time:{warm_time}\n"

        with open(file_name, "a") as file:
            file.write(line)

        print(f"Iteration {i+1}: Data written to {file_name}")
        print(line)
        time.sleep(12 * 60)
