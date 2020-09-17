# importing the requests library
import requests
import numpy as np
import pandas as pd
import json
import configparser
import sys

#Example run:python dataCollector.py id1,id2,id3...,id50
#can only accept a maximum of 50 ids
#google doc pages are 45 lines long 
class dataCollector:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('secret.ini')
        #grab authentication
        self.authCode = config['DEFAULT']['auth']
        #increment filename
        self.increment = config['DEFAULT']['increment']
        config['DEFAULT']['increment'] = str(int(self.increment)+1)
        with open('secret.ini', 'w') as configfile:
            config.write(configfile)

    def APICall(self):
        def cleaner():
            data = input("Enter ids")
            data = data.replace("spotify:track:", ",")
            ids = data[1:]
            # print(data)
            return ids
        # songs to look
        ids = cleaner()
        # api-endpoint
        URL = "https://api.spotify.com/v1/audio-features?ids="+ids
        # auth given here
        auth = "Bearer " + self.authCode
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'Authorization': auth}
        # sending get request and saving the response as response object
        r = requests.get(url=URL, headers=PARAMS)
        # extracting data in json format
        data = r.json()
        # check if the request is not an error
        if "audio_features" in data:
            data = data["audio_features"]
            df = pd.read_json(json.dumps(data))
            # remove columns
            df = df.drop(columns=['track_href', 'type', 'uri', 'analysis_url'])
            # reorder columns
            df = df.reindex(columns=['id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                                     'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
            result = df
            # Merging with old data
            # oldData = pd.read_csv("newCSV.csv")
            # frames = [data,oldData]
            # result = pd.concat(frames, sort =False)

            # Get name of song
            URL = "https://api.spotify.com/v1/tracks?ids="+ids
            r = requests.get(url=URL, headers=PARAMS)
            data = r.json()
            data = data["tracks"]
            df = pd.read_json(json.dumps(data))
            # grab name column
            name = df.pop("name")
            pop = df.pop("popularity")
            #insert name column
            result.insert(1, "name", name)
            result.insert(2,"popularity",pop)
            print(result)
            result.to_csv("data/SpotifyData"+str(self.increment)+".csv")
        else:
            print(data)


Object = dataCollector()
Object.APICall()
