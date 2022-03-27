import pandas as pd

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

class SentimentAnalyzer():
    def __init__(self):
        super().__init__()
        
    def analyzeCorpus(self, corpus):
        sa = SentimentIntensityAnalyzer()

        total_score = []

        for doc in corpus:
            scores = sa.polarity_scores(doc)
            total_score.append(scores['compound'])
            
        return (sum(total_score) / len(total_score))

    def sentimentByDate(self, corpus):
        corpus = corpus.reset_index()  
        newest_date = datetime.strptime(corpus['date'].iloc[0].split('T')[0], "%Y-%m-%d").date()
        tweets = []
        res = pd.DataFrame(columns=['date', 'score'])
        for index, row in corpus.iterrows():
            date = datetime.strptime(row['date'].split('T')[0], "%Y-%m-%d").date()
            if (date < newest_date):
                day_score = self.analyzeCorpus(tweets)
                res = res.append({'date': newest_date, 'score': day_score}, ignore_index=True)
                newest_date = date
                tweets = []
            tweets.append(row['text'])
        
        return res