import requests
from bs4 import BeautifulSoup

def extract_wikipedia_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    internal_links = []
    for a in soup.find_all('a', href=True):
        if '/wiki/' in a['href'] and ':' not in a['href'] and len(internal_links) < 5:
            internal_links.append((a.text, 'https://pl.wikipedia.org' + a['href']))

    image_urls = []
    for img in soup.find_all('img', src=True):
        if len(image_urls) < 3:
            image_urls.append('https:' + img['src'])

    external_links = []
    for a in soup.find_all('a', href=True):
        if 'http' in a['href'] and 'wikipedia.org' not in a['href'] and len(external_links) < 3:
            external_links.append(a['href'])

    categories = []
    for a in soup.find_all('a', href=True):
        if 'Kategorie:' in a['href'] and len(categories) < 3:
            categories.append(a.text)

    return internal_links, image_urls, external_links, categories

def main():
    category = input("Podaj kategorię (np. Matematyka): ")
    category_url = f'https://pl.wikipedia.org/wiki/Kategoria:{category.replace(" ", "_")}'
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for a in soup.find_all('a', href=True):
        if '/wiki/' in a['href'] and ':' not in a['href']:
            articles.append('https://pl.wikipedia.org' + a['href'])
            print(f"Found article: {a['href']}")
        if len(articles) == 2:
            break

    print(f"Found articles: {articles}")

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
