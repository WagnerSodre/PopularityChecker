import os
import json
import shutil

import pandas as pd

from src.utils import Utils
from src.twitterClient import TwitterClient
from src.csvGenerator import CSV
from src.pdfGenerator import PDF
from src.graphGenerator import Graph
from src.sentimentAnalyzer import SentimentAnalyzer

from translatte import Translator
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BEARER')

fname = 'data/request.json'
if not os.path.isfile(fname):
    raise Exception("Error! File data/request.json not found")
request_parameters = json.load(open(fname))

os.mkdir('data/tmp')

utils = Utils()
twitter = TwitterClient(token)
csv = CSV()
pdf = PDF(request_parameters['topic'])
graph = Graph()
sentimentAnalyzer = SentimentAnalyzer()

fname = 'data/tweets.csv'
if not os.path.isfile(fname):
    tweets = twitter.request('search', request_parameters['topic'], request_parameters['search'])
    csv.generate(tweets, fname)
df = pd.read_csv(fname, sep=';', encoding='utf-8', engine='python')

tweets_df = df.drop_duplicates(subset=['user_name', 'text'])

plts = []

tweetCount = twitter.request('count', request_parameters['topic'], request_parameters['count'])
x, y = utils.sort(tweetCount, 'start', 'tweet_count')

averageNumberOfTweets = int(sum(y) / len(y))

outliers = utils.getOutliers(tweetCount, 'start', 'end', 'tweet_count', averageNumberOfTweets)

translated_df = tweets_df
for idx, row in tweets_df.iterrows():
    try:
        translated_df.loc[idx,'text'] = str(Translator.translate(translated_df.loc[idx,'text'], 'en'))
        print(translated_df.loc[idx,'text'])
    except:
        print('ERROR WITH: ', translated_df.loc[idx,'text'])

sample = ' '.join(translated_df['text'])

plts.append(graph.generateWordcloud(sample))

plts.append(graph.generateLineGraph(x, y, 'tweetTimeline'))

sentimentByDate = sentimentAnalyzer.sentimentByDate(translated_df[['text', 'date']])

plts.append(graph.generateLineGraph(sentimentByDate['date'], sentimentByDate['score'], 'sentimentTimeline'))

for outlier in outliers:
    outlier_data = translated_df.loc[(translated_df['date'] > outlier['start']) & (translated_df['date'] < outlier['end'])]
    outlier_x, outlier_y = utils.filterTweetCount(tweetCount, outlier)

    sample = ' '.join(outlier_data['text'])

    plts.append(graph.generateWordcloud(sample, outlier['start'].split('T')[0], outlier['end'].split('T')[0]))

    plts.append(graph.generateLineGraph(outlier_x, outlier_y, 'tweetTimeline', outlier['start'].split('T')[0], outlier['end'].split('T')[0]))

    sentimentByDate = sentimentAnalyzer.sentimentByDate(outlier_data[['text', 'date']])

    plts.append(graph.generateLineGraph(sentimentByDate['date'], sentimentByDate['score'], 'sentimentTimeline', outlier['start'].split('T')[0], outlier['end'].split('T')[0]))

print('Average Sentiment: ', sentimentAnalyzer.analyzeCorpus(translated_df['text']))

pdf.print_images(plts)
pdf.output()

shutil.rmtree('data/tmp')