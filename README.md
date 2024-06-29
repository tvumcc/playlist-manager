# Playlist Manager

This was a tiny project made to replace a command line program I had for the same purpose so as to make it more accessible to the non-programmers I know. I'm still thinking of a better name.

## Demo Video
[![YouTube](http://i.ytimg.com/vi/JLFLVA6pyWQ/hqdefault.jpg)](https://www.youtube.com/watch?v=JLFLVA6pyWQ)

## Installation and Setup
Currently, there are only releases available for Windows.
Download the latest release and run the .exe file.

Before you do anything, you need to enter in your Spotify API client credentials to allow you to get data from Spotify. Click on "Settings" in the menu bar and select "Spotify Client Info" which will open a dialog window. 

There you can enter your client ID and secret which can be obtained by following [these instructions](https://developer.spotify.com/documentation/web-api/tutorials/getting-started). 

Once you enter these in once, they will be saved and you do not have to enter them again unless you modify client_info.txt or enter in different credentials using the same dialog.

## Building
To build, an [ffmpeg executable](https://www.ffmpeg.org/download.html#build-windows) needs to be downloaded and placed in the project's root directory. From there, use pyinstaller to package the project as an executable.

```bash
pyinstaller src/main.py --name playlist_manager_v1.0 --add-binary "ffmpeg.exe;." --onefile --noconsole
```