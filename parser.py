from multiprocessing import pool
from multiprocessing.dummy import Pool
from utils import *

from driver import DriverObjectManager
from dbclass import DataBaseManager, SQLCommands
import time
from datetime import datetime as dt


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Locators:
    """Локаторы для парсинга"""
    BASE_CARD = (By.CLASS_NAME, "kp-hc")
    SCROLL_ELEMENT = (By.CLASS_NAME, "review-dialog-list")
    CONTAINER_RAITING = (By.CLASS_NAME, "review-score-container")
    OPEN_CARD_REWIES = "//a[@role='button']/span"
    REVIEW = "gws-localreviews__google-review"
    RAITING = "*//span[@aria-hidden='true']"
    COUNT_REVIEWS = "*//span[@style='white-space:nowrap']"
    TEXT = "*//div[@style='vertical-align:top']/div"
    MORE_TEXT = "review-more-link"
    FULL_TEXT = "review-full-text"
    DATE_COMMENT = "dehysf"
    RAITING_REVIEW = "Fam1ne"
    SECTION_REVIEWS = (By.ID, "reviewSort")

            
class DataBaseToParser(DataBaseManager, SQLCommands):
    """Класс БД для опеределенного парсера"""
    def __init__(self):
       super().__init__()
    
    def insert_result_parse(self, sql:str, sql_review:str, data:dict, resurs:str):
        
        userid = next(iter(data.keys()))
        date_parse, raiting, count, comments = data[userid].values()
        self.execute(sql.format(resurs=resurs,date_parse=date_parse, raiting=raiting, count=count, userid=userid))
        
        for i in comments:
            self.execute(sql_review.format(*i))
             



class Parser(Locators, DriverObjectManager):
   name = "google"
   
   def __init__(self, *data_parser):
    super(DriverObjectManager, self).__init__()   
    #self.url_list = data_parser
   
   def count_like(self, l:int, element):
    """Получаем колличество лайков отзыва"""
    if l > 0:
        like = self.find_element(element,By.TAG_NAME, "button").text
        if like == 'Нравится':
            like = 0
        else:
            like = int(like)
    else:
        like = 0
    return like    
   
   def review_parsing(self,element, userid):
    '''Парсим отзыв'''
    date = date_comment(self.find_element(element, By.CLASS_NAME,self.DATE_COMMENT).text)
    rating = self.find_element(element, By.CLASS_NAME, self.RAITING_REVIEW).get_attribute("aria-label").split()[1]
    raiting = int(rating.split(",")[0])    
    author = self.find_elements(element,By.TAG_NAME, "a")[1].text
    text_list = self.find_elements(element, By.XPATH, self.TEXT) 
    dislike = 0
    full_text = self.find_element(element, By.CLASS_NAME, self.MORE_TEXT)
    
    if full_text is not None:    
        full_text.click()
        text = self.find_element(element,By.CLASS_NAME, self.FULL_TEXT).text    
    
    elif full_text is None:
        text = text_list[1].text
    
    like = self.count_like(len(text), element)    
    ("google",1,'Опубликован','test','test text','12.02.2022', 3, 0, 3, 21)
    review = ("google",1,"Опубликован", author,text,date,like,dislike, raiting, userid)
    
    if None not in review:
        return review    
    else:
        raise Exception(f"Результат не должен содержать None: {review}")
   
   def run(self, url:tuple):
    """Запуск парсера"""
    
    date_parse = dt.strftime(dt.now(), "%d.%m.%Y")
    self.get_url(url[1])
    card = self.load_element((By.XPATH, "*//div[@data-md='101']"))
    text = card.text.split("\n")
    
    
    #span = self.load_element(self.CONTAINER_RAITING)
    raiting = text[0]
    count = text[1].split(" ")[0]
    count = int(count)
    print(f"{raiting}-{count}")
    self.find_element(card, By.TAG_NAME, "a").click()
    '''card.find_element(
        By.XPATH,self.OPEN_CARD_REWIES).click()'''
    
    if self.load_element(self.SECTION_REVIEWS) is not None:
        scrol = self.load_element(self.SCROLL_ELEMENT)    
        result = self.scroll_element(scrol,self.REVIEW, count)
    else:
        raise Exception("Элемент не загрузился") 
    
    list_reviews = list(map(lambda i: self.review_parsing(i, url[0]), result))
    parse_result = {
            url[0]: {
                "date": date_parse,
                "raiting": raiting,
                "count_comments": count,
                "comments": list_reviews
            }
        }

    return  parse_result


    
def parsing_map(url):
    p = Parser()
    result = p.run(url)
    return result
   

if __name__ == '__main__':
    
    dbp = DataBaseToParser()
    list_url =[count_comment(i) for i in dbp.select_url(dbp.SELECT_URL)]
    name = Parser.name
    with Pool(processes=3) as p:
        data = p.map(parsing_map, list_url)
    
    for i in data:
        dbp.insert_result_parse(dbp.INSERT_RESULT,dbp.INSERT_COMMENTS, i, name)
    
    dbp.connect.close()


    



 