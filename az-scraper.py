import requests
import time
import re
from bs4 import BeautifulSoup as bs

# AZLyrics requires a user agent, otherwise it will close the connection immediately.
header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

# We'll ask for a main URL of an artist's page. 
# We will then get all song links from this site and start crawling. 
# Quite likely one can do this with AZLyrics's search and only require the artist from the user, but I'm lazy.
main = raw_input('Artist URL: ')
r = requests.get(main, headers=header)
html = r.content

# Let's get the links from the artist's main page.
links = bs(html, 'lxml')(id='listAlbum')[0]('a', href=True)

# And now let's construct our list of urls to crawl.
urls = []
for l in links:
    urls.append('https://www.azlyrics.com'+l['href'][2:])

# Get the lyrics.
words = []
for url in urls:
    print 'Getting: ' + url

    response = requests.get(url, headers=header)
    read_lyrics = response.content
    soup = bs(read_lyrics)

    # Perhaps to make it harder to scrape, AZLyrics doesn't add any class or id to their lyrics.
    lyrics = soup.find_all("div", attrs={"class": None, "id": None})[0].text.replace('\'','-')

    # Let's use a quick regex to get the words individually
    words.append(re.findall(r'[a-zA-Z\-]+', lyrics))

    # Sleep a bit. We don't want to crawl too fast. Not only out of good practice, but also because AZLyrics will also ban your IP for a while if you don't wait. Be patient.
    time.sleep(3)

# Flatten the list
words = [y.lower() for x in words for y in x]

# Export a CSV with the word count
import pandas as pd
import collections
count = collections.Counter(words)
dataset = pd.Series(count)
dataset.to_csv(raw_input('Save dataset as: '))

