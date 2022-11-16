from datetime import datetime as dt, timedelta
import yaml


DATE = {
    "день" : 1,
    "дня": 1, 
    "дней":1,
    "месяц" : 30,
    "месяцев" : 30,
    "месяца" : 30,
    "год": 365,
    "года": 365,
    "лет" : 365
}

class BaseConfig(object):
    #Базовый класс конфигурации
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.cfg = yaml.load(f, Loader=yaml.Loader)


class Config(BaseConfig):
    #Методы  возвращают кофиги для необходимых ресурсов
    file_config = "config.yaml"
    
    def __init__(self):
        super().__init__(self.file_config)
    
    def get_config_db(self):
        """Получаем данные для подключения к БД"""
        return self.cfg['database']
    def get_config_proxy(self):
        """Получаем настйроки прокси"""
        return self.cfg['proxy']

def date_comment(string_date:str) -> str:
    #Преобразование строки даты в формат DD.MM.YYYY"""    
    try:
        if len(string_date) == 0:
            print("Необходимо передать параметры")
        period = string_date.split()
        days = get_number_of_days(period[0], period[1])
        if days is not None:
            date_review = dt.now() - timedelta(days=days)
            date_review = date_review.strftime("%d.%m.%Y")
        else:
            date_review = dt.now().strftime("%d.%m.%Y")
    except Exception:
        date_review = None
        raise TypeError("Передан не верный формат данных")       

    return date_review

def count_comment(args):
    if args[2] is None:
        args = args[0:2]+(0,)
    return args
    
def get_number_of_days(*args):
    #Получаем количество дней с моммента написани отзыва
    try:
        period = DATE[args[1]]
        days = int(args[0]) * period
    except KeyError:
        days = None     
    return days
