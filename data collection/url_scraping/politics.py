import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"
# make soup
response = requests.get(url)
soup = BeautifulSoup(response.content, features="html.parser")

tables = soup.findAll('table',{'class':'wikitable sortable'})

reps = tables[2]

links = reps.findAll('a')

for link in links:
	try:
		print(link['href'])
	except:
		continue
