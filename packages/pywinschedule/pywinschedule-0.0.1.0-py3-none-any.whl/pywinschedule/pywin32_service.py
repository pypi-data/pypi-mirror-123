import socket

import win32serviceutil

import servicemanager
import win32event
import win32service
import shutil
import os
def _get_site_packages_path():
    import site
    paths=site.getsitepackages()
    for p in paths:
        if 'site-packages' in p:
            return p

def fix_pywin32_bug():
    "copy pywintypes310.dll from pywin32_system32 to win32"
    dll_name='pywintypes310.dll'
    site_packages_path=_get_site_packages_path()
    src_dll_path=os.path.join(site_packages_path,'pywin32_system32',dll_name)
    dst_dll_path=os.path.join(site_packages_path,'win32',dll_name)
    if not os.path.exists(dst_dll_path):
        shutil.copy(src_dll_path,dst_dll_path)

class WinService(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        fix_pywin32_bug()
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        pass

def demo():
    class PythonCornerExample(WinService):
        _svc_name_ = "PythonCornerExample"
        _svc_display_name_ = "Python Corner's Winservice Example"
        _svc_description_ = "That's a great winservice! :)"

        def start(self):
            self.isrunning = True

        def stop(self):
            self.isrunning = False

        def main(self):
            import random
            from pathlib import Path
            import time
            while self.isrunning:
                random.seed()
                x = random.randint(1, 1000000)
                Path(f'D:/Projects/PythonProjects/pywinschedule/demo/{x}.txt').touch()
                time.sleep(5)

    PythonCornerExample.parse_command_line()
# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    demo()