import os

_root=os.path.dirname(__file__)
_data_dir=os.path.join(_root,'data')

NSSM_PATH= os.path.join(_data_dir,'nssm.exe')

class NSSM:
    def __init__(self,path):
        self.path=path
    def asAdmin(self):
        pass
        # code below might be useless
        # if not isUserAdmin():
        #     runAsAdmin()
    def updateService(self,name,executable,params=''):
        self.setServiceExecutable(name,executable)
        self.setServiceParams(name,params)
    def installService(self,name,executable,params=''):
        self.asAdmin()
        os.system('%s install %s "%s" "%s"'%(self.path,name,executable,params))
    def setServiceExecutable(self,name,executable):
        self.asAdmin()
        os.system('%s set %s Application "%s"' % (self.path, name, executable))
    def setServiceParams(self,name,params):
        self.asAdmin()
        os.system('%s set %s AppParameters "%s"' % (self.path, name, params))
    def setServiceWorkdir(self,name,work_dir):
        self.asAdmin()
        os.system('%s set %s AppDirectory "%s"' % (self.path, name, work_dir))
    def startService(self,name):
        self.asAdmin()
        os.system('%s start %s' % (self.path, name))
    def stopService(self,name):
        self.asAdmin()
        os.system('%s stop %s' % (self.path, name))
    def removeService(self,name):
        self.asAdmin()
        os.system('%s remove %s confirm' % (self.path, name))

nssm=NSSM(NSSM_PATH)
def demo():

    # nssm.installService('MyService', sys.executable,r"D:\Projects\PythonProjects\pywinschedule\demo\demo_service.py")
    nssm.startService('MyService')
    # nssm.stopService('MyService')


if __name__ == '__main__':
    demo()