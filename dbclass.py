
from utils import Config

import psycopg2
 

class BaseDB(object):
    # концигурации к БД
    def __init__(self) -> None:
        self.cfg = Config().get_config_db()



class DataBaseManager(BaseDB, object):
    #класс операциямий с бд
    def __init__(self) -> None:
        super().__init__()
        if self.cfg is None:
            self.cfg = Config().get_config_db()
        #получаем коннект курсор
        self.connect = psycopg2.connect(
            dbname=self.cfg['dbname'],user=self.cfg['user'],
            password=self.cfg['password'], host=self.cfg['host'], 
            port=self.cfg['port'])
        self.cursor = self.connect.cursor()
        self.connect.autocommit = True
    
    def execute(self, sql:str):
        #выолнение команд не требуищих возврата данных
        self.cursor.execute(sql)    
    
    def select_url(self, sql):
        #Достаем url для парсинга
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def select_comments(self, sql,*args):
        #Выбираем отзывы
        self.cursor.execute(sql.format(*args))
        return self.cursor.fetchall()
            
class SQLCommands:
    #SQL команды select, insert, update
    SELECT_URL = "SELECT c.id, c.url_google, (SELECT comment_number FROM comments WHERE comment_key_id = c.id ORDER BY comment_number DESC LIMIT 1) FROM clients c WHERE c.status='active' AND c.url_google != 'url';"
    SELECT_COMMENTS = "SELECT comment_resurs, author_comment, text_comment FROM comments WHERE status_comment='Опубликован' AND comment_key_id={} AND comment_resurs='{}';"
    INSERT_RESULT = "INSERT INTO {resurs}(date_parse, raiting, count_comments, table_key_id) VALUES ('{date_parse}','{raiting}', {count}, {userid});"
    INSERT_COMMENTS = "INSERT INTO comments (comment_resurs, comment_number, status_comment, author_comment, text_comment, date_comment, mylike, dislike,comment_stars, comment_key_id) VALUES('{}',{},'{}','{}','{}','{}',{},{},'{}',{});"
    UPDATE_COMMENTS = "UPDATE comments SET status_comment='Удален', date_delete='{}' WHERE comment_resurs='{}' AND author_comment='{}' AND text_comment='{}'"


