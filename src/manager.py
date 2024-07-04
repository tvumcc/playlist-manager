import os
import sqlite3

from track import Track

class Manager:
    def __init__(self):
        # Initialize handles to the sqlite databases
        self.con = sqlite3.connect("main.db")
        self.cursor = self.con.cursor()

        # Initialize the special table which maps playlist names to their corresponding locations on disk
        self.playlist_to_path_table = "__playlist_to_path__"

        if not self.playlist_exists(self.playlist_to_path_table):
            self.cursor.execute(f"CREATE TABLE '{self.playlist_to_path_table}'(playlist TEXT, path TEXT)")

    # Playlists
    """Returns true if the playlist exists and false otherwise"""
    def playlist_exists(self, playlist_name: str) -> bool:
        playlist_name = playlist_name.replace("'", "''")
        return self.cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{playlist_name}' AND type='table'").fetchone() is not None
    
    """Returns the path to the location of the specified playlist"""
    def get_playlist_path(self, playlist_name: str) -> str:
        playlist_name = playlist_name.replace("'", "''")
        
        return self.cursor.execute(f"SELECT path FROM {self.playlist_to_path_table} WHERE playlist='{playlist_name}'").fetchone()[0]

    """Returns a list of all the playlist names stored in the database"""
    def get_playlists(self) -> list:
        playlists = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND NOT name='{self.playlist_to_path_table}'").fetchall()
        return [x[0].replace("''", "'") for x in playlists]

    """Creates a new playlist with a given name and adds it to the database"""
    def new_playlist(self, playlist_name: str, playlist_path: str) -> bool:
        if playlist_name not in self.get_playlists():
            playlist_name = playlist_name.replace("'", "''")        
            playlist_path = playlist_path.replace("'", "''")
            self.cursor.execute(f"CREATE TABLE '{playlist_name}'(title TEXT, artists TEXT, yt TEXT, spotify TEXT, album TEXT, artpath TEXT, arturl TEXT, filepath TEXT, synced INTEGER DEFAULT 0)")
            self.cursor.execute(f"INSERT INTO '{self.playlist_to_path_table}' VALUES ('{playlist_name}', '{playlist_path}')")
            self.con.commit()
            return True
        else:
            return False

    """Removes a playlist and all its tracks from the database. Returns true if the playlist exists and false otherwise"""
    def delete_playlist(self, playlist_name: str) -> bool:
        if playlist_name in self.get_playlists():
            playlist_name = playlist_name.replace("'", "'")
            self.cursor.execute(f"DROP TABLE '{playlist_name}'")
            self.cursor.execute(f"DELETE FROM '{self.playlist_to_path_table}' WHERE playlist='{playlist_name}'")
            self.con.commit()
            return True
        else:
            return False

    # Tracks
    """Returns a track object from the database given the track's name"""
    def get_track(self, playlist_name: str, track_name: str) -> Track:
        playlist_name = playlist_name.replace("'", "''")
        track_name = track_name.replace("'", "''")

        track_data = self.cursor.execute(f"SELECT title, artists, yt, spotify, album, artpath, arturl FROM '{playlist_name}' WHERE title='{track_name}'").fetchone()
        return Track(*track_data)

    """Returns true if the track is in the playlist and false otherwise"""
    def track_exists(self, playlist_name: str, track_name: str) -> bool:
        playlist_name = playlist_name.replace("'", "''")
        track_name = track_name.replace("'", "''")

        return self.cursor.execute(f"SELECT title FROM '{playlist_name}' WHERE title='{track_name}'").fetchone() is not None

    """Adds a track to the specified playlist. Returns false if a track with that title already exists in that playlist and true otherwise"""
    def add_track(self, playlist_name: str, track: Track) -> bool:
        if not self.track_exists(playlist_name, track.title.replace("'", "''")):
            playlist_name = playlist_name.replace("'", "''")
            self.cursor.execute(f"""
                INSERT INTO '{playlist_name}' VALUES 
                ('{track.title.replace("'", "''")}', 
                '{track.artists.replace("'", "''")}',
                '{track.yt.replace("'", "''")}',
                '{track.spotify.replace("'", "''")}',
                '{track.album.replace("'", "''")}',
                '{track.art_path.replace("'", "''")}',
                '{track.art_url.replace("'", "''")}', '', 0)
            """)
            self.con.commit()
            return True
        else:
            return False

    """Replaces a track in a specified playlist with a new track"""
    def replace_track(self, playlist_name: str, track_name: str, new_track: Track):
        playlist_name = playlist_name = playlist_name.replace("'", "''")
        track_name = track_name = track_name.replace("'", "''")

        self.cursor.execute(f"""
            UPDATE '{playlist_name}' SET 
            title='{new_track.title.replace("'", "''")}',
            artists='{new_track.artists.replace("'", "''")}',
            yt='{new_track.yt.replace("'", "''")}',
            spotify='{new_track.spotify.replace("'", "''")}',
            album='{new_track.album.replace("'", "''")}',
            artpath='{new_track.art_path.replace("'", "''")}',
            arturl='{new_track.art_url.replace("'", "''")}', 
            synced=0 
            WHERE title='{track_name}'
        """)
        self.con.commit()

    """Removes a track from the specified playlist's table. Returns true if the track exists and false otherwise."""
    def delete_track(self, playlist_name: str, track_name: str) -> bool:
        if self.track_exists(playlist_name, track_name):
            playlist_name = playlist_name.replace("'", "''")
            track_name = track_name.replace("'", "''")

            self.cursor.execute(f"DELETE FROM '{playlist_name}' WHERE title='{track_name}'")
            self.con.commit()
            return True
        else:
            return False

    """Returns a list of Track objects which need to be synced. This consists of tracks which don't have a file associated with them or have not been marked as synced."""
    def get_tracks_to_sync(self, playlist_name: str) -> list[Track]:
        tracks = []
        tracks_query = self.cursor.execute(f"SELECT title, filepath, synced FROM '{playlist_name.replace("'", "''")}'").fetchall()
        for record in tracks_query:
            if not os.path.isfile(record[1]) or record[2] != 1:
                tracks.append(self.get_track(playlist_name, record[0]))
        return tracks

    """Sets the specified track to be synced in the database."""
    def set_track_to_synced(self, playlist_name: str, track_name: str, file_path: str):
        playlist_name = playlist_name.replace("'", "''")
        track_name = track_name.replace("'", "''")
        file_path = file_path.replace("'", "''")

        self.cursor.execute(f"UPDATE '{playlist_name}' SET filepath='{file_path}', synced=1 WHERE title='{track_name}'")
        self.con.commit()