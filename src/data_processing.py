import pandas as pd
import os
import logging

def setup_logging():
    logging.basicConfig(
        filename='files/processing.log', 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def process_nba_data(input_file, output_file, mvp_file=None, team_file=None, include_mvp=True, include_w_pct=True):
    data = pd.read_excel(f'files/{input_file}')
    
    # Nettoyage des données
    data_cleaned = data.drop(columns=["RANK", "EFF"], errors='ignore')
    data_cleaned['Season'] = data_cleaned['Season'].astype(str)
    
    # Ajout du statut MVP si applicable (uniquement pour la saison régulière)
    if include_mvp and mvp_file:
        mvp_data = pd.read_excel(f'files/{mvp_file}')
        mvp_data['Season'] = mvp_data['Season'].astype(str)
        mvp_data['Season'] = mvp_data['Season'].apply(lambda x: f"{x}-{str(int(x)+1)[-2:]}")
        data_cleaned = data_cleaned.merge(mvp_data, left_on=['Season', 'PLAYER'], right_on=['Season', 'MVP Winner'], how='left')
        data_cleaned['MVP'] = data_cleaned['MVP Winner'].notna().astype(int)
        data_cleaned.drop(columns=['MVP Winner'], inplace=True)
    else:
        data_cleaned['MVP'] = 0  # Ajouter une colonne MVP avec 0 si non applicable
    
    # Ajout du pourcentage de victoire de l'équipe si applicable (uniquement pour la saison régulière)
    if include_w_pct and team_file:
        team_data = pd.read_excel(f'files/{team_file}')
        team_data['Season'] = team_data['Season'].astype(str)
        data_cleaned = data_cleaned.merge(team_data[['Season', 'Team', 'W_PCT']], left_on=['Season', 'TEAM'], right_on=['Season', 'Team'], how='left')
        data_cleaned.drop(columns=['Team'], inplace=True)
    else:
        data_cleaned['W_PCT'] = None  # Ajouter une colonne W_PCT vide si non applicable
    
    # Ajout de la saison actuelle si elle manque
    latest_season = "2024-25"
    if latest_season not in data_cleaned['Season'].unique():
        missing_season_data = data_cleaned.iloc[-1:].copy()
        missing_season_data['Season'] = latest_season
        missing_season_data['MVP'] = 0  # Aucune donnée MVP pour la saison en cours
        missing_season_data['W_PCT'] = None  # Pas encore de % victoire
        data_cleaned = pd.concat([data_cleaned, missing_season_data], ignore_index=True)
    
    # Extraction correcte de season_start_year
    data_cleaned['season_start_year'] = data_cleaned['Season'].str.extract(r'^(\d{4})').astype(float).astype('Int64')
    
    # Création des variables de changement de saison
    data_cleaned['PTS_next_season'] = data_cleaned.groupby('PLAYER_ID')['PTS'].shift(-1)
    
    data_cleaned.to_excel(f'files/{output_file}', index=False)
    print(f"Processed player stats saved to files/{output_file}")

if __name__ == "__main__":
    setup_logging()
    
    # Traitement des données de la saison régulière avec MVP et % de victoire de l'équipe
    process_nba_data('players_stats_regular.xlsx', 'processed_players_stats_regular.xlsx', 'mvp_winners.xlsx', 'team_standings.xlsx', include_mvp=True, include_w_pct=True)
    
    # Traitement des données des playoffs sans MVP ni % de victoire de l'équipe
    process_nba_data('players_stats_playoff.xlsx', 'processed_players_stats_playoff.xlsx', include_mvp=False, include_w_pct=False)
