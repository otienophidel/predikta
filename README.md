# Sentiment Analysis for Stock Price Prediction

This program performs sentiment analysis on tweets related to a particular stock and then predicts the future stock prices based on the sentiment analysis. 

## Requirements
- Python 3.x
- pandas
- numpy
- matplotlib
- scikit-learn

## How to Use

1. Install all required libraries using pip or conda.
2. Put all the csv files containing the tweets in the same folder as the python script.
3. Run the `predict.py [csvfilename] [csvfilename]` script.

The script performs the following operations:
1. Reads the CSV files containing the tweets.
2. Cleans the tweets by removing URLs, hashtags, usernames, punctuations, and harmonizes the cases.
3. Performs sentiment analysis on the cleaned tweets.
4. Adds the sentiment labels to the CSV files.
5. Merges the sentiment labels with the stock prices CSV file.
6. Splits the merged dataset into training and testing sets.
7. Scales the features using the StandardScaler from scikit-learn.
8. Trains a neural network model using the MLPRegressor from scikit-learn.
9. Evaluates the model's performance on the test set.
10. Predicts future stock prices based on the sentiment analysis using the trained model.

The predicted stock prices are plotted using matplotlib.