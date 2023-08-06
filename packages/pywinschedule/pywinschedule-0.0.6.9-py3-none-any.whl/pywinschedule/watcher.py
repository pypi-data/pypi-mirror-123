import time
import os
import sys
import subprocess
import signal
import json
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileModifiedEvent
from pywinschedule.config import HOME
from pathlib import Path
def json_load(f,encoding='utf-8',*args,**kwargs):
    import json
    with open(f,'r',encoding=encoding) as fp:
        return json.load(fp,*args,**kwargs)
def json_dump(obj,fp,encoding='utf-8',ensure_ascii=False,*args,**kwargs):
    import json
    with open(fp,'w',encoding=encoding) as f:
        json.dump(obj,f,ensure_ascii=ensure_ascii,*args,**kwargs)

def load_yaml(path):
    import yaml
    with open(path,encoding='utf-8') as f:
        return yaml.safe_load(f)
def dump_yaml(obj,path):
    import yaml
    with open(path,'w',encoding='utf-8') as f:
        yaml.dump(obj,f)

# 
# class IService:
#     def __init__(self):
#         self.config_path=Path(HOME)/'watcher-config.json'
#         self.lock_file=Path(HOME)/'watcher.lock'
#         self.socket_file=Path(HOME)/'watcher.socket'
#         if os.path.exists(self.config_path):
#             self.cfg=json_load(self.config_path)
#         else:
#             self.cfg={
#                 'watch_dirs':[]
#             }
#             json_dump(self.cfg,self.config_path)
#         self.observers={}
#     def start(self):
#         print('Start watching...')
#         for watch_dir in self.cfg['watch_dirs']:
#             watcher = Watcher(watch_dir)
#             o=watcher.start()
#             self.observers[watch_dir]=o
#     def stop(self):
#         print('Stop watching...')
#     def enable(self):
#         pass
#     def disable(self):
#         pass
# 
# class Service:
#     def __init__(self,name,root):
#         root=Path(root)
#         self.root=root
#         self.config_path=root/'%s-config.yaml'%(name)
#         self.lock_file=root/'%s.lock'%(name)
#         self.socket_file=root/'%s.socket'%(name)
#         if os.path.exists(self.config_path):
#             self.cfg=load_yaml(self.config_path)
#         else:
#             self.cfg=self.get_default_config()
#             dump_yaml(self.cfg,self.config_path)
#     def get_default_config(self):
#         return {}
#     def main(self):
#         while True:
#             time.sleep(1)
#             
#     def start(self):
#         print('Start watching...')
#         self.main()
#     def stop(self):
#         print('Stop watching...')
# 
#     def enable(self):
#         pass
#     def disable(self):
#         pass
# 
# 
# 







class Watcher(FileSystemEventHandler):
    def __init__(self,root_path:str):
        super(Watcher, self).__init__()
        self.root=root_path
        self.main_file=os.path.join(root_path,'main.py')
        self.process=None
    def run(self,file):
        if self.process:
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.process.pid))
        os.chdir(self.root)
        self.process=subprocess.Popen([sys.executable,file])
    def start(self):
        self.run(self.main_file)
        self.watch()
    def on_modified(self, event:FileModifiedEvent):
        print('Modified:',event.src_path)
        if event.src_path.endswith('.py') and os.path.samefile(event.src_path,self.main_file):
            self.run(event.src_path)
    def watch(self):
        observer = Observer()
        observer.schedule(self, self.root, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def demo():
    watcher = Watcher(r'D:\Projects\PythonProjects\pywinschedule\demo\run')
    watcher.start()

if __name__ == "__main__":
    demo()