import sys
import tweepy

import secret

def main(username):
    # Twitter authentication
    auth = tweepy.OAuthHandler(secret.TWITTER_CLIENT, secret.TWITTER_SECRET)
    auth.set_access_token(secret.TWITTER_ACCESS, secret.TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)

    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=username, count=200)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=username, count=200, max_id=oldest)
        # save most recent tweets
        alltweets.extend(new_tweets)
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    # transform the tweepy tweets into a 2D array that will populate the csv
    with open("corpus.txt", "w") as corpus:
        for tweet in alltweets:
            corpus.write("\n".join(tweet.txt))



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Pass the username as arg")
    username = sys.argv[1]
    main(username)
