import requests
from bs4 import BeautifulSoup
import html


def wiki_article(name):
    url = f'https://pl.wikipedia.org{name}'
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        content = []
        soup = BeautifulSoup(html_content, 'html.parser')
        main_div = soup.find("div", class_="mw-body-content")

        internal_links = [a['title'] for a in main_div.find_all('a', href=True)
                          if a['href'].startswith('/wiki/') and ':' not in a['href'][6:]][:5]

        content.append(" | ".join(internal_links))

        image_urls = [img["src"] for img in main_div.find_all("img") if '/wiki/' not in img['src']][:3]
        content.append(" | ".join(image_urls) if image_urls else "")

        refs_div = soup.find("div", class_="mw-references-wrap mw-references-columns") or \
                   soup.find("div", class_="do-not-make-smaller refsection")

        if refs_div:
            refs = refs_div.find_all("li")
            external_refs = [html.escape(a['href']) for ref in refs
                             for span in ref.find_all("span", class_="reference-text")
                             for a in span.find_all("a", href=True) if "http" in a['href']][:3]
            content.append(" | ".join(external_refs))
        else:
            content.append("")

        category_div = soup.find("div", class_="mw-normal-catlinks")
        category_list = [cat.text.strip() for cat in category_div.find('ul').find_all("a")[:3]]
        content.append(" | ".join(category_list))

        return content
    else:
        print("Błąd podczas pobierania strony:", response.status_code)


def main():
    term = input().replace(" ", '_')
    base_url = 'https://pl.wikipedia.org/wiki/Kategoria:'
    url = base_url + term
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        main_div = soup.find("div", class_="mw-category mw-category-columns")
        links = [link["href"] for link in main_div.find_all("a")[:2]]

        for link in links:
            for detail in wiki_article(link):
                print(detail)
    else:
        print("Błąd podczas pobierania strony:", response.status_code)


main()
