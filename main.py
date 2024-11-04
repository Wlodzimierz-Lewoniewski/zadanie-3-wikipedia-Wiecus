import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def get_category_articles(category_name):
    encoded_name = quote(category_name.replace(' ', '_'))
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{encoded_name}"
    print(f"Pobieranie URL kategorii: {url}")
    html = requests.get(url).text
    return url, html


def extract_article_links(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = [(a.get_text(), a['href']) for a in soup.find_all('a', href=True)
                if a['href'].startswith('/wiki/') and not any(
            excluded in a['href'] for excluded in ['/wiki/Pomoc:', '/wiki/Plik:'])][:2]
    return articles


def get_article(article_name):
    encoded_name = quote(article_name.replace(' ', '_'))
    url = f"https://pl.wikipedia.org/wiki/{encoded_name}"
    print(f"Pobieranie URL artykułu: {url}")
    html = requests.get(url).text
    return url, html


def extract_article_data(html):
    soup = BeautifulSoup(html, "html.parser")

    links = [(a.get_text(), a['href']) for a in soup.find_all('a', href=True)
             if a['href'].startswith('/wiki/')][:5]

    images = [img['src'] for img in soup.find_all('img', src=True)][:3]

    external_links = [a['href'] for a in soup.find_all('a', href=True)
                      if a['href'].startswith('http')][:3]

    categories = [a.get_text() for a in soup.find_all('a', href=True)
                  if a['href'].startswith('/wiki/Kategoria:')][:3]

    return {
        "links": links,
        "images": images,
        "external_links": external_links,
        "categories": categories
    }


category_name = input("Podaj nazwę kategorii na Wikipedii (np. Sport): ")
url, html = get_category_articles(category_name)

articles = extract_article_links(html)

for article_title, article_href in articles:
    print(f"\nDane dla artykułu: {article_title}")
    url, html = get_article(article_title)
    data = extract_article_data(html)

    print(f"Linki wewnętrzne: {data['links'] if data['links'] else 'Brak danych'}")
    print(f"URL-e obrazków: {data['images'] if data['images'] else 'Brak danych'}")
    print(f"Zewnętrzne linki: {data['external_links'] if data['external_links'] else 'Brak danych'}")
    print(f"Kategorie: {data['categories'] if data['categories'] else 'Brak danych'}")
