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
    
    # custom_settings = {
    #     'SCRAPEOPS_API_KEY': 'da0d3577-212c-40cc-8870-6f64ee7a3e22',
    #     'SCRAPEOPS_FAKE_USER_AGENT_ENABLED': True,
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'salla_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
    #     }
    # }
    
    start_urls = ['https://s.salla.sa/login']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Set to '--headless' to run Chrome in headless mode
        chrome_options.add_argument('--no-sandbox')  # May be required depending on your system configuration
        #chrome_options.add_argument('--disable-dev-shm-usage')  # May be required depending on your system configuration
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(10)
        username_input = self.driver.find_element(By.ID, 'login-email')
        password_input = self.driver.find_element(By.ID, 'login-password')
        
        username_input.send_keys('eyacleanproksaa@gmail.com')
        password_input.send_keys('Sally@Eyanew6869')
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(10)
        
        
        
        ######################### LOGIN DONE!!
        ########################################## GET DATA FROM CLIENT PAGE ##############
        
        feedback_url = 'https://s.salla.sa/orders'
                            
        self.driver.get(feedback_url)
        time.sleep(10)
        

        # Read the concatenated CSV file into a DataFrame
        concatenated_df = pd.read_csv('C:/Users/HP/Desktop/orders_v30.csv', encoding='utf-8-sig')
        
        # Extract the "urls" column as a list
        url_list = concatenated_df['URL'].tolist()
        
               
        print('........... Moving To the Final second page ...........')   
        
        phone_number = []
        page_url = []
        num = 0
        for url in url_list[:50000]:
            self.driver.get(url)
            time.sleep(1)
            
            
            print(num)
            num +=1
     
            
            # phone 
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, 'a.direct-phone') 
                phone = element.text 
                
                pattern = r'\+966\d{9}'
                # Find the phone number in the string using the regular expression pattern
                match = re.search(pattern, phone)
                
                if match:
                    # Extract the matched phone number
                    number = match.group()
                    phone_number.append(number)
                    
                else:
                    
                    phone_number.append(None)
            except:
                phone_number.append(None)
            
            # url
            page_url.append(url)
             
            
        data = zip(phone_number, page_url)

        
        # Write the data to the CSV file
        with open(self.csv_file, "a", encoding="utf-8-sig", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:  # Check if file is empty
            
                writer.writerow(["phone number" ,"url"])  # Write the header row
                
            writer.writerows(data)  # Write the data rows
        
        csvfile.close()
        print("Data saved successfully to orders_phones.csv")
    
    
            
     
            
        self.driver.quit()
    
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        