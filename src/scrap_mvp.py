import requests
import pandas as pd
from bs4 import BeautifulSoup
import unidecode

def format_name(name):
    """
    Formate les noms en respectant les majuscules et caractères spéciaux.
    Exemple: "nikola jokic" -> "Nikola Jokić"
    """
    name_parts = name.split()
    formatted_name = " ".join([part.capitalize() for part in name_parts])
    
    # Gestion manuelle des cas spéciaux comme "Jokić"
    special_names = {
        "Jokic": "Jokić",
        "Joel Embiid": "Joel Embiid"
    }
    
    formatted_name = " ".join([special_names.get(part, part) for part in formatted_name.split()])
    return formatted_name

def scrape_mvp_winners(output_file):
    url = "https://www.nba.com/news/history-mvp-award-winners"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    mvp_data = []
    content_div = soup.find('div', class_='ArticleContent_article__NBhQ8')
    if content_div:
        paragraphs = content_div.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and "-" in text:
                parts = text.split("-", 1)
                if len(parts) == 2:
                    season = parts[0].strip().split(" ")[0]  # Garder uniquement l'année
                    winner = " ".join(parts[1].split(" ")[1:]).split(',')[0].strip().replace("—", "").strip()  # Supprimer le numéro au début, les tirets et garder le nom
                    
                    # Correction du format du nom
                    winner = format_name(winner)
                    
                    if season.isdigit() and int(season) >= 2013:
                        mvp_data.append([season, winner])
    
    df = pd.DataFrame(mvp_data, columns=["Season", "MVP Winner"])
    df.to_excel(f'files/{output_file}', index=False)
    print(f"MVP data saved to files/{output_file}")

if __name__ == "__main__":
    scrape_mvp_winners("mvp_winners.xlsx")
