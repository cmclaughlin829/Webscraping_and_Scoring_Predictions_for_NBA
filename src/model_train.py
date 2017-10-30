"""
Module to create ridge regression model for nba scoring margin predictions
"""
import sys
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from settings import *
from utils import *


if __name__ == "__main__":
    data = import_pickle()
    print('Data Loaded')

    #Limit data set to only include 11th game of season or later for each team
    data = data[(data['home_game_season'] > 10) &
                 (data['away_game_season'] > 10)]

    #Remove unwanted columns and set X, y
    columns = list(data.columns.values)
    final_cols = [col for col in list(data.columns.values) if col not in removed_cols]
    X = data[final_cols].copy()
    y = data['score_margin'].copy()

    #Standardize X
    std_scaler = StandardScaler()
    X_scaled = std_scaler.fit_transform(X)

    #train, test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y,
                                                        test_size=0.3,
                                                        random_state=0)

    #Train ridge regression model
    alphas = 10**np.linspace(-2,4,50)
    model = RidgeCV(alphas=alphas, cv=8)
    model.fit(X_train, y_train)

    #Export fit model
    print('Model successfully fit')
    filename = '../models/fit_model.sav'
    pickle.dump(model, open(filename, 'wb'))
    print('Fit model exported to ../models/fit_model.sav')
    sys.exit()
