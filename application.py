from PyQt6.QtWidgets import *

import os

from manager import Manager
from ui import *
from track import Track

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
        self.open_playlist_menu_dialog = OpenPlaylistMenuDialog(self.manager.get_playlists(), self.open_playlist, self.delete_playlist)

        self.track_new = False

    def run(self):
        self.gui.show()
        self.app.exec()

    def open_playlist_menu(self):
        self.open_playlist_menu_dialog.load_playlists(self.manager.get_playlists())
        self.open_playlist_menu_dialog.exec()

    def open_playlist(self, name: str):
        print(f"Opening playlist: {name}")
        self.manager.open_playlist(name)
        self.gui.current_playlist_label.setText(f"Current Playlist: {self.manager.current_playlist}")
        self.load_sql_table()

    def load_sql_table(self):
        self.gui.table_model.setTable(self.manager.current_playlist)
        self.gui.table_model.select()
        self.gui.table.resizeColumnsToContents()
        self.gui.table.hideColumn(2)
        self.gui.table.hideColumn(3)
        self.gui.table.hideColumn(4)
        self.gui.table.hideColumn(5)


    def delete_playlist(self, name: str):
        print(f"Deleting playlist: {name}")
        self.manager.delete_playlist(name)
        self.open_playlist_menu_dialog.load_playlists(self.manager.get_playlists())
        if self.manager.current_playlist == name:
            self.manager.current_playlist = None;
            self.gui.current_playlist_label.setText(f"Current Playlist: {self.manager.current_playlist}")

    def new_playlist_menu(self):
        self.new_playlist_menu_dialog.exec()

    def new_playlist(self, name: str, path: str) -> bool:
        if not self.manager.playlist_exists(name) and os.path.isdir(path):
            print(f"Making new playlist {name}, at {path}")
            self.manager.new_playlist(name)
            return True 
        else:
            print("A playlist with that name already exists or the directory is invalid")
            return False 

    def sync_playlists(self):
        pass

    def open_track(self, name: str):
        self.gui.data_box.setEnabled(True)
        self.manager.current_track = name

    def close_track(self):
        self.gui.data_box.setEnabled(False)

    def new_track(self):
        self.gui.data_box.setEnabled(True)
        self.track_new = True

    def save_track(self):
        title = self.gui.track_title_input.text()
        artists = self.gui.track_artists_input.text()
        yt = self.gui.youtube_link_input.text()
        spotify = self.gui.spotify_link_input.text()
        art_path = ""

        track = Track("", title, artists, yt, spotify, art_path)

        if self.track_new:
            self.manager.add_track(track)
            print("saved")
        else:
            return
        
        self.load_sql_table()

    def delete_track(self):
        pass

    def browse_image(self):
        pass

    def select_track(self):
        pass