"""
Author: Fernando Collado
Github: ForFer
"""

# Bot intended to be used from the terminal, as fast access to some twitter
# resources. 

# If you want to make it work, just create your own OATH keys from the
# twitter dev website, and past them on their variables

import tweepy
import configparser


def Main():
     
    access_token, consumer_key, access_token_secret, consumer_secret = get_data()
    
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

        if option==1:
            tweet(api)
        elif option==2:
            get_tweets(api)
        elif option==3:
            delete_tweet(api)
        elif option==4:
            view_own_tweets(api)
        elif option==5:
            view_own_retweets(api)
        elif option==6:
            follow_unfollow(api)
        elif option==7:
            check_stats(api)
        elif option==8:
            check_sent_message(api)
        elif option==9:
            check_trends(api)
        elif option==10:
            run=False
        else:
            print("uh oh, something went wrong, exitting program")
            run=False
#Here ends the main

def get_data():
    config = configparser.ConfigParser()
    config.read('config/oath.conf')
    return [config['data'][x] for x in config['data']]

def set_data(d1='',d2='',d3='',d4=''):
    config = configparser.ConfigParser()
    data = {}
    data['consumer_key'] = d1
    data['consumer_secret'] = d2 

    data['access_token'] = d3
    data['access_token_secret'] = d4 
    config['data'] = data
    
    with open('config/oath.conf', 'w') as conf:
        config.write(conf)


def get_user():
    return input("Name of the user?\n")

def tweet(api):
    status = input("Enter text to tweet\n")
    api.update_status(status)   
    print("Tweet sent\n\n")

def print_tweets(api,user,n):
    tweets = api.user_timeline(screen_name = user,count=n)
    for i, tweet in enumerate(tweets):
        print(str(i) + '. ' +  tweet.text)

#Maybe rethink
def try_again(error=1):
    errorMessage = ''
    if error == 0:
        errorMessage="Wrong username"
    print(errorMessage + " do you want to try again? (y/n)")
    again = input()

    if again.lower()=="yes" or again.lower()=='y':
        return True
    else:
        return False

def get_number_of(option=0):
    s = ''
    if option == 0:
        s ="How many tweets do you want to see?\n"
    elif option == 1:
        s = "How many messages would you like to check?\n"
    else:
        s = "Input number"
    return int(input(s))


def get_friend(api):
    print("List of friends")
    friendList = []
    for i, friend in enumerate(api.friends()):
        print(str(i) + ". " + friend.screen_name)
        friendList.append(friend.screen_name)
    
    index = int(input("Input number of selected friend\n"))
    try:
        return friendList[index]
    except:
        return None


def get_tweets(api, again=0):
    option = input("Would you like to search with\n"+ 
                   " a. Name\n"+                        
                   " b. From your list of friend\n"+        
                   " c. Go back, I pressed this option by mistake\n")

    if option is 'a' or again==1:
        user = get_user(api)
        n = get_number_of(0)
        try:
            print_tweets(api, user, n)
        except:
            if try_again(0):
                search_tweets(api,user,name)

    elif option is 'b':
        name = get_friend(api)
        n = get_number_of()
        search_tweets(api,name,n)

    elif option is 'c':
        print("Going back, try to not miss this time ;) ")
        print()
    else:
        print("Uh oh, invalid option")


def search_tweets(api,name="",n=0):
    
    try:
        print_tweets(api, name, n)
    except:
        if try_again(0):
            get_tweets(again=1)
    print("#########################################")


def delete_tweet(api):
    #TODO
    print("Delete tweets")
    #api.destroy_status(status.id)

def view_own_tweets(api):
    n = get_number_of(0)
    print_tweets(api, '', n)

def view_own_retweets(api):
    n = get_number_of(0)
    public_retweets = api.retweets_of_me(count=n)
    for i,tweet in enumerate(public_retweets):
        print(str(i) + ". " + tweet.text)


def check_stats(api):

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
        if try_again(0):
            check_stats(api)


def check_sent_message(api):

    option = int(input( "Would you like to \n"+ 
                        "1. Check your own DM's?\n"+
                        "2. Send a DM?\n")
                )

    if option==1:

        n =get_number_of(1) 
        messages = api.direct_messages(count=n)
        for message in messages:
            print(message)

    elif option==2:
        option= int( input( "Would you like to send a DM to\n"+
                            "1. Someone from your follower list\n"+
                            "2. Other\n") )
        if option==1:
            name = get_friend(api)
            message = input("Type now the message\n")
            sendMessage(api, name, message)

        elif option==2:
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
        print("Going back to menu")


def checkCurrentTrends(api):
    #TODO: check trends in a specific place
    trends = api.trends_available()


def follow_unfollow(api):
    option = int(input( "Would your like to\n"+
                        "1. Follow someone\n"+
                        "2. Unfollow someone\n"))
    if option==1:
        name=input("Say exact name of person to follow\n")
        try:
            api.create_friendship(name)
            print("User %s followed!" % name)
        except:
            print("Oops, there was some error")
    elif option==2:
        print("Choose who would you like to unfollow")
        name = get_friend(api)
        try:
            api.destroy_friendship(name)
            print("User %s unfollowed" % name)
        except:
            print("Oops, there was some error")

if __name__ == "__main__":
    Main()
