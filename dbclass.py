
from utils import Config

import asyncio
import asyncpg
import psycopg2
 

class BaseDB(object):
    def __init__(self) -> None:
        self.cfg = Config().get_config_db()



class DataBaseManager(BaseDB, object):
    
    def __init__(self) -> None:
        super().__init__()
        if self.cfg is None:
            self.cfg = Config().get_config_db()
        
        self.connect = psycopg2.connect(
            dbname=self.cfg['dbname'],user=self.cfg['user'],
            password=self.cfg['password'], host=self.cfg['host'], 
            port=self.cfg['port'])
        self.cursor = self.connect.cursor()
        self.connect.autocommit = True
    
    def execute(self, sql:str):
        self.cursor.execute(sql)    
    
    def select_url(self, sql):
        """Достаем url для парсинга"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def select_comments(self, sql,**kwargs):
        self.cursor.execute(sql.format(**kwargs))
        return self.cursor.fetchall()
    
    
    
        
class SQLCommands:
    """SQL команды SELECT, INSERT """
    SELECT_URL = "SELECT c.id, c.url_google, (SELECT comment_number FROM comments WHERE comment_key_id = c.id ORDER BY comment_number DESC LIMIT 1) FROM clients c WHERE c.status='active' AND c.url_google != 'url';"
    SELECT_COMMENTS = "SELECT comment_resurs, author_comment, text_comment FROM comments WHERE status_comment='Опубликован' AND comment_key_id={userid} AND comment_resurs='{resurs}';"
    INSERT_RESULT = "INSERT INTO {resurs}(date_parse, raiting, count_comments, table_key_id) VALUES ('{date_parse}','{raiting}', {count}, {userid});"
    INSERT_COMMENTS = "INSERT INTO comments (comment_resurs, comment_number, status_comment, author_comment, text_comment, date_comment, mylike, dislike,comment_stars, comment_key_id) VALUES('{}',{},'{}','{}','{}','{}',{},{},'{}',{});"


