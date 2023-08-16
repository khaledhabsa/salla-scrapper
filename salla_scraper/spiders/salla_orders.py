import scrapy
from scrapy import Spider
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from scrapy import  Request
from scrapy.http import TextResponse
import re
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv

class LoginSpider(Spider):
    name = 'salla_orders_1'
    csv_file = "orders_phones.csv"
    
    # ... (other settings and variables) ...
    
    start_urls = ['https://s.salla.sa/login']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(10)
        
        # ... (login logic) ...
        
        feedback_url = 'https://s.salla.sa/orders'
        self.driver.get(feedback_url)
        time.sleep(10)
        
        # Read the concatenated CSV file into a DataFrame
        concatenated_df = pd.read_csv('C:/Users/HP/Desktop/orders_v30.csv', encoding='utf-8-sig')
        url_list = concatenated_df['URL'].tolist()
        
        print('........... Moving To the Final second page ...........')
        
        for url in url_list[:50000]:
            self.driver.get(url)
            time.sleep(1)
            
            phone_number = None
            page_url = url
            
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, 'a.direct-phone') 
                phone = element.text 
                pattern = r'\+966\d{9}'
                match = re.search(pattern, phone)
                
                if match:
                    number = match.group()
                    phone_number = number
            except:
                pass
            
            with open(self.csv_file, "a", encoding="utf-8-sig", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if csvfile.tell() == 0:
                    writer.writerow(["phone number", "url"])
                writer.writerow([phone_number, page_url])
            
            print("Data saved for URL:", page_url)
    
        self.driver.quit()
