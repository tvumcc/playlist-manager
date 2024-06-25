from PyQt6.QtCore import QSize, Qt, QDir
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QAction, QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

import os
import requests

from track import Track

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Playlist Manager")
        self.setFixedSize(QSize(1200, 900))
        settings_menu = self.menuBar().addMenu("Settings")
        self.spotify_action = QAction("Spotify Client Info", self)
        settings_menu.addAction(self.spotify_action)
        help_menu = self.menuBar().addMenu("Help")

        self.init_table_view()
        self.init_controls_box()
        self.init_track_data_box()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.current_playlist_label)
        self.main_layout.addWidget(self.table)
        self.main_layout.addWidget(self.control_box)
        self.main_layout.addWidget(self.data_box)

        self.art_path = ""
        self.art_image_browse_button.clicked.connect(self.browse_art_image)

        main_container = QWidget()
        main_container.setLayout(self.main_layout)
        self.setCentralWidget(main_container)

    def init_table_view(self):
        self.qdb = QSqlDatabase("QSQLITE")
        self.qdb.setDatabaseName("main.db")
        self.qdb.open()

        self.current_playlist_label = QLabel("Current Playlist: None")
        self.table = QTableView()
        self.table_model = QSqlTableModel(self, self.qdb)
        self.table.setModel(self.table_model)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

    def init_controls_box(self):
        self.control_box = QGroupBox("Controls")
        control_box_layout = QVBoxLayout()
        self.control_box.setLayout(control_box_layout)

        control_box_buttons_layout = QHBoxLayout()
        self.open_playlist_button = QPushButton("Open Playlist")
        self.new_playlist_button = QPushButton("New Playlist")
        self.sync_playlists_button = QPushButton("Sync Playlist")
        self.new_track_button = QPushButton("New Track")
        control_box_buttons_layout.addWidget(self.open_playlist_button)
        control_box_buttons_layout.addWidget(self.new_playlist_button)
        control_box_buttons_layout.addWidget(self.sync_playlists_button)
        control_box_buttons_layout.addWidget(self.new_track_button)

        self.status_label = QLabel()
        self.status_label.setText("Status: Not Started")

        self.download_progress_bar = QProgressBar()
        self.download_progress_bar.setRange(0, 100)
        self.download_progress_bar.setValue(0)

        control_box_buttons_container = QWidget()
        control_box_buttons_container.setLayout(control_box_buttons_layout)
        control_box_layout.addWidget(control_box_buttons_container)
        control_box_layout.addWidget(self.status_label)
        control_box_layout.addWidget(self.download_progress_bar)

    def init_track_data_box(self):
        self.data_box = QGroupBox("Track Data")
        data_box_layout = QHBoxLayout()
        self.data_box.setLayout(data_box_layout)

        # Text Part
        text_entry_container = QWidget()
        text_entry_container_layout = QVBoxLayout()
        text_entry_container.setLayout(text_entry_container_layout)

        text_entry_container_layout.setSpacing(0)
        text_entry_container_layout.setContentsMargins(0, 0, 0, 0)

        button_container = QWidget()
        button_container_layout = QHBoxLayout()
        button_container.setLayout(button_container_layout)

        self.track_entry_save_button = QPushButton("Save")
        self.track_entry_delete_button = QPushButton("Delete")
        button_container_layout.addWidget(self.track_entry_save_button)
        button_container_layout.addWidget(self.track_entry_delete_button)

        text_entry_container_layout.addWidget(self.init_youtube_link_input())
        text_entry_container_layout.addWidget(self.init_spotify_link_input())
        text_entry_container_layout.addWidget(self.init_track_title_input())
        text_entry_container_layout.addWidget(self.init_track_artists_input())
        text_entry_container_layout.addWidget(self.init_track_album_input())
        text_entry_container_layout.addWidget(button_container)

        # Image Part
        image_entry_container = QGroupBox("Track Art Preview")
        image_entry_container_layout = QVBoxLayout()
        image_entry_container.setLayout(image_entry_container_layout)

        self.art_image_label = QLabel()
        self.art_image_display = QLabel()
        self.art_image_display.setFixedSize(QSize(200, 200))
        self.art_image_display.setScaledContents(True)
        self.set_art_image("")

        self.art_image_browse_button = QPushButton("Browse")

        image_entry_container_layout.addWidget(self.art_image_label)
        image_entry_container_layout.addWidget(self.art_image_display)
        image_entry_container_layout.addWidget(self.art_image_browse_button)

        data_box_layout.addWidget(text_entry_container) 
        data_box_layout.addWidget(image_entry_container)
        self.data_box.setEnabled(False)

    def init_youtube_link_input(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout()
        self.youtube_link_input = QLineEdit()
        label = QLabel("Youtube Link")
        label.setFixedWidth(70)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container.setLayout(layout)
        layout.addWidget(label)
        layout.addWidget(self.youtube_link_input)
        return container 

    def init_spotify_link_input(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout()
        self.spotify_link_input = QLineEdit()
        container.setLayout(layout)
        label = QLabel("Spotify Link")
        label.setFixedWidth(70)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(self.spotify_link_input)
        return container 

    def init_track_title_input(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout()
        self.track_title_input = QLineEdit()
        container.setLayout(layout)
        label = QLabel("Title")
        label.setFixedWidth(70)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(self.track_title_input)
        return container 

    def init_track_artists_input(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout()
        self.track_artists_input = QLineEdit()
        container.setLayout(layout)
        label = QLabel("Artists")
        label.setFixedWidth(70)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(self.track_artists_input)
        return container 

    def init_track_album_input(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout()
        self.track_album_input = QLineEdit()
        container.setLayout(layout)
        label = QLabel("Album")
        label.setFixedWidth(70)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(self.track_album_input)
        return container 

    def load_sql_table(self, playlist_name: str):
        self.table_model.setTable(playlist_name)
        self.table_model.select()
        self.table.resizeColumnsToContents()
        # hidden_columns = [2, 3, 5, 6, 7]
        # for col in hidden_columns:
        #     self.table.hideColumn(col)

    def set_data_box_greyed_out(self, state: bool):
        self.data_box.setEnabled(not state)

    def set_art_image(self, path: str):
        if path != "" and path is not None:
            self.art_image_label.setText(f"Image: {os.path.basename(path)[:20]}")
            self.art_image_display.setPixmap(QPixmap(path))
        else: # No Image
            self.art_image_display.clear()
            self.art_image_label.setText("No Image Selected")

    def set_spotify_art_image(self, url: str):
        self.art_image_label.setText("Spotify Image")

        image = QPixmap()
        image.loadFromData(requests.get(url).content)
        self.art_image_display.setPixmap(image)

    def browse_art_image(self):
        self.art_path = QFileDialog.getOpenFileName(self, "Open Image", QDir.homePath(), "Images (*.jpg *.png *.bmp *.webp)", options=QFileDialog.Option.ReadOnly)[0]
        self.set_art_image(self.art_path)

    def clear_data_box(self):
        self.track_title_input.clear()
        self.track_artists_input.clear()
        self.youtube_link_input.clear()
        self.spotify_link_input.clear()
        self.track_album_input.clear()
        self.set_art_image("")

    def load_track_into_data_box(self, track: Track):
        self.track_title_input.setText(track.title)
        self.track_artists_input.setText(track.artists)
        self.youtube_link_input.setText(track.yt)
        self.spotify_link_input.setText(track.spotify)
        self.track_album_input.setText(track.album)

        if track.art_path != "":
            self.set_art_image(track.art_path)
        elif track.art_url != "":
            self.set_spotify_art_image(track.art_url)
        else:
            self.set_art_image(None)

    def get_selected_track_name(self) -> str:
        row = self.table.selectionModel().currentIndex().row()
        track_name = self.table_model.index(row, 0).data() # Get the title of the track
        return track_name

    def track_invalid_message_box(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Invalid Track")
        dialog.setText("The track was not saved. A track must have at least a valid YouTube Video URL, and valid Spotify Track URL or title.")
        button = dialog.exec()
        if button == QMessageBox.StandardButton.Ok:
            dialog.close()

class NewPlaylistMenuDialog(QDialog):
    def __init__(self, ok_callback):
        super().__init__()

        self.file_path = ""

        self.setWindowTitle("New Playlist")
        self.closeEvent = self.clear_lines

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.ok_callback = ok_callback
        
        self.layout = QVBoxLayout()

        name_container = QWidget()
        name_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        name_container.setLayout(name_layout)
        name_layout.addWidget(QLabel("Name"))
        name_layout.addWidget(self.name_input)

        dir_container = QWidget()
        dir_layout = QHBoxLayout()
        self.dir_button = QPushButton("Browse")
        self.dir_button.clicked.connect(self.file_browse)
        dir_container.setLayout(dir_layout)
        dir_layout.addWidget(QLabel("Path"))
        dir_layout.addWidget(self.dir_button)

        self.button_box.accepted.connect(self.ok)
        self.button_box.rejected.connect(self.cancel)

        self.layout.addWidget(name_container)
        self.layout.addWidget(dir_container)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
        
    def ok(self):
        if self.ok_callback(self.name_input.text(), self.file_path):
            self.clear_lines()
            self.close()
        else:
            print("Try again")

    def clear_lines(self, event=None):
        self.name_input.clear()
        self.file_path = ""

    def file_browse(self):
        self.file_path = QFileDialog.getExistingDirectory(self, "Open Directory", QDir.homePath(), options=QFileDialog.Option.ReadOnly)

    def cancel(self):
        self.clear_lines()
        self.close()

class OpenPlaylistMenuDialog(QDialog):
    def __init__(self, playlist_names: list, open_callback, delete_callback):
        super().__init__()

        self.setWindowTitle("Open Playlist")
        self.open_callback = open_callback
        self.delete_callback = delete_callback

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.list_view = QListView()
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

        self.load_playlists(playlist_names)

        button_layout = QHBoxLayout()
        button_container = QWidget()
        button_container.setLayout(button_layout)

        open_button = QPushButton("Open")
        open_button.clicked.connect(self.open_playlist)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_playlist)

        button_layout.addWidget(open_button)
        button_layout.addWidget(delete_button)

        layout.addWidget(self.list_view)
        layout.addWidget(button_container)
    
    def load_playlists(self, playlists: list):
        self.model.clear()
        for playlist in playlists:
            item = QStandardItem(playlist)
            item.setEditable(False)
            self.model.appendRow(item)

    def open_playlist(self):
        playlist = self.list_view.selectionModel().currentIndex().data()        
        self.open_callback(playlist)
        self.close()

    def delete_playlist(self):
        playlist = self.list_view.selectionModel().currentIndex().data()        
        self.delete_callback(playlist)

class SpotifyClientInfoDialog(QDialog):
    def __init__(self, ok_callback):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setWindowTitle("Spotify Client Credentials")
        self.setFixedWidth(500)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.ok)
        self.button_box.rejected.connect(self.cancel)
        self.ok_callback = ok_callback

        client_id_container = QWidget()
        client_id_layout = QHBoxLayout()
        client_id_container.setLayout(client_id_layout)
        self.client_id_input = QLineEdit()
        client_id_layout.addWidget(QLabel("Client ID"))
        client_id_layout.addWidget(self.client_id_input)

        client_secret_container = QWidget()
        client_secret_layout = QHBoxLayout()
        client_secret_container.setLayout(client_secret_layout)
        self.client_secret_input = QLineEdit()
        client_secret_layout.addWidget(QLabel("Client Secret"))
        client_secret_layout.addWidget(self.client_secret_input)

        self.layout.addWidget(client_id_container)
        self.layout.addWidget(client_secret_container)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def ok(self):
        if self.ok_callback(self.client_id_input.text(), self.client_secret_input.text()):
            self.clear_lines()
            self.close()
        else:
            print("Try again")

    def cancel(self):
        self.clear_lines()
        self.close()

    def clear_lines(self, event=None):
        self.client_id_input.clear()
        self.client_secret_input.clear()