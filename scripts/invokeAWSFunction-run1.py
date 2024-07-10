
from collections import OrderedDict
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

session = boto3.Session(aws_access_key_id="XXXXX",
                                aws_secret_access_key="XXXXXX",
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


    fun_ids=["Func1", "Func3", "Func5", "Func6", "Func7", "Func8", "Func9", "Func10","Func11","Func12","Func13","Func14","Func15","Func16","Func17","Func18","Func19","Func21","Func22","Func23","Func24","Func25","Func26","Func27","Func28","Func30","Func31","Func32","Func33","Func34","Func35","Func36","Func37","Func38","Func39","Func40","Func41","Func42","Func43","Func44","Func45","Func46","Func47","Func48","Func49","Func50","Func58","Func59","Func61","Func62","Func63","Func64","Func65"]

    fun_names = ["adv_aws_rdrand","params_aws", "Fun5-dev-imageProssFun", "Fun6-dev-chameleonFun", "Fun7-dev-linpackFun","Fun8-dev-matmulFun", "Fun9-dev-pyaesFun","Fun10dd","Fun11gzip", "Fun12-dev-imageConvertorFun","Fun13helloworld","Fun14json_dumps_loads","Fun15","Fun16RLTrain","Fun17Classify","Fun18RNN","aws-authfun19-dev-auth","Fun21bot-dev-botFun","Fun22videopro-dev-videoFun","Fun23getPrice","Fun24Publish","speechFun25-dev-speech","Fun26extract-image-dev-extract","Fun27rekognition","Fun28thumbnail-dev-thumbnail","Fun30feature-dev-extract","Fun31featurereducor","Fun32float_operation","Fun33sequential_disk_io","Fun34Alu","Fun35keyDownloader","Fun36together","Fun37head","Fun38head","Fun39tail","Fun40split-dev-video","Fun41extract-dev-video","Fun42classify","Fun43PCA-dev-pca","Fun44ParamTune","Fun45CombineModels","Fun46SplitChatBot-dev-bot","Fun47TrainIntentClassifier-dev-bot","Fun48compression_handler","Fun49pagerank-dev-function","Fun50recognization","Fun58resize-dev-fun","Fun59predict","Fun61readcsv-dev-fun","Fun62sentiment-dev-fun","Fun63python-dev-fun","Fun64fetch-file-and-store-in-s3-dev-save","Fun65analysis-s3-image-dev-imageAnalysis"]

    events =[{},{}, {"input_bucket":"bucketwendycyn", "object_key":"1.jpeg","output_bucket":"bucketwendycyn1"}, {"num_of_rows": 2,"num_of_cols": 3},{"n": 20}, {"n": 20}, {"length_of_message": 300, "num_of_iterations": 20},{"bs":"5120","count":"5"},{"file_size":5},{'img': "test.jpg", 'height': 200, 'width': 200}, {"key1": "value1","key2": "value2","key3": "value3"},{"link": "https://jsonplaceholder.typicode.com/users"}, {"x": "The ambiance is magical. The food and service was nice! The lobster and cheese was to die for and our steaks were cooked perfectly.",  "dataset_object_key": "reviews20mb.csv", "dataset_bucket": "bucketwendycyn",  "model_bucket": "bucketwendycyn1", "model_object_key": "lr_model.pk"},{"dataset_object_key": "reviews20mb.csv", "dataset_bucket": "bucketwendycyn", "model_bucket": "bucketwendycyn1", "model_object_key": "lr_model_new.pk"},{"object_key": "animal-dog.jpg", "input_bucket": "bucketwendycyn", "model_bucket": "bucketwendycyn1", "model_object_key": "squeezenet_weights_tf_dim_ordering_tf_kernels.h5"},{"language": "German","start_letters": "ABCDEFGHIJKLMNOP",    "model_bucket": "bucketwendycyn","model_object_key": "rnn_model.pth",    "model_parameter_object_key": "rnn_params.pkl"},{"body":"https://www.baidu.com/"},{"trigger_word":"show","text": "you show me."}, {"input_bucket": "bucketwendycyn", "object_key": "SampleVideo_1280x720_10mb.mp4", "output_bucket": "bucketwendycyn1"},{"id":6},{"id":10,"price":80.76,"user":"cynthia","authorization":"finished",    "approved": "true","failureReason":"epsagon problem"},{"batch_size":5,"file_name":"data_smoke_test_LDC93S1.wav"},{"s3Bucket": "bucketwendycyn", "s3Key": "test_input.jpg"},{"s3Bucket": "bucketwendycyn", "s3Key": "test_input.jpg"},{"s3Bucket": "bucketwendycyn","s3Key": "1.jpeg","objectID": "l3j4234-234", "extractedMetadata": {"dimensions": {"width": 4567,"height": 3456}}},{"input_bucket":"bucketwendycyn","key":"reviews20mb.csv"},{"input_bucket":"bucketwendycyn2"},{"n":1000},{"file_size": 8,"byte_size":4},{"execTime": 1000,"loopTime": 100},{"key1":"value1"},{"key":"loopTime.txt","execTime": 1000,"loopTime": 10},{"payload_size": 100,"uploadTime": 1589702810028,"retTime":1589702811486},{"payload_size": 100,"uploadTime": 1589702810028,"retTime":589702811486},{"payload_size": 100,"uploadTime": 1589702810028,"retTime": 589702811486},{"src_name": "0","DOP": "30","detect_prob": 2},{"values": [0], "source_id": "0", "millis": [1667464845061], "detect_prob": 2},{"millis1": [1667464845061],"millis2": [1667466554979], "source_id": "0", "detect_prob": 2, "values": [0]},{"bundle_size": 4, "key1": "300"},{"mod_index": 4,"PCA_Download": 410, "PCA_Process": 13881,"PCA_Upload": 1131, "key1": "inv_300", "num_of_trees": [5,10,15,20],"max_depth": [10,10,10,10],"feature_fraction": [0.95, 0.95,0.95,0.95],"threads": 6},{"trees_max_depthes": ["5_10_0.95","10_10_0.95","15_10_0.95","20_10_0.95"], "accuracies": [ 0.9242, 0.9542, 0.9716, 0.9802]},{"skew": 4,"bundle_size": 1,"Network_Bound": 1},{"values":[{"intent_name": "Greeting", "skew": 4,"Network_Bound": 1}],"duration": 14019},{"bucket": {"input":"bucketwendycyn1","output":"bucketwendycyn"}, "object": {"key":"Fun48Dir"}},{"size":1000},{"bucket":{"input":"bucketwendycyn", "model":"bucketwendycyn"},"object":{"input":"animal-dog.jpg", "model":"resnet50-19c8e357.pth"}},{},{},{},{"body": {"reviewType": 0, "reviewID": "123", "customerID": "456", "productID": "789", "feedback": "Great product"}},{"cmds": OrderedDict([("sleep", 0), ("stat", {"argv": 1}), ("run", False), ("io", False), ("net", False), ("cpu", False), ("cpuu", False)])},{"image_url": "http://e.hiphotos.baidu.com/image/pic/item/a1ec08fa513d2697e542494057fbb2fb4316d81e.jpg","key": "github.jpg"},{"body": {"bucket": "bucketwendycyn1","imageName": "github.jpg"}}]


    output_file="Result/AWS-add.txt"

    for i in range(50):
        time.sleep(1800)
        for f in range(len(fun_names)):
            fstr=fun_ids[f]
            print(">>>>>--repeat--{}--times--{}---".format(i, fstr))
            try:
                function_invoke(fun_names[f], events[f], output_file, fstr)
                time.sleep(5)
                function_invoke(fun_names[f], events[f], output_file, fstr)
            except Exception as e:
                print(e)


   







