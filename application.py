from PyQt6.QtWidgets import *

from manager import Manager
from ui import MainWindow

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

    def run(self):
        self.gui.show()
        self.app.exec()

    def open_playlist_menu(self):
        pass

    def new_playlist_menu(self):
        pass

    def sync_playlists(self):
        pass

    def new_track(self):
        pass

    def save_track(self):
        pass

    def browse_image(self):
        pass

    def select_track(self):
        pass