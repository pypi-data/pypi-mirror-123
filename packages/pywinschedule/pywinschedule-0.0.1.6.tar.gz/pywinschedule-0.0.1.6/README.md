# pywinschedule
Schedule script with windows task scheduler

### Demo
**run python script daily**
```python
import pywinschedule as pws

pws.schedule_python_script(
    './daily_task.py',
    daytime='18:51',
    trigger_type='once',# can be 'once','daily','weekly','monthly'
    name='demo_task'
)
```
