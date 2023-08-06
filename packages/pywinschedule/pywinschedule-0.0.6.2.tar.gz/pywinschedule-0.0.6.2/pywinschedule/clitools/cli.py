import fire
import os
import subprocess
from pywinschedule.watcher import Watcher
from pywinschedule.config import HOME
from pywinschedule.utils.dbutils import DBList
from pywinschedule.utils.ipc import IPC
from pywinschedule.utils.process import kill_process

ipc=IPC()

watch_dirs_dblist=DBList(os.path.join(HOME,'watch_dirs.db'))

def generate_hash(s, times=1):
    assert times >= 1
    import hashlib
    m = hashlib.md5()

    def gen():
        m.update(s.encode('utf-8'))
        return m.hexdigest()[:10]

    for i in range(times):
        data = gen()
    return data


def startupdirectory():
    return os.path.join(os.path.expanduser('~'), r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')

STARTUP_PATH=startupdirectory()
def add_startup_command(command,script_name):
    bat_path = os.path.join(
        HOME,
        script_name + '.bat'
    )
    bat_content = command
    vbs_path = os.path.join(
        STARTUP_PATH,
        script_name + '.vbs'
    )
    vbs_content = 'CreateObject("Wscript.Shell").Run "%s", 0, True' % (bat_path)
    print('Writing to %s , %s' % (bat_path, vbs_path))
    with open(bat_path, 'w') as f:
        f.write(bat_content)
    with open(vbs_path, 'w') as f:
        f.write(vbs_content)

def remove_startup_command(script_name):
    bat_path = os.path.join(
        HOME,
        script_name + '.bat'
    )
    vbs_path = os.path.join(
        STARTUP_PATH,
        script_name + '.vbs'
    )
    os.remove(bat_path)
    os.remove(vbs_path)

def get_watch_dirs():
    return watch_dirs_dblist.list()
def add_watch_dir(watch_dir):
    watch_dir=os.path.abspath(watch_dir)
    watch_dirs_dblist.add(watch_dir)
    watch_dirs_dblist.commit()
def remove_watch_dir(watch_dir):
    watch_dir = os.path.abspath(watch_dir)
    if watch_dirs_dblist.contains(watch_dir):
        watch_dirs_dblist.remove(watch_dir)
        watch_dirs_dblist.commit()
    else:
        raise Exception('Path is unwatched : %s'%(watch_dir))

processes=[]

class CLI:
    @classmethod
    def enable(cls):
        add_startup_command(
            command='pywinschedule start',
            script_name='pywinschedule_start'
        )
    @classmethod
    def start(cls):
        for watch_dir in get_watch_dirs():
            args=['pywinschedule','watch',watch_dir]
            print(['pywinschedule','watch',watch_dir])

            proc=subprocess.Popen(['pywinschedule','watch',watch_dir])
            # proc=os.popen(' '.join(args))
            processes.append(proc)
        def kill_all_process(*args):
            print('Going to stop')
            for proc in processes:
                kill_process(proc.pid)
            quit(0)
        ipc.subscribe('stop_all_watcher', kill_all_process)
        ipc.listen()
    @classmethod
    def stop(cls):
        ipc.dispatch('stop_all_watcher','')
    @classmethod
    def disable(cls):
        remove_startup_command('pywinschedule_start')
    @classmethod
    def add(cls,path):
        if not os.path.exists(path):
            os.makedirs(path)
        assert os.path.isdir(path)
        add_watch_dir(path)
    @classmethod
    def list(cls):
        wds=get_watch_dirs()
        for wd in wds:
            print(wd)
    @classmethod
    def remove(cls,path):
        remove_watch_dir(path)
    @classmethod
    def watch(cls,path):
        print('Watch:',path)
        try:
            watcher = Watcher(path)
            watcher.start()
        except Exception as e:
            print(e)
            raise e
def main():
    fire.Fire(CLI)

if __name__ == '__main__':
    main()