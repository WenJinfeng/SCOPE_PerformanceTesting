from xlrd import open_workbook
from statsmodels.tsa.stattools import adfuller
import scipy.stats as kl
import math
import sys
import numpy as np
import numpy.random as npr
from recombinator.optimal_block_length import optimal_block_length

# This is SCOPE, which provides three types of CI implementation methods: general, bootstrapping, and block bootstrapping.
def determineStopRun(data, interval, CImethod, confidence_level, error_bound):

    Data_Size = len(data)
    # check new distribution if its number of data is greater than the interval
    if Data_Size < interval:
        print("newly added data is not enough!")
        return 0
    
    # obtainthe previous performance data
    old_data = data[:Data_Size-interval]

    # method1: use the general confidence interval calculation
    if CImethod == "general":
        value_narrow1 = isNarrowCI_general(data, confidence_level, error_bound, 0.25)
        value_narrow2 = isNarrowCI_general(data, confidence_level, error_bound, 0.50)
        value_narrow3 = isNarrowCI_general(data, confidence_level, error_bound, 0.75)

        value_narrow4 = isNarrowCI_general(old_data, confidence_level, error_bound, 0.25)
        value_narrow5 = isNarrowCI_general(old_data, confidence_level, error_bound, 0.50)
        value_narrow6 = isNarrowCI_general(old_data, confidence_level, error_bound, 0.75)


        # accuracy check
        if value_narrow1 == "yes" and value_narrow2 == "yes" and value_narrow3 == "yes" and value_narrow4 == "yes" and value_narrow5 == "yes" and value_narrow6 == "yes":
            value_narrow = "yes"
        elif value_narrow1 == "error" or value_narrow2 == "error" or value_narrow3 == "error" or value_narrow4 == "error" or value_narrow5 == "error" or value_narrow6 == "error":
            return 0
        else:
            value_narrow = "no"

        print("General method's stop condition is {}".format(value_narrow))
        # if value_narrow == "error":
        #     return 0


    # method2: use boorstrap calculation method
    if CImethod == "bootstrapping":

        value_narrow1 = isNarrowCI_bootstrap(data, confidence_level, error_bound, 0.25)

        value_narrow2 = isNarrowCI_bootstrap(data, confidence_level, error_bound, 0.50)

        value_narrow3 = isNarrowCI_bootstrap(data, confidence_level, error_bound, 0.75)


        value_narrow4 = isNarrowCI_bootstrap(old_data, confidence_level, error_bound, 0.25)

        value_narrow5 = isNarrowCI_bootstrap(old_data, confidence_level, error_bound, 0.50)

        value_narrow6 = isNarrowCI_bootstrap(old_data, confidence_level, error_bound, 0.75)

        # accuracy check
        if value_narrow1 == "yes" and value_narrow2 == "yes" and value_narrow3 == "yes" and value_narrow4 == "yes" and value_narrow5 == "yes" and value_narrow6 == "yes" :
            value_narrow = "yes"
        else:
            value_narrow = "no"

        
        print("Bootstrapping's stop condition is {}".format(value_narrow))



    #method3: use block-based bootstrapping calculation method
    if CImethod == "block bootstrapping":

        value_narrow1 = isNarrowCI_blockbootstrap(data, confidence_level, error_bound, 0.25)

        value_narrow2 = isNarrowCI_blockbootstrap(data, confidence_level, error_bound, 0.50)

        value_narrow3 = isNarrowCI_blockbootstrap(data, confidence_level, error_bound, 0.75)


        value_narrow4 = isNarrowCI_blockbootstrap(old_data, confidence_level, error_bound, 0.25)

        value_narrow5 = isNarrowCI_blockbootstrap(old_data, confidence_level, error_bound, 0.50)

        value_narrow6 = isNarrowCI_blockbootstrap(old_data, confidence_level, error_bound, 0.75)

        # accuracy check
        if value_narrow1 == "yes" and value_narrow2 == "yes" and value_narrow3 == "yes" and value_narrow4 == "yes" and value_narrow5 == "yes" and value_narrow6 == "yes" :
            value_narrow = "yes"
        else:
            value_narrow = "no"

        print("Block Bootstrapping's stop condition for new data is {}".format(value_narrow))




    #  stability check
    if value_narrow == "yes":
        print("=====> The current performance data is accurate and reliable, and its number of repetitions is {} ********".format(Data_Size))
        return "Yes"
        
    else:
        print("=====>{} performance data is not enough. Please continue running the serverless function!!!".format(Data_Size))
        return "No"



def identifyEffectiveness(data, totalData, confidence_level):

    print("tested data has {} points".format(len(data)))
    print("total data has {} points".format(len(totalData)))
    
    resultData=[]
    resultData.append(len(data))

    # 1. obtain the testing result accuracy
    data_dist = np.array(data)
    totalData_dist = np.array(totalData)
    similarity = distSimilarity(data_dist, totalData_dist)
    print("1.1. The similarity is {}".format(similarity))
    resultData.append(similarity)

    # 2. the credibility at 25th/50th/75th/90th percentile performance
    # obtain the percentage of serverless functions with the credible performance

    metric25 = np.percentile(data, 25)

    median = np.percentile(data, 50)
    
    metric75 = np.percentile(data, 75)
   
    metric90 = np.percentile(data, 90)


    # use the general confidence interval calculation method

    lo_CI_g, hi_CI_g = CI_general(totalData, confidence_level, 0.25)
 
    if metric25 > lo_CI_g and metric25 < hi_CI_g:
        print("The 25th percentile performance of the testing result is in ground truth's confidence interval!---1")
        resultData.append(1)
    else:
        print("The 25th percentile performance of the testing result is not in ground truth's confidence interval!---0")
        resultData.append(0)

    lo_CI_g, hi_CI_g = CI_general(totalData, confidence_level, 0.50)
    
    if median > lo_CI_g and median < hi_CI_g:
        print("The 50th percentile performance of the testing result is in ground truth's confidence interval!---1")
        resultData.append(1)
    else:
        print("The 50th percentile performance of the testing result is not in ground truth's confidence interval!---0")
        resultData.append(0)

    lo_CI_g, hi_CI_g = CI_general(totalData, confidence_level, 0.75)
   
    if metric75 > lo_CI_g and metric75 < hi_CI_g:
        print("The 75th percentile performance of the testing result is in ground truth's confidence interval!---1")
        resultData.append(1)
    else:
        print("The 75th percentile performance of the testing result is not in ground truth's confidence interval!---0")
        resultData.append(0)

    lo_CI_g, hi_CI_g = CI_general(totalData, confidence_level, 0.90)
    
    if metric90 > lo_CI_g and metric90 < hi_CI_g:
        print("The 90th percentile performance of the testing result is in ground truth's confidence interval!---1")
        resultData.append(1)
    else:
        print("The 90th percentile performance of the testing result is not in ground truth's confidence interval!---0")
        resultData.append(0)

    

    strResult=""
    for k in range(len(resultData)):
        if k==0:
            strResult="{}".format(resultData[k])
        else:
            strResult=strResult +"\t {}".format(resultData[k])
    
    print(strResult)
  


def distSimilarity(data1, data2):
    """
    data1 and data2 represent the data distribution to be compared.
    """
    dataFirst = data1
    dataSecond = data2
    intervalCount = 1000
    # intervalCount = 60
    # calculate the kernel-density estimation using Gaussian kernels
    kde1 = kl.gaussian_kde(dataFirst)
    kde2 = kl.gaussian_kde(dataSecond)
    # get the data range of the two data sets
    maxVal = max([dataFirst.max(),dataSecond.max()])
    minVal = min([dataFirst.min(),dataSecond.min()])
    dataVar = (maxVal - minVal)/intervalCount
    dataMin = minVal
    # general the index for calculating the integration of probability density function
    iList = []
    for n in range(intervalCount):
        iList.append(dataMin + dataVar)
        dataMin = dataMin + dataVar
    
    # the probability density functions (PDFs)
    
    data1PDFs = kde1.pdf(iList)
    data2PDFs = kde2.pdf(iList)


    if len(data1PDFs) < len(data2PDFs):
        data2PDFs = data2PDFs[0:len(data1PDFs)]
        intervalCount = len(data1PDFs)
    else:
        data1PDFs = data1PDFs[0:len(data2PDFs)]
        intervalCount = len(data2PDFs)
    # calculate the KL divergence
    dataKLM2 = 0
    dataKLM1 = 0

    
    # print(data1PDFs)

    for p in range(intervalCount):

        try:
            
            # 10**300 in top and bottom
            dataKLM2 += data2PDFs[p]* dataVar * math.log2((data2PDFs[p]*(10**300))/(data1PDFs[p]*(10**300)))
        
        except:
            e = sys.exc_info()[0]
            print( "kk-Math Error in KLD: %s" % e )
            print(len(data1))
            return 0
    
    for q in range(intervalCount):
    
        try:
            dataKLM1 += data1PDFs[q]* dataVar * math.log2((data1PDFs[q]*(10**300))/(data2PDFs[q]*(10**300)))
        except:
             e = sys.exc_info()[0]
             print( "ll-Math Error in KLD: %s" % e )
             print(len(data2))
             return 0
    # calculating the symmetrical KL-Divergence
    symKL = dataKLM2 + dataKLM1
    # calculating the likelihood 
    dataScoreM = 2**(-symKL)
    # print("Similarity probability(symmetric):", "%.16f%%" % float(100*round(dataScoreM,16)))
    return dataScoreM


def isNarrowCI_bootstrap(data, confidence_level, error_bound, metricValue):
    """
    the accuracy check about basic bootstrapping method of the confidence interval
    """

    # calculate the confidence interval
    lo_CI, hi_CI = CI_bootstrap(data, confidence_level, metricValue)
    
    # the observed true metric
    metric_data= np.percentile(data, metricValue*100)
    
    metric_lo = metric_data - metric_data * error_bound
    metric_hi = metric_data + metric_data * error_bound



    # the accuracy check
    if lo_CI > metric_lo and hi_CI < metric_hi:
        return "yes"
    else:
        return "no"



def isNarrowCI_general(data, confidence_level, error_bound, metricValue):
    """
    the accuracy check about the general calculation method of the confidence interval
    """
    low, top = calculateTopLow(len(data), confidence_level, metricValue)
    
    
    if low > 0 and top<len(data):
        # sort
        data_sorted = sorted(data)
        lo_CI = data_sorted[low]
        hi_CI = data_sorted[top]

        # obtain the observed true metric
        metric_data= np.percentile(data, metricValue*100)
        
        metric_lo = metric_data - metric_data * error_bound
        metric_hi = metric_data + metric_data * error_bound
    
        # accuracy check
        if lo_CI > metric_lo and hi_CI < metric_hi:
            return "yes"
        else:
            return "no"
    else:
        print("data cannot support to obtain CI!")
        return "error"


def calculateTopLow(n, confidence_level, metricValue):

    p = metricValue
   
    if confidence_level == 0.90:
        z=1.65
    if confidence_level == 0.95:
        z=1.96
    if confidence_level == 0.99:
        z=2.58

    low=int(np.rint(n * p - z * np.sqrt(n*p*(1-p))))
    top=int(np.rint(1 + n * p + z * np.sqrt(n*p*(1-p))))

    return low,top


def CI_bootstrap(data, confidence_level, metricValue):
    """
    obtain the top and bottom bounds for the basic bootstrap method
    """
    bootstrap_metric=[]
    for k in range(1000):
        # with replacement
        sample_temp = npr.choice(data, size=len(data), replace= True)
        #obtain the specific metric
        sample_metric=np.percentile(sample_temp, metricValue*100)
       
        bootstrap_metric.append(sample_metric)

    
    cl_val=(1.00-confidence_level)/2
    lo_CI = np.percentile(bootstrap_metric,cl_val*100)
    hi_CI = np.percentile(bootstrap_metric,(1.00-cl_val)*100)

    return lo_CI, hi_CI

    
def CI_general(data, confidence_level, metricValue):
    """
    obtain the top and bottom bounds for general method
    """
    low, top = calculateTopLow(len(data), confidence_level, metricValue)
    
    if low > 0 and top<len(data):
        
        data_sorted = sorted(data)
        lo_CI = data_sorted[low]
        hi_CI = data_sorted[top]

    return lo_CI, hi_CI



#Generate moving window blocks for block_bootstrap
def gen_mvwin_blocks(data, block_length):
    #the samples which can generate blocks
    block_count = len(data) - block_length
    blocks = []
    
    for i in range(block_count):
        new_block = data[i : i + block_length]
        blocks.append(new_block)
        
    return np.array(blocks)

        


def isNarrowCI_blockbootstrap(data, confidence_level, error_bound, metricValue):
    """
    the accuracy check about the block bootstrapping method of confidence interval
    """

    lo_CI, hi_CI = CI_blockbootstrap(data, confidence_level, metricValue)
    
    metric_data= np.percentile(data, metricValue*100)
    
    metric_lo = metric_data - metric_data * error_bound
    metric_hi = metric_data + metric_data * error_bound


    if lo_CI > metric_lo and hi_CI < metric_hi:
        
        return "yes"
    else:
        
        return "no"


def CI_blockbootstrap(data, confidence_level, metricValue):
    """
    the top and bottom of the confidence interval of the block bootstrapping method
    """
    block_length_bound = 1
    try:
        b_star = optimal_block_length(np.array(data))
        block_length = math.ceil(b_star[0].b_star_cb)
        if block_length_bound >= block_length:
            block_length = block_length_bound
    except Exception as e:
        block_length = block_length_bound

    blocks_1 = gen_mvwin_blocks(data, block_length)
    
    block_count_1 = blocks_1.shape[0]
    block_length_1 = blocks_1.shape[1]
    required_blocks_1 = math.floor(block_count_1 / block_length_1)

    index_1 = []
    for i in range(1000):
        idx1 = npr.choice(block_count_1, size = required_blocks_1,
                          replace = True)
        index_1.append(idx1)

    bootstrapData1 = np.array(blocks_1[index_1])

    data1PercentileStarBar = []
    for i in range(1000):
        lis_cache = []
        for j in range(bootstrapData1.shape[1]):
            lis_cache = np.append(lis_cache, bootstrapData1[i][j])
        data1PercentileStarBar.append(lis_cache)
    

    data1PercentileStar = np.percentile(data1PercentileStarBar, metricValue*100, axis=1) 


    cl_val=(1.00-confidence_level)/2

    lo_CI = np.percentile(data1PercentileStar,cl_val*100)
    hi_CI = np.percentile(data1PercentileStar,(1.00-cl_val)*100)

    return lo_CI, hi_CI



if __name__ == "__main__": 

    # 1. data preparation

    # read tested data from the file, where raw data is saved.
    workbook=open_workbook('Performance_Data.xlsx')

    # select the sheet label to be tested
    sheet_name = "Cold-start performance"
    # sheet_name = "Warm-start performance"

    worksheet=workbook.sheet_by_name(sheet_name)
    # select the serverless function to be tested, use column number
    col = 0
    x = worksheet.col_values(col)
    # print(x)

    # the number of performance data to be tested
    test_number = 50

    # read the corresponding performance data, 1 represents the column title, removing it
    testData = x[1:test_number+1] 


    # totalData is all performance data of the ground truth, containing 1,000 points. This ground truth is used to evalaute the effectiveness of testing results
    totalData = x[1:1001]

    # 2. parameter settings
    
    # the number of repetitions of the run interval
    interval = 5

    # the confidence level, used in SuperFlow
    confidence_level = 0.95

    # SuperFlow's error demand of the stop condition
    error_bound = 0.01


    #-------------------------------------------------

    CImethod1 = "general"
    print("************SCOPE 1 - General method:{}".format(CImethod1))
    result = determineStopRun(testData, interval, CImethod1, confidence_level, error_bound)
    if result == "Yes":
        # evaluate the accuracy and credibility
        identifyEffectiveness(testData, totalData, confidence_level)


    CImethod2="bootstrapping"
    print("************SCOPE 2 - Basic Bootstrapping method:{}".format(CImethod2))
    result = determineStopRun(testData, interval, CImethod2, confidence_level, error_bound)
    if result == "Yes":
        # evaluate the accuracy and credibility
        identifyEffectiveness(testData, totalData, confidence_level)


    CImethod3 = "block bootstrapping"
    print("************SCOPE 3 - Block Bootstrapping method:{}".format(CImethod3))
    result = determineStopRun(testData, interval, CImethod3, confidence_level, error_bound)
    if result == "Yes":
        # evaluate the accuracy and credibility
        identifyEffectiveness(testData, totalData, confidence_level)




