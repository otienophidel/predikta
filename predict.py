"""
# Clean tweets
# Analyse tweets
# Sentiment analysis and classification
# Predict
"""

import csv
import re
import string
import html
import sys
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from typing import List


class Cleaner:
    def __init__(self):
        self.remove_punctuations = str.maketrans('', '', string.punctuation)

    def read_csv(self, csv_name):
        cleaned_text = []
        with open(csv_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                text = row['text']
                clean_text = self.clean_tweets(text)
                cleaned_text.append(clean_text)
        self.save_cleaned_csv('cleaned_safaricom_tweets.csv', cleaned_text)

    def clean_tweets(self,tweet):
        # harmonize the cases
        lower_case_text = tweet.lower()
        # remove urls
        removed_url = re.sub(r'http\S+', '', lower_case_text)
        # remove hashtags
        removed_hash_tag = re.sub(r'#\w*', '', removed_url) # hastag
        # remove usernames from tweets
        removed_username = re.sub(r'@\w*\s?','',removed_hash_tag)
        # removed retweets
        removed_retweet = removed_username.replace("rt", "", True) # remove to retweet
        # removing punctuations
        removed_punctuation = removed_retweet.translate(self.remove_punctuations)
        # remove spaces
        remove_g_t = removed_punctuation.replace("&gt", "", True)
        remove_a_m_p = remove_g_t.replace("&amp", "", True)
        final_text = remove_a_m_p
        return final_text

    def pre_cleaning(self,text):
        html_escaped = html.unescape(text)
        final_text = html_escaped.replace(';','')
        return final_text

    def pre_labeling(self,text):
        lower_case_text = text.lower()
        removed_url = re.sub(r'http\S+', '', lower_case_text)
        return removed_url

    def save_cleaned_csv(self,name,tweets_list):
        with open(name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["text"])

            for tweet in tweets_list:
                writer.writerow([tweet,])
        pass

    def save_pre_labled_csv(self,csv_name):
        cleaned_text = []
        with open(csv_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                text = row['text']
                clean_text = self.pre_labeling(text)
                cleaned_text.append(clean_text)
        self.save_pre_labeled_csv('unlabeled_' + csv_name, cleaned_text)

    def save_pre_labeled_csv(self,name,tweets_list):
        with open('pre_labeled_' + name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["text","label"])

            for tweet in tweets_list:
                writer.writerow([tweet,])
        pass
        
class SentimentAnalyzer:
    def __init__(self, positive_words_file:str, negative_words_file:str):
        self.positive_words = self.load_words(positive_words_file)
        self.negative_words = self.load_words(negative_words_file)
        
    def load_words(self, words_file:str) -> List[str]:
        with open(words_file, 'r', encoding='latin-1') as f:
            words = f.readlines()
        return [word.strip() for word in words]
    
    def analyze_sentiment(self, tweet:str) -> int:
        positive_count = sum([tweet.count(word) for word in self.positive_words])
        negative_count = sum([tweet.count(word) for word in self.negative_words])
        if positive_count > negative_count:
            return 1
        elif positive_count < negative_count:
            return -1
        else:
            return 0
    
    def add_sentiment_labels(self, input_file:str, output_file:str):
        with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
            reader = csv.DictReader(in_file)
            writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames + ['sentiment'])
            writer.writeheader()
            for row in reader:
                sentiment = self.analyze_sentiment(row['text'])
                writer.writerow(dict(row, sentiment=sentiment))

# Add sentiments to stock prices
class SentimentMerger:
    def __init__(self):
        pass

    def read_sentiment_column(self, csv_name):
        sentiments = []
        with open(csv_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sentiment = row['sentiment']
                sentiments.append(sentiment)
        return sentiments

    def merge_sentiment(self, csv_name, sentiments):
        new_rows = []
        with open(csv_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for index, row in enumerate(reader):
                row['label'] = sentiments[index]
                new_rows.append(row)
        fieldnames = new_rows[0].keys()
        with open('merged_' + csv_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in new_rows:
                writer.writerow(row)

# finally train model and predict prices
class Predict:
    def __init__(self, filename):
        self.filename = filename
    
    def predict_stock_prices(self):
        # Read the merged CSV file
        try:
            df = pd.read_csv(self.filename)
        except:
            print(f"Error reading file {self.filename}")
            return

        # Prepare the data for prediction
        df_close = df[['Close']]
        forecast_out = int(30) # predicting 30 days into future
        df['Prediction'] = df_close.shift(-forecast_out) # label column with data shifted 30 units up
        X = np.array(df.drop(columns=['Prediction', 'label'])) # remove unnecessary columns
        X = preprocessing.scale(X)
        X_forecast = X[-forecast_out:] # set X_forecast equal to last 30
        X = X[:-forecast_out] # remove last 30 from X
        y = np.array(df['Prediction'])
        y = y[:-forecast_out]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Training
        clf = MLPRegressor(max_iter=1000, random_state=42)
        clf.fit(X_train, y_train)

        # Testing
        confidence = clf.score(X_test, y_test)
        print("confidence: ", confidence, "\n")
        forecast_prediction = clf.predict(X_forecast)
        print('30 Days prediction')
        print(forecast_prediction)

        # Plot predicted prices against next 30 days
        plt.plot(forecast_prediction)
        plt.title('Safaricom Stock Price Prediction')
        plt.xlabel('Day')
        plt.ylabel('Closing Price')
        plt.show()

banner = '''
██████╗ ██████╗ ███████╗██████╗ ██╗██╗  ██╗████████╗ █████╗ 
██╔══██╗██╔══██╗██╔════╝██╔══██╗██║██║ ██╔╝╚══██╔══╝██╔══██╗
██████╔╝██████╔╝█████╗  ██║  ██║██║█████╔╝    ██║   ███████║
██╔═══╝ ██╔══██╗██╔══╝  ██║  ██║██║██╔═██╗    ██║   ██╔══██║
██║     ██║  ██║███████╗██████╔╝██║██║  ██╗   ██║   ██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
'''

def main():
	
	print(banner)
	
	# read filename from command line argument
	if len(sys.argv) != 3:
		print("Usage: python {} <tweetsfile.csv> <stockprices.csv>".format(sys.argv[0]))
		print("Example: python {} example.csv example_prices.csv".format(sys.argv[0]))
		sys.exit(-1)
	filename = sys.argv[1]
	prices_file = sys.argv[2]
	
	# clean crawled tweets
	print("Cleaning Tweets")
	cleaner = Cleaner()
	cleaner.read_csv(filename)
	time.sleep(5)

	# sentiment classification
	print("Classifying Tweet Sentiments")
	analyzer = SentimentAnalyzer('positive_words.txt', 'negative_words.txt')
	analyzer.add_sentiment_labels('cleaned_safaricom_tweets.csv', 'sentiment_labeled_safaricom_tweets.csv')

	# merge sentiment to stock prices
	merger = SentimentMerger()
	sentiments = merger.read_sentiment_column('sentiment_labeled_safaricom_tweets.csv')
	merger.merge_sentiment(prices_file, sentiments)
	
	predictor = Predict('merged_safaricom_master.csv')
	predictor.predict_stock_prices()

if __name__ == "__main__":
	main()
