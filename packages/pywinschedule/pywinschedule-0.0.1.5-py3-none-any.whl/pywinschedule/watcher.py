import sys
import time
import logging
import os
import sys

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler,FileSystemEvent,FileModifiedEvent

class Watcher(FileSystemEventHandler):
    def __init__(self,root_path:str):
        super(Watcher, self).__init__()
        self.root=root_path
        self.main_file=os.path.join(root_path,'main.py')
    def run(self,file):
        os.chdir(self.root)
        cmd='%s %s' % (sys.executable, file)
        os.popen(cmd)
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