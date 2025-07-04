import datetime
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

def generate_exel(data:dict[str:str]) -> None:
    dataframe = pd.DataFrame(data=data)
    dataframe.to_excel(f"sectors_data_{datetime.date.today()}.xlsx", index=False)



def sector_instrument(div: str, pattern: str, find:str="market_cap") -> str:
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

def get_stock_name(a: str) -> str:
    soup = BeautifulSoup(str(a), "html.parser")
    stock_name = soup.find_all("span")[0].get_text(strip=True)
    return stock_name

def sector_wise_stocks(sector_info: dict[str:str]) -> list[str]:
    stocks = []
    response = requests.get(sector_info["link"])
    soup = BeautifulSoup(response.text, "html.parser")
    all_stocks = soup.find_all("a",class_=re.compile("sectors__"))
    for stock in all_stocks:
        stocks.append(get_stock_name(stock))
    return stocks



def sector_wise_scrap(url: str) -> None:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    sectors_dict = sector_info(soup=soup, link=url)
    stocks= sector_wise_stocks(sectors_dict[1])
    print(stocks)
    # generate_exel(sectors_dict)


def main():
    sector_wise_scrap(url="https://www.moneycontrol.com/markets/sector-analysis/")

if __name__ == "__main__":
    main()
