#Get the audio features as graphs for a specific album

import sys

import spotipy
import spotipy.util as util

import matplotlib.pyplot as plt
import numpy as np

from statistics import mode

def analyse_data(features):
    
    analysis,valence,danceability,energy,instrumentalness,liveness,acousticness,mode,keySig = ([] for i in range (9))
    keySigDict = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0}
    major, minor = 0,0

    for track in features:
        valence.append(track[0]['valence'])
        danceability.append(track[0]['danceability'])
        energy.append(track[0]['energy'])
        instrumentalness.append(track[0]['instrumentalness'])
        liveness.append(track[0]['liveness'])
        acousticness.append(track[0]['acousticness'])
        keySig.append(track[0]['key'])

        #major 1 minor 0
        if track[0]['mode'] == 1:
            major +=1
        else:
            minor +=1

    for key in keySig:
        for i in range(12):
            if key == i:
               keySigDict[str(key)] += 1
    
    mode.extend([major,minor])
    analysis.extend([valence,danceability,energy,instrumentalness,liveness,acousticness,keySigDict,mode])

    return analysis

def create_graphs(features):
        
        
        plt.figure(1)
        plt.plot(features[0],'-bD', label='Valence')
        plt.plot(features[1],'-rD', label='Danceability')
        plt.plot(features[2],'-gD', label='Energy')
        plt.xlabel('track')
        plt.ylabel('value')
        plt.xticks(np.arange(0, len(features[0])+1, step=1))
        plt.yticks(np.arange(0.0, 1.0+0.1, step=0.1))
        plt.legend(loc="best")
        
        plt.figure(2)
        plt.plot(features[3],'-bD', label='Instrumentalness')
        plt.plot(features[4],'-rD', label='Liveness')
        plt.plot(features[5],'-gD', label='Acousticness')
        plt.xlabel('track')
        plt.ylabel('value')
        plt.xticks(np.arange(0, len(features[0])+1, step=1))
        plt.yticks(np.arange(0.0, 1.0+0.1, step=0.1))
        plt.legend(loc="best")
    
        keysList = list(features[6].values())
        tonal_counterparts = ['C','C♯','D','D♯','E','F','F♯','G','G♯','A','A♯','B']
        
        plt.figure(3)
        plt.bar(tonal_counterparts,keysList)
        plt.yticks(np.arange(0, int(max(keysList))+1, step=1))
        plt.ylabel('No. of tracks')
        plt.title('Key Signatures')
        
        plt.figure(4)
        plt.bar(['major','minor'],features[7])
        plt.yticks(np.arange(0, len(features[0])+1, step=1))
        plt.ylabel('No. of tracks')
        plt.title('Major and Minor tracks')
        
        plt.show()
        

username = sys.argv[1]
token = util.prompt_for_user_token(username,
                                       scope = 'user-read-recently-played playlist-modify-public user-read-private user-top-read',
                                       client_id='xxxxxxxxxxxxxxxxxxxxxxxx',
                                       client_secret='xxxxxxxxxxxxxxx',
                                       redirect_uri='http://google.com/')
sp = spotipy.Spotify(auth=token)
sp.trace = False

tracks = []
tracklist = []

albumID = input("Please enter the album ID which you wish to analyse\n")

results = sp.album_tracks(albumID)
tracks.extend(results['items'])
for track in tracks:
    tracklist.append(track)

features = []
for track in tracklist:
    feature = sp.audio_features(tracks=[track['id']])
    features.append(feature)

analysis = analyse_data(features)
create_graphs(analysis)
        
