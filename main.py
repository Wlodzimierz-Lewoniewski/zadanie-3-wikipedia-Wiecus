import requests
from bs4 import BeautifulSoup


def fetch_article_data(article_url):
    response = requests.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    internal_links = []
    for a in soup.select('a[href^="/wiki/"]'):
        if len(internal_links) < 5 and "Kategoria:" not in a['href']:
            internal_links.append(f"{a.text} | https://pl.wikipedia.org{a['href']}")

    images = []
    for img in soup.select('img'):
        if len(images) < 3:
            images.append(f"https://upload.wikimedia.org{img['src']}")

    external_links = []
    for a in soup.select('a.external'):
        if len(external_links) < 3:
            external_links.append(a['href'])

    categories = []
    for a in soup.select('a[title^="Kategoria:"]'):
        if len(categories) < 3:
            categories.append(a.text)

    return {
        'internal_links': internal_links,
        'images': images,
        'external_links': external_links,
        'categories': categories
    }


def main():
    search_query = input("Podaj kategorię (np. 'Miasta na prawach powiatu'): ")
    category_url = f"https://pl.wikipedia.org/wiki/Kategoria:{requests.utils.quote(search_query)}"

    response = requests.get(category_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    article_links = soup.select('.mw-category-group a')[:2]

    if not article_links:
        print("Nie znaleziono artykułów w tej kategorii.")
        return

    for article_link in article_links:
        article_url = f"https://pl.wikipedia.org{article_link['href']}"
        article_data = fetch_article_data(article_url)

        output_lines = []
        output_lines.append(f"Article URL: {article_url}")
        output_lines.append(
            "Internal Links:\n" + "\n".join(article_data['internal_links']) if article_data['internal_links'] else "")
        output_lines.append("Image URLs:\n" + "\n".join(article_data['images']) if article_data['images'] else "")
        output_lines.append(
            "External Links:\n" + "\n".join(article_data['external_links']) if article_data['external_links'] else "")
        output_lines.append(
            "Categories:\n" + "\n".join(article_data['categories']) if article_data['categories'] else "")

        print("\n".join(output_lines))
        print("\n" + "-" * 40 + "\n")  # Separator between articles


if __name__ == "__main__":
    main()
