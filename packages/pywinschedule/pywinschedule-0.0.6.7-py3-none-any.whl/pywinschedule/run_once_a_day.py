from pywinschedule.utils.dbutils import DBList
import datetime
import os
from pywinschedule.config import HOME
DB_PATH=os.path.join(HOME,'run_once_a_day.db')

dblist=DBList(DB_PATH)
def run_if_have_not_been_run_today(func,tag):
    today=datetime.datetime.today().date().strftime('%Y-%m-%d')+'-'+tag
    if dblist.contains(today):
        return
    else:
        func()
        dblist.add(today)
        dblist.commit()


