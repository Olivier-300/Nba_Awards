# 🏀 NBA Awards

**NBA Awards** est un projet de scraping et d'analyse des statistiques des joueurs NBA afin de prédire les récompenses annuelles. L'application récupère et traite les données des joueurs de la saison régulière et des playoffs pour identifier les meilleurs joueurs dans différentes catégories.

## 📌 Fonctionnalités

- **Scraping des données** 🕵️‍♂️ : Récupération des statistiques des joueurs via l'API de la NBA.
- **Nettoyage et transformation** 🔄 : Harmonisation et structuration des données pour une analyse efficace.
- **Visualisation et analyse** 📊 : Exploration des tendances et des performances des joueurs.
- **Modélisation et prédiction** 🤖 : Utilisation d’algorithmes pour identifier les futurs gagnants des NBA Awards.

## 📂 Structure du projet

```plaintext
NBA_Awards/
│── scraping_pages/            # Scripts de scraping des statistiques NBA
│── players_stats.xlsx         # Fichier contenant les statistiques globales des joueurs
│── players_stats_regular.xlsx # Données des saisons régulières
│── players_stats_playoff.xlsx # Données des playoffs
│── scrap.ipynb                # Notebook Jupyter pour l'extraction et l'analyse des données
│── .gitattributes             # Configuration Git pour les fichiers spécifiques
```

## 🚀 Installation et Exécution

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/Olivier-300/Nba_Awards.git
   cd Nba_Awards
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Exécuter le notebook Jupyter**
   ```bash
   jupyter notebook scrap.ipynb
   ```

## 📊 Exemples de Données

| Joueur        | Équipe | PPG  | RPG  | APG  | Saison |
|--------------|-------|------|------|------|--------|
| LeBron James | LAL   | 27.2 | 7.4  | 7.8  | 2022-23 |
| Giannis A.   | MIL   | 31.1 | 11.5 | 5.7  | 2022-23 |
| J. Embiid    | PHI   | 33.1 | 10.2 | 4.2  | 2022-23 |

## 📈 Prédictions des NBA Awards

Les analyses permettent d’estimer les favoris pour les distinctions suivantes :
- **🏆 MVP (Most Valuable Player)**
- **🏀 Rookie of the Year**
- **🛡️ Defensive Player of the Year**
- **🌟 Sixth Man of the Year**
- **📈 Most Improved Player**

## 🎯 Objectifs du projet

- Développer un modèle robuste pour prédire les récompenses NBA.
- Fournir une interface intuitive pour explorer les statistiques des joueurs.
- Automatiser la collecte et la mise à jour des données NBA.

## 🔥 Contributions

Les contributions sont les bienvenues ! Si tu veux améliorer le projet, n’hésite pas à **ouvrir une issue** ou une **pull request**.

## 📜 Licence

Ce projet est sous licence **MIT**. Consulte le fichier [LICENSE](LICENSE) pour plus d’informations.
