import fire
import os

from pywinschedule.watcher import Watcher
from pywinschedule.config import HOME
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


class CLI:
    @classmethod
    def serve(cls,path):
        if not os.path.exists(path):
            os.makedirs(path)
        assert os.path.isdir(path)
        def startupdirectory():
            return os.path.join(os.path.expanduser('~'),r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        STARTUP_PATH=startupdirectory()
        name='pywinschedule_watch_%s'%(generate_hash(os.path.abspath(path)))
        bat_path=os.path.join(
            HOME,
            name+'.bat'
        )
        bat_content='pywinschedule watch %s'%(os.path.abspath(path))
        vbs_path=os.path.join(
            STARTUP_PATH,
            name+'.vbs'
        )
        vbs_content='CreateObject("Wscript.Shell").Run "%s", 0, True'%(bat_path)
        print('Writing to %s , %s'%(bat_path,vbs_path))
        with open(bat_path,'w') as f:
            f.write(bat_content)
        with open(vbs_path,'w') as f:
            f.write(vbs_content)
        cls.watch(path)
    @classmethod
    def watch(cls,path):
        watcher=Watcher(path)
        watcher.start()


def main():
    fire.Fire(CLI)

if __name__ == '__main__':
    main()