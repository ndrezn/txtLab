## Generates a metadata sheet for Wikipedia's American Novels category

from bs4 import BeautifulSoup
import requests
import csv
from codecs import open


def urls_collect(soup):
    urls = []
    # add link to list
    for link in soup.find_all('a'):
        urls.append(str(link.get('href')))

    start = urls.index("/wiki/Wikipedia:FAQ/Categorization#Why_might_a_category_list_not_be_up_to_date?") + 1

    for url in urls:
        if "https://en.wikipedia.org/w/index.php?title=Category:" in url:
            end = urls.index(url)
            break

    return urls[start:end]


def titles_collect(soup):
    titles = []

    # add title to list
    for title in soup.find_all('a'):
        titles.append(title.text)
    # make ascii
    for title in titles:
        titles[titles.index(title)] = title.encode('ascii', 'ignore')

    start = titles.index("learn more") + 1

    for title in titles:
        if "https://en.wikipedia.org/w/index.php?title=Category:" in title:
            end = titles.index(title)
            break

    return titles[start:end]


def main():
    titles = ["titles"]
    urls = ["urls"]
    years = ["years"]

    for i in range(0, 217):
        # create url
        url = "https://en.wikipedia.org/wiki/Category:" + str(i+1801) + "_American_novels"
        print url
        # attack url
        response = requests.get(url)
        # check if real page
        if response.status_code != 200:
            continue
        # create soup for page
        soup = BeautifulSoup(response.content, features="html.parser")
        # add titles, urls, years
        titles_list = titles_collect(soup)
        titles.extend(titles_list)
        urls.extend(urls_collect(soup))

        for j in range(0, titles_list.__len__()):
            years.append(i+1801)

    urls_dir = '/Users/nathandrezner/OneDrive - McGill University/McGill/' \
               'txt Lab/r directory/csv_outputs/novels csvs/novels_urls.csv'
    titles_dir = '/Users/nathandrezner/OneDrive - McGill University/McGill/' \
                 'txt Lab/r directory/csv_outputs/novels csvs/novels_titles.csv'
    years_dir = '/Users/nathandrezner/OneDrive - McGill University/McGill/' \
                'txt Lab/r directory/csv_outputs/novels csvs/novels_years.csv'

    with open(urls_dir, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
        wr.writerow(urls)

    with open(titles_dir, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
        wr.writerow(titles)

    with open(years_dir, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
        wr.writerow(years)


main()