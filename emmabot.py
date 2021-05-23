import time
import io
import tweepy

import tweetgen
import secret

def main():
    # Twitter authentication
    auth = tweepy.OAuthHandler(secret.TWITTER_CLIENT, secret.TWITTER_SECRET)
    auth.set_access_token(secret.TWITTER_ACCESS, secret.TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)

    # Open and read corpus
    corpus = io.open("corpus.txt", "r", encoding="utf-8")
    word_lines = corpus.readlines()
    corpus.close()

    # Check if the bot has been mentioned
    def check_mentions():
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
        return new_since_id

    since_id = 1
    cur_time = 0
    max_time = 3600

    while True:
        since_id = check_mentions()
        cur_time = 60 + cur_time

        if cur_time > max_time:
            cur_time = 0
            tweet = tweetgen.make_tweet(word_lines)
            print(tweet)
            api.update_status(tweet)

        time.sleep(60)


if __name__ == '__main__':
    main()


