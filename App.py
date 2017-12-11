from __future__ import print_function  # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import os
import datetime
import os

# http://everynoise.com/everynoise1d.cgi?scope=all
genre_list = ['pop', 'rap', 'latin', '"hip hop"', '"trap music"']

'''
{
    "track_href": "https://api.spotify.com/v1/tracks/1YMBg7rOjxzbya0fPOYfNX", 
    "analysis_url": "https://api.spotify.com/v1/audio-analysis/1YMBg7rOjxzbya0fPOYfNX", 
    "energy": 0.764, 
    "liveness": 0.152, 
    "tempo": 104.988, 
    "speechiness": 0.0391, 
    "uri": "spotify:track:1YMBg7rOjxzbya0fPOYfNX", 
    "acousticness": 0.512, 
    "instrumentalness": 1.14e-06, 
    "time_signature": 4, 
    "danceability": 0.78, 
    "key": 8, 
    "duration_ms": 198286, 
    "loudness": -4.098, 
    "valence": 0.545, 
    "type": "audio_features", 
    "id": "1YMBg7rOjxzbya0fPOYfNX", 
    "mode": 1
}

'''
headers = ['id', 'energy', 'liveness', 'tempo', 'speechiness',
           'acousticness', 'instrumentalness', 'time_signature', 'danceability',
           'key', 'duration_ms', 'loudness', 'valence']

# current time
curTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dir_path = r"/Users/Nit/Documents/Python"
training_path = dir_path + "dataSet.csv"
testing_path = dir_path + "artistFeatures.csv"

# This number tracks will be (factor + 1) * 50
number_of_tracks_factor = 20

# auth
client_credentials_manager = SpotifyClientCredentials(client_id='6d7a082b13e64022ae30c0cf1bf1a679',
                                                      client_secret='e84f8dde423f4a67843108b0e03c789c')

# spotify client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False


def resultParser(json_obj):
    values = json.loads(json.dumps(json_obj))
    line = ""
    comma = ""
    try:
        for col in headers:
            line += comma + str(values[col])
            comma = ","
        print(line)
    except:
        pass
    return line
    # for i in values:
    #    print (i)


def writeToFile(lists, dir):
    with open(dir, 'a') as f:
        for newLine in lists:
            f.write(newLine + '\n')


def getTrackIds(genre, offset):
    dir = training_path
    for index in range(offset):
        results = sp.search(q='genre:' + genre, limit=50, offset=index * 50)
        tids = []
        for i, t in enumerate(results['tracks']['items']):
            print(' ', i, t['name'])
            tids.append(t['uri'])
        getFeatures(tids, dir)


def getFeatures(tids, dir):
    start = time.time()
    features = sp.audio_features(tids)
    delta = time.time() - start
    print("[latency] " + str(delta))
    lists = []
    for feature in features:
        newLine = resultParser(feature)
        lists.append(newLine)
        # print(json.dumps(feature, indent=4))
        # print()
        # analysis = sp._get(feature['analysis_url'])
        # print(json.dumps(analysis, indent=4))
    writeToFile(lists, dir)


def getTrackIds_artist(urn):
    # urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
    tids = []
    track = sp.artist_top_tracks(urn)
    for t in track['tracks']:
        tids.append(t['uri'])

    try:
        os.remove(testing_path)
    except OSError:
        pass
    headerLine = ",".join(headers)
    if not os.path.exists(testing_path):
        with open(testing_path, 'w') as f:
            f.write(headerLine + '\n')

    getFeatures(tids, testing_path)

def getArtistID(artist):
    result = sp.search(artist, type='artist')
    return result['artists']['items'][0]['uri']

def getArtist(tid):
    result = sp.track(tid)
    return result['artists'][0]['name']

def generateTopTracks(artist):
    artistID = getArtistID(artist)
    getTrackIds_artist(artistID)



if __name__ == '__main__':
    # test out one example
    # getTrackIds('pop', 1)


    # create file
    headerLine = ",".join(headers)

    try:
        os.remove(training_path)
    except OSError:
        pass
    # create the file if doesn not exist
    if not os.path.exists(training_path):
        with open(training_path, 'w') as f:
            f.write(headerLine + '\n')

    # you can use for loop to get a lot more data
    for genre in genre_list:
        print("getting tracks on " + genre)
        getTrackIds(genre, number_of_tracks_factor)

'''
for feature in features:
    print(json.dumps(feature, indent=4))
    print()
    analysis = sp._get(feature['analysis_url'])
    print(json.dumps(analysis, indent=4))
    print()
print ("features retrieved in %.2f seconds" % (delta,))
'''
