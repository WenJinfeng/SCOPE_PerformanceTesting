import time
import random
import json
from multiprocessing import Process, Pipe

defaultLoopTime = 100
defaultParallelIndex = 100

def doAlu(times, childConn, clientId):
    a = random.randint(10, 100)
    b = random.randint(10, 100)
    temp = 0
    for i in range(times):
        if i % 4 == 0:
            temp = a + b
        elif i % 4 == 1:
            temp = a - b
        elif i % 4 == 2:
            temp = a * b
        else:
            temp = a / b
    # print(times)
    childConn.send(temp)
    childConn.close()
    return temp

def alu(times, parallelIndex):
    per_times = int(times / parallelIndex)
    threads = []
    childConns = []
    parentConns = []
    for i in range(parallelIndex):
        parentConn, childConn = Pipe()
        parentConns.append(parentConn)
        childConns.append(childConn)
        t = Process(target=doAlu, args=(per_times, childConn, i))
        threads.append(t)
    for i in range(parallelIndex):
        threads[i].start()
    for i in range(parallelIndex):
        threads[i].join()
    
    results = []
    for i in range(parallelIndex):
        results.append(parentConns[i].recv())
    return str(results)

def GetTime():
    return int(round(time.time() * 1000))
def lambda_handler(event, context):
    startTime = GetTime()
    # print(event)
    event['Records'][0]['body'] = json.loads(event['Records'][0]['body'])
    if 'execTime' in event['Records'][0]['body']:
        execTime_prev = event['Records'][0]['body']['execTime']
    else:
        execTime_prev = 0
    if 'loopTime' in event['Records'][0]['body']:
        loopTime = event['Records'][0]['body']['loopTime']
    else:
        loopTime = defaultLoopTime
    parallelIndex = defaultParallelIndex
    temp = alu(loopTime, parallelIndex)
    retTime = GetTime()

    time_diff = time.time() * 1000 - int(event['Records'][0]['attributes']['SentTimestamp'])
    print(f"TIME: {time_diff} ms")
    return {
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "result": temp,
        'execTime_prev': execTime_prev
    }
