# Spotify-Playlist-Downloader

* Uses Spotipy [Wrapper for Spotify API] to extract song titles from a playlist
* YT API gets the URLs for each track title.
* Pytube lib is used to download YT videos from the URLs. Videos are stored in a temporary buffer to save space. 


OPTION 1:
* Download Audio Stream from Pytube

OPTION 2:
* Within buffer, MoviePy lib is is used to extract audio from the video. Possible audio formats include MP3 and AAC or AC3.
* Results are stored in a folder.

Plan to deploy as a web app where user needs to give the link of the spotify playlist.

* Note that this is a form of copyright infringement and will not be used for commercial purposes.

ISSUES:
* To circumvent Quota limit on YT API, current implementation supports 1200 song downloads for every 24h
