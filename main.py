from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from selenium.common.exceptions import WebDriverException

import pandas as pd
import lxml.html
import time
import datetime


def initialize_driver(address):
    """
    Function to initialize the webdriver with the specified address using Google Chrome.
    """
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    service = Service()
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument(f"--user-agent={agent}")

    link = "https://www.rappi.com.ar/restaurantes"

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)

    add_address(driver, address)
    select_category(driver)
    
    return driver

def add_address(driver, address):
    """
    Function to add the given address in the input field on the website to retrieve the restaurant details.
    """
    adress_click = driver.find_element(By.XPATH, '//*[@id="rappi-web-toolbar"]/div[2]/div/div/div')
    adress_click.click()
    time.sleep(2)

    address_input = driver.find_element(By.XPATH, '//div[@class="chakra-input__group css-4302v8"]/input')
    address_input.send_keys(address)
    time.sleep(2)

    choice_click = driver.find_element(By.XPATH, '//li[@class="sc-hAZoDl FcjuD sc-ikZpkk fpunMk"]/button')
    choice_click.click()
    time.sleep(2)

    confirm_click = driver.find_element(By.XPATH, '//div[@class="css-ldo4d5"]/button')
    confirm_click.click()
    time.sleep(2)

    save_click = driver.find_element(By.XPATH, '//div[@class="css-ldo4d5"]/button')
    save_click.click()
    print("Direccion agregada")

def select_category(driver):
    """
    Function to select the category of restaurants on the website.
    """
    category = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[3]/div[3]/div/div/div/button[2]')
    category.click()
    time.sleep(4)
    print("Categoria Seleccionada")

def extract_data(driver):
    """
    Function to extract data like name, price, and link for each restaurant from the page source.
    """
    result = []
    time_list_raw = []
    time_list = []
    print("Extrayendo datos")
    content = driver.page_source
    doc = lxml.html.fromstring(content)
    title = doc.xpath('//h3[@class="sc-bxivhb bLhELA sc-189c7408-3 gnnFng"]')
    price = doc.xpath('//span[@class="sc-bxivhb dVvqfA sc-189c7408-6 ixXqkX"]')
    link = doc.xpath('//div[@class="sc-77e0e0c5-2 cLMlKB"]/a')
    times = doc.xpath('//span[@class="sc-bxivhb dVvqfA sc-189c7408-5 jeSkjq"]')

    for i in range(len(times)):
        time = times[i].text.strip()
        time_list_raw.append(time)
        time_list = time_list_raw[0::2]
        
    for i in range(len(title)):
        result.append(
                {
                "Nombre": title[i].text.strip(),
                "Tiempo": time_list[i],
                "Precio": price[i].text.strip(),
                "Link": link[i].get('href')
                }
                )
    return result

def save_results(result, address):
    """
    Function to save the extracted data into a CSV file with the specified address as the filename. '
    """
    df = pd.DataFrame(result)
    df.to_csv(f'{address}.csv', index=False)
    return df

if __name__ == "__main__":
    address = input("Ingrese la dirección: ")
    print("Abriendo navegador")
    start = datetime.datetime.now()
    driver = initialize_driver(address)
    extracted_data = extract_data(driver)
    df = save_results(extracted_data, address)
    print("Listo")
    #print(df)
    finish = datetime.datetime.now() - start
    print("Tiempo de ejecucion: ",finish)
    

# time = '//span[@class="sc-bxivhb dVvqfA sc-189c7408-5 jeSkjq"]'
#adress = "Malabia 500, capital federal"