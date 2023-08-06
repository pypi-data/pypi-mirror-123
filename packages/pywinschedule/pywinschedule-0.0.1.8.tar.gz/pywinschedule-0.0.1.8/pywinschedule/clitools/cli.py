import fire
import os
from pywinschedule.watcher import Watcher
from pywinschedule.utils.admin import isUserAdmin,runAsAdmin
if not isUserAdmin():
    runAsAdmin()

class CLI:
    @classmethod
    def serve(cls,path):
        if not os.path.exists(path):
            os.makedirs(path)
        assert os.path.isdir(path)
        from win32com.shell import shell, shellcon
        def startupdirectory():
            return shell.SHGetFolderPath(
                0,
                shellcon.CSIDL_COMMON_STARTUP,
                0,  # null access token (no impersonation)
                0  # want current value, shellcon.SHGFP_TYPE_CURRENT isn't available, this seems to work
            )
        STARTUP_PATH=startupdirectory()
        bat_path=os.path.join(STARTUP_PATH,'pywinschedule_watch.bat')
        print('Writing to %s'%(bat_path))
        with open(bat_path,'w') as f:
            f.write('pywinschedule watch %s'%(path))
        cls.watch(path)
    @classmethod
    def watch(cls,path):
        watcher=Watcher(path)
        watcher.start()


def main():
    fire.Fire(CLI)

if __name__ == '__main__':
    main()