import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

def load_model():
    model_path = "files/mvp_model.pkl"
    scaler_path = "files/mvp_scaler.pkl"
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    return None, None

def predict_mvp(data_file, model, scaler, threshold=0.05):
    data = pd.read_excel(f'files/{data_file}')
    latest_season = "2024-25"
    
    features = ["GP", "FG_PCT", "AST", "STL", "BLK", "PTS", "W_PCT", "MIN", "FT_PCT", "FG3_PCT"]
    data_current_season = data[data["Season"] == latest_season]
    
    if data_current_season.empty:
        return pd.DataFrame()
    
    X_current = data_current_season[features].dropna()
    X_current_scaled = scaler.transform(X_current)
    
    predictions_proba = model.predict_proba(X_current_scaled)[:, 1]  # Probabilité d'être MVP
    data_current_season["MVP_Probability"] = predictions_proba
    
    predicted_mvp = data_current_season[data_current_season["MVP_Probability"] >= threshold]
    return predicted_mvp

def main():
    st.set_page_config(page_title="NBA MVP Prediction", layout="wide")
    st.title("🏀 NBA MVP Prediction Dashboard")
    
    model, scaler = load_model()
    if model is None or scaler is None:
        st.error("Le modèle n'est pas encore entraîné. Lancez le script de training avant de prédire.")
        return
    
    predicted_mvp = predict_mvp('processed_players_stats_regular.xlsx', model, scaler, threshold=0.05)
    predicted_mvp = predicted_mvp.sort_values(by="MVP_Probability", ascending=False)
    
    if predicted_mvp.empty:
        st.warning("Aucune donnée disponible pour la saison actuelle 2024-25.")
    else:
        st.subheader("📋 Liste des candidats MVP pour 2024-25")
        st.dataframe(predicted_mvp[["PLAYER", "PTS", "AST", "REB", "W_PCT"]])
        
        # Graphique de probabilité MVP
        st.subheader("📊 Probabilités de MVP des joueurs")
        fig, ax = plt.subplots()
        ax.barh(predicted_mvp["PLAYER"], predicted_mvp["PTS"], color='orange')
        ax.set_xlabel("PPG")
        ax.set_ylabel("Joueurs")
        ax.set_title("Probabilités MVP des joueurs pour 2024-25")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
