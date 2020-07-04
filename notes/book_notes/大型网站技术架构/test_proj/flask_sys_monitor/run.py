import random
import socket
import platform
import psutil
from flask import Flask, render_template
from datetime import datetime
import getpass
from pprint import pprint

app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def sysinfo():
    boot_time=psutil.boot_time()
    boot_time=datetime.fromtimestamp(boot_time)
    now_time=datetime.now()
    delta_time=now_time - boot_time
    delta_time=str(delta_time).split('.')[0]
    data = dict(
        master=socket.gethostname(),
        system=platform.system(),
        machine=platform.machine(),
        version=platform.version(),
        architecture=platform.architecture(),
        now_time=now_time,
        boot_time=boot_time,
        delta_time=delta_time
    )
    pprint(data)
    return render_template('sysinfo.html', **data)


@app.route('/cpu/')
def cpu():
    C_times=psutil.cpu_times()
    data = dict(
        Phy_cpu=psutil.cpu_count(logical=False),
        Log_cpu=psutil.cpu_count(),
        user=C_times.user,
        system=C_times.system,
        # nice=C_times.nice,
        # iowait=C_times.iowait
    )
    pprint(data)
    return render_template('cpu.html', **data)


@app.route('/memory/')
def memory():
    info=psutil.virtual_memory()
    data = dict(
        total=str(round(info.total / 1024 / 1024 / 1024)),
        available=str(round(info.available / 1024 / 1024 / 1024)),
        percent=str(round(info.percent)),
        used=str(round(info.used / 1024 / 1024 / 1024)),
        free=str(round(info.free / 1024 / 1024 / 1024)),
        # buffers=str(round(info.buffers / 1024 / 1024)),
        # cached=str(round(info.cached / 1024 / 1024 / 1024))
    )
    pprint(data)
    return render_template('memory.html', **data)


@app.route('/disk/')
def disk():
    disk_info=psutil.disk_partitions()
    info1=disk_info[0]
    content1=psutil.disk_usage(info1.mountpoint)
    info2=disk_info[1]
    content2= psutil.disk_usage(info2.mountpoint)
    info3=disk_info[2]
    content3 = psutil.disk_usage(info3.mountpoint)
    info4=disk_info[3]
    content4 = psutil.disk_usage(info4.mountpoint)
    # info5=disk_info[4]
    # content5 = psutil.disk_usage(info5.mountpoint)

    data = dict(
        device1=info1.device,
        mountpoint1=info1.mountpoint,
        total1=str(round(content1.total /1024 /1024 /1024)),
        used1=str(round(content1.used /1024 /1024 /1024)),
        percent1=str(round(content1.percent)),
        free1=str(round(content1.free /1024 /1024 /1024)),
        fstype1=info1.fstype,
        opts1=info1.opts,
        device2=info2.device,
        mountpoint2=info2.mountpoint,
        total2=str(round(content2.total / 1024 / 1024 / 1024)),
        used2=str(round(content2.used / 1024 / 1024 / 1024)),
        percent2=str(round(content2.percent)),
        free2=str(round(content2.free / 1024 / 1024 / 1024)),
        fstype2=info2.fstype,
        opts2=info2.opts,
        device3=info3.device,
        mountpoint3=info3.mountpoint,
        total3=str(round(content3.total / 1024 / 1024 / 1024)),
        used3=str(round(content3.used / 1024 / 1024 / 1024)),
        percent3=str(round(content3.percent)),
        free3=str(round(content3.free / 1024 / 1024 / 1024)),
        fstype3=info3.fstype,
        opts3=info3.opts,
        device4=info4.device,
        mountpoint4=info4.mountpoint,
        total4=str(round(content4.total / 1024 / 1024 / 1024)),
        used4=str(round(content4.used / 1024 / 1024 / 1024)),
        percent4=str(round(content4.percent)),
        free4=str(round(content4.free / 1024 / 1024 / 1024)),
        fstype4=info4.fstype,
        opts4=info4.opts,
        # device5=info5.device,
        # mountpoint5=info5.mountpoint,
        # total5=str(round(content5.total / 1024 / 1024 / 1024)),
        # used5=str(round(content5.used / 1024 / 1024 / 1024)),
        # percent5=str(round(content5.percent)),
        # free5=str(round(content5.free / 1024 / 1024 / 1024)),
        # fstype5=info5.fstype,
        # opts5=info5.opts
    )
    pprint(data)
    return render_template('disk.html', **data)


@app.route('/user/')
def user():
    data = dict(
        user=getpass.getuser(),
        master=socket.gethostname(),
        now_time=datetime.now()
    )
    pprint(data)
    return render_template('user.html', **data)


@app.route('/routes')
def get_all_routes():
    routes = [i.rule for i in app.url_map._rules]
    data = dict(routes=routes)
    return str(data)


if __name__ == '__main__':
    app.run(debug=True)
