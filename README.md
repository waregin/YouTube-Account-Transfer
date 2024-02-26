# Description

Simple Python script to take YouTube watch history from JSON file and open in an account in Chrome. This is handy for account transfer or to restore deleted history (if you have a Google Takeout file handy). Most of the credit should go to the OP of the Reddit post below. I have modified for Chrome instead of Vivaldi and assuming the clicknium extension is already installed and enabled.


# Original Source

https://www.reddit.com/r/automation/comments/ydzgzn/importing_youtube_history_via_clicknium_and_python/


# Instructions

There are multiple ways to accomplish many of the below steps. I have listed what I did.

1. Start Google Takeout of YouTube and YouTube Music history as JSON format
1. Install Visual Studio Code (VSC) (if not already installed)
1. Clone this project and open in VSC
1. Install VSC Python extension if prompted
1. Install VSC Powershell extension if needed
1. Install VSC Clicknium extension if needed
1. Open Clicknium Explorer in VSC by clicking on the rhino head icon
1. Sign in, creating account if necessary
1. Ensure Python module is installed
1. Ensure Chrome Browser automation extension (or whichever browser you wish to use) is installed - for Chrome, this might require enabling Developer Mode under Manage Extensions (chrome://extensions/), which is in the upper right
1. Enable Clicknium Recorder extension (Chrome will prompt for this upon being opened after the previous step)
1. Download your Takeout file(s), extract archive, and look for the watch-history.json file in Takeout -> YouTube and YouTube Music -> history
1. Copy watch-history.json to the same folder as this README
1. Finally, you are ready to run the script! Either open a PowerShell terminal (in VSC or otherwise) to this directory and run ``python .\ImportHistory.py`` or right click on ImportHistory.py in VSC's Explorer and select ``Run Python File in Terminal`` (it was the bottom of the list for me)
1. Note: If you don't want to hear the first 10 seconds of every video in your history, but wish to avoid muting your entire computer, I recommend the Tab Muter Chrome extension, which allows you to mute specifically the tab that Clicknium is using to run this script.
1. Note: I experienced an occassional "Are you sure you want to Leave? Changes may not be saved" popup, especially with YouTube Music. I simply kept the Clicknium tab open on another monitor so I could click the "Leave" button when this happened.


# Changes from Source

- removed ``['history']`` from line 15
- changed lines 6-7 to use Chrome rather than vivaldi
- commented out line 6 (which was meant to install the Clicknium extension in Chrome)
- modified script to go through history backwards and output every 1000 videos to show progress
- added search history as well
