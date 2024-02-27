from clicknium import clicknium as cc
from datetime import datetime, time
import json

# install chrome extension and open a tab to automate
# cc.chrome.extension.install_or_update()
tab = cc.chrome.open("www.google.com") # can be any url, just need to open a tab

for filename in ["history/watch-history.json", "history/search-history.json"]:
    # open the google takeout json for history
    with open(filename, encoding="utf8") as f:
        data = json.load(f)
        data.reverse()
    
        count = 0
        # loop through each item in our history.
        for i in data:
            #If there is a title url we can load it
            if 'titleUrl' in i:
                # strip the https:// from the url in order to make goto work properly.
                url = str(i['titleUrl']).replace("https://", "")
                count += 1

                # open the url and then wait for it to fully register youtube history
                tab.goto(url)
                time.sleep(10) # arbitrary number, feel free to make shorter if it works
            if count % 500 == 0:
                if 'time' in i:
                    print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - History added through {i['time']}")
                print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Opened {count} of {len(data)} so far")
    
        # closing file
        f.close()

# closing tab
tab.close()
