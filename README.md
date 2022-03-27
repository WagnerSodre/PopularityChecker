# Popularity Checker

This project was made to check the popularity of a topic/enterprise, by getting the tweets of the topic/enterprise, building a wordcloud about it, a timeline of the tweets amount and a timeline of the sentiment. It also builds the same graphs of the dates with more tweets than usual.

To run it, you will need python installed.

Execution steps:
- make a .env file based on .env.example
- configure data/request.json with your parameters
- delete data/tweets.csv if you want to generate a new one
-  `pip install -r requirements.txt`
-  `python3 run.py`