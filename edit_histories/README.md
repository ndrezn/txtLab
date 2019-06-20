# Search links

Amazon's books are sorted into lists by genre when using the search function to narrow books down by genre. The following is a complete list of base links for searches by genre on Amazon:

```
/Arts-Photography-Books/s?rh=n%3A1&page=
/Biographies-Memoirs-Books/s?rh=n%3A2&page=
/Business-Money-Books/s?rh=n%3A3&page=
/Calendars-Books/s?rh=n%3A3248857011&page=
/Christian-Books-Bibles/s?rh=n%3A12290&page=
/Computers-Technology-Books/s?rh=n%3A5&page=
/Cookbooks-Food-Wine-Books/s?rh=n%3A6&page=
/Crafts-Hobbies-Home-Books/s?rh=n%3A48&page=
/Education-Teaching-Books/s?rh=n%3A8975347011&page=
/Health-Fitness-Dieting-Books/s?rh=n%3A10&page=
/History-Books/s?rh=n%3A9&page=
/Humor-Entertainment-Books/s?rh=n%3A86&page=
/Law-Books/s?rh=n%3A10777&page=
/Lesbian-Gay-Bisexual-Transgender-Books/s?rh=n%3A301889&page=
/Literature-Fiction-Books/s?rh=n%3A17&page=
/Medical-Books/s?rh=n%3A173514&page=
/Mystery-Thriller-Suspense-Books/s?rh=n%3A18&page=
/Parenting-Relationships-Books/s?rh=n%3A20&page=
/Politics-Social-Sciences-Books/s?rh=n%3A3377866011&page=
/Religion-Spirituality-Books/s?rh=n%3A22&page=
/Romance-Books/s?rh=n%3A23&page=
/Science-Math-Books/s?rh=n%3A75&page=
/Science-Fiction-Fantasy-Books/s?rh=n%3A25&page=
/Self-Help-Books/s?rh=n%3A4736&page=
/Sports-Outdoors-Books/s?rh=n%3A26&page=
/Teen-Young-Adult-Books/s?rh=n%3A28&page=
/Test-Preparation-Books/s?rh=n%3A5267710011&page=
/Travel-Books/s?rh=n%3A27&page=
/Action-Adventure-Literature-Fiction/s?rh=n%3A720360&page=
/African-American-United-States/s?rh=n%3A9823&page=
/Ancient-Medieval-Literature-Fiction/s?rh=n%3A5391236011&page=
/British-Irish-Literature-Fiction/s?rh=n%3A10016&page=
/Classics-Literature-Fiction/s?rh=n%3A10399&page=
/Contemporary-Literature-Fiction/s?rh=n%3A10129&page=
/Dramas-Plays-Literature-Fiction/s?rh=n%3A2159&page=
/Erotica-Literature-Fiction/s?rh=n%3A10141&page=
/Essays-Correspondence-Literature-Fiction/s?rh=n%3A10108&page=
/Genre-Fiction-Literature/s?rh=n%3A10134&page=
/Historical-Genre-Fiction/s?rh=n%3A10177&page=
/History-Criticism-Literature-Fiction/s?rh=n%3A10204&page=
/Humor-Satire-Literature-Fiction/s?rh=n%3A4465&page=
/Literary-Literature-Fiction/s?rh=n%3A10132&page=
/Mythology-Folk-Tales-Literature-Fiction/s?rh=n%3A5391238011&page=
/Poetry-Literature-Fiction/s?rh=n%3A10248&page=
/Short-Stories-Anthologies-Literature-Fiction/s?rh=n%3A10300&page=
/United-States-Literature-Fiction/s?rh=n%3A9822&page=
/Womens-Fiction-Literature/s?rh=n%3A542654&page=
/World-Literature-Fiction/s?rh=n%3A10311&page=
```

Using BeautifulSoup, links to each individual book can be pulled from the search result pages. The syntax below will generate a list of urls to each book where the initial URL is a base link from above with `https://amazon.com` concatonated at the beginning and an integer concatonated at the end. The integer endings start at 1 and can be increased as high as needed--each page of search results returns twenty or so books. 

For example, to get urls to the all "Mythology Folk Tales" books contained on the first page of results for that genre, the url would be `https://amazon.com/Mythology-Folk-Tales-Literature-Fiction/s?rh=n%3A5391238011&page=1`. This pattern extends to all genres and pages.


```python
books = []
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
soup = BeautifulSoup(response.content, 'lxml')

for b in soup.findAll('a', attrs={'class':'a-link-normal a-text-normal'}, href=True):
	b = str(b['href'])
	if 'https://www.amazon.com/' not in b:
		b='https://www.amazon.com/'+b
	if (re.match(re.escape('/') +'product', b)):
		continue
	if (re.findall('stripbooks', b)):
		continue
	if (b in books):
		continue
	books.append(b)
```