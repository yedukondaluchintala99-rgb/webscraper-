import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


def initiate_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    
    project_folder = os.path.dirname(os.path.abspath(__file__))
    chrome_driver_path = os.path.join(project_folder, "chromedriver.exe")
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def find_text(element, xpath):
    try:
        return element.find_element('xpath', xpath).text.strip()
    except NoSuchElementException:
        return ""
    
def find_attr(element, xpath, attr):
    try:
        return element.find_element('xpath', xpath).get_attribute(attr)
    except NoSuchElementException:
        return ""

def main(url, retries=3):
    # Initialization of driver
    driver = initiate_driver(headless=True)
    driver.maximize_window()
    # Open a desired website
    driver.get(url)
    time.sleep(5)
    products_list = []
    #Extracting the products info from the suggested data fields
    products = driver.find_elements('xpath', '//div[@class="row"]//div[@class="product-wrapper card-body"]')
    for product in products:
        try:
            title = find_attr(product, './/h4/a[@class="title"]', 'title')
            price = find_text(product, './/h4/span[@itemprop="price"]')
            rating_reviews_nodes = product.find_elements('xpath', './/div[@class="ratings"]//p')
            rating_review_json = {'ratings':'', 'reviews_count':''}
            for rat_rev in rating_reviews_nodes:
                ratings = rat_rev.get_attribute('data-rating')
                if ratings:
                    rating_review_json.update({'ratings':ratings})
                reviews_count = rat_rev.find_element('xpath', './/span').text.strip()
                if reviews_count:
                    rating_review_json.update({'reviews_count':reviews_count})
            product_url = find_attr(product, './/h4/a[@class="title"]', 'href')
            description = ""
            if product_url:
                for attempt in range(retries):
                    try:
                        driver.execute_script("window.open(arguments[0]);", product_url)
                        #Switching to next window to extract description in suggested format
                        driver.switch_to.window(driver.window_handles[1])
                        wait = WebDriverWait(driver, 2)
                        description = wait.until(EC.presence_of_element_located(('xpath', '//p[@itemprop="description"]'))).text
                        break
                    except (TimeoutException, WebDriverException) as e:
                        time.sleep(1)
                        if attempt == retries - 1:
                            print("Skipping description after maximum retries.")
                            description = ""
                    finally:
                        if len(driver.window_handles) > 1:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])

            #Updating data to dict
            laptop_data = {}
            laptop_data['title'] = title
            laptop_data['price'] = price
            laptop_data['ratings'] = rating_review_json.get('ratings', '')
            laptop_data['reviews_count'] = rating_review_json.get('reviews_count', '')
            laptop_data['product_url'] = product_url
            laptop_data['description'] = description
            #Appending products dict to json
            products_list.append(laptop_data)
        except Exception as e:
            print(f"Skipping products listing page due to error: {e}")
        time.sleep(0.5)

    #Quitting the driver after extracting all the products data
    driver.quit()

    #Writing data in json format
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(products_list, f, ensure_ascii=False, indent=4)

# This ensures main() runs only when the script is executed directly
if __name__ == "__main__":
    url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'

    main(url)

