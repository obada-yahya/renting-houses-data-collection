from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common import by
import time
DRIVER_PATH = "c:/development/chromedriver.exe"


headers = {
    "Accept-Language": "en-GB,en;q=0.9,ar-AE;q=0.8,ar;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                  " like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def repeat_request():
    url_website = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagi" \
                  "nation%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64481581640625%2C%22" \
                  "east%22%3A-122.22184218359375%2C%22south%22%3A37.633501230568804%2C%22north%22%3A37.91681026" \
                  "1970156%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22pr" \
                  "ice%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22val" \
                  "ue%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2" \
                  "C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue" \
                  "%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D" \
                  "%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
    content = requests.get(url_website, headers=headers)
    soup = BeautifulSoup(content.text, "html.parser")
    urls_temp = [format_urls(url) for url in soup.select("div.list-card-info a")]
    addresses_temp = [address.text for address in soup.select("div.list-card-info address")]
    prices_temp = [format_money(price.text) for price in soup.select("div.list-card-info div.list-card-price")]
    if len(urls_temp) == 0:
        urls_temp, addresses_temp, prices_temp = repeat_request()
    return urls_temp, addresses_temp, prices_temp


def format_money(money: str):
    if '+' in money:
        return money.split("+")[0]
    if '/mo' in money:
        return money.split("/mo")[0]


def format_urls(url):
    temp = url.get("href")
    if temp[:2] == '/b':
        temp = "https://www.zillow.com/" + temp
    return temp


urls, addresses, prices = repeat_request()
data = zip(addresses, prices, urls)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSeqCa0WfC5gVRjCj-d3yXxL5KU6Htj7w0sj4QwCsncoci1I9w/viewform")
time.sleep(2)
for address, price, url in list(data):
    t = driver.find_elements(by=by.By.CSS_SELECTOR, value='input[type="text"]')
    values = [address, price, url]
    for i in range(3):
        t[i].click()
        t[i].send_keys(values[i])
    driver.find_element(by=by.By.CSS_SELECTOR, value='div[role="button"]').click()
    driver.find_element(by=by.By.CSS_SELECTOR, value='a').click()

driver.quit()