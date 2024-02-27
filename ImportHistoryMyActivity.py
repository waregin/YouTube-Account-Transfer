from clicknium import locator, clicknium as cc
from datetime import datetime, time

# get clicknium license key from .env file
license_key = ""
with open(".env", "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("CLICKNIUM"):
            license_key = line.split("|")[1]
            break
    f.close()

# set clicknium license key (necessary to use locator)
cc.config.set_license(license_key)

# ensure the extension is installed in Chrome (change this line to your preferred browser if desired)
# NOTE: clicknium will NOT work if it is installed where the path has a space in it, such as your account folder under C:\Users
# a workaround for this is to create a tempuser, log in as that user, and start the instructions over
# I would love to hear about a better workaround or if clicknium ever fixes this bug
cc.chrome.extension.install_or_update()

# open a tab to your activity page
# NOTE: you will need to be signed in to your Google account for this script to work
# there are two lines with open() to give an option between all YouTube history or history prior to a specified date
# to use a specified date, go to the first url below, select your desired date, and replace the second url with the resulting url
# then, remove the # from the second line and put one in front of the first line (VSC keyboard shortcut: go to the line and press Ctrl+/ to toggle comment)
activity_tab = cc.chrome.open("https://myactivity.google.com/product/youtube?hl=en")
# activity_tab = cc.chrome.open("https://myactivity.google.com/product/youtube?hl=en&max=1708405199999999")

# give the page a second to load - please increase this number if your internet is slow
time.sleep(1)

# collect any previously opened urls to save time
# NOTE: if the previous run of the script failed to scroll to the bottom of the page,
# rename the "watch-history.txt" to "watch-history-previous.txt" and re-run the script to try again
previous_urls = []
try:
    with open("watch-history-previous.txt", "r") as f:
        for line in f:
            previous_urls.append(line.strip())
        f.close()
except FileNotFoundError:
    pass

# NOTE: change these values to increase wait for more videos to load
orig_sleep_time = 10
sleep_time_incr = 2
max_sleep_time = 60

# scroll through activity list and gather video urls
index = 1
urls = []
curr_sleep_time = orig_sleep_time
# NOTE: you must create a locator using the Clicknium extension in VSC for this to work (see README.md)
while activity_tab.is_existing(locator.chrome.myactivity.div_watched, {'indexValue': index}):
    element = activity_tab.find_element(locator.chrome.myactivity.div_watched, {'indexValue': index})
    # there should just be one child, containing the link to the video
    for child in element.children:
        href = child.get_property('href')
        if href and href not in previous_urls:
            urls.append(href)
            break
    # every 20th video, wait a bit for the page to load more videos
    if index % 20 == 0:
        time.sleep(curr_sleep_time)
    # every 1000th video, increase the wait time, up to 60 seconds
    if index % 1000 == 0 and curr_sleep_time < max_sleep_time:
        curr_sleep_time = curr_sleep_time + sleep_time_incr
    index += 1
# leave activity tab OPEN to check if the scroll went all the way down

# reverse order of the urls so the script can replicate the original watch order
urls.reverse()

# save a txt of all the urls, just in case something goes wrong going through the list
# or to aid in starting again if the script failed to scroll all the way down the activity history
with open("watch-history.txt", "w") as f:
    for url in urls:
        f.write(f"{url}\n")
    f.close()

# open a new tab so we can check the activity tab later
watch_tab = cc.chrome.open("www.google.com") # can be any url, just need to open a tab

# go through our list of urls and open each one, adding it to youtube history
# NOTE: as written, this will NOT create a red bar across the bottom of the video in your YouTube history
# one easy option to make that full red bar more likely is to increase the number in time.sleep(10)
# however, that will make the script take that much longer per video
count = 0
for url in urls:
    count += 1
    # open the url and then wait for it to fully register youtube history
    watch_tab.goto(url)
    time.sleep(10) # arbitrary number, feel free to make shorter if it works
    # print progress every 50th video - change the number if you want more or less frequent updates
    if count % 50 == 0:
        print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Opened {count} of {len(urls)} so far")

# close the tab 
watch_tab.close()
