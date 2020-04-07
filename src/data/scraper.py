from bs4 import BeautifulSoup
import requests
import re

def scrape_poems():

    get_urls = requests.get("https://www.poesie-francaise.fr/poemes-charles-baudelaire/")

    soup_url = BeautifulSoup(get_urls.text, "html.parser")

    links = []

    for link in soup_url.findAll('a', attrs={'href': re.compile("^https://www.poesie-francaise.fr/charles-baudelaire/")}):
        links.append(link.get('href'))

    extracted_poems = []
    for link in links:
        source = requests.get(link)
        soup = BeautifulSoup(source.text, "html.parser")

        title = soup.find("h2", class_="titrepoeme").text.strip().replace("Titre : ", "")
        poem = soup.find("div", class_="postpoetique").find("p")
        list_changes = {"<br/>": "\n", "<p>": "", "</p>": "", "<span class=\"decalage28\"></span>": "",\
                    "<span class=\"decalage11\"></span>": "", "<span class=\"decalage12\"></span>": "",\
                    "<span class=\"decalage2\"></span>": "", "<span class=\"decalage16\"></span>": ""  }
        for i, j in list_changes.items():
            poem = str(poem).replace(i, j)
        extracted_poems.append(title)
        extracted_poems.append(poem)
    
    with open("/home/tdelatte/Projects/Deep_Learning/NLP/Baudelaire_Poem_Generator/data/raw/baudelaire.txt", "w") as f:
        for line in extracted_poems:
            f.write("%s\n" % line)
    
    print("Poems scraped from the web!")