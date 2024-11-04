import requests
from bs4 import BeautifulSoup

def get_wikipedia_search_results(query):
    search_url = f"https://pl.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    response = requests.get(search_url)
    return response.json()

def extract_wikipedia_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    internal_links = []
    for a in soup.select('a[href^="/wiki/"]:not([href*=":"])'):
        if len(internal_links) < 5:
            link_text = a.text.strip()
            link_url = 'https://pl.wikipedia.org' + a['href']
            if link_text and link_url not in [link[1] for link in internal_links]:
                internal_links.append((link_text, link_url))

    image_urls = []
    for img in soup.select('img'):
        if len(image_urls) < 3:
            img_src = img['src']
            if not img_src.startswith('http'):
                img_src = 'https:' + img_src
            image_urls.append(img_src)

    external_links = []
    for a in soup.select('a[href^="http"]:not([href*="wikipedia.org"])'):
        if len(external_links) < 3:
            external_links.append(a['href'])

    categories = []
    for a in soup.select('div#mw-normal-catlinks ul li a'):
        if len(categories) < 3:
            categories.append(a.text.strip())

    return internal_links, image_urls, external_links, categories

def main():
    category = input("Podaj kategorię (np. Miasta na prawach powiatu): ")
    search_results = get_wikipedia_search_results(category)
    articles = [f"https://pl.wikipedia.org/wiki/{result['title'].replace(' ', '_')}" for result in search_results['query']['search'][:2]]

    if not articles:
        print("No articles found.")
        return

    for article_url in articles:
        internal_links, image_urls, external_links, categories = extract_wikipedia_info(article_url)
        print(f"Article URL: {article_url}")
        print("Internal Links:")
        internal_links_text = " | ".join(f"{link_text} | {link_url}" for link_text, link_url in internal_links)
        print(internal_links_text if internal_links_text else "")
        print("Image URLs:")
        image_urls_text = " | ".join(image_urls)
        print(image_urls_text if image_urls_text else "")
        print("External Links:")
        external_links_text = " | ".join(external_links)
        print(external_links_text if external_links_text else "")
        print("Categories:")
        categories_text = " | ".join(categories)
        print(categories_text if categories_text else "")
        print("\n")

if __name__ == '__main__':
    main()
