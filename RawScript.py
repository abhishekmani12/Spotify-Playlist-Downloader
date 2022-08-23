# -*- coding: utf-8 -*-



#SPOTIPY - FOR EXTRACTING SONG TITLES VIA SPOTIFY API

!pip install spotipy

#wrapper for spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd

#defining scope of API Access
scope_='playlist-read-collaborative'

#Auth with c_id and c_secret, URI Redirect-Local Host for Auth
#Enter c_id and c_secret credentials
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='xxxxxxxxxxxxxxxxxx', client_secret='yyyyyyyyyyyyyyyyyyyy', redirect_uri='http://localhost:9000', scope=scope_))

#User's Username ID. Can be accessed through spotify desktop
print("Enter Spotify Username ID")
spid=input()
username=spid#spotify.me()['id']--for my own account

#Fetching Playlists of the user
TrackList=[]
playlists=spotify.user_playlists(username)

len(playlists['items'])

totaltracks=0
countlist=[]
counter=0
for i in playlists['items']: #iterating through playlists

        print(counter,".",i['name']) #Playlist Name
        
        print("Total Songs: ",i['tracks']['total']) #total count of songs
        counter+=1
        
        countlist.append(i['tracks']['total']) #saving counts
        totaltracks+=i['tracks']['total']

        
        print(' ')

print('total songs=',totaltracks)

print("Enter the index of playlist you would like to download:")
idx=input()

#To save tracks of a playlist
track_info=[]

def trackname(result):
    for i, item in enumerate(result['items']):
        
        track = item['track']
        
        title=track['artists'][0]['name']+' '+track['name'] #combining Artiste and Song Name
        
        #print(track['artists'][0]['name'], track['name'])
        
        track_info.append(title)

for playlist in playlists['items']:
        #if playlist['owner']['id'] == username:
        
        # fetching the next tracks in the playlist 
            results = spotify.playlist(playlist['id'], fields="tracks,next")
            
            tracks = results['tracks']
            trackname(tracks)

            
            while tracks['next']:
                tracks = spotify.next(tracks)
                trackname(tracks)



totaltracks=len(track_info)

#calculating the starting and ending index of the set of songs belonging to a playlist

def extractorP(playlistchoice):
    j=playlistchoice
    offset=0

    for j in countlist[playlistchoice:]:
    
        offset+=j
       
    startOfP=totaltracks-offset
    endOfP=totaltracks-(offset-countlist[playlistchoice])

    desiredP=track_info[startOfP:endOfP]
    
    return desiredP

TRACKS=extractorP(idx) #passing idx to function

TRACKS

#EXTRACT URL OF TRACKS THROUGH YOUTUBE API with query:

! pip install google-api-python-client

import googleapiclient.discovery

api_name='youtube'
api_version='v3'

def switcher(api_key):
    yt=googleapiclient.discovery.build( api_name, api_version, developerKey=api_key)

#API KEY SWITCHING:


URLlist=[]    
count=0

#Enter API key for yt data V3 API through gcloud
apikeyList=['xxxxxxxxxxxxxxxx','yyyyyyyyyyyyyyyy'] # needs 12 api keys to fetch 1200 urls at max per day
apiIndex=0
yt=googleapiclient.discovery.build( api_name, api_version, developerKey=apikeyList[apiIndex])


limit=[99, 198] # current limit is 300. With 12 API keys, limit will be 1200 

for Tindex in range(len(TRACKS)):    
    
    if len(limit)!=0:
        if Tindex==limit[0]:
            
            if len(limit)==1:
                print("The number of tracks has exceeded the quota. Process ended at song number: ",Tindex)
                break
            else:
                
                print("Switching api",Tindex)
                apiIndex=apiIndex+1
            
                api_key=apikeyList[apiIndex]
                yt=googleapiclient.discovery.build( api_name, api_version, developerKey=api_key)
                
        
            
                del limit[0]
                

    request=yt.search().list(
    
        part='id',
        type='video',
        q=TRACKS[Tindex],
        maxResults=1,
        fields='items(id(videoId))'
        )

    #Extracting URL from YT:
    
    response=request.execute()

    vidID=response['items'][0]['id']['videoId']

    URL="https://www.youtube.com/watch?v="+vidID
    
    URLlist.append(URL)
    
    count+=1
    #print(count)
    
print("End of Request. Total songs:",count)



URLdf=pd.DataFrame(URLlist)

URLdf.to_csv("url.csv") #saving URL list

#PYTUBE - DOWNLOADING YT VIDEOS

!pip install pytube

#URLdf=pd.read_csv('url.csv')

#URLlist=URLdf.values.tolist()

#DOWNLOADING AUDIO STREAM FROM YT VIA PYTUBE:

from pytube import YouTube

count=0

for url in URLlist:
    youtube=YouTube(url)
    
    streams=youtube.streams.filter(only_audio=True)

    stream = youtube.streams.get_by_itag(251)
    stream.download()
    count+=1
    print(count)
    
print("Download Complete!")

