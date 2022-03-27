import pandas as pd

class CSV():
    def __init__(self):
        super().__init__()

    def generate(self, tweets, fname):
        tweets_df = pd.DataFrame()
        for tweet in tweets:
            hashtags = []
            try:
                for hashtag in tweet.entities["hashtags"]:
                    hashtags.append(hashtag["text"])
            except:
                pass
            tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet['user']['name'].replace(';', ','), 
                                                    'user_location': tweet['user']['location'].replace(';', ',') if hasattr(tweet['user'], 'location') else None,
                                                    'user_description': tweet['user']['description'].replace(';', ','),
                                                    'user_verified': tweet['user']['verified'],
                                                    'date': tweet['created_at'].replace(';', ','),
                                                    'text': tweet['text'].replace(';', ','), 
                                                    'hashtags': [hashtags.replace(';', ',') if hashtags else None],
                                                    'language': tweet['lang'].replace(';', ','),
                                                    'source': tweet['source'].replace(';', ',')}))
            tweets_df = tweets_df.reset_index(drop=True)
        tweets_df.to_csv(fname, sep=';', encoding='utf-8')
