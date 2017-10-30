"""
Utilities module
"""
import pandas as pd
import numpy as np
import pickle
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from settings import *

def import_pickle():
    """
    Function to import pickled files
    """
    x = input('enter file name ')
    data = pickle.load(open("../data/{}".format(x), 'rb'))
    return data

def read_raw():
    """
    Function to read in csv exported from nba_scrape.py
    """
    x = input('enter file name ')
    df = pd.read_csv("../data/{}".format(x), index_col=0)
    return df

def initial_clean(df):
    """
    Function to provide initial cleaning of raw data
    """
    df.date_game = pd.to_datetime(df.date_game, infer_datetime_format = True)
    df['w_l'] = np.where(df['game_result'] == 'W', 1, 0)
    return df

def expanding_means(df, groups, unwanted_cols):
    """
    Function to create expanding means features by season and team
    """
    df = df.sort_values(groups, ascending=[True, True])
    cols = [col for col in list(df.columns) if col not in unwanted_cols]
    for col in cols:
        df[col+'_mean']=df.groupby(groups)[col].transform(lambda x: x.expanding().mean().shift(1))
    return df

def rolling_window_mean(df, column_list, width):
    """
    Function to create features to account for performance over previous n
    games
    """
    for column in column_list:
        df[column+'_last5']=df.groupby(['season', 'team'])[column].transform(lambda x: x.rolling(window=width).mean().shift(1))
    return df

def calc_distance(df):
    """
    Function to create feature showing distance traveled by away team (miles)
    """
    return vincenty(df['home_lat_long'], df['away_lat_long']).miles

def create_schedule(df):
    """
    Function to create nba schedule dataframe
    """
    df['home_team'] = np.where(df['game_location'] == '@', df['opp_id'],
                      df['team'])
    df['away_team'] = np.where(df['game_location'] == '@', df['team'],
                      df['opp_id'])
    df.drop(['team', 'game_location', 'opp_id'], axis=1, inplace=True)
    df.drop_duplicates(inplace=True)
    return df
