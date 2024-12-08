import pandas as pd
import numpy as np
from scipy.special import comb as ncr
from xlrd import open_workbook
import scipy.stats as kl
import sys
import math

def median_and_ci(s):
    """
    For a value series (or dataframe column), return median and median CI, as defined by a nonparametric approach.
    """
    n = len(s)
    if n >= 10:
        s_median = s.median()
        lo_rank = int(np.rint(n / 2.0 - 1.96 * np.sqrt(n) / 2.0))
        hi_rank = int(np.rint(1 + n / 2.0 + 1.96 * np.sqrt(n) / 2.0))
        s_sorted = sorted(s.tolist())
        lo_val = s_sorted[lo_rank]
        hi_val = s_sorted[hi_rank]
        return s_median, lo_val, hi_val, 0
    else:
        # Not enough data to construct CI
        return None, None, None, 1

def CONFIRM(data, desired_error, sample_size_min=10, sample_size_max=None, max_rep_count=20):
    """
    Function to evaluate the confidence interval (CI) by sampling the dataset and determining if it meets desired criteria.
    """
    if not sample_size_max:
        sample_size_max = len(data)

    ci_results = []
    for sample_size in range(sample_size_min, sample_size_max + 1):
        rep_count = min(max_rep_count, int(ncr(sample_size_max, sample_size)))
        
        for rep in range(rep_count):
            # Use different seed for each repetition to ensure randomization
            np.random.seed()
            selected_sample = data.sample(sample_size, replace=False)
            med, ci_lb, ci_ub, errc = median_and_ci(selected_sample)

            if not errc:
                ci_results.append({
                    "rep": rep,
                    "sample_size": sample_size,
                    "med": med,
                    "ci_lb": ci_lb,
                    "ci_ub": ci_ub
                })

    # Convert results to a DataFrame for easier analysis
    df_ci = pd.DataFrame(ci_results)
    stopping_sample_size = 0

    # Group by sample size to calculate means for confidence bounds
    if len(df_ci) > 0:
        df_avg = df_ci.groupby(['sample_size']).mean()
        df_avg["desired_lb"] = df_avg["med"] - desired_error * df_avg["med"]
        df_avg["desired_ub"] = df_avg["med"] + desired_error * df_avg["med"]
        df_avg["stopping_ub"] = df_avg["ci_ub"] <= df_avg["desired_ub"]
        df_avg["stopping_lb"] = df_avg["ci_lb"] >= df_avg["desired_lb"]
        df_avg["stopping"] = df_avg["stopping_lb"] & df_avg["stopping_ub"]
        df_avg["sample_size"] = df_avg.index.values

        # Find the first sample size that meets the stopping criteria
        stopping_sample_size = df_avg[df_avg["stopping"]].sample_size.min() if not df_avg[df_avg["stopping"]].empty else None
        print(f"The recommended stopping sample size is: {stopping_sample_size}")
        
    # else:
    #     df_avg = pd.DataFrame()

    return stopping_sample_size

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



def identidyEffectiveness(data, totalData, confidence_level):

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

    

    # strResult=""
    # for k in range(len(resultData)):
    #     if k==0:
    #         strResult="{}".format(resultData[k])
    #     else:
    #         strResult=strResult +"\t {}".format(resultData[k])
    
    # print(strResult)
    # return strResult
    return resultData
  

if __name__ == "__main__": 
    workbook=open_workbook('Performance_Data.xlsx')
    sheet_name = "Cold-start performance"
    worksheet=workbook.sheet_by_name(sheet_name)
    ncols = worksheet.ncols
    interval = 20
    desired_error = 0.03
    confidence_level = 0.95

    # outputResult = "Result/ComfirmColdInterval3.txt"
    # outputResult = "Result/ComfirmWarm1%.txt"
    # with open(outputResult, "a") as test:
    #     test.truncate(0)
    # test.close()
    # try:
    sum_values = [0] * 6

    for col in range(ncols):
        x = worksheet.col_values(col)
        col_name = x[0]
        totalData = x[1:1001]
        for DN in range(interval, 1001, interval):
            test_number = DN
            testData = x[1:test_number+1] 
            data = pd.Series(testData)
            print(DN)
            result = CONFIRM(data, desired_error)
            # print(result)
            if result != 0 and result != None:
                strResult = identidyEffectiveness(testData, totalData, confidence_level)
                # print(len(strResult))
                for i in range(len(strResult)):
                    sum_values[i] += strResult[i]

                # strResult = "{}\t {}".format(col_name, strResult)
                # with open(outputResult, "a") as f:
                #     f.write(strResult)
                #     f.write("\n")
                # f.close()
                # print(strResult)
                break
    average_values = [round(sum_value / 65, 6) for sum_value in sum_values]
    print("{}, {}, {}, {}, {}, {}".format(average_values[0], average_values[1], average_values[2], average_values[3], average_values[4], average_values[5]))
    
    # except Exception as e:
    #         print(e)
