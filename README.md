# Scripts for Recovering or Transferring YouTube Data

This project contains several Python scripts using Clicknium to help in recovering or transferring YouTube data:
1. Import History using Google Takeout File(s)
1. Import History using Google My Activity Page
1. Import Playlists using Google Takeout File(s) (in progress)


### Inspiring Source

All of these scripts are inpired by [this Reddit post](https://www.reddit.com/r/automation/comments/ydzgzn/importing_youtube_history_via_clicknium_and_python/). Most of the credit for the first script should go to that OP. I've included a list of my changes.


## VERY IMPORTANT CLICKNIUM NOTE

If you are working on Windows and your user account folder name (under C:\Users) has a space in it, Clicknium will NOT work. A workaround for this is to create a tempuser with no spaces, log in as that user, and follow the instructions from there. You may need to create a new Microsoft account for this. I would love to hear about a better workaround or if Clicknium ever fixes this bug.



## 1. Import History using Google Takeout File(s)

ImportHistoryTakeout.py

### Description

Script to take YouTube watch and search history from Google Takeout JSON files and open in an account in Chrome. This is handy for restoring deleted history if you have a Google Takeout from before the deletion or account transfer.


# Instructions

There are multiple ways to accomplish many of the below steps. I have listed what I did.

1. Start Google Takeout of YouTube and YouTube Music history as JSON format (if not already done)
1. Install Visual Studio Code (VSC) (if not already installed)
1. Clone this project and open in VSC OR open a folder in VSC and create a new file, then copy and paste the script
1. Install VSC Python, Powershell, and Clicknium extensions if not already installed
1. Open Clicknium Explorer in VSC by clicking on the rhino head icon
1. Sign in, creating account if necessary
1. Ensure Clicknium Python module is installed
1. Ensure Chrome Browser automation extension (or whichever browser you wish to use) is installed
    - For Chrome, this might require enabling Developer Mode under Manage Extensions (chrome://extensions/), which is in the upper right
    - It will prompt to close your browser
1. Enable Clicknium Recorder extension (Chrome will prompt for this upon being opened after the previous step)
1. Download your Takeout file(s), extract archive, and look for the history folder in Takeout -> YouTube and YouTube Music
    - It should contain two files: search-history.json and watch-history.json
1. Copy history folder into the same folder as the script
1. Ensure you are logged in to the desired target Google Account on Chrome (or your desired browser)
1. Finally, you are ready to run the script! Either open a PowerShell terminal (in VSC or otherwise) to the script's folder and run ``python .\ImportHistoryTakeout.py`` or right click on ImportHistoryTakeout.py in VSC's Explorer and select ``Run Python File in Terminal`` (it was the bottom of the list for me)
    - Note: If you don't want to hear the first 10 seconds of every video in your history, but wish to avoid muting your entire computer, I recommend the Tab Muter Chrome extension, which allows you to mute specifically the tab that Clicknium is using to run this script.
    - Note: I experienced an occassional "Are you sure you want to Leave? Changes may not be saved" popup, especially with YouTube Music. I simply kept the Clicknium tab open on another monitor so I could click the "Leave" button when this happened.


# Changes from Source

- removed ``['history']`` from line 15
- changed lines 6-7 to use Chrome rather than vivaldi
- commented out line 6 (which was meant to install the Clicknium extension in Chrome)
- modified script to go through history backwards and output every 1000 videos to show progress
- added search history as well



## 2. Import History using Google My Activity Page

ImportHistoryMyActivity.py

### Description

Script to scroll through YouTube history on My Activity page for Google account, gather the URLs, and add them to YouTube's Watch History. This is handy to restore deleted history when you have no Takeout file, although it likely only has a limited timeframe where it will work. Inspired by the next script in this project.


# Instructions

There are multiple ways to accomplish many of the below steps. I have listed what I did.

1. Install Visual Studio Code (VSC) (if not already installed)
1. Clone this project and open in VSC OR open a folder in VSC and create a new file, then copy and paste the script
1. Install VSC Python, Powershell, and Clicknium extensions if not already installed
1. Open Clicknium Explorer in VSC by clicking on the rhino head icon
1. Sign in, creating account if necessary
1. Find your Clicknium license key by going to [account.clicknium.com](), and copy your Personal Professional license key using the copy icon
1. Create a file named ``.env`` in the same folder as the script and add the line ``CLICKNIUM|YOUR_KEY``, replacing "YOUR_KEY" with the key copied in the previous step
    - This allows you to use Locators, which we'll set up shortly
    ![Clicknium License Key](screenshots\ClickniumLicenseKey.png)
1. Ensure Clicknium Python module is installed
1. Ensure Chrome Browser automation extension (or whichever browser you wish to use) is installed
    - For Chrome, this might require enabling Developer Mode under Manage Extensions (``chrome://extensions/``), which is in the upper right
    - It will prompt to close your browser
1. Enable Clicknium Recorder extension (Chrome will prompt for this upon being opened after the previous step)
1. In Chrome or your preferred browser, navigate to your [YouTube Activity History page](https://myactivity.google.com/product/youtube?hl=en)
    - If you desire to only go back from a certain date, select that data and copy the URL into the line of the script that has a similar URL (around line 28, see comments)
1. Set up your Locator
    1. Click the Capture icon on the LOCATORS section of EXPLORER in VSC
    ![Locators Capture Button](screenshots\LocatorsCapture.png)
    1. Hover over an item in your list, specifically on the word "Watched", until you see a greyed out ``<div>`` like in the below screenshot - if the grey box isn't lining up very similarly to the below, try closing/minimizing other tabs or moving your history tab to a different monitor
    ![Locating Div Watched](screenshots\LocatingDivWatched.png)
    1. You should see a div_watched in your Clicknium Recorder. Click ``Complete`` if you do
    ![Clicknium Recorder](screenshots\ClickniumRecorder.png)
    1. Close your YouTube History tab to avoid confusion with the one the script will open
    1. Back in VSC, open your new div_watched locator by clicking on it in the Locators part of the Explorer panel. Modify the ``index`` in the right side panel to say ``{{indexValue}}`` instead of the number, as in the below screenshot
    ![Div Watched Locator](screenshots\DivWatchedLocator.png)
1. Finally, you are ready to run the script! Either open a PowerShell terminal (in VSC or otherwise) to the script's folder and run ``python .\ImportHistoryMyActivity.py`` or right click on ImportHistory.py in VSC's Explorer and select ``Run Python File in Terminal`` (it was the bottom of the list for me)
    - Note: If you don't want to hear the first 10 seconds of every video in your history, but wish to avoid muting your entire computer, I recommend the Tab Muter Chrome extension, which allows you to mute specifically the tab that Clicknium is using to run this script.
    - Note: I experienced an occassional "Are you sure you want to Leave? Changes may not be saved" popup, especially with YouTube Music. I simply kept the Clicknium tab open on another monitor so I could click the "Leave" button when this happened
1. After the script has completed, check whether your entire history was collected
    1. First, look at the output from the script. The last line of output should say something like "Opened 4350 of 4365". If the numbers match, this indicates the script might not have scrolled all the way to the bottom
    1. Second, look at the YouTube History tab opened by the script. If it does not say "Looks like you've reached the end", you are missing some of your history
    1. If you wish to try again, simply rename your generated ``watch-history.txt`` to ``watch-history-previous.txt``, increase the values in ``orig_sleep_time`` and/or ``sleep_time_incr`` as desired, and re-run the script
        - NOTE: If you want to re-try again, instead of renaming the watch-history.txt, copy the contents of that file and add them to watch-history-previous.txt


### Potential Future Enhancements

- modify ImportHistoryMyActivity.py to gather search history as well
- modify ImportHistoryTakeout.py to use all files in the history folder dynamically instead of hardcoding two filenames
- when opening a video for history, check the length and wait that long (or half that long?)
- increase video playback speed for opening videos for history
- if video unavailable (private, removed, members only), do not wait at all
- handle bug for YouTube Music where it asks about leaving without saving changes (bug might be fixed by video watch length enhancements)
- add option to include or ignore YouTube Music urls to both ImportHistory scripts
