from PyQt6.QtWidgets import *

import os

from manager import Manager
from ui import *

class Application:
    def __init__(self):
        self.app = QApplication([])
        self.gui = MainWindow()
        self.manager = Manager()

        self.gui.open_playlist_button.clicked.connect(self.open_playlist_menu)
        self.gui.new_playlist_button.clicked.connect(self.new_playlist_menu)
        self.gui.sync_playlists_button.clicked.connect(self.sync_playlists)
        self.gui.new_track_button.clicked.connect(self.new_track)
        self.gui.track_entry_save_button.clicked.connect(self.save_track)
        self.gui.art_image_browse_button.clicked.connect(self.browse_image)

        self.new_playlist_menu_dialog = NewPlaylistMenuDialog(self.new_playlist)
        self.open_playlist_menu_dialog = OpenPlaylistMenuDialog(self.open_playlist, self.delete_playlist)

    def run(self):
        self.gui.show()
        self.app.exec()

    def open_playlist_menu(self):
        self.open_playlist_menu_dialog.exec()

    def open_playlist(self, name: str):
        print(f"Opening playlist: {name}")

    def delete_playlist(self, name: str):
        print(f"Deleting playlist: {name}")

    def new_playlist_menu(self):
        self.new_playlist_menu_dialog.exec()

    def new_playlist(self, name: str, path: str) -> bool:
        if not self.manager.playlist_exists(name) and os.path.isdir(path):
            print(f"Making new playlist {name}, at {path}")
            return True 
        else:
            print("A playlist with that name already exists or the directory is invalid")
            return False 

    def sync_playlists(self):
        pass

    def new_track(self):
        pass

    def save_track(self):
        pass

    def delete_track(self):
        pass

    def browse_image(self):
        pass

    def select_track(self):
        pass