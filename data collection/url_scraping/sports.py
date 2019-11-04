from bs4 import BeautifulSoup
import requests
import csv
import pandas


def get_meta():
    url = "https://en.wikipedia.org/wiki/List_of_popular_music_genres"
    # make soup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    start = soup.find('h2') # Start here
    genre = start.text.strip() # the main header
    subgenre = soup.find('h3').text.strip() # the subheader

    urls, titles, genres, subgenres = [],[],[],[]
    
    for nextSibling in soup.find_all():
        if nextSibling.name == 'h3':
            subgenre = nextSibling.text.strip()
        if nextSibling.name == 'h2':
            genre = nextSibling.text.strip()
            subgenre = ""
        if 'Contents' in genre or 'References' in genre or 'Navigation' in genre or 'See also' in genre:
            continue
        
        if nextSibling.name == 'ul':
            for li in nextSibling.findAll('li'):
                if li.find('ul'):
                    break
                try:
                    urls.append(li.a['href'])
                except:
                    continue
                titles.append(li.a.text)
                genres.append(genre[:-6])
                subgenres.append(subgenre[:-6])



    meta = pandas.DataFrame()
    meta['title'] = titles
    meta['url'] = urls
    meta['genre'] = genres
    meta['subgenres'] = subgenres

    return meta


def main():
    meta = get_meta()

    out = '/Users/ndrezn/OneDrive - McGill University/Github/txtLab/results/metadata/music.csv'

    meta.to_csv(out)


main()
