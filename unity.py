from flask import Flask, render_template, request
import random
import requests as fetch
import requests
from bs4 import BeautifulSoup as beautifulSoup
import re

app = Flask(__name__)
order = []
i = 0

@app.route('/')
def index():
    global order
    global i #there are 22 projects, so i from 0-21 

    if request.method == 'GET':
        #randomize the 22 projects again in beginning or after one full pass
        if i == 0 or i == 22:
            order = random.sample(range(22), 22)
            i = 0
        else:
            i += 1
        
        return render_template('page.html', fetched = fetchData(order[i]))


def fetchData(index):
    info =  fetch.get('https://unity.com/madewith')
    soup = beautifulSoup(info.text, "lxml")

    link = soup.find_all('div',attrs={'class':'section-home-stories--item-image','style':True})
    images = []
    for count,pics in enumerate(link):
            images.append("https://unity.com"+re.findall("\('(/sites/.*)'\)",link[count]['style'])[0])
    
    projects = [proj.text for proj in soup.find_all('div', attrs={'class': 'section-home-stories--item-title'})]
    authors = [auth.text for auth in soup.find_all('div', attrs={'class': 'section-home-stories--item-studio'})]

    urls = []
    for links in soup.find_all('article'):
        urls.append("https://unity.com" + links.find('a').attrs['href'])

    page = fetch.get(urls[index])
    soup2 = beautifulSoup(page.text, "lxml")

    headers = [head.text for head in soup2.find_all('div', attrs={'class': 'title-large'})]
    texts = [txt.text for txt in soup2.find_all('div', attrs={'class': 'section-article-text'})]
    
    fetched = [
        {
            'project' : projects[index],
            'author' : authors[index],
            'link' : urls[index],
            'bg' : images[index],
            'h1' : headers[0],
            'h2' : headers[1],
            'h3' : headers[2],
            'h1text' : texts[0],
            'h2text' : texts[1],
            'h3text' : texts[2],
        }
    ]

    return fetched



if __name__ == '__main__':
	app.run()
