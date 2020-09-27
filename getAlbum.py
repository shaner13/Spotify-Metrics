#get the albumID for the album you wish to analyse

import sys

import spotipy
import spotipy.util as util

username = sys.argv[1]
token = util.prompt_for_user_token(username,
                                       scope = 'user-read-recently-played playlist-modify-public user-read-private user-top-read',
                                       client_id='xxxxxxx',
                                       client_secret='xxxxxxx',
                                       redirect_uri='http://google.com/')
sp = spotipy.Spotify(auth=token)
sp.trace = False


artists = []
albums = []

namesearch = input("please enter an artist to search for\n")

results = sp.search(q='artist:' + namesearch, type='artist', limit=1)
for i in results['artists']['items']:
    print(i['name'])
    print(i['id'])
    print()
    artists.append(i['id'])
    
    
for artist in artists:
    results = sp.artist_albums(artist, album_type='album')
    for album in results['items']:
        albums.extend(results['items'])
    unique = []  # skip duplicate albums
    names = [] #for ids
    for album in albums:
        if album['id'] in names:
            continue
        else:
            names.append(album['id'])
            unique.append(album)

for album in unique:
    print(album['name'])
    print(album['id'])
    print()


        
