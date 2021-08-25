# oddsbook-git

WebScraping football odds infomation from HKJC (and more to go...) periodicially by given interval and update it on OddsBook.xlsx.

Setup step:
1. Download the package from git.
2. pip install -r requirements.txt
3. Replace the chromedriver with the version matching the Chrome on your desktop from https://chromedriver.chromium.org/downloads.

Command to one-off execution:
- python -m oddsbook

Command to repeatly running (for every 10 mins for example):
- python -m oddsbook --interval 10
