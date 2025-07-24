# scraper.py

import httpx
from bs4 import BeautifulSoup
import json
from models import db, Quote
from app import app

BASE_URL = "https://quotes.toscrape.com"
quotes = []

def scrape_quotes():
    url = BASE_URL
    while len(quotes) < 100:
        response = httpx.get(url)
        if response.status_code != 200:
            print(f"Failed to load {url}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        quote_elements = soup.find_all('div', class_='quote')

        for element in quote_elements:
            text = element.find('span', class_='text').get_text()
            author = element.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in element.find_all('a', class_='tag')]

            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })

            if len(quotes) >= 100:
                break

        # Siguiente página
        next_button = soup.find('li', class_='next')
        if next_button:
            next_href = next_button.find('a')['href']
            url = BASE_URL + next_href
        else:
            break

def save_to_json():
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)
    print("✅ Quotes saved to quotes.json")

def save_to_db():
    with app.app_context():
        db.create_all()
        for item in quotes:
            new_quote = Quote(
                text=item['text'],
                author=item['author'],
                tags=",".join(item['tags'])
            )
            db.session.add(new_quote)
        db.session.commit()
        print("✅ Quotes saved to database")

if __name__ == "__main__":
    scrape_quotes()
    save_to_json()
    save_to_db()
