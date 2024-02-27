from clicknium import locator, clicknium as cc
import time

license_key = ""
with open(".env", "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("CLICKNIUM"):
            license_key = line.split("|")[1]

cc.config.set_license(license_key)
cc.chrome.extension.install_or_update()
tab = cc.chrome.open("www.google.com")

PLAYLIST_URL_PREFIX = "music.youtube.com/playlist?list="
# first, get list of files in playlists directory
# look at playlists.csv first
# import the csv into a list of dicts
# for each playlist in the list:
#   if it is not Private
#     open the playlist url
#     click the buttons to "Save to playlist", creating a new playlist with the same name and making it Private (or make a channel so I can make things unlisted)
#     remove from the list
# remove playlists.csv from the list of the other files
# for each file:
#   get the playlist name from the filename
#   if the playlist name matches a playlist name in the other list
#     if playlist name is NOT Favorites or Watch Later
#       create a new playlist with the same name
#   get the list of video ids from the file
#   for each video:
#     open the url
#     add to playlist of the appropriate name
#   close file
# close tab
# will still need to manually compare, but if I can get the script to do the bulk of the work for me...