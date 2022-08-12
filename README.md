# Spotify-Playlist-Downloader

* Uses Spotify API to extract song titles from a playlist
* Pytube lib is used to download YT videos based on the extracted song titles. Videos are stored in a temporary buffer to save space.
* Within buffer, MoviePy lib is is used to extract audio from the video. Possible audio formats include MP3 and AAC or AC3.
* Results are stored in a folder.
