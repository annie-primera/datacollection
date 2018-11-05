from __future__ import print_function
import time
import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException
from pprint import pprint


class Grammar:
    def __init__(self):
        configuration = ProWritingAidSDK.Configuration()
        configuration.host = 'https://api.prowritingaid.com'
        configuration.api_key['licenseCode'] = 'A17D00BF-3DF2-40DA-AE0F-0B8172F2CB1C'

    @staticmethod
    def summary(text):
        text = text
        settings = {"settings": {
            "shortestAverageSentenceLength": 11,
            "longestAverageSentenceLength": 18,
            "longestIndividualSentence": 30,
            "highestPassiveIndex": 25,
            "maxGlueIndex": 40,
            "minSentenceVariety": 3,
            "highestPronounPercentage": 15,
            "lowestPronounPercentage": 4,
            "highestAcademicPronounPercentage": 2,
            "highestInitialPronounPercentage": 30,
            "lowestInitialPronounPercentage": 0,
            "lowestWeWeScore": 0.6,
            "longestAverageParagraphLength": 6
        },
            "style": "Academic",
            "language": "en_uk"
        }

        api_instance = ProWritingAidSDK.SummaryApi()
        requestp = ProWritingAidSDK.SummaryAnalysisRequest(text, settings)  # SummaryAnalysisRequest |

        summary_response = api_instance.post(requestp)
        return(summary_response.result.text)
        #return pprint(summary_response.result.text)