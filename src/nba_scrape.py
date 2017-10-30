"""
A module for scraping game level statistics for regular season NBA games
from basketball-reference.com
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from settings import *


#Create list of years to scrape
seasons = list(map(str, range(2008, 2018)))

#Create lists of column headers on basketball-reference
complete_columns = additional_columns + columns + advanced_columns

def scrape(team_list, year):
    gamelogs_internal = []
    for team in team_list:
        team_year = [team, year]
        team_data = []

        url = 'https://www.basketball-reference.com/teams/' \
              '{}/{}/gamelog/'.format(team, year)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        data_rows = soup.findAll('tr', {'id':re.compile('^tgl_basic')})
        data = [[td.getText() for td in data_rows[i].findAll('td',
                                        {'data-stat':columns})]
                for i in range(len(data_rows))]

        urlA = 'https://www.basketball-reference.com/teams/' \
               '{}/{}/gamelog-advanced'.format(team, year)
        htmlA = urlopen(urlA)
        soupA = BeautifulSoup(htmlA, 'lxml')
        data_rowsA = soupA.findAll('tr', {'id':re.compile('^tgl_advanced')})
        dataA = [[td.getText() for td in data_rowsA[i].findAll('td',
                                        {'data-stat':advanced_columns})]
                                        for i in range(len(data_rowsA))]

        for row, rowA in zip(data, dataA):
            new_row = team_year + row + rowA
            team_data.append(new_row)
        gamelogs_internal.append(team_data)
        print('{} {} scraped'.format(team, year))
    return gamelogs_internal


def gamelog_scrape(team_list1, team_list2, team_list3, team_list4,
                   team_list5, year_list):
    gamelogs = []
    for year in year_list:
        if year == '2008':
            game_log_piece = scrape(team_list1, year)
            gamelogs.append(game_log_piece)
        elif year in ['2009', '2010', '2011', '2012']:
            game_log_piece = scrape(team_list2, year)
            gamelogs.append(game_log_piece)
        elif year == '2013':
            game_log_piece = scrape(team_list3, year)
            gamelogs.append(game_log_piece)
        elif year == '2014':
            game_log_piece = scrape(team_list4, year)
            gamelogs.append(game_log_piece)
        elif year in ['2015', '2016', '2017']:
            game_log_piece = scrape(team_list5, year)
            gamelogs.append(game_log_piece)
    return gamelogs

if __name__ == "__main__":
    data = gamelog_scrape(team_list1=teams_08, team_list2=teams_09_12,
                          team_list3=teams_13, team_list4=teams_14,
                          team_list5=teams_15_17, year_list=seasons)

    #Format and export scraped data to csv file
    df = pd.concat([pd.DataFrame(d[i]) for d in data for i in range(30)])
    df.columns=complete_columns
    df = df.reset_index(drop=True)
    df.to_csv('../data/gamelogs_advanced.csv')
