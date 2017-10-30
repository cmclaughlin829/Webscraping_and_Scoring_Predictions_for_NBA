"""
Module to clean and organize data prior to modeling
"""
import sys
import pandas as pd
import numpy as np
import pickle
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from settings import *
from utils import *


if __name__ =="__main__":
    data = read_raw()
    print('Data Loaded')

    #Complete initial data cleaning
    data = initial_clean(data)

    #Create copy of data to allow for formatting
    data_split = data.copy()

    #Create features for expanding means by season and team
    data_split = expanding_means(data_split, ['season', 'team'],
                                 unwanted_columns)

    #Create features to represent recent team performace (last 5 games)
    data_split = rolling_window_mean(data_split,
                                     ['off_rtg_mean', 'w_l_mean'], 5)

    #Create feature to show teams rest (days) coming into game
    data_split['days_rest']=data_split.groupby(['season', 'team'])['date_game'].transform(lambda x: x.diff()/np.timedelta64(1, 'D'))

    #Create feature to show latitude and longitude for each team's home city
    geolocator = Nominatim()
    for abbrv, city in cities.items():
        location = geolocator.geocode(city)
        cities[abbrv]=(location.latitude, location.longitude)

    data_split['lat_long']=data_split['team'].map(cities)

    #Remove unwanted columns from dataframe
    cols = list(data_split.columns.values)
    cols = [cols[0]]+cols[2:4]+[cols[7]]+cols[58:]
    data_split = data_split[cols].copy()

    #Create second copy of data to represent NBA schedule
    schedule = data.copy()
    schedule = schedule[['date_game', 'team', 'season', 'game_location',
                'opp_id']].sort_values(by='date_game').reset_index(drop=True)
    schedule = create_schedule(schedule)

    #Preliminary dataframe merge for all home teams
    final = schedule.merge(data_split, left_on=['home_team', 'date_game'],
                                       right_on=['team', 'date_game'])

    #Rename home team columns
    home_column_dict = {column:'home_'+column for column in cols}
    final = final.rename(columns = home_column_dict)

    #Preliminary dataframe merge for all away teams
    final = final.merge(data_split, left_on=['away_team', 'home_date_game'],
                                   right_on=['team', 'date_game'])

    #Rename away team columns
    away_column_dict = {column:'away_'+column for column in cols}
    final = final.rename(columns = away_column_dict)

    #Rename date_game column
    final = final.rename(columns = {'home_date_game':'date_game'})

    #Remove duplicate columns
    final = final.loc[:,~final.columns.duplicated()]

    #Create score margin feature
    final['score_margin']=final['home_pts']-final['away_pts']

    #Create feature to represent miles traveled by away team
    final['distance_traveled'] = final.apply(calc_distance, axis=1)

    #Export file
    filename = '../data/cleaned_data.sav'
    pickle.dump(final, open(filename, 'wb'))
    print('Clean file exported to ../data/cleaned_data.sav')
    sys.exit()
