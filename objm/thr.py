# This file is placed in the Public Domain.


"show running threads"


import threading
import time


from objx.face    import Object, update, laps
from objr.runtime import STARTTIME


def thr(event):
    "show running threads."
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.name):
        if str(thread).startswith('<_'):
            continue
        obj = Object()
        update(obj, vars(thread))
        if getattr(obj, 'current', None):
            thread.name = obj.current
        if getattr(obj, 'sleep', None):
            uptime = obj.sleep - int(time.time() - obj.state["latest"])
        elif getattr(obj, 'starttime', None):
            uptime = int(time.time() - obj.starttime)
        else:
            uptime = int(time.time() - STARTTIME)
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[1]):
        lap = laps(uptime)
        res.append(f'{txt}/{lap}')
    if res:
        event.reply(' '.join(res))
    else:
        event.reply('no threads')
