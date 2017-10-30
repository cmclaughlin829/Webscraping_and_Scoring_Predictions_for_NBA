"""
Settings Module
"""
#List of team abbreviations by season
teams_08 = ['ATL', 'NJN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
            'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
            'NOH', 'NYK', 'SEA', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
            'TOR', 'UTA', 'WAS']

teams_09_12 = [team for team in teams_08 if team != 'SEA']
teams_09_12.append('OKC')

teams_13 = [team for team in teams_09_12 if team != 'NJN']
teams_13.append('BRK')

teams_14 = [team for team in teams_13 if team != 'NOH']
teams_14.append('NOP')

teams_15_17 = [team for team in teams_14 if team != 'CHA']
teams_15_17.append('CHO')

all_teams = list(set(teams_08+teams_09_12+teams_13+teams_14+teams_15_17))

#List of regular statistics columns
columns = ['game_season', 'date_game', 'game_location', 'opp_id',
            'game_result', 'pts', 'opp_pts', 'fg', 'fga', 'fg_pct',
            'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'trb',
            'ast', 'stl', 'blk', 'tov', 'pf', 'opp_fg', 'opp_fga',
            'opp_fg_pct', 'opp_fg3', 'opp_ft', 'opp_fta', 'opp_ft_pct',
            'opp_orb', 'opp_trb', 'opp_ast', 'opp_stl', 'opp_blk',
            'opp_tov', 'opp_pf']

#List of advanced statistics columns
advanced_columns = ['off_rtg', 'def_rtg', 'pace', 'fta_per_fga_pct',
                    'fg3a_per_fga_pct', 'ts_pct', 'trb_pct', 'ast_pct',
                    'stl_pct', 'blk_pct', 'efg_pct', 'tov_pct',
                    'orb_pct', 'ft_rate', 'opp_efg_pct', 'opp_tov_pct',
                    'drb_pct', 'opp_ft_rate']

additional_columns = ['team', 'season']

#List of columns to be removed when sorting by season and team
unwanted_columns = ['team', 'season', 'game_season', 'date_game', 'game_location',
                    'opp_id', 'game_result']

#Dict of home city for each team
cities = {'NJN':'Newark, New Jersey', 'NOP':'New Orleans, Louisiana',
          'NYK':'New York City, New York', 'CLE':'Cleveland, Ohio',
          'MIA':'Miami, Florida', 'DEN':'Denver, Colorado',
          'HOU':'Houston, Texas', 'LAL':'Los Angeles, California',
          'SAS':'San Antonio, Texas', 'DAL':'Dallas, Texas',
          'BOS':'Boston, Massachusetts', 'NOH':'New Orleans, Louisiana',
          'ATL':'Atlanta, Georgia', 'MIL':'Milwaukee, Wisconsin',
          'POR':'Portland, Oregon', 'CHO':'Charlotte, North Carolina',
          'MIN':'Minneapolis, Minnesota', 'GSW':'San Francisco, California',
          'LAC':'Los Angeles, California', 'UTA':'Salt Lake City, Utah',
          'OKC':'Oklahoma City, Oklahoma', 'BRK':'Brooklyn, New York',
          'CHI':'Chicago, Illinois', 'SAC':'Sacramento, California',
          'MEM':'Memphis Tennessee', 'PHI':'Philadelphia, Pennsylvania',
          'WAS':'Washington, D.C.', 'ORL':'Orlando, Florida',
          'IND':'Indianapolis, Indiana', 'CHA':'Charlotte, North Carolina',
          'PHO':'Phoenix, Arizona', 'DET':'Detroit, Michigan',
          'SEA':'Seattle, Washington', 'TOR':'Toronto, Ontario'}

#List of columns to be removed prior to training model
removed_cols = ['date_game', 'season', 'home_team', 'away_team',
                'home_game_season', 'home_pts', 'away_game_season',
                'away_date_game', 'away_pts', 'score_margin',
                'away_off_rtg_mean_last5', 'away_w_l_mean_last5',
                'home_lat_long', 'away_lat_long']
