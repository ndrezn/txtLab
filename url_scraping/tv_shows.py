from bs4 import BeautifulSoup
import requests
import csv
from codecs import open


def url_collect():
    urls = []
    url = "https://en.wikipedia.org/wiki/List_of_American_television_programs"
    # make soup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    # add link to list

    for link in soup.find_all('a'):
        urls.append((link.get('href')))
    # clean
    urls.insert(0, 'urls')
    start = urls.index("/wiki/Wikipedia:FAQ/Categorization#Why_might_a_category_list_not_be_up_to_date?") + 1

    for url in urls:
        if "https://en.wikipedia.org/w/index.php?title=Category:" in url:
            end = urls.index(url)
            break

    return urls[start:end]


def title_collect():
    titles = []
    url = "https://en.wikipedia.org/wiki/List_of_American_television_programs"
    # make soup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    # add title to list
    for title in soup.find_all('a'):
        titles.append(title.text)
    # make ascii
    for title in titles:
        titles[titles.index(title)] = title.encode('ascii', 'ignore')
    # clean
    titles = titles[39:2526]
    titles.insert(0, 'titles')

    return titles


def main():
    urls = url_collect()
    titles = title_collect()

    urls_dir = '/Users/nathandrezner/OneDrive - McGill University/McGill/' \
               'txt Lab/r directory/csv_outputs/tv csvs/tv_urls.csv'
    titles_dir = '/Users/nathandrezner/OneDrive - McGill University/McGill/' \
                 'txt Lab/r directory/csv_outputs/tv csvs/tv_titles.csv'

    with open(urls_dir, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
        wr.writerow(urls)

    with open(titles_dir, 'wb') as myfile:
       wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
       wr.writerow(titles)


main()
