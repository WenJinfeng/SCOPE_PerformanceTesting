# SCOPE: Performance Testing for Serverless Computing



- Data:
    - The details of serverless functions from an existing dataset (including 65 serverless functions):
        - see the file "**Dataset_Serverless Functions.xlsx**", containing the function ID, function name, tested input, executed serverless platform, programming language, timeout time (second), memory size (MB), and code link.
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
        - see the file "**state-of-the-arts.py**" and use the methods "fse19method" and "ase21method". Moreover, **the evaluation of testing results is in the method - identifyEffectiveness.**
    -  The implementation of our approach SCOPE
        - see the file "**SCOPE.py**" and use the method "determineStopRun" with different variants: general, bootstrapping, and block bootstrapping. Moreover, **the evaluation of testing results is in the method - identifyEffectiveness.**
        
 
