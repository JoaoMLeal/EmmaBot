import sys
import io
import tweepy
import json

import tweetgen
import secret


# Twitter authentication
def tweepy_auth():
    auth = tweepy.OAuthHandler(secret.TWITTER_CLIENT, secret.TWITTER_SECRET)
    auth.set_access_token(secret.TWITTER_ACCESS, secret.TWITTER_ACCESS_SECRET)
    api_ = tweepy.API(auth)
    return api_


# Open and read corpus
def read_corpus():
    corpus = io.open("corpus.txt", "r", encoding="utf-8")
    word_lines_ = corpus.readlines()
    corpus.close()
    return word_lines_


# Send replies to mentions
def check_mentions():
    # Get last tweet id
    since_id, index = read_id_file()

    # Send tweets to mentions
    new_since_id = since_id
    for at_tweet in tweepy.Cursor(api.mentions_timeline,
                                  since_id=since_id).items():
        new_since_id = max(at_tweet.id, new_since_id)
        if at_tweet.in_reply_to_status_id is not None:
            continue

        # Reply with generated tweet
        reply_tweet = get_from_many_tweets(index)
        reply_tweet = "@{} {}".format(at_tweet.user.screen_name, reply_tweet)
        api.update_status(
            status=reply_tweet,
            in_reply_to_status_id=at_tweet.id
        )
        index += 1

    # Write last tweet id
    update_id_file(new_since_id, index)


# Send tweet
def send_single_tweet():
    since_id, index = read_id_file()

    tweet = get_from_many_tweets(index)
    api.update_status(tweet)

    update_id_file(since_id, index+1)


# Get tweet from file
def get_from_many_tweets(index):
    with io.open("many_tweets.txt", "r", encoding="utf-8") as many:
        tweets = many.readlines()
        tweet = tweets[index]
    return tweet


# Update log file
def update_id_file(since_id, tweet_count):
    data = dict()
    data['since_id'] = since_id
    data['tweet_count'] = tweet_count

    id_file = open("ids.json", "w")
    json.dump(data, id_file)
    id_file.close()


# Read log file
def read_id_file():
    id_file = open("ids.json", "r")
    data = json.load(id_file)
    id_file.close()

    return data['since_id'], data['tweet_count']


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No command")
    else:
        api = tweepy_auth()
        word_lines = read_corpus()
        if sys.argv[1] == "hourly_tweet":
            send_single_tweet()
        elif sys.argv[1] == "check_mentions":
            check_mentions()
        elif sys.argv[1] == "gen":
            tweetgen.gen_many_tweets(word_lines, 3000)

