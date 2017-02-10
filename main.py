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
            option = int( input("1. Tweet something \n" +   
                              "2. See last n tweets of a someone (possibly a friend)\n"+ 
                                 "3. Delete some tweets\n"+ 
                                 "4. View own tweets\n"+
                                 "5. View your retweeted tweets\n"+
                                 "6. Follow or unfollow a user\n"+
                                 "7. Check stats (own, or from a friend)\n"+
                                 "8. Check or send direct message\n"+
                                 "9. Check trends\n"+
                                 "10. Exit\n") )

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
    option = input("Would you like to search with\n"+ 
                   " a. Name\n"+                        
                   " b. From your list of friend\n"+        
                   " c. Go back, I pressed this option by mistake\n")

    if(option is 'a' or again==1):
        user = input("Name of the user?\n")
        n = int(input("How many tweets do you want to see?\n"))
        try:
            tweets = api.user_timeline(screen_name = user,count=n)
            for tweet in tweets:
                print(tweet.text)
        except:
            print("Wrong username, do you want to try again? (y/n)")
            tryAgain = input()
            if(tryAgain=="yes" or tryAgain=='y'):
                searchTweets(api,user,name)
    elif(option is 'b'):
        print("List of friends")
        i = 0
        for friend in api.friends():
            print(str(i) + ". " + friend.screen_name)
            i+=1
        index = int(input("Input number of selected friend\n"))
        n = int(input("How many tweets do you wish to see?\n"))
        i = 0
        name=''
        for friend in api.friends():
            if(i==index):
               name=friend.screen_name 
            i+=1
        searchTweets(api,name,n)

    elif(option is 'c'):
        print("Going back, try to not miss this time ;) ")
        print()
    else:
        print("Uh oh, invalid option")


def searchTweets(api,name="",n=0):
    try:
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
    #api.destroy_status(status.id)

def viewOwnTweets(api):
    n = int(input("How many tweets would you like to see?\n"))
    public_tweets = api.home_timeline(count=n)
    i = 1
    for tweet in public_tweets:
        print(str(i) + ". " + tweet.text)
        i+=1


def viewOwnRetweets(api):
    n = int(input("How many retweets would you like to see?\n"))
    public_retweets = api.retweets_of_me(count=n)
    i = 1
    for tweet in public_retweets:
        print(str(i) + ". " + tweet.text)
        i+=1


def checkStats(api):

    name = input("Name of the account that you want stats from\n")
    try:
        user = api.get_user(name)

        print('Followers: ' + str(user.followers_count))

        print('Tweets: ' + str(user.statuses_count))

        print('Likes: ' + str(user.favourites_count))
    
        print('Friends: ' + str(user.friends_count))

        print('Appears on ' + str(user.listed_count) + ' lists')

        print("\n\n")

    except:
        print("uh oh, incorrect name")
        option = input("do you want to try again? y/n\n")
        if option=='y':
            checkStats(api)


def checkSentMessage(api):

    option = int(input( "Would you like to \n"+ 
                        "1. Check your own DM's?\n"+
                        "2. Send a DM?\n")
                )

    if(option==1):

        n = int( input("How many messages would you like to check?\n") )
        messages = api.direct_messages(count=n)
        for message in messages:
            print(message)
    elif(option==2):
        option= int( input( "Would you like to send a DM to\n"+
                            "1. Someone from your follower list\n"+
                            "2. Other\n") )
        if(option==1):
            i = 0
            for friend in api.friends():
                print(str(i) + ". " + friend.screen_name)
                i+=1
            index = int(input("Input number of selected friend\n"))
            i = 0
            name=''
            for friend in api.friends():
                if(i==index):
                   name=friend.screen_name 
                i+=1
            message = input("Type now the message\n")

            sendMessage(api, name, message)

        elif(option==2):
            name=input("Say exact name of account to send the DM to\n")
            message = input("Type message\n")     

            sendMessage(api,name,message)

        else:
            print("Invalid number, going back")
        
def sendMessage(api, name, message):
    try:
        api.send_direct_message(user=name,text=message)
        print("Message sent!")
    except:
        print("Uh oh, something didnt go as planned")


def checkCurrentTrends(api):
    #TODO: check trends in a specific place
    trends = api.trends_available()


def followUnfollow(api):
    option = int(input( "Would your like to\n"+
                        "1. Follow someone\n"+
                        "2. Unfollow someone\n"))
    if(option==1):
        name=input("Say exact name of person to follow\n")
        try:
            api.create_friendship(name)
            print("User followed!")
        except:
            print("oops, there was some error")
    elif(option==2):
        print("Choose who would you like to unfollow")
        i = 1
        for friend in api.friends():
            print(str(i) + ". " + friend.screen_name)
            i+=1

        n=int(input())
        i = 0
        name=''
        for friend in api.friends():
            print(friend.screen_name)
            if(i+1==n):
               name=friend.screen_name 
            i+=1   
        print(name)
        try:
            api.destroy_friendship(name)
            print("User unfollowed")
        except:
            print("Oops, there was some error")

if __name__ == "__main__":
    Main()
