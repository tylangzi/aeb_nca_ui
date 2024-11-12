"""
driver驱动器
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class Driver():
    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9224")
        return webdriver.Chrome(options=chrome_options)



driver = Driver().get_driver()
