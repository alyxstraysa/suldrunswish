import requests
import re

tree = ET.fromstring(requests.get(
    'https://myanimelist.net/sitemap/anime-000.xml').text)


for child in tree:
    url = child[0].text
    output = re.search('\d.*', url)[0]
    anime_id, anime_name = output.split("/")

    with open("officialmap.txt", "a+") as f:
        f.write(anime_id + " " + anime_name + "\n")
