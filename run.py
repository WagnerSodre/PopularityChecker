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
tweets_df = pd.read_csv(fname, sep=';', encoding='utf-8', engine='python')

plts = []

tweetCount = twitter.request('count', request_parameters['topic'], request_parameters['count'])
x, y = utils.sort(tweetCount, 'start', 'tweet_count')

averageNumberOfTweets = int(sum(y) / len(y))

outliers = utils.getOutliers(tweetCount, 'start', 'end', 'tweet_count', averageNumberOfTweets)

filtered_df = tweets_df.loc[tweets_df['language'] == 'en']
sample = ' '.join(filtered_df['text'])

plts.append(graph.generateWordcloud(sample))

plts.append(graph.generateLineGraph(x, y, 'tweetTimeline'))

sentimentByDate = sentimentAnalyzer.sentimentByDate(filtered_df[['text', 'date']])

plts.append(graph.generateLineGraph(sentimentByDate['date'], sentimentByDate['score'], 'sentimentTimeline'))

for outlier in outliers:
    outlier_data = filtered_df.loc[(filtered_df['date'] > outlier['start']) & (filtered_df['date'] < outlier['end'])]
    outlier_x, outlier_y = utils.filterTweetCount(tweetCount, outlier)

    sample = ' '.join(outlier_data['text'])

    plts.append(graph.generateWordcloud(sample, outlier['start'].split('T')[0], outlier['end'].split('T')[0]))

    plts.append(graph.generateLineGraph(outlier_x, outlier_y, 'tweetTimeline', outlier['start'].split('T')[0], outlier['end'].split('T')[0]))

    sentimentByDate = sentimentAnalyzer.sentimentByDate(outlier_data[['text', 'date']])

    plts.append(graph.generateLineGraph(sentimentByDate['date'], sentimentByDate['score'], 'sentimentTimeline', outlier['start'].split('T')[0], outlier['end'].split('T')[0]))

print('Average Sentiment: ', sentimentAnalyzer.analyzeCorpus(filtered_df['text']))

pdf.print_images(plts)
pdf.output()

shutil.rmtree('data/tmp')