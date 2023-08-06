from pywinschedule.utils.sqlitekvstore import KeyValueStore
import datetime
class DBList:
    def __init__(self,path):
        self.kv=KeyValueStore(path)
    def commit(self):
        self.kv.commit()
    def close(self):
        self.kv.close()
    def clear(self):
        for key in self.kv.keys():
            self.remove(key)

    def list(self):
        return list(self.kv.keys())
    def add(self,record):
        self.kv[record]=datetime.datetime.now().isoformat()
    def remove(self,record):
        del self.kv[record]
    def contains(self,record):
        return record in self.kv.keys()