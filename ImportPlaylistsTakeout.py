# from clicknium import locator, clicknium as cc
# import time

# license_key = ""
# with open(".env", "r") as f:
#     for line in f:
#         line = line.strip()
#         if line.startswith("CLICKNIUM"):
#             license_key = line.split("|")[1]

# cc.config.set_license(license_key)
# cc.chrome.extension.install_or_update()
# tab = cc.chrome.open("www.google.com")

# PLAYLIST_URL_PREFIX = "music.youtube.com/playlist?list="


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


import os, sys, time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# LIMIT OF 200 REQUESTS PER DAY

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_local_server(port=0)
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


# gather list of playlists that have already been successfully transferred
existing_playlists = []
existing_file = open("playlists/existing_playlists.txt", "r")
for line in existing_file:
    existing_playlists.append(line.strip())
existing_file.close()
existing_file = open("playlists/existing_playlists.txt", "a")

# gather playlist data from playlists.csv
playlist_data = []
playlist_file = open("playlists/playlists.csv", "r")
key_list = []
for line in playlist_file:
    line = line.strip()
    if line.startswith("Playlist ID"):
        key_list = line.split(",")
    elif line:
        values = line.split(",")
        record = {}
        for i in range(len(values)):
            record[key_list[i]] = values[i]
        playlist_data.append(record)
playlist_file.close()

# gather list of csv files containing playlist data
playlist_file_names = os.listdir("playlists")
titles_no_file = []

# loop through playlist data, ignoring any in the existing list
for playlist in playlist_data:
    playlist_title = playlist["Playlist Title (Original)"]
    if playlist_title in existing_playlists:
        continue

    # first, insert the playlist to the YouTube account
    request = youtube.playlists().insert(
        part="snippet,status,id",
        body={
            "snippet": {
                "title": playlist_title,
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        }
    )

    # run request and get playlist id
    response = request.execute()
    playlist_id = ""
    try:
        playlist_id = response['id']
        print("Created playlist titled: " + playlist_title)
    except Exception as error:
        # if we can't get a playlist id, print info and exit
        print(response)
        print("An exception occurred:", error)
        existing_file.close()
        sys.exit()

    # find the file for the current playlist, get video_ids list from it
    curr_filename = ""
    for filename in playlist_file_names:
        title_from_name = filename.split(".")[0].split("-")[0]
        if title_from_name in playlist_title:
            curr_filename = filename
            break
    
    if not curr_filename:
        titles_no_file.append(playlist_title)
        continue

    video_ids = []
    with open(f"playlists/{curr_filename}", "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("Video") and "," in line:
                video_ids.append(line.split(",")[0])
        f.close()

    # loop through video ids and add to newly created playlist
    for video_id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
                }
            }
            }
        )

        # print if successful, move on to next if just 404, stop program otherwise (in case quota reached)
        try:
            response = request.execute()
            print(f"{response['snippet']['title']} added to {playlist_title}")
        except Exception as error:
            if response: print(response)
            print(f"An exception occurred while building {playlist_title}:", error)
            if "Video not found." in str(error):
                continue
            existing_file.write(f"{playlist_title}\n")
            existing_file.close()
            if titles_no_file:
                print("Unable to find a playlist file for these playlists:")
                for title in titles_no_file:
                    print(title)
            sys.exit()
    
    existing_file.write(f"{playlist_title}\n")
    time.sleep(10)

existing_file.close()
if titles_no_file:
    print("Unable to find a playlist file for these playlists:")
    for title in titles_no_file:
        print(title)
