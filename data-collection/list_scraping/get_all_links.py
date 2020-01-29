import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_links(soup):
    links = soup.findAll("a")
    hrefs = []
    for link in links:
        try:
            if (
                "cite" in link["href"]
                or "#" in link["href"]
                or "/wiki/" not in link["href"]
                or ":" in link["href"]
            ):
                continue
            hrefs.append(link["href"])
        except:
            continue
    return hrefs


def main():
    kind = "sports"

    big_df = pd.DataFrame()
    sports_urls = [
        "https://en.wikipedia.org/wiki/National_Football_League",
        "https://en.wikipedia.org/wiki/National_Hockey_League",
        "https://en.wikipedia.org/wiki/National_Basketball_Association",
        "https://en.wikipedia.org/wiki/Major_League_Baseball",
    ]
    science_urls = [
        "https://en.wikipedia.org/wiki/Biology",
        "https://en.wikipedia.org/wiki/Mathematics",
        "https://en.wikipedia.org/wiki/Physics",
        "https://en.wikipedia.org/wiki/Chemistry",
    ]

    if kind is "science":
        urls = science_urls
    else:
        urls = sports_urls
    for url in urls:
        df = pd.DataFrame()
        # make soup
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="html.parser")
        lst = get_links(soup)
        df["URL"] = lst
        print(len(lst))

        df["Type"] = url.split("/")[-1]
        big_df = big_df.append(df)
    big_df = big_df.reset_index(drop=True)

    big_df.to_csv(
        "/Users/ndrezn/OneDrive - McGill University/Github/txtLab/data collection/"
        + kind
        + ".csv"
    )


main()
