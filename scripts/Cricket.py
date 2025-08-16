from turtledemo.minimal_hanoi import play

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

url ='https://www.espncricinfo.com'
r = requests.get('https://www.espncricinfo.com/series/icc-cricket-world-cup-2010-11-381449/match-schedule-fixtures-and-results')
soup = BeautifulSoup(r.text,'lxml')

#data = soup.find_all(class_=['ds-bg-fill-content-prime', 'hover:ds-bg-ui-fill-translucent'])
link = soup.find_all('a',class_='ds-no-tap-higlight')

#columns =['Player','Runs','Balls']
#batting_data =pd.DataFrame(columns=columns)

combined_batting_data = pd.DataFrame()

for i in link[14:]:
    href = i.get('href')
    url_np = url + href
    #print(url_np)
    next_page = requests.get(url_np)
    new_soup = BeautifulSoup(next_page.text, 'lxml')



    #batting_stats =new_soup.find_all('td',class_=['ds-w-0 ds-whitespace-nowrap', 'ds-min-w-max', 'ds-flex', 'ds-items-center'])

    batting_stats = new_soup.find_all('table',class_='ci-scorecard-table')

    for j in batting_stats:
        tr_data = j.find_all('tr',class_=True)
        all_player_data = []

        for k in tr_data:

            td_data = k.find_all('td',class_=['ds-w-0', 'ds-whitespace-nowrap'])


            for l in td_data:
                player_data=l.text

                all_player_data.append(player_data)


        data = all_player_data


        #print(data)
        batting_columns = ['Player', 'Runs', 'Balls', 'Mins', '4s', '6s', 'SR']
        #bowling_columns = ['Player', 'Overs', 'Maidens', 'Runs', 'Wickets', 'Econ', 'Dots', '4s', '6s','WD','NB']

        batting_data = [data[w:w + 7] for w in range(0, len(data), 7)]

        batting_df = pd.DataFrame(batting_data, columns=batting_columns)
        combined_batting_data = pd.concat([combined_batting_data,batting_df],ignore_index=True)


#print(combined_batting_data)

combined_batting_data.to_csv('WorldCup_11_batting_data',index=False)
