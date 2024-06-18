import requests
import pytube
import subprocess
import os
import re

class Track:
    """Constructs a Track object which can be downloaded"""
    def __init__(self, access_token: str, title: str, artists: str, yt: str, spotify: str, art_path: str):
        self.title = title
        self.artists = artists
        self.yt = yt
        self.spotify = spotify
        self.art_path = art_path
        self.art_url = None

        if spotify != "": 
            self.get_spotify_metadata(access_token)

            # Ensure that precedence is given to the user defined title, artist, and artwork
            if title != "": self.track_title = title
            if artists != "": self.track_artists = artists
            if art_path != "": self.track_art_path = art_path

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
            self.track_title= spotify_response.json()["name"]
            self.track_artists = ", ".join([artist["name"] for artist in spotify_response.json()["artists"]])
            self.track_artwork_url = spotify_response.json()["album"]["images"][0]["url"]
        
        return spotify_response.status_code
    
    """Downloads the YouTube audio, Spotify image (if applicable), and splices it into an mp3 file"""
    def download(self, root_path: str) -> str:
        # Download video audio using pytube
        pytube.YouTube(self.yt_link).streams.filter(only_audio=True, adaptive=True).get_by_itag(251).download(filename="intermediate.webm")

        # Download image data from spotify (if not overridden by user artwork path)
        if self.track_artwork_url is not None and self.track_art_path == "":
            artwork = requests.get(self.track_artwork_url)
            with open("cover.jpg", "bw") as artwork_file:
                artwork_file.write(artwork.content)

        # Splice image, audio, artists, and title together
        subprocess.run([
            "ffmpeg",
            "-loglevel", "quiet", 
            "-i", "intermediate.webm",
            "intermediate1.mp3",
            "&&",
            "ffmpeg",
            "-loglevel", "quiet", 
            "-i", "intermediate1.mp3",
            "-i", f"{self.track_art_path if self.track_art_path != "" else "cover.jpg"}",
            "-c", "copy",
            "-map", "0",
            "-map", "1",
            "-metadata", f"artist={self.track_artists}", 
            "-metadata", f"title={self.track_title}",
            "intermediate.mp3"
        ], shell=True)

        # Clean up intermediate files
        os.remove("intermediate.webm")
        os.remove("intermediate1.mp3")
        try: 
            os.rename("intermediate.mp3", os.path.join(root_path, f"{re.sub(r"[,:]", "", self.track_title)}.mp3")) # Sanitize file name so that it can exist
        except FileExistsError: print(f"File \"{self.track_title}.mp3\" already exists!")

        return f"{self.track_title}.mp3"