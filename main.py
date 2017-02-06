"""
Author: Fernando Collado
Github: ForFer
"""

# Bot intended to be used from the terminal, as fast access to some twitter
# resources. 

# If you want to make it work, just create your own OATH keys from the
# twitter dev website, and past them on their variables


import tweepy


def Main():

    consumer_key = ''
    consumer_secret = ''

    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    run = True
    while(run):
        print("Welcome to twitter bot, what would you like to do")
        option = -1
        while(option>10 or option<1):
            option = int( input(  \
                "\
 1. Tweet something \n  \
 2. See last n tweets of a someone (possibly a friend)\n \
 3. Delete some tweets\n \
 4. View own tweets\n \
 5. View own retweets\n \
 6. Follow or unfollow a user\n \
 7. Check stats (own, or from a friend)\n \
 8. Check or send direct message\n \
 9. Check trends\n \
 10. Exit\n") )

        if(option==1):
            tweet(api)
        elif(option==2):
            getTweets(api)
        elif(option==3):
            deleteTweet(api)
        elif(option==4):
            viewOwnTweets(api)
        elif(option==5):
            viewOwnRetweets(api)
        elif(option==6):
            followUnfollow(api)
        elif(option==7):
            checkStats(api)
        elif(option==8):
            checkSentMessage(api)
        elif(option==9):
            checkTrends(api)
        elif(option==10):
            run=False
        else:
            print("uh oh, something went wrong, exitting program")
            run=False
#Here ends the main

def tweet(api):

    status = input("Enter text to tweet\n")
    api.update_status(status)   
    print("Sent")
    print()


def getTweets(api, again=0):
    option = input("Would you like to search with\n  \
                    a. Name\n                        \
                    b. From your listfriend\n        \
                    c. Go back, I pressed this option by mistake")

    if(option is 'a' or again==1):
        user = input("Name of the user?\n")
        n = input("How many tweets do you want to see?\n")
        try:
            api.user_timeline(screen_name = '_yairodriguez',count=200)
        except:
            print("Wrong username, do you want to try again? (y/n)")
            tryAgain = input()
            if(tryAgain=="yes"):
                searchTweets()
    elif(option is 'b'):
        #TODO
        #Sacar lista de amigos, y luego buscar tweets de esa persona    
        print("List of friends")
        i = 0
        for friend in user.friends():
            print(str(i) + ". " + friend.screen_name)
            i+=1
        name = input("Input number of selected friend\n")
        n = input("How many tweets do you wish to see?\n")
        searchTweets(name,n)

    elif(option is 'c'):
        print("Going back, try to not miss this time ;) ")
        print()
    else:
        print("Uh oh, invalid option")

def searchTweets(api,name="",n=-1):
    try:
        #for status in tweepy.Cursor(api.user_timeline,id='_yairodriguez').items():
            #print(status.author)
        tweets = api.user_timeline(screen_name = name,count=n)
        for tweet in tweets:
            print(tweet.text)
    except:
        print("Wrong username, do you want to try again? (y/n)")
        tryAgain = input()
        if(tryAgain=="yes"):
            getTweets(again=1)
    print("#########################################")

def deleteTweet(api):
    #TODO
    print("Delete tweets")

def viewOwnTweets(api):
    n = input("How many tweets would you like to see?\n")
    public_tweets = api.home_timeline(count=n)
    for tweet in public_tweets:
        print(tweet.text)

def viewOwnRetweets(api):
    n = input("How many retweets would you like to see?\n")
    public_retweets = api.retweets_of_me(count=n)
    for tweet in public_retweets:
        print(tweet.text)

def checkStats(api):

    """
    print(user.screen_name)
    print(user.followers_count)
    """

def checkSentMessage(api):
    option = input("Would you like to \n      \
                    1. Check your own DM's?\n \
                    2. Send a DM?\n")
    if(option==1):
        n = input("How many messages would you like to check?\n")
        messages = api.direct_messages(count=n)
        for message in messages:
            print(message)

def checkCurrentTrends(api):
    trends = api.trends_available()

if __name__ == "__main__":
    Main()
