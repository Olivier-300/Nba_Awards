import pandas as pd
import os
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib

def setup_logging():
    logging.basicConfig(
        filename='files/processing.log', 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def train_mvp_model(data_file):
    data = pd.read_excel(f'files/{data_file}')
    
    # Sélection des features
    features = ["GP", "FG_PCT","AST", "STL", "BLK", "PTS", "W_PCT", "MIN", "FT_PCT", "FG3_PCT"]
    target = "MVP"
    
    # Suppression des lignes avec valeurs manquantes
    data = data.dropna(subset=features + [target])
    
    X = data[features]
    y = data[target]
    
    # Normalisation des données
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Séparation des données en train et test
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Entraînement du modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Évaluation
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    # Sauvegarde du modèle et du scaler
    joblib.dump(model, "files/mvp_model.pkl")
    joblib.dump(scaler, "files/mvp_scaler.pkl")
    print("Model and scaler saved.")

def predict_mvp(data_file, threshold=0.1):
    data = pd.read_excel(f'files/{data_file}')
    latest_season = "2024-25"
    
    # Charger le modèle et le scaler
    model = joblib.load("files/mvp_model.pkl")
    scaler = joblib.load("files/mvp_scaler.pkl")
    
    # Sélection des joueurs de la saison actuelle
    features = ["GP", "FG_PCT", "AST", "STL", "BLK", "PTS", "W_PCT", "MIN", "FT_PCT", "FG3_PCT"]
    data_current_season = data[data["Season"] == latest_season]
    
    if data_current_season.empty:
        print("No data available for the current season.")
        return
    
    X_current = data_current_season[features].dropna()
    X_current_scaled = scaler.transform(X_current)
    
    # Prédiction des probabilités
    predictions_proba = model.predict_proba(X_current_scaled)[:, 1]  # Probabilité d'être MVP
    data_current_season["MVP_Probability"] = predictions_proba
    
    # Sélection des candidats MVP avec une probabilité >= threshold
    predicted_mvp = data_current_season[data_current_season["MVP_Probability"] >= threshold]
    print("Predicted MVP Candidates:")
    print(predicted_mvp[["PLAYER", "PTS", "AST", "REB", "W_PCT", "MVP_Probability"]])
    
    return predicted_mvp

if __name__ == "__main__":
    setup_logging()
    train_mvp_model('processed_players_stats_regular.xlsx')
    predict_mvp('processed_players_stats_regular.xlsx', threshold=0.05)
