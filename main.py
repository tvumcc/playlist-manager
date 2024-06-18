from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
import pytube

from manager import Manager
from track import Track
from ui import MainWindow
from application import Application

if __name__ == "__main__":
    app = Application()
    app.run()

    # man = Manager()
    # man.new_playlist("Test")
    # man.open_playlist("Test")
    # man.add_track(Track("", "Sage Laruto", "Koji Kondo", "https://www.youtube.com/watch?v=qEG3Iw7IasI", "", "art/windwaker.png"))
    # man.add_track(Track("", "Sage Laruto 2", "Koji Kondo", "https://www.youtube.com/watch?v=qEG3Iw7IasI", "", "art/windwaker.png"))
    
    # print(man.get_playlists())
    # man.print_out_tracks()

    # pytube.YouTube("https://www.youtube.com/watch?v=kK81m-A3qpU").streams.get_audio_only(subtype="webm").download(filename="intermediate.webm")