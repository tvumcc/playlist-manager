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