from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

# This is like your ID card when you visit a website. It tells the website what kind of device and browser you are using.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}


# The site that will be used for extraction.
url = "https://www.imdb.com/chart/top/"

# The print should be <Response [200]>, if something goes wrong, the headers must be incorrect
page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

scraped_movies = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-4929eaf6-0 DLYcv cli-parent')
movie_data = []
for html in scraped_movies:

    movie_dic = {}
    # Movie Name
    movie_name = html.find('h3', class_='ipc-title__text')
    movie_dic['Movie Name'] = movie_name.text.strip() if movie_name else 'unknown movie name'

    # Release Date
    rel_date = html.find('span', class_='sc-5bc66c50-5 hVarDB cli-title-metadata')
    movie_dic['Release Date'] = rel_date.text.strip() if rel_date else 'unknown release date'

    # Duration
    duration = html.find_all('span', class_='sc-5bc66c50-6 OOdsw cli-title-metadata-item')[1]
    movie_dic['Duration'] = duration.text.strip() if duration else 'unknown duration'


    # Rating
    rating = html.find('span', class_='ipc-rating-star')['aria-label'].split()[-1]
    movie_dic['Rating'] = rating if rating else 'unknown rating'

    # Viewers
    viewers = html.find('span', class_='ipc-rating-star--voteCount')
    viewers = viewers.text.strip()
    viewers = re.match(r'\(([\d.]+[MK]?)\)', viewers)
    movie_dic['Viewers'] = viewers.group(1) if viewers else 'unknown viewers'
    movie_data.append(movie_dic)

data = pd.DataFrame(movie_data)
print(data)
