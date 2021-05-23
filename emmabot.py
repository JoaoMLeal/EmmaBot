import sys
import time
import io
import tweepy

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
    id_file = open("since_id.txt", "r+")
    since_id = int(id_file.read())

    # Send tweets to mentions
    new_since_id = since_id
    for at_tweet in tweepy.Cursor(api.mentions_timeline,
                                  since_id=since_id).items():
        new_since_id = max(at_tweet.id, new_since_id)
        if at_tweet.in_reply_to_status_id is not None:
            continue

        # Reply with generated tweet
        reply_tweet = tweetgen.make_tweet(word_lines)
        reply_tweet = "@{} {}".format(at_tweet.user.screen_name, reply_tweet)
        print(reply_tweet, at_tweet.id_str, at_tweet.user.screen_name)
        api.update_status(
            status=reply_tweet,
            in_reply_to_status_id=at_tweet.id
        )

    # Write last tweet id
    id_file.write(new_since_id)


# Send tweet
def send_tweet():
    tweet = tweetgen.make_tweet(word_lines)
    print(tweet)
    api.update_status(tweet)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No command")
    else:
        api = tweepy_auth()
        word_lines = read_corpus()
        if sys.argv[1] == "hourly_tweet":
            check_mentions()
        elif sys.argv[1] == "check_mentions":
            send_tweet()

