import json
import pandas as pd

tweet_json = 'filename'
# Convert from JSON to Python object
tweet = json.loads(tweet_json)


def flatten_tweets(tweets_json):
    """ Flattens out tweet dictionaries so relevant JSON
        is in a top-level dictionary."""
    tweets_list = []

    # Iterate through each tweet
    for tweet in tweets_json:
        tweet_obj = json.loads(tweet)

        # Store the user screen name in 'user-screen_name'
        tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']

        # Check if this is a 140+ character tweet
        if 'extended_tweet' in tweet_obj:
            # Store the extended tweet text in 'extended_tweet-full_text'
            tweet_obj['extended_tweet-full_text'] = tweet_obj['extended_tweet']['full_text']

        if 'retweeted_status' in tweet_obj:
            # Store the retweet user screen name in 'retweeted_status-user-screen_name'
            tweet_obj['retweeted_status-user-screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']

            # Store the retweet text in 'retweeted_status-text'
            tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status']['text']

        tweets_list.append(tweet_obj)
    return tweets_list


# Flatten the tweets and store in `tweets`
tweets = flatten_tweets(tweet_json)

# Create a DataFrame from `tweets`
ds_tweets = pd.DataFrame(tweets)


# Convert the created_at column to np.datetime object
ds_tweets['created_at'] = pd.to_datetime(ds_tweets['created_at'])

# Print created_at to see new format
print(ds_tweets['created_at'].head())

# Set the index of ds_tweets to created_at
ds_tweets = ds_tweets.set_index('created_at')


# Generate average sentiment scores for #python
# NOTE (ikorsakov): Pay attention that dataframe is filtered by series (from the same df)
#                   Resample() function works with series and create bins to apply statistics on
sentiment_py = sentiment[check_word_in_tweet('#python', ds_tweets)].resample('1 d').mean()