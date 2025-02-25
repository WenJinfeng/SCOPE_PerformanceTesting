# SCOPE: Performance Testing for Serverless Computing

This work has been accepted in ACM Transactions on Software Engineering and Methodology (TOSEM).


- New Data:
    - We explore the effectiveness of SCOPE in other situations, including mixed cold and warm conditions, serverless applications composed of multiple functions, varying input conditions, functions with other types of triggers, highly bursty workloads, and functions executed across different platforms.
    - Their tested performance data is saved in the file "**AddData.xlsx**".

- New Code (The directory "AddExperiment"):
    - We implement two serverless applications from AWS and Google, repectively. Please see the directories "AWSApplication" and "Google Application", which also includes invocation scripts.
    - We implement three serverless functions with different triggers, incorporating Amazon S3, Amazon SQS, and Amazon DynamoDB, repectively. Please see the directories "S3InvokeFunction", "SQSInvokeFunction", and "DynamoDBInvokeFunction", which also include invocation scripts.
    - We implement four serverless functions executed Microsoft Azure Functions and Alibaba Function Compute. Please see the directories "AzureFunctions" and "AliFunctions", which also includes invocation scripts.


- Data:
    - The details of serverless functions from an existing dataset (including 65 serverless functions):
        - see the file "**Dataset_Serverless Functions_updated.xlsx**", containing the function ID, function name, tested input, executed serverless platform, programming language, timeout time (second), memory size (MB), code link, and **task type**.
    - The performance data of serverless functions:
        - see the file "**Performance_Data.xlsx**", containing 1,000 performance results of each serverless function that is repeatedly executed.
    - We provide the additional performance data of 500 runs to analyze trustworthy ground truth. Please see the file "**AdditionalPerformance_Data500.xlsx**"
      

- Code：
    - We made publicly available the deployment packages for the 65 serverless functions we used.
        - see the directory "**Deployment Packages**", containing the source code from func1 to func65.
        - see the included directory "**input**", containing the long input payload sample about func20, func29, func54, func56, func57, and func60.
    - Invocation scripts for serverless functions are included in the directory "**scripts**", which have the invocation code for serverless functions hosted in serverless platforms (AWS Lambda and Google Cloud Functions).
      - "**invokeAWSFunction-run1.py**" and **invokeAWSFunction-run2.py**" are the scripts that invoke serverless functions executed on AWS Lambda
      - "**invokeGoogleFunction.py**" is the script that invokes serverless functions executed on Google Cloud Functions
    - The implementation of state-of-the-art techniques: PT4Cloud and Metior
        - see the file "**state-of-the-arts.py**" and use the methods "fse19method" and "ase21method".
        - see the file "**CONFIRM.py**" and use the method "CONFIRM".
        - **the evaluation of testing results is in the method - identifyEffectiveness.**
    -  The implementation of our approach SCOPE
        - see the file "**SCOPE.py**" and use the method "determineStopRun" with different variants: general, bootstrapping, and block bootstrapping. Moreover, **the evaluation of testing results is in the method - identifyEffectiveness.**
        
 
