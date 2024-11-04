import requests
from bs4 import BeautifulSoup

def extract_wikipedia_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    internal_links = []
    for a in soup.select('a[href^="/wiki/"]:not([href*=":"])'):
        if len(internal_links) < 5:
            internal_links.append((a.text.strip(), 'https://pl.wikipedia.org' + a['href']))

    image_urls = []
    for img in soup.select('img[src]'):
        if len(image_urls) < 3:
            image_urls.append('https:' + img['src'])

    external_links = []
    for a in soup.select('a[href^="http"]:not([href*="wikipedia.org"])'):
        if len(external_links) < 3:
            external_links.append(a['href'])

    categories = []
    for a in soup.select('a[href*="/wiki/Kategoria:"]'):
        if len(categories) < 3:
            categories.append(a.text.strip())

    return internal_links, image_urls, external_links, categories

def main():
    category = input("Podaj kategorię (np. Matematyka): ")
    category_url = f'https://pl.wikipedia.org/wiki/Kategoria:{category.replace(" ", "_")}'
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for a in soup.select('a[href^="/wiki/"]:not([href*=":"])'):
        articles.append('https://pl.wikipedia.org' + a['href'])
        if len(articles) == 2:
            break

    for article_url in articles:
        internal_links, image_urls, external_links, categories = extract_wikipedia_info(article_url)
        print(f"Article URL: {article_url}")
        print("Internal Links:")
        for link_text, link_url in internal_links:
            print(f"  Text: {link_text}, URL: {link_url}")
        print("Image URLs:")
        for url in image_urls:
            print(f"  {url}")
        print("External Links:")
        for url in external_links:
            print(f"  {url}")
        print("Categories:")
        for category in categories:
            print(f"  {category}")
        print("\n")

if __name__ == '__main__':
    main()
