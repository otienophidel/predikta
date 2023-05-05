"""
# Download sentimental tweets
# Downloads tweets from up to 3000 days ago
# Streams in live tweets
#
# Usage:
#       python sentiments.py <keyword>
#
#
"""

import tweepy
import csv
import sys
import time
from datetime import datetime, timedelta
from tweepy.streaming import Stream

# Replace with your access keys and tokens
def twitter_auth():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''

    # Authenticate to twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    # Check for authentication status
    print('Authenticating API')
    try:
        api.verify_credentials()
        print('Successful API authentication')
    except:
        print('Failed authentication')
        sys.exit(-1)

    return api

# Tweepy Class - Download historical tweets
class HistoricalTweets():        
    def __init__(self, keyword, output_file, api):
        self.keyword = keyword
        self.output_file = output_file
        self.api = api
        
        # Define date range
        today = datetime.today().date()
        end_date = today - timedelta(days=3000)
        
        # Search Queries
        self.search_query = f'{keyword} since:{end_date}'
        # Initialize csv with header row
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Tweet ID', 'Username', 'Text', 'Created At'])

    # Crawl twitter for historical tweets
    def tweet_saver(self):
        # Search for tweets
        for tweet in tweepy.Cursor(self.api.search_tweets, q=self.search_query, tweet_mode='extended').items():
            tweet_id = tweet.id_str
            username = tweet.user.screen_name
            text = tweet.full_text.replace('\n', '')
            created_at = tweet.created_at.strftime('%Y%m%d')

            # Write to output file
            with open(self.output_file, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([tweet_id, username, text, created_at])
            
            print(f'Tweet saved: {username}: {text}')

# Stream listener - for new incoming tweets
class StreamListener(tweepy.Stream):
    def on_status(self, status):
        # Check if tweet contains keyword
        if keyword.lower() in status.text.lower():
            # Extract juicy information
            tweet_id = status.id_str
            username = status.user.screen_name
            text = status.text.replace('\n', '')
            created_at = status.created_at.strftime('%Y%m%d')

            # Write to output
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([tweet_id, username, text, created_at])
            
            print(f'Tweet saved: {username}: {text}')
    
    def on_error(self, status_code):
        print(f'Error: {status_code}')
        return False

def main():
    # Check if company name(keyword) specified as argument
    if len(sys.argv) < 2:
        print('Missing key argument: company name')
        print("Usage: python {sys.argv[0]} ")
        print("Example: python {sys.argv[0] safricom}")
        sys.exit(-1)
    
    # Define search keywords
    company_name = sys.argv[1]
    keyword = f'{company_name}'

    # Output filename - a .csv file
    output_file = f'{company_name}_tweets.csv'

    # Auth
    api = twitter_auth()

    # Download tweets
    historical = HistoricalTweets(keyword, output_file, api)
    historical.tweet_saver()

    # Stream In
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')
    stream.filter(track=[keyword], languages=['en'])

if __name__ == "__main__":
    main()