import pandas as pd
import requests
import numpy as np
import time
import logging
import os
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def setup_logging():
    logging.basicConfig(
        filename='files/scraper.log', 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def load_existing_data(output_file):
    if os.path.exists(f'files/{output_file}'):
        return pd.read_excel(f'files/{output_file}')
    return pd.DataFrame()

def get_seasons_since_2013():
    current_year = datetime.now().year
    seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(2013, current_year)]
    return seasons

def scrape_nba_stats(season_types, file_name):
    session = get_session()
    time_taken = time.time()
    existing_data = load_existing_data(file_name)
    years = get_seasons_since_2013()
    
    all_data = []
    for y in years:
        for s in season_types:
            url = f'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season={y}&SeasonType={s}&StatCategory=PTS'
            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()
                r = response.json()
                
                table_headers = r['resultSet']['headers']
                temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
                temp_df2 = pd.DataFrame({'Years': [y] * len(temp_df1), 'Season_Type': [s] * len(temp_df1)})
                temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
                
                all_data.append(temp_df3)
                logging.info(f'Successfully scraped {y} {s}')
            except requests.exceptions.RequestException as e:
                logging.error(f'Error scraping {y} {s}: {e}')
    
    if all_data:
        df_new = pd.concat(all_data, ignore_index=True)
        
        if not existing_data.empty:
            existing_data.set_index(["Years", "PLAYER"], inplace=True)
            df_new.set_index(["Years", "PLAYER"], inplace=True)
            
            updated_data = existing_data.combine_first(df_new)
            updated_data.reset_index(inplace=True)
        else:
            updated_data = df_new.reset_index()
        
        updated_data.to_excel(f'files/{file_name}', index=False)
        print(f"Player stats updated and saved to files/{file_name}")
    
    logging.info(f'Finished scraping in {round((time.time() - time_taken) / 60, 2)} minutes')

if __name__ == "__main__":
    setup_logging()
    season_types_regular = ['Regular%20Season']
    season_types_playoff = ['Playoffs']
    
    scrape_nba_stats(season_types_regular, 'players_stats_regular.xlsx')
    scrape_nba_stats(season_types_playoff, 'players_stats_playoff.xlsx')
