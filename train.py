import numpy as np
from sklearn.cluster import KMeans
import random
import App as app

dir_path = r"/Users/Nit/Documents/Python"

def filearray(path):
    data = []
    with open(path) as f:
        line = f.readline()
        while line:
            data.append(parseline(line))
            line = f.readline()
    return np.array(data)

def parseline(string):
    string = string.replace('\n', '')
    array = string.split(',')
    return array

def training_kmeans(features):
    return KMeans(n_clusters=5, random_state=0).fit(features[1:, 1:])

def findArtists():
    # training
    training_path = dir_path + "dataSet.csv"
    training_features = filearray(training_path)
    kmeans = training_kmeans(training_features)
    training_labels = kmeans.labels_

    # testing
    testing_path = dir_path + "artistFeatures.csv"
    testing_features = filearray(testing_path)
    predicted_labels = kmeans.predict(testing_features[1:, 1:])

    track_indices = []
    for label in predicted_labels:
        indices = np.where(training_labels == label)[0]
        track_indices.append(random.choice(indices))

    # get similar artists
    similar_artists = []
    tid_array = []

    tid_array_features = filearray(training_path)
    for index in track_indices:
        tid_array.append(tid_array_features[index + 1, 0])

    for tid in tid_array:
        anArtist = app.getArtist(tid)
        similar_artists.append(anArtist)

    return similar_artists

def getArtists(input, artists):
    similar_artists = []
    for i in range(len(artists)):
        for j in range(len(similar_artists)):
            if artists[i] == similar_artists[j]:
                break
            elif artists[i] == input:
                break
        similar_artists.append(artists[i])
        if len(similar_artists) > 5:
            break
    return similar_artists
