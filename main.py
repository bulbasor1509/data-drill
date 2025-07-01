import re
from http.client import responses

import requests
from bs4 import BeautifulSoup

def sector_market_cap(div: str, pattern: str) -> str:
    market_cap_div = div.find("div", class_=re.compile(pattern))
    soup = BeautifulSoup(str(market_cap_div), "html.parser")
    market_cap = soup.find_all("span")[0].get_text(strip=True)
    return market_cap

def sector_price_to_earnings(div: str, pattern: str) -> str:
    price_to_earnings_div = div.find("div", class_=re.compile(pattern))
    print(price_to_earnings_div)

def sector_instrument(div: str, pattern: str, find:str="market_cap") -> str:
    # instrument_div = div.find("div", class_=re.compile(pattern))
    soup = BeautifulSoup(str(div), "html.parser")
    instrument = soup.find_all("span")[0].get_text(strip=True)
    if find != "market_cap":
        instrument = soup.find_all("span")[1].get_text(strip=True)
    return instrument


def sector_info(soup: BeautifulSoup,link: str) -> list[str]:
    sectors = []
    anchors = soup.find_all("a", href=True)
    for a in anchors:
        if a.get("href").startswith(link) and a.find("div"):
            sector_link, sector = a.get("href"), a.get("href").split("/")[-2]
            sector_instruments = a.find_all("div", class_=re.compile("markCap_values__"))
            market_cap = sector_instrument(div=sector_instruments[0], pattern="values_")
            price_to_earning = sector_instrument(div=sector_instruments[2], pattern="values_", find="price_to_earning")
            if  sector!= "undefined":
                sector_info = {
                    "sector": sector,
                    "link": sector_link,
                    "market_cap": market_cap,
                    "price_to_earning": price_to_earning,
                }
                sectors.append(sector_info)
    return sectors

def sector_wise_scrap(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(sector_info(soup,url))

def main():
    sector_wise_scrap(url="https://www.moneycontrol.com/markets/sector-analysis/")

if __name__ == "__main__":
    main()
