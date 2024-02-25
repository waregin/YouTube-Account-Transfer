from clicknium import clicknium as cc
import json
import time

# install chrome extension and open a tab to automate
# cc.chrome.extension.install_or_update()
tab = cc.chrome.open("www.google.com") #Can be any url, just need to open a tab

for filename in ["watch-history.json", "search-history.json"]:
    # Open the google takeout json for history
    with open(filename, encoding="utf8") as f:
        data = json.load(f)
        data.reverse()
    
        count = 0
        #Loop through each item in our history.
        for i in data:
            #If there is a title url we can load it
            if 'titleUrl' in i:
                #Strip the https:// from the url in order to make goto work properly.
                url = str(i['titleUrl']).replace("https://", "")
                count += 1

                #Open the url and then wait for it to fully register youtube history
                tab.goto(url)
                time.sleep(10) #Arbitrary number, feel free to make shorter if it works
            if count % 500 == 0:
                if 'time' in i:
                    print(f"History added through {i['time']}")
                print(f"Opened {count} of {len(data)} so far")
    
        # Closing file
        f.close()

# Closing tab
tab.close()