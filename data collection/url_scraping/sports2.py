from bs4 import BeautifulSoup
import requests
import csv
import pandas
import urllib
import re

def get_meta():
	html_page = urllib2.urlopen("https://arstechnica.com")
	soup = BeautifulSoup(html_page)
	for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
	    print(link.get('href'))


def main():
    meta = get_meta()

    out = '/Volumes/NATHAN/out/metadata/new_data/sports2.csv'

    meta.to_csv(out)


main()

