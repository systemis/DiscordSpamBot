import os.path
import time
from selenium import webdriver 

chrome_driver_path = '/Users/thinh/Downloads/chromedriver';
driver = webdriver.Chrome(chrome_driver_path)
driver.get("https://www.discord.com")

driver.execute_script("window.scrollTo(0, 300)") 

time.sleep(200)
