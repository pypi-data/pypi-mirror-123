from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import pandas as pd
from typing import Optional

obj = SentimentIntensityAnalyzer()

def sentimentAnalysis(ticker:list,headlines:list, date:list) -> Optional[pd.DataFrame]:
    '''
    This function is used to perform sentiment analysis on stocks

    The purpose of this function is to create a dictionary, use 
    each headline from the headlines list and perform sentiment analysis

    Args:
        ticker: Stock ticker symbol of stock

        headlines: List of headlines

        date: The date of the headline
    
    Returns:
        Pandas dataframe: a datatable containing sentiment data
    '''
    dict_name = ['date','ticker','headline','sentiment']
    sentiment_data = {}
    for i in range(len(dict_name)):
        sentiment_data[dict_name[i]] = []

    counter = 0
    for headline in headlines:
        if headline == "Unknown":
            pass
        else:
            sentiment_eg=obj.polarity_scores(headline)
            sentiment_compound = sentiment_eg['compound']
            sentiment_value = [date[counter],ticker[counter],headline,sentiment_compound]
            counter +=1
            for i in range(len(sentiment_value)):
    
                    sentiment_data[dict_name[i]].append(str(sentiment_value[i]))
    df = pd.DataFrame.from_dict(sentiment_data) 

    return df


