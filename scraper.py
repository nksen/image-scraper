# scraper.py
# Naim Sen
# Apr 2020
# A simple script for scraping images from the web

### Imports ###
from pathlib import Path
from yarl import URL
from bs4 import BeautifulSoup
import requests
import sys


if __name__ == "__main__":
    BASE = URL("https://www.simonstalenhag.se/")
    try:
        ROOT = Path(sys.argv[1])
        if not ROOT.exists():
            print(f"{ROOT} does not exist")
    except:
        print(f"{sys.argv[1]} is not a valid path")
    DEST = ROOT / "stalenhag_imgs"
    DEST.mkdir()
    # load html into soup
    req = requests.get(str(BASE))
    soup = BeautifulSoup(req.content, 'html.parser')
    # print(soup.prettify())

    # get only img tags
    img_tags = soup.findAll('img')
    for tag in img_tags:
        # filter out gui images and 'detail' images
        if ("bilder/" in tag['src'] and
                not "detalj" in tag['src'] and
                not "text" in tag['src']):
            img_url = BASE / tag['src']
            with open(DEST / img_url.name, 'wb') as handler:
                print(f"Downloading: {img_url}")
                res = requests.get(img_url, stream=True)
                if not res.ok:
                    print(res)
                # iterate over the response and write non-null content
                for chunk in res.iter_content(1024):
                    if not chunk:
                        break
                    handler.write(chunk)
