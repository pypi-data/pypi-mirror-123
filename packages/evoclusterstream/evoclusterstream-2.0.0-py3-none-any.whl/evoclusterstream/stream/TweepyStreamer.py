# From the paper:
# Evolutionary Clustering and 
# Community Detection Algorithms for Social Media Health Surveillance

# Kyle Spurlock, Tanner Bogart, Heba Elgazzar
# 2020

# Twitter Streaming Class with Tweepy integration
# -----------------------------------------------
# Current configuration collects user geographical location based on tweet
# keywords.

'''
Requires Twitter API keys and tokens
Retrieve from here https://developer.twitter.com
'''

'''
Example usage:
---------------------
    search_terms = ['tweet1', 'tweet2']
    
    
    consumer_key = "your_consumer_key"
    consumer_secret_key = "your_consumer_secret_key"
    
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"
    
    Streamer = TweepyStreamer(consumer_key, consumer_secret_key, access_token,
                              access_token_secret)
    
    user info = Streamer.stream_tweets(search_terms, n_samples = 100)
'''

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import tweepy
import numpy as np
import pkg_resources

# Need this for conversion of user location
try:
    data = pkg_resources.resource_stream(__name__, 'data/uscities.csv')
    uscities = pd.read_csv(data).iloc[:,[0,3,6,7]]
except FileNotFoundError as e:
    print(e)
    print("Could not include uscities.csv for TweepyStream module.")
# (2020). United States Cities Database.
# SimpleMaps. https://simplemaps.com/data/us-cities.

def location_verify(location, uscities):
    """Performs match of user location to US Cities database """
    for index, city in uscities['city'].iteritems():
        if location.find(city) != -1:
            return True
    return False
            

def location_change(location, uscities):
    """Expands verified location to include state and coordinate elements"""
    for index, city in uscities['city'].iteritems():
        if location.find(city) != -1:
            loc_line = [str(uscities['city'][index]),
                        str(uscities['state_name'][index]),
                        str(uscities['lat'][index]),
                        str(uscities['lng'][index])]
            return loc_line
        
def full_preprocess(df):
    """Preprocesses and saves dataset as csv"""
    
    # Encoding user values for anonymity
    df['User'] = LabelEncoder().fit_transform(df['User'])
    
    T = df['Timestamp'].to_list()
    # Processing of timestamps
    for i in range(len(T)):
        timestamp = str(T[i])
        year, daytime = timestamp.split(' ')
        hour, minute, sec = daytime.split(':') 
        time = int(minute)*60+int(sec) # Convert to seconds
        T[i] = time # Replace timestamp with encoded version
        
    T = LabelEncoder().fit_transform(T) # Encode the time values
    
    df['Timestamp'] = T # Replace timestamp column with encoded values
    
    df = (df.sort_values(by=['Timestamp'], ascending = True)).values
    
    df = pd.DataFrame(df, columns=['User','City','State','Lat','Long','Time'])
    
    return df

class TweepyStreamer():
    """Class implementation for Twitter Streamer
    
        Vars:
        ---------------------
            -auth: Tweepy OAuthHandler class, authorizes API with keys.
            -api: Tweepy API class, provides access to RESTful Twitter API.
            -wait_on_rate_lim: specifies whether to sleep upon reaching max
                               stream requests.
            -wait_on_rate_lim_notify: verbose for wait_on_rate_lim
    """
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_secret,*, wait_on_rate_lim=True,
                 wait_on_rate_lim_notify=True):
        
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.auth,
                              wait_on_rate_limit=wait_on_rate_lim,
                              wait_on_rate_limit_notify=wait_on_rate_lim_notify)
        
    def stream_tweets(self, search_terms, n_samples, verbose = True):
        """Method for accessing Twitter stream API using Tweepy Cursor
        
            Args:
            ---------------------
                -search_terms: Array of keywords to search for in tweets
                -n_samples: Number of samples total to collect
                -verbose: Bool, controls console outputs
                
            Returns:
            ---------------------
                -full_list: Dataframe with user info
        """
        if verbose: print('Starting stream.')
        # List to hold various user characteristics
        full_list = []
        cols = ['User','City','State','Lat','Long','Timestamp']
        
        # List of users to ensure the same user/tweet
        # is not picked up several times
        seen_users = []
        
        # Counter to keep track of iterations
        max_itr = int(n_samples/len(search_terms))+1
        for keyword in search_terms:
            itr = 0
            for tweet in tweepy.Cursor(self.api.search,
                                       q='\"{}\" -filter:retweets'.format(keyword),
                                       count=10,
                                       lang='en').items():
                if not itr == max_itr:
                    if (tweet.user.location 
                        and (tweet.user.id_str not in seen_users)
                        and 60 < tweet.user.followers_count < 10000):
                        if (location_verify(tweet.user.location, uscities)):
                            # If user's location is enabled and verified
                            if verbose: print('Found.')
                            loc = tweet.user.location
                            # Match location with US Cities database
                            loc = location_change(loc, uscities)
                            
                            # Append all tweet information to array
                            tweet_info_list = []
                            tweet_info_list = np.append(tweet_info_list, 
                                                        tweet.user.id_str)
                            tweet_info_list = np.append(tweet_info_list, loc)
                            tweet_info_list = np.append(tweet_info_list,
                                                        tweet.created_at)
                            
                            # Append tweet info list to the full collection list
                            full_list.append(tweet_info_list)
                            itr+=1
                else:
                    break
                
        full_list = pd.DataFrame(data=full_list, columns=cols)
        full_list = full_preprocess(full_list)
        if verbose: print("Finished.")
        return full_list