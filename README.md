# mlbscraper

# Installation:
`import sqlite3`
`import requests`
`from bs4 import BeautifulSoup`
`from datetime import date, datetime`

# What is does:
This python file allow you to do 2 things:
1) Grab pitchfx game day data from via parse_mlbgame_site(url).
   Do so by passing a specific URL such as http://gd2.mlb.com/components/game/mlb/year_2015/month_07/day_10/gid_2015_07_10_arimlb_nynmlb_1/inning/inning_all.xml
   
2) Grab pitchfx player day data from via parse_mlbplayer_site(url_player).
   Do so by passing a specific URL such as 
   http://gd2.mlb.com/components/game/mlb/year_2015/month_07/day_10/gid_2015_07_10_arimlb_nynmlb_1/players.xml

In the code, I give an example method of using this functions and generalizing them to a year's worth of data and putting this data in a sqlite database.
