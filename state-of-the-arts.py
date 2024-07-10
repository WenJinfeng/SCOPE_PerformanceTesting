from xlrd import open_workbook
from statsmodels.tsa.stattools import adfuller
import scipy.stats as kl
import math
import sys
import numpy as np
import numpy.random as npr
from recombinator.optimal_block_length import optimal_block_length

# baseline 1
def fse19method(data, interval, thresholdSim):

    Data_Size = len(data)
    # check new distribution if its number of data is greater than interval
    if Data_Size < interval:
        print("newly added data is not enough!")
        return 0
    
    # start the data analysis
    old_data = data[:Data_Size-interval]

    old_dist = np.array(old_data)
    new_dist = np.array(data)
    # calculate the distribution similarity
    similarity = distSimilarity(old_dist, new_dist)
    

    if similarity >= thresholdSim:
        print("=====> The current performance data is accurate and reliable, and its number of repetitions is {} ********".format(Data_Size))
        return "Yes"
        
    else:
        print("=====>{} performance data is not enough. Please continue running the serverless function!!!".format(Data_Size))
        return "No"


# baseline 2
def ase21method(data, interval, object_accu):
    
    Data_Size = len(data)
    # check new distribution if its number of data is greater than interval
    if Data_Size < interval:
        print("newly added data is not enough!")
        return 0
    
    # start the data analysis
    old_data = data[:Data_Size-interval]
    block_length_bound = 1
    

    try:
        b_star = optimal_block_length(np.array(old_data))
        block_length = math.ceil(b_star[0].b_star_cb)
        if block_length_bound >= block_length:
            block_length = block_length_bound
    except Exception as e:
        block_length = block_length_bound
        
    

    # calculate the percentage error for the 50th percentile performance, the median
    errRate = block_bootstrap(old_data, data, 1000, 50, block_length)
    
    if (errRate <= 1-object_accu):
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

    
def CI_general(data, confidence_level, metricValue):

    # obtain the top and bottom bounds of condidence interval
    low, top = calculateTopLow(len(data), confidence_level, metricValue)
    
    if low > 0 and top<len(data):
        
        data_sorted = sorted(data)
        lo_CI = data_sorted[low]
        hi_CI = data_sorted[top]

    return lo_CI, hi_CI


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

    



#Generate moving window blocks for block_bootstrap
def gen_mvwin_blocks(data, block_length):
    #the samples which can generate blocks
    block_count = len(data) - block_length
    blocks = []
    
    for i in range(block_count):
        new_block = data[i : i + block_length]
        blocks.append(new_block)
        
    return np.array(blocks)

#The main logic for block bootstrap
def block_bootstrap(data1, data2, bootstrapTimes, percentile, block_length):
    #data1 is the smaller data sample
    #bootstrap times preferred to be larger than 1000
    #percentile could be any integer percentile value or "average"
    
    #generate blocks
    blocks_1 = gen_mvwin_blocks(data1, block_length)
    blocks_2 = gen_mvwin_blocks(data2, block_length)
    
    #generate block1 information
    block_count_1 = blocks_1.shape[0]
    block_length_1 = blocks_1.shape[1]
    required_blocks_1 = math.floor(block_count_1 / block_length_1)
    
    #generate block2 information
    block_count_2 = blocks_2.shape[0]
    block_length_2 = blocks_2.shape[1]
    required_blocks_2 = math.floor(block_count_2 / block_length_2)

    # Apply bootstrap on data1
    index_1 = []
    for i in range(bootstrapTimes):
        idx1 = npr.choice(block_count_1, size = required_blocks_1,
                          replace = True)
        index_1.append(idx1)
    bootstrapData1 = np.array(blocks_1[index_1])

    # Apply bootstrap on data2  
    index_2 = []
    for i in range(bootstrapTimes):
        idx2 = npr.choice(block_count_2, size = required_blocks_2, 
                          replace = True)
        index_2.append(idx2)
    bootstrapData2 = np.array(blocks_2[index_2])
    
    #calculate the statistics
    if (percentile == "average"):
        #un-block and calculate the means        
        data1MeanStarBar = []
        for i in range(bootstrapTimes):
            lis_cache = []
            for j in range(bootstrapData1.shape[1]):
                lis_cache = np.append(lis_cache, bootstrapData1[i][j])
            data1MeanStarBar.append(lis_cache)
            
        data2MeanStarBar = []
        for i in range(bootstrapTimes):
            lis_cache = []
            for j in range(bootstrapData2.shape[1]):
                lis_cache = np.append(lis_cache, bootstrapData2[i][j])
            data2MeanStarBar.append(lis_cache)
        
        data1MeanStar = np.mean(data1MeanStarBar, axis=1) 
        data2MeanStar = np.mean(data2MeanStarBar, axis=1)
        

        errorRates = []
        for i in range(bootstrapTimes):
            bootstrappedError = np.abs(data1MeanStar[i]-data2MeanStar[i])/data2MeanStar[i]
            errorRates.append(bootstrappedError)
        #generate bootstrapped error rate list    
        errorPercentile = np.percentile(errorRates,95)
        #get mean error rate at 95% CL
        return errorPercentile
        
    else:
        #un-block and calculate the percentiles 
        data1PercentileStarBar = []
        for i in range(bootstrapTimes):
            lis_cache = []
            for j in range(bootstrapData1.shape[1]):
                lis_cache = np.append(lis_cache, bootstrapData1[i][j])
            data1PercentileStarBar.append(lis_cache)
            
        data2PercentileStarBar = []
        for i in range(bootstrapTimes):
            lis_cache = []
            for j in range(bootstrapData2.shape[1]):
                lis_cache = np.append(lis_cache, bootstrapData2[i][j])
            data2PercentileStarBar.append(lis_cache)
        
        data1PercentileStar = np.percentile(data1PercentileStarBar, percentile, axis=1) 
        data2PercentileStar = np.percentile(data2PercentileStarBar, percentile, axis=1)
        
        errorRates = []
        for i in range(bootstrapTimes):
            bootstrappedError = np.abs(data1PercentileStar[i]-data2PercentileStar[i])/data2PercentileStar[i]
            errorRates.append(bootstrappedError)
        #generate bootstrapped error rate list    
        errorPercentile = np.percentile(errorRates,95)
        #get X-percentile error rate at 95% CL
        return errorPercentile



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


    # totalData is all performance data of the ground truth, containing 1,000 points. This ground truth is used to evaluate the effectiveness of testing results
    totalData = x[1:1001]

    # 2. parameter settings
    
    # the number of repetitions of the run interval
    interval = 5

    # the objective similarity probability of PT4Cloud
    thresholdSim = 0.90


    # Metior's maximum allowed error
    ASEerror = 0.03
    object_accu = 1 - ASEerror


    # the confidence level, used in Metior
    confidence_level = 0.95




    #-------------------------------------------------


    print("************FSE'19 - PT4Cloud:")
    result = fse19method(testData, interval, thresholdSim)
    if result == "Yes":
        # evaluate the accuracy and credibility
        identifyEffectiveness(testData, totalData, confidence_level)



    print("************ASE'21 - Meitor:")
    result = ase21method(testData, interval, object_accu)
    if result == "Yes":
        # evaluate the accuracy and credibility
        identifyEffectiveness(testData, totalData, confidence_level)

