import tweepy
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import collections
import time
import csv
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster
countryName = []
cn_a2_code = []
longi = []
lati = []
frequency = []

#empty map
# world_map= folium.Map(tiles="cartodbpositron")
# marker_cluster = MarkerCluster().add_to(world_map)
# #for each coordinate, create circlemarker of user percent
# for i in range(len(df)):
#         lat = df.iloc[i]['Latitude']
#         lon = df.iloc[i]['Longitude']
#         radius=5
#         popup_text = """Country : {}<br>
#                     %of Users : {}<br>"""
#         popup_text = popup_text.format(df.iloc[i]['Country'],
#                                    df.iloc[i]['User_Percent']
#                                    )
#         folium.CircleMarker(location = [lat, lon], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
# #show the map
# world_map

def create_dataframe():
	# dict = {'countryName': countryName, 'cn_a2_code': cn_a2_code, 'lati': lati, 'longi': longi}  
	# df = pd.DataFrame(dict)
	# df.sort_values("cn_a2_code", axis = 0, ascending = True,inplace = True, na_position ='last')
	# # count = df.groupby(['countryName']).count()
	# print(df)
	counter=collections.Counter(cn_a2_code)
	od = collections.OrderedDict(sorted(counter.items()))
	print(od)

def fill_loc_arr():
	for c in countryName:
		geolocate(c)

geolocator = Nominatim()
def geolocate(country):
    try:
        # Geolocate the center of the country
        loc = geolocator.geocode(country)
        # And return latitude and longitude
        l = loc.latitude
        l1 = loc.longitude
        lati.append(str(l))
        longi.append(str(l1))
    except:
        # Return missing value
        lati.append('nan')
        longi.append('nan')

def get_continent(col):
    try:
        a =  country_name_to_country_alpha2(col)
        cn_a2_code.append(a)
        countryName.append(col)
        geolocate(a)
    except:
        cn = 'Unknown'



# def create_plot(loc_list):
# 	train = pd.read_csv('tweet.csv',error_bad_lines = False)


def saving_csv(tweet):
	loc = str(tweet.user.location)
	get_continent(loc)
	if len(countryName)>5:
		create_dataframe()



# def write_csv(dict):
# 	with open('tweet.csv', "a", encoding="utf-8") as file:
# 		for key in dict.keys():
# 			file.write("%s, %s\n" % (key, dict[key]))
# 	file.close()

	
	

consumer_key = 'hQPh8DurzbBLNfudONerRPM9r'
consumer_secret = 'dRemA54f0FiNG6ra4iULV5jzBSCppcWAkQ25OKcnjG11PUVwWP'
access_token = '1264432304295944192-ADLGhXgrV7BTqn1N0cgtWKgxg1d4F6'
access_token_secret = 'eBnp64F7HDXUf0qqLbAynKaloUlyzmT9bEbepbJjFpCgJ'
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        saving_csv(tweet)

    def on_error(self, status):
        print("Error detected")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)

stream.filter(track=["covid"], languages=["en"])



