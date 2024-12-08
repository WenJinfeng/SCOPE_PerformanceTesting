import time
import requests

file_name = "/your/filename"


url = 'function url'  #Replace with your actual URL
input = {'N': "10"}


def trigger_function():

    response = requests.get(url, params=input)

    if response.status_code == 200:
        return True
    else:
        return False


if __name__ == "__main__":


    for i in range(500):
        time1 = time.time()
        cold_is_successful = trigger_function()
        time2 = time.time()

        if not cold_is_successful:
            time.sleep(5)
            continue

        time.sleep(5)

        time3 = time.time()
        warm_is_successful = trigger_function()
        time4 = time.time()

        if not warm_is_successful:
            time.sleep(5)
            continue

        cold_time = (time2 - time1) * 1000
        warm_time = (time4 - time3) * 1000
        line = f"Function-Name:azurefunctionmatmul, status:cold, End-to-end-Time:{cold_time}, status:warm, End-to-end-Time:{warm_time}\n"

        with open(file_name, "a") as file:
            file.write(line)

        print(f"Iteration {i+1}: Data written to {file_name}")
        print(line)
        time.sleep(7 * 60)
