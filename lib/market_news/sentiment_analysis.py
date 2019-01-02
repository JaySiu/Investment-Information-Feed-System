import numpy as np
import pandas as pd
import module_path as mp
from nlp import nlp
from snownlp import SnowNLP
from mk_user_portfolio import retrieve_client_news

TITLE_WEIGHT = 0.5
CONTENT_WEIGHT = 1 - TITLE_WEIGHT

##### helpers ##################################################################






################################################################################

def get_news_sentiment():
    print("Analyzing news' sentiments...")
    df = retrieve_client_news()
    sentiment = []
    for idx, row in df.iterrows():
        if row.Content == '-----':
            sentiment.append('-----')
        else:
            s = SnowNLP(row.Content)
            sentences_sen = []
            for sentence in s.sentences:
                ss = SnowNLP(sentence)
                sentences_sen.append(ss.sentiments)
            mean_score = np.mean(np.array(sentences_sen))
            s = SnowNLP(row.Title)
            score = TITLE_WEIGHT * s.sentiments + CONTENT_WEIGHT * mean_score
            sentiment.append(score)
    df['Sentiment'] = sentiment
    print("Saving results...")
    df.to_csv(mp.DIR_DATA_CUSTOMERS + 'customer_related_news.csv', index=False, encoding='utf_8_sig')
    nlp()
