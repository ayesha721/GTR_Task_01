from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

query = "television"
file =0

driver.get(f"https://www.daraz.com.bd/catalog/?spm=a2a0e.tm80335411.search.5.735212f7H08WJV&q=television&_keyori=ss&clickTrackInfo=abId--379294__textId--7005515778755778082__score--1186.0__pvid--7915849b-1766-46da-99f5-abcf40e01305__matchType--1__matchList--1__listNo--3__inputQuery--tele__srcQuery--television__spellQuery--television__ctrScore--0.0__cvrScore--0.0&from=suggest_normal&sugg=television_3_1")
elems = driver.find_elements(By.CLASS_NAME, "Bm3ON")
print(f"{len(elems)} items found")
for elem in elems:
    info = elem.get_attribute("outerHTML")
    with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
        f.write(info)
        file+=1

time.sleep(2)
driver.close()