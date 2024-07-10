import os
import time
import json

# google cloud function deploy command
# gcloud functions deploy XX --entry-point XX --runtime python37 --trigger-http --allow-unauthenticated 

def run_cmd(cmd):
    """
    The simplest way to run an external command
    """
    return os.popen(cmd).read()



def getLog(invocation_num, func_name):
    # obtain function execution time according to the latest invocation
    # invocation_num =1 is the newest duration time, invocation_num=3 is results of the first three calls
    log_num = invocation_num*3
    resp = run_cmd("gcloud functions logs read %s --limit=%s" % (func_name, log_num))
    duration = resp.split("Function execution took ")
    for i in range(invocation_num):
        info = duration[i+1].split(" ms")[0]
        print(info)



def invoke_fun(fun_name, req_para, output_file, fun_id):
    tm_st = time.time() * 1000
    
    try:
    	# google function invoke command
        resp = run_cmd("gcloud functions call %s --data %s" % (fun_name, req_para))
        tm_ed = time.time() * 1000
        print(resp)
        init_st = resp.split("InitStart:")[1].split(",InitEnd:")[0]
        init_ed = resp.split(",InitEnd:")[1].split(",functionStart:")[0]
        fun_st = resp.split(",functionStart:")[1].split(",functionEnd:")[0]
        fun_ed = resp.split(",functionEnd:")[1].split(",")[0]



        totalTime = tm_ed-tm_st
        
        if (float(init_st)-tm_st)<0:
            prepareTime = float(fun_st)-tm_st
            initTime=0
        else:
            prepareTime = float(init_st)-tm_st
            initTime = float(fun_st)-float(init_st)
        

        funTime = float(fun_ed)-float(fun_st)



        with open(output_file,"a") as f:
            if initTime==0:
                print("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}, Billed-Duration:{}, Used-Memory:{}, Prepare-Time:{}".format(fun_id, fun_name,"warm",totalTime,initTime,funTime,"no","no", prepareTime))
                f.write("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}, Billed-Duration:{}, Used-Memory:{}, Prepare-Time:{}".format(fun_id, fun_name,"warm",totalTime,initTime,funTime,"no","no", prepareTime))
                f.write("\n")
            else:
                print("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}, Billed-Duration:{}, Used-Memory:{}, Prepare-Time:{}".format(fun_id, fun_name,"cold",totalTime,initTime,funTime,"no","no", prepareTime))
                f.write("Function-ID:{}, Function-Name:{}, status:{}, End-to-end-Time:{}, Init-Duration:{}, Function-Duration:{}, Billed-Duration:{}, Used-Memory:{}, Prepare-Time:{}".format(fun_id, fun_name,"cold",totalTime,initTime,funTime,"no","no", prepareTime))
                f.write("\n")


    except Exception as e:
        print(e)
        

    


if __name__ == "__main__":


    fun_ids=["Func2","Func4","Func51","Func52","Func53"]

    fun_names = ["adv_gcp_rdrand_fun2", "params_gcp", "fun51factor", "fun52matrix", "fun53filesystem"]

    events =["{}","{}","{}","{}","{}"]

    output_file="Result/GoogleFunctions.txt"

    for i in range(50):
        time.sleep(1800)
        for f in range(len(fun_names)):
            fstr=fun_ids[f]
            print(">>>>>--repeat--{}--times--{}---".format(i, fstr))
            try:
                event1=json.dumps(events[f])
                invoke_fun(fun_names[f], event1, output_file, fstr)
                time.sleep(5)
                invoke_fun(fun_names[f], event1, output_file, fstr)
            except Exception as e:
                print(e)

