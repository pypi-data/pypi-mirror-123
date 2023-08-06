# pywinschedule
Schedule script with windows task scheduler

### Demo
**run python script daily**
```python
import pywinschedule as pws

pws.schedule_python_script(
    './daily_task.py',
    daytime='13:00',
    trigger_type='daily',# can be 'once','daily','weekly','monthly'
    name='demo_task'
)
```
