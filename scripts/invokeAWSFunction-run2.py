import json
import boto3
import time
import base64
import botocore

config = botocore.config.Config(
    read_timeout=900,
    connect_timeout=900,
    retries={"max_attempts": 0}
)

session = boto3.Session(aws_access_key_id="XXXX",
                                aws_secret_access_key="XXXXX",
                                region_name="us-west-1")
client = session.client(service_name='lambda', config=config)


def caltimeDelta(tm_st,tm_ed):
    #time interval processing

    tm_st_fen = tm_st.split(" ")[1].split(":")[1]

    tm_st_s = tm_st.split(" ")[1].split(":")[2].split(".")[0]
    tm_st_m = tm_st.split(" ")[1].split(":")[2].split(".")[1]

    tm_ed_fen = tm_ed.split(" ")[1].split(":")[1]
    tm_ed_s = tm_ed.split(" ")[1].split(":")[2].split(".")[0]
    tm_ed_m = tm_ed.split(" ")[1].split(":")[2].split(".")[1]

    timeDelta =(int(tm_ed_fen) - int(tm_st_fen))*60*1000 +(int(tm_ed_s)-int(tm_st_s))*1000+(int(tm_ed_m)-int(tm_st_m))/1000
    return timeDelta


 
def function_invoke(fun_name, event, output_file, fun_id):

    tm_st =time.time()
    # tm_st = datetime.datetime.now()

    resp = client.invoke(FunctionName=fun_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(event))


    tm_ed = time.time()
   
    # time.sleep(5)
    print(base64.b64decode(resp['LogResult']))


    # funStart = str(base64.b64decode(resp['LogResult'])).split(',functioStart:')[1].split(",")[0]
    duration = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Duration:")[1].split(" ")[1]
    memory = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Max Memory Used:")[1].split(" ")[1]
    bill = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Billed Duration:")[1].split(" ")[1]
    

    initDuration = 0
    if ",Init Duration:" in str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ","):
        print("yes")
        initDuration = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Init Duration:")[1].split(" ")[1]
    addDuration = ""
 

    print("---------------")

    with open(output_file,"a") as f:


        if initDuration==0:
            print("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_id, fun_name,"warm",(tm_ed - tm_st)*1000,initDuration,duration,addDuration,bill,memory))

            f.write("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_id, fun_name,"warm",(tm_ed - tm_st)*1000,initDuration,duration,addDuration,bill,memory))
            f.write("\n")

        else:
            print("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_id, fun_name,"cold",(tm_ed - tm_st)*1000,initDuration,duration,addDuration,bill,memory))

            f.write("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_id, fun_name,"cold",(tm_ed - tm_st)*1000,initDuration,duration,addDuration,bill,memory))
            f.write("\n")
    f.close()



if __name__ == "__main__":


    fun_ids=["Func20","Func29","Func54","Func55","Func56","Func57","Func60"]

    fun_names = ["facefun20-dev-faceFun","Fun29transform-metadata","Fun54identifyphi","Fun55anonymize","Fun56deidentify","Fun57analytics-dev-analytics","Fun60render-dev-fun"]

    event_files =["input/func20_input.json","input/func29_input.json","input/func54_input.json","input/func55_input.json","input/func56_input.json","input/func57_input.json","input/func60_input.json"]

    output_file="Result/AWS2.txt"

    for i in range(50):
        time.sleep(1800)
        for f in range(len(fun_names)):
            fstr=fun_ids[f]
            print(">>>>>--repeat--{}--times--{}---".format(i, fstr))
            try:
                event1={}
                with open(event_files[f],'r') as load_f:
                    event1 = json.load(load_f)
                function_invoke(fun_names[f], event1, output_file, fstr)
                time.sleep(5)
                function_invoke(fun_names[f], event1, output_file, fstr)
            except Exception as e:
                print(e)











