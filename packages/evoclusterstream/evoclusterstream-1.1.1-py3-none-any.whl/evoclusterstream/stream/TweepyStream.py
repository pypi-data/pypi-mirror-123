#From the paper:
#Evolutionary Clustering and Community Detection Algorithms for Social Media Health Surveillance
#Heba Elgazzar, Kyle Spurlock, Tanner Bogart
#2020

#This collection app includes preprocessing that masks the identity of the collected users.
#Twitter API credentials may also not be disclosed based on Twitter Developer terms & conditions.

import numpy as np
#Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 0.1038/s41586-020-2649-2. (Publisher link).
import pandas as pd
#McKinney, W. (2010, June). Data structures for statistical computing in Python. Proceedings of the 9th Python in Science Conference, 445, 51-56. doi:10.25080/majora-92bf1922-00a.
import matplotlib.pyplot as plt
#Hunter, J. D. (2007). Matplotlib: a 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95. doi:10.1109/mcse.2007.55.
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import LabelEncoder
#Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., . . . Duchesnay, E. (2011). Scikit-learn: machine learning in python (M. Braun, Ed.). The Journal of Machine Learning Research, 12, 2825-2830. Retrieved November 16, 2020, from jmlr.org.
import community as community_louvain
#Aynaud, T. (2020). python-louvain x.y: Louvain algorithm for community detection. GitHub. https://github.com/taynaud/python-louvain.
import networkx as nx
#Hagberg, A., Swart, P., & S Chult, D. (2008, August). Exploring network structure, dynamics, and function using networkx. Proceedings of the 7th Python in Science Conference, 11-16. Retrieved November 16, 2020, from www.osti.gov.
import tweepy
#Roesslein, J. (2009). Tweepy documentation. Retrieved November 16, 2020, from https://docs.tweepy.org/en/v3.5.0/
import pkg_resources

#Requires Twitter API keys
#Retrieve from here https://developer.twitter.com
consumer_key = ''
consumer_secret_key = ''
access_token = ''
access_token_secret = ''
###############################################################################

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)

user_list = [] #Lists to hold various user characteristics, 
city_list = [] #later to be included within csv file.
state_list = []
lat_list = []
long_list = []
time_list = []

seen_users = [] #Ensuring the same user is not being picked up multiple times.

try:
    data = pkg_resources.resource_stream(__name__, 'data/uscities.csv')
    uscities = pd.read_csv(data).iloc[:,[0,3,6,7]]
except FileNotFoundError as e:
    print(e)
    print("Could not include uscities.csv for TweepyStream module.")

#(2020). United States Cities Database. SimpleMaps. https://simplemaps.com/data/us-cities.

###############################################################################

def stream_tweets(search_term, n_iter = 1000):
    counter = 0 # counter to keep track of each iteration
    for tweet in tweepy.Cursor(api.search, q='\"{}\" -filter:retweets'.format(search_term), count=10, lang='en').items():
            if counter == n_iter:
                break
            
            else:
                if (tweet.user.location and (tweet.user.id_str not in seen_users)
                    and 40 < tweet.user.followers_count < 10000):
                    if (location_verify(tweet.user.location, uscities)): #If user's location is enabled and verified
                        print('Found')
                        loc = tweet.user.location
                        loc = location_change(loc, uscities) #Perform conversion of user location using uscities database.
                        seen_users.append(tweet.user.id_str)
                        user_list.append(tweet.user.id_str)
                        city_list.append(loc[0])
                        state_list.append(loc[1])
                        lat_list.append(loc[2])
                        long_list.append(loc[3])
                        time_list.append(tweet.created_at)
                        
                        counter+=1
    return 1

def location_verify(location, uscities): #Verifies that the location for the user actually exists
    for index, city in uscities['city'].iteritems():
        if location.find(city) != -1:
            return True
    return False
            

def location_change(location, uscities): #Expands verified location to include state and coordinate elements
    for index, city in uscities['city'].iteritems():
        if location.find(city) != -1:
            loc_line = [str(uscities['city'][index]), str(uscities['state_name'][index]), str(uscities['lat'][index]), str(uscities['lng'][index])]
            return loc_line
        
def full_preprocess(df):
    lbe = LabelEncoder()

    df['User'] = lbe.fit_transform(df['User'])
    
    T = df['Timestamp'].to_list() #Take the timestamp column again and turn it into a list
    t = [] #List to hold time converted to seconds
    
    for i in T: #For item in the timestamps
        i = str(i)
        year, daytime = i.split(' ') #Split the year/month from the time of day
        hour, minute, sec = daytime.split(':') #Split the time of day into hours, minutes, and seconds
        time = int(minute)*60+int(sec) #Change the time to seconds, not using hours because it won't matter
        t.append(time) #Add the converted time in seconds to the t list
        
    lbe = LabelEncoder() #LabelEncoder class object
    t = lbe.fit_transform(t) #Encode the time in second values 
    
    df['Timestamp'] = t #Replace the timestamps of our data with the new encoded values
    
    df = (df.sort_values(by=['Timestamp'], ascending = True)).values #Sort these data points by the smallest time to the longest time
    
    df = pd.DataFrame(df, columns=['ID','City','State','Lat','Long','Time'])
    
    df.to_csv('twitter_dataset_new.csv', index=False)