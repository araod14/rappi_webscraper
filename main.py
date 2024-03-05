from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from selenium.common.exceptions import WebDriverException

import pandas as pd
import lxml.html
import time


adress = str(input("Ingrese la direccion: "))
#adress = "Malabia 500, capital federal"
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
service = Service()
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument(f"--user-agent={agent}")

link = "https://www.rappi.com.ar/restaurantes"

driver = webdriver.Chrome(service=service, options=options)
driver.get(link) #

#-----------------Adding cookies----------------
"""
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()
"""

#------------------Adding adrres-------------------
adress_click = driver.find_element(By.XPATH, '//*[@id="rappi-web-toolbar"]/div[2]/div/div/div')
adress_click.click()
time.sleep(2)

adress_input = driver.find_element(By.XPATH, '//div[@class="chakra-input__group css-4302v8"]/input')
adress_input.send_keys(adress)
time.sleep(2)

choice_click = driver.find_element(By.XPATH, '//li[@class="sc-hAZoDl FcjuD sc-ikZpkk fpunMk"]/button')
choice_click.click()
time.sleep(2)

confirm_click = driver.find_element(By.XPATH, '//div[@class="css-ldo4d5"]/button')
confirm_click.click()
time.sleep(2)

save_click = driver.find_element(By.XPATH, '//div[@class="css-ldo4d5"]/button')
save_click.click()

#--------------select category---------------
category = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[3]/div[3]/div/div/div/button[2]')
category.click()
time.sleep(4)

#-------------parser section----------------- 
result = []
# tite = '//h3[@class="sc-bxivhb bLhELA sc-189c7408-3 gnnFng"]'
# time = '//span[@class="sc-bxivhb dVvqfA sc-189c7408-5 jeSkjq"]'
# price = '//span[@class="sc-bxivhb dVvqfA sc-189c7408-6 ixXqkX"]'
content = driver.page_source
doc = lxml.html.fromstring(content)
title = doc.xpath('//h3[@class="sc-bxivhb bLhELA sc-189c7408-3 gnnFng"]')
price = doc.xpath('//span[@class="sc-bxivhb dVvqfA sc-189c7408-6 ixXqkX"]')
link = doc.xpath('//div[@class="sc-77e0e0c5-2 cLMlKB"]/a')

#------------Results------------------------
for i in range(len(title)):
    result.append(
            {
            "Nombre": title[i].text.strip(),
            "Precio": price[i].text.strip(),
            "Link": link[i].get('href')
            }
            )
df = pd.DataFrame(result)
df.to_csv(f'{adress}.csv', index=False)

#stop = input("esto es para detener",)

print("Listo")
print(df)