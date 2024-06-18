from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Playlist Manager")
        self.setFixedSize(QSize(1200, 900))
        self.menuBar().addMenu("Settings")
        self.menuBar().addMenu("Help")

        self.init_table_view()
        self.init_controls_box()
        self.init_track_data_box()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.current_playlist_label)
        self.main_layout.addWidget(self.table)
        self.main_layout.addWidget(self.control_box)
        self.main_layout.addWidget(self.data_box)

        main_container = QWidget()
        main_container.setLayout(self.main_layout)
        self.setCentralWidget(main_container)

    def init_table_view(self):
        self.current_playlist_label = QLabel("Current Playlist: None")
        self.table = QTableView()
        pass

    def init_controls_box(self):
        self.control_box = QGroupBox("Controls")
        control_box_layout = QVBoxLayout()
        self.control_box.setLayout(control_box_layout)

        control_box_buttons_layout = QHBoxLayout()
        self.open_playlist_button = QPushButton("Open Playlist")
        self.new_playlist_button = QPushButton("New Playlist")
        self.sync_playlists_button = QPushButton("Sync Playlists")
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

        self.track_entry_save_button = QPushButton("Save")

        text_entry_container_layout.addWidget(self.init_youtube_link_input())
        text_entry_container_layout.addWidget(self.init_spotify_link_input())
        text_entry_container_layout.addWidget(self.init_track_title_input())
        text_entry_container_layout.addWidget(self.init_track_artists_input())
        text_entry_container_layout.addWidget(self.init_track_album_input())
        text_entry_container_layout.addWidget(self.track_entry_save_button)

        # Image Part
        image_entry_container = QGroupBox("Track Art")
        image_entry_container_layout = QVBoxLayout()
        image_entry_container.setLayout(image_entry_container_layout)

        self.art_image_label = QLabel("Image: blue_turtle.jpg")

        self.art_image_display = QLabel()
        self.art_image_display.setFixedSize(QSize(200, 200))
        self.art_image_display.setPixmap(QPixmap("blue_turtle.jpg"))
        self.art_image_display.setScaledContents(True)

        self.art_image_browse_button = QPushButton("Browse")

        image_entry_container_layout.addWidget(self.art_image_label)
        image_entry_container_layout.addWidget(self.art_image_display)
        image_entry_container_layout.addWidget(self.art_image_browse_button)

        data_box_layout.addWidget(text_entry_container) 
        data_box_layout.addWidget(image_entry_container)

    #
    # Helper Functions
    #

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