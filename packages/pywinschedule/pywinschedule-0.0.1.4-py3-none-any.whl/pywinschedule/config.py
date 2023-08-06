import os
from pathlib import Path
USER_HOME=os.path.expanduser('~')
HOME=os.path.join(USER_HOME,'.pywinschedule')
Path(HOME).mkdir(exist_ok=True)