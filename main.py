import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

CHROME_DRIVE_PATH = "./chromedriver.exe"
GOOGLE_FORM_URL = "https://forms.gle/CNjvhqsa5j5V6gXG8"

url_renting_list = "https://flatfy.ua/uk/search?currency=UAH&geo_id=1&is_without_" \
                   "fee=false&price_sqm_currency=UAH&section_id=2&sort=insert_time&sub_geo_id=28752"
response = requests.get(url=url_renting_list)
response.raise_for_status()
site = response.text
soup = BeautifulSoup(site, 'html.parser')

links = soup.find_all("a", "realty-preview__content-link")
list_of_links = ["https://flatfy.ua"+str(link.get('href')) for link in links if str(link.get('href')).startswith("/uk")]
list_of_links = list(dict.fromkeys(list_of_links))  # REMOVING DUPES

costs = soup.find_all("div", "realty-preview-price realty-preview-price--main")
list_of_cost = [cost.text.replace("Â\xa0", "").split(" ")[0] for cost in costs]
# There is probably better way to deal with this, but I'm tired

addresses = soup.find_all("a", "realty-preview-title__link")
list_of_address = [address.text.encode("l1").decode() for address in addresses]     # Decoding Dragon Language lol

time.sleep(1)

driver = webdriver.Chrome(service=Service(CHROME_DRIVE_PATH))
driver.get(GOOGLE_FORM_URL)
time.sleep(2)

for index in range(len(list_of_links)):
    one = driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    one.send_keys(list_of_address[index])
    two = driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    two.send_keys(list_of_cost[index])
    tree = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    tree.send_keys(list_of_links[index])
    button = driver.find_element(By.XPATH,
                                 '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    button.click()
    time.sleep(1)
    cont = driver.find_element(By.LINK_TEXT, "Надіслати іншу відповідь")
    cont.click()
    time.sleep(0.5)
