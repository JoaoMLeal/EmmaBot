import tweepy
import secret


def main():
    # Twitter authentication
    auth = tweepy.OAuthHandler(secret.TWITTER_CLIENT, secret.TWITTER_SECRET)
    auth.set_access_token(secret.TWITTER_ACCESS, secret.TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)


    # Open and read corpus
    #corpus = open("simple-corpus.txt", "r")
    #word_lines = corpus.readlines()
    #corpus.close()

    # Create word map
    #word_map = create_word_map(word_lines)
    #tweet_array = gen_message(word_map)
    #tweet = ' '.join(tweet_array)



    # Try to tweet
    try:
        print("Tweet")
        #api.update_status(tweet)
    except tweepy.TweepError:
        print("Could not tweet")


if __name__ == '__main__':
    main()


