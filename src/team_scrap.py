import pandas as pd
import requests
import time
import logging
import os
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        filename='files/team_scraper.log', 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_session():
    session = requests.Session()
    return session

def load_existing_data(output_file):
    if os.path.exists(f'files/{output_file}'):
        return pd.read_excel(f'files/{output_file}')
    return pd.DataFrame(columns=["Season", "Team", "W_PCT"])

def get_seasons_since_2013():
    current_year = datetime.now().year
    seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(2013, current_year)]
    return seasons

def abbreviate_team_name(team_name):
    team_abbreviations = {
        "Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Brooklyn Nets": "BKN",
        "Charlotte Hornets": "CHA",
        "Charlotte Bobcats": "CHA",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "Los Angeles Clippers": "LAC",
        "LA Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHX",
        "Portland Trail Blazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTA",
        "Washington Wizards": "WAS"
    }
    return team_abbreviations.get(team_name, team_name)  # Retourne l'abréviation ou le nom original si non trouvé

def scrape_nba_team_standings(output_file):
    base_url = "https://stats.nba.com/stats/leaguestandingsv3"
    session = get_session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive",
        "Referer": "https://www.nba.com/stats/standings/",
        "x-nba-stats-origin": "stats"
    }
    team_data = []
    
    existing_data = load_existing_data(output_file)
    existing_seasons = set(existing_data["Season"].astype(str) + existing_data["Team"])
    seasons = get_seasons_since_2013()
    
    for year in seasons:
        params = {
            "GroupBy": "conf",
            "LeagueID": "00",
            "Season": year,
            "SeasonType": "Regular Season",
            "Section": "overall"
        }
        attempts = 0
        success = False
        
        while attempts < 5 and not success:
            try:
                response = session.get(base_url, headers=headers, params=params, timeout=15)
                
                if response.status_code == 200 and response.text.strip():
                    try:
                        data = response.json()
                    except ValueError:
                        print(f"Non-JSON response received for {year}:", response.text[:500])
                        raise ValueError("Server returned non-JSON response")
                    
                    headers_list = data['resultSets'][0]['headers']
                    rows = data['resultSets'][0]['rowSet']
                    
                    team_city_index = headers_list.index("TeamCity")
                    team_name_index = headers_list.index("TeamName")
                    win_pct_index = headers_list.index("WinPCT")
                    
                    for row in rows:
                        team_city = row[team_city_index]
                        team_name = row[team_name_index]
                        win_pct = row[win_pct_index]
                        team_full_name = f"{team_city} {team_name}"
                        team_abbr = abbreviate_team_name(team_full_name)
                        unique_key = f"{year}{team_abbr}"
                        
                        if unique_key not in existing_seasons:
                            team_data.append([year, team_abbr, win_pct])
                    
                    logging.info(f'Successfully scraped data for {year}')
                    success = True
                else:
                    raise ValueError("Empty or invalid response from server")
            except (requests.exceptions.RequestException, ValueError) as e:
                attempts += 1
                wait_time = attempts * 10  # Attente progressive
                logging.error(f'Error scraping {year} (attempt {attempts}): {e}, retrying in {wait_time} seconds')
                time.sleep(wait_time)
        
    df_new = pd.DataFrame(team_data, columns=["Season", "Team", "W_PCT"])
    df_combined = pd.concat([existing_data, df_new], ignore_index=True)
    df_combined.to_excel(f'files/{output_file}', index=False)
    print(f"Team standings updated and saved to files/{output_file}")

if __name__ == "__main__":
    setup_logging()
    scrape_nba_team_standings("team_standings.xlsx")
