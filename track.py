import requests
import pytube
import subprocess
import os
import re

from token_validator import *

class Track:
    """Constructs a Track object which can be downloaded"""
    def __init__(self, title: str, artists: str, yt: str, spotify: str, album: str, art_path: str, art_url: str = ""):
        self.title = title
        self.artists = artists
        self.yt = yt
        self.spotify = spotify
        self.album = album
        self.art_path = art_path
        self.art_url = art_url

        if spotify != "" and (self.title == "" or self.artists == "" or self.album == "" or self.art_url == ""):
            access_token = get_access_token()
            if access_token is not None:
                self.get_spotify_metadata(access_token)

                # Ensure that precedence is given to the user defined title, artist, album, and artwork
                if title != "": self.title = title
                if artists != "": self.artists = artists
                if album != "": self.album = album
                if art_path != "": self.art_path = art_path
    
    """
    Returns true if the track is valid.
    For a track to be valid, it must have a YouTube link and a title OR a Spotify link.
    In addition, the YouTube link must point to a valid video, and if the Spotify link is provided, it must point to a valid track.
    Album, Artwork Path, and Artists are optional and thus do not count towards the validity of the track.
    """
    def valid(self):
        # Check YouTube Link
        if self.yt.startswith("https://www.youtube.com/watch?v="):
            response = requests.get(self.yt)
            if "video isn't available" in response.text: return False
        else:
            return False

        # Check Spotify Link
        if self.spotify != "": # Could be empty
            if self.spotify.startswith("https://open.spotify.com/track/"):
                response = requests.get(self.spotify)
                if "Page not found" in response.text: return False
            else:
                return False

        if self.spotify == "" and self.title == "":
            return False

        return True

    """Returns a string representation of the track for debugging purposes"""
    def __str__(self) -> str:
        return f"Title={self.title}, Artists={self.artists}, Yt={self.yt}, Spotify={self.spotify}, Album={self.album}, Art Path={self.art_path}"

    """Requests metadata about the track through the Spotify API, returns the status code of the response"""
    def get_spotify_metadata(self, access_token: str) -> int:
        # Get the track ID from the Spotify link
        spotify_link_list = self.spotify.split("/")
        spotify_track_id = spotify_link_list[spotify_link_list.index("track")+1]

        # Send the Spotify API Request
        api_url = f"https://api.spotify.com/v1/tracks/{spotify_track_id}"
        spotify_response = requests.get(api_url, headers={"Authorization" : f"Bearer {access_token}"})

        # Assign data from the response to title, artist, and artwork fields
        if spotify_response.status_code == 200: 
            self.title = spotify_response.json()["name"]
            self.artists = ", ".join([artist["name"] for artist in spotify_response.json()["artists"]])
            self.art_url = spotify_response.json()["album"]["images"][0]["url"]
            self.album = spotify_response.json()["album"]["name"]
        
        return spotify_response.status_code
    
    """Downloads the YouTube audio, Spotify image (if applicable), and splices it into an mp3 file"""
    def download(self, root_path: str) -> str:
        # Download video audio using pytube
        pytube.YouTube(self.yt).streams.get_audio_only(subtype="webm").download(filename="intermediate.webm")
        # pytube.YouTube(self.yt).streams.filter(only_audio=True, adaptive=True).get_by_itag(251).download(filename="intermediate.webm")

        # Download image data from spotify (if not overridden by user artwork path)
        if self.art_url != "" and self.art_path == "":
            artwork = requests.get(self.art_url)
            with open("cover.jpg", "bw") as artwork_file:
                artwork_file.write(artwork.content)

        artwork_file = None
        if os.path.isfile(self.art_path): artwork_file = self.art_path
        elif os.path.isfile("cover.jpg"): artwork_file = "cover.jpg"

        commands = ["ffmpeg", "-loglevel", "quiet", "-i", "intermediate.webm", "intermediate1.mp3", "&&", "ffmpeg", "-loglevel", "quiet", "-i", "intermediate1.mp3"]
        if artwork_file is not None:
            commands += ["-i", f'{artwork_file}', "-c", "copy", "-map", "0", "-map", "1"]
        commands += ["-metadata", f'artist={self.artists}', "-metadata", f'title={self.title}', "-metadata", f"album={self.album}", "intermediate.mp3"]

        # Splice image, audio, artists, and title together
        subprocess.run(commands, shell=True)

        # Clean up intermediate files
        os.remove("intermediate.webm")
        os.remove("intermediate1.mp3")
        try: 
            os.rename("intermediate.mp3", os.path.join(root_path, f"{re.sub(r"[,:]", "", self.title)}.mp3")) # Sanitize file name so that it can exist
        except FileExistsError: print(f"File \"{self.title}.mp3\" already exists!")