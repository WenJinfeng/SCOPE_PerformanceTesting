try:
  import unzip_requirements
except ImportError:
  pass

import time
import nltk
nltk.data.path.append('nltk_data/')
from nltk.tokenize import word_tokenize
from util import *

def main(event,context):
    startTime = 1000*time.time()
    tokens = word_tokenize(event['body']['message'])
    response = {'statusCode': 200, "body":len(tokens)}
    endTime = 1000*time.time()
    return timestamp(response, event, startTime, endTime, 0)


# if __name__=="__main__":
#     print(main(
# {
#     "body":{
#     "message": "Pt is 87 yo woman, highschool teacher with past medical history that includes   - status post cardiac catheterization in April 2019.She presents today with palpitations and chest pressure.HPI : Sleeping trouble on present dosage of Clonidine. Severe Rash  on face and leg, slightly itchy  Meds : Vyvanse 50 mgs po at breakfast daily,             Clonidine 0.2 mgs -- 1 and 1 / 2 tabs po qhs HEENT : Boggy inferior turbinates, No oropharyngeal lesion Lungs : clear Heart : Regular rhythm Skin :  Mild erythematous eruption to hairline Follow-up as scheduled"
# } }, {}))
