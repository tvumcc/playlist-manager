from PyQt6.QtWidgets import *

import os

from manager import Manager
from token_validator import * 
from ui import *
from track import Track

"""Manages all the logic for the application, tying the db and ui code together"""
class Application:
    def __init__(self):
        self.app = QApplication([])
        self.gui = MainWindow()
        self.manager = Manager()

        self.gui.open_playlist_button.clicked.connect(self.open_playlist_menu)
        self.gui.new_playlist_button.clicked.connect(self.new_playlist_menu)
        self.gui.sync_playlists_button.clicked.connect(self.sync_playlist)
        self.gui.new_track_button.clicked.connect(self.new_track)
        self.gui.track_entry_save_button.clicked.connect(self.save_track)
        self.gui.track_entry_delete_button.clicked.connect(self.delete_track)
        self.gui.table.selectionModel().selectionChanged.connect(self.select_track)
        self.gui.spotify_action.triggered.connect(self.spotify_client_info_menu)

        self.new_playlist_menu_dialog = NewPlaylistMenuDialog(self.new_playlist)
        self.open_playlist_menu_dialog = OpenPlaylistMenuDialog(self.manager.get_playlists(), self.open_playlist, self.delete_playlist)
        self.spotify_client_info_dialog = SpotifyClientInfoDialog(self.store_spotify_client_info)

        self.current_playlist = None
        self.current_track = None
        self.track_new = False

    def run(self):
        self.gui.show()
        self.app.exec()

    # Playlists

    def open_playlist_menu(self):
        self.open_playlist_menu_dialog.load_playlists(self.manager.get_playlists())
        self.open_playlist_menu_dialog.exec()

    def open_playlist(self, name: str):
        self.current_playlist = name
        self.current_track = None
        self.track_new = False
        self.gui.current_playlist_label.setText(f"Current Playlist: {self.current_playlist}")
        self.gui.set_data_box_greyed_out(True)
        self.gui.clear_data_box()
        self.gui.load_sql_table(self.current_playlist)

    def delete_playlist(self, name: str):
        self.manager.delete_playlist(name)
        self.open_playlist_menu_dialog.load_playlists(self.manager.get_playlists()) # Refresh list of playlists

        # Currently selected playlist gets deleted
        if self.current_playlist == name:
            self.current_playlist = None
            self.current_track = None
            self.track_new = False
            self.gui.clear_data_box()
            self.gui.set_data_box_greyed_out(True)
            self.gui.current_playlist_label.setText(f"Current Playlist: {self.current_playlist}")
        
        self.gui.load_sql_table(self.current_playlist)

    def new_playlist_menu(self):
        self.new_playlist_menu_dialog.exec()

    def new_playlist(self, name: str, path: str) -> bool:
        if not self.manager.playlist_exists(name) and os.path.isdir(path):
            self.manager.new_playlist(name, path)
            self.open_playlist(name)
            return True 
        else: # Playlist already exists
            return False 

    def sync_playlist(self):
        if self.current_playlist is not None:
            tracks = self.manager.get_tracks_to_sync(self.current_playlist)
            for track in tracks:
                track.download(self.manager.get_playlist_path(self.current_playlist))

    # Tracks
    def new_track(self):
        if self.current_playlist is not None:
            self.gui.data_box.setEnabled(True)
            self.current_track = None
            self.track_new = True
            self.gui.clear_data_box()

    def save_track(self):
        title = self.gui.track_title_input.text()
        artists = self.gui.track_artists_input.text()
        yt = self.gui.youtube_link_input.text()
        spotify = self.gui.spotify_link_input.text()
        album = self.gui.track_album_input.text()
        art_path = self.gui.art_path

        track = Track(title, artists, yt, spotify, album, art_path)

        if not track.valid():
            self.gui.track_invalid_message_box()
            return

        # Either add or replace the track
        if self.current_track is None and self.track_new:
            self.manager.add_track(self.current_playlist, track)
        else:
            self.manager.replace_track(self.current_playlist, self.current_track, track)

        self.gui.load_track_into_data_box(track)
        self.track_new = False
        self.current_track = track.title
        self.gui.load_sql_table(self.current_playlist)

    def delete_track(self):
        self.manager.delete_track(self.current_playlist, self.current_track)
        self.open_playlist(None)

    def select_track(self):
        self.current_track = self.gui.get_selected_track_name()
        self.track_new = False
        self.gui.load_track_into_data_box(self.manager.get_track(self.current_playlist, self.current_track))
        self.gui.set_data_box_greyed_out(False)

    # Other
    def spotify_client_info_menu(self):
        self.spotify_client_info_dialog.exec()

    def store_spotify_client_info(self, client_id: str, client_secret: str) -> bool:
        return load_client_credentials(client_id, client_secret)