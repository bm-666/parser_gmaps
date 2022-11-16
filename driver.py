from proxy import background_js, manifest_json

import time
import zipfile

from selenium.webdriver import chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.common import desired_capabilities, keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver



class Webdriver:
    width=1366
    height=844
    
    def __init__(self, browser="chrome", proxy=False):
        options_chrome = webdriver.ChromeOptions()
        if proxy:
            plugin = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(plugin, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            options_chrome.add_extension(plugin)
        options_chrome.add_argument('--headless')
        options_chrome.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options_chrome)
        self.driver.set_window_size(self.width,self.height)

class DriverObjectManager(Webdriver):
    
    def __init__(self):
        super().__init__()

    def get_url(self, url):
        #Загружаем url
        self.driver.get(url)
    
    def load_element(self, locator, timeout=40):
        #Ожидаем зарузки элемента на странице
        try:
            element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))
        except Exception as e:
            print("Ошибка в переданных параметрах:\n{}".format(locator))
            element = None
        return element
    
    def load_elements(self, locator, timeout=40):
        #Ожидаем зарузки элементов
        try:
            elements = elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        
        except Exception as e:
            print("Ошибка в переданных параметрах")
            elements = None

    def find_element(self, parent, type_search,  locator):
        #Поиск елементов внутри родителя
        try:
            element = parent.find_element(type_search, locator)
        except Exception as err:
            element = None
        return element
    
    def find_elements(self, parent, type_search,  locator):
        #Поиск всех елементов внутри родителя
        try:
            elements = parent.find_elements(type_search,locator)
        except Exception as e:
            elements = None
        return elements   
    
    
    def scroll_element(self, scroll, locator:str, count_reviews:int):
        #Скрол динамических отзывов
        elements = set()        
        if scroll is not None:
            coord = 0
            while len(elements) < count_reviews:
                coord = coord + 500
                self.driver.execute_script(
                    f"document.querySelector('.review-dialog-list').scrollTo(0, {coord});")               
                
                if self.find_elements(scroll, By.CLASS_NAME, locator) is None:
                    self.find_elements(scroll, By.CLASS_NAME, locator)
                el = {i for i in self.find_elements(scroll, By.CLASS_NAME, locator)}
                
                elements = elements.union(el)
            
        else:
            return ""    
        return elements
    



