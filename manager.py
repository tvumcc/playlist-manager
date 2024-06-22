import os
import sqlite3

from track import Track

class Manager:
    def __init__(self):
        self.con = sqlite3.connect("main.db")
        self.cursor = self.con.cursor()
        self.current_playlist = None
        self.current_track = None

    def playlist_exists(self, name: str) -> bool:
        return self.cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{name}' AND type='table'").fetchone() is not None
    
    def track_exists(self, name: str) -> bool:
        return self.cursor.execute(f"SELECT title FROM '{self.current_playlist}' WHERE title='{name}'").fetchone() is not None

    def get_playlists(self) -> list:
        playlists = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        return [x[0] for x in playlists]

    def get_track(self):
        print(self.cursor.execute(f"SELECT * FROM '{self.current_playlist}' WHERE title='{self.current_track}'"))

    def open_playlist(self, name: str):
        self.current_playlist = name

    def select_track(self, name: str):
        self.current_track = name

    def new_playlist(self, name: str) -> bool:
        if name not in self.get_playlists():
            self.cursor.execute(f"CREATE TABLE '{name}'(title, artists, yt, spotify, artpath, filepath)")
            return True
        else:
            return False

    def delete_playlist(self, name: str) -> bool:
        if name in self.get_playlists():
            self.cursor.execute(f"DROP TABLE '{name}'")
            return True
        else:
            return False

    def add_track(self, track: Track) -> bool:
        if not self.track_exists(track.title):
            self.cursor.execute(f"INSERT INTO '{self.current_playlist}' VALUES ('{track.title}', '{track.artists}', '{track.yt}', '{track.spotify}', '{track.art_path}', '')")
            self.con.commit()
            return True
        else:
            return False

    def print_out_tracks(self):
        tracks = self.cursor.execute(f"SELECT * FROM '{self.current_playlist}'").fetchall()
        print(tracks)