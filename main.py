import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def get_category_articles(category_name):
    encoded_name = quote(category_name.replace(' ', '_'))
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{encoded_name}"
    print(f"Pobieranie URL kategorii: {url}")
    html = requests.get(url).text
    return html


def extract_article_links(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/wiki/') and not a['href'].startswith('/wiki/Kategoria:'):
            articles.append((a.get_text(), a['href']))
            if len(articles) >= 2:
                break

    return articles


def get_article_data(article_url):
    full_url = f"https://pl.wikipedia.org{article_url}"
    print(f"Pobieranie URL artykułu: {full_url}")
    html = requests.get(full_url).text
    return html, full_url


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


category_name = input("Podaj nazwę kategorii na Wikipedii (np. Miasta na prawach powiatu): ")
category_html = get_category_articles(category_name)

articles = extract_article_links(category_html)

for article in articles:
    article_title, article_url = article
    article_html, article_full_url = get_article_data(article_url)

    data = extract_article_data(article_html)

    print(f"Dane dla artykułu: {article_full_url}")

    internal_links_output = ' | '.join([link[0] for link in data['links']]) if data['links'] else ''
    print(f"Linki wewnętrzne: {internal_links_output}")

    images_output = ' | '.join(data['images']) if data['images'] else ''
    print(f"URL-e obrazków: {images_output}")

    external_links_output = ' | '.join(data['external_links']) if data['external_links'] else ''
    print(f"Zewnętrzne linki: {external_links_output}")

    categories_output = ' | '.join(data['categories']) if data['categories'] else ''
    print(f"Kategorie: {categories_output}\n")
