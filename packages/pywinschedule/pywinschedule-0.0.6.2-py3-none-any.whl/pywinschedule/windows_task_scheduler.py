import os
import dateutil.parser
import win32com.client
import datetime

from pywinschedule.config import USER_HOME,HOME


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
def add_executable_to_windows_task_scheduler(path,daytime,params='',trigger_type='once',name='some task'):
    trigger_type_dict={
        'once':1,
        'daily':2,
        'weekly':3,
        'monthly':4,
    }


    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    # Create trigger
    # start_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    start_time = daytime if  isinstance(daytime,datetime.datetime) else dateutil.parser.parse(daytime)

    TASK_TRIGGER_TIME = trigger_type_dict[trigger_type]
    trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
    trigger.StartBoundary = start_time.isoformat()

    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = name
    action.Path = path
    # action.Path = r'python.exe'
    action.Arguments = params

    # Set parameters
    task_def.RegistrationInfo.Description = name
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False


    # set condition
    task_def.Settings.DisallowStartIfOnBatteries=False

    # Register task
    # If task already exists, it will be updated
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        name,  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE)


def schedule_python_script(path,work_dir=None,daytime=None,params='',trigger_type='once',name='some_task'):
    path=os.path.abspath(path)
    if not os.path.exists(HOME):
        os.makedirs(HOME)
    if not work_dir:
        work_dir=HOME
    if not daytime:
        daytime= datetime.datetime.now() + datetime.timedelta(minutes=1)
    bat_path=os.path.join(HOME,'schedule_script_%s.bat'%(generate_hash(name)))
    with open(bat_path,'w') as f:
        f.write('cd %s\npython.exe %s %s'%(work_dir,path,params))
    add_executable_to_windows_task_scheduler(bat_path,daytime,trigger_type=trigger_type,name=name)

def demo():
    schedule_python_script('./hi.py', name='打招呼')

if __name__ == '__main__':
    demo()