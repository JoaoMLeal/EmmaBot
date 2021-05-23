import sys
import io
import tweepy

import secret

def main(username):
    # Twitter authentication
    auth = tweepy.OAuthHandler(secret.TWITTER_CLIENT, secret.TWITTER_SECRET)
    auth.set_access_token(secret.TWITTER_ACCESS, secret.TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)

    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=username, count=200, include_rts=False)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(oldest)
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=username, count=200, max_id=oldest, include_rts=False)
        # save most recent tweets
        alltweets.extend(new_tweets)
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    # write the tweets in a txt file
    with io.open("corpus.txt", "w", encoding="utf-8") as corpus:
        for tweet in alltweets:
            corpus.write(tweet.text + "\n")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main("catraslave")
    else:
        username = sys.argv[1]
        main(username)

