# -*- coding: utf-8 -*-
'''
__author__  = 'Kevin'
Email = 'testcn@vip.qq.com'
'''
import logging
import os
import subprocess
import sys
import time

import SnapScreen as snap
import MonkeyTest_Offline as MTOFF


# hours
Run_Time = 72

# 发送Event数量
events = 50000

# 3为最高，1为最低
log_lev = 3

# 传说中可以回归到相同的Event事件序列
seed = False

# 插入固定延时
throttle = 500

# 触摸事件百分比
pct_touch = False

# 调整动作事件百分比（动作事件由屏幕上某处的一个down事件、一系列的伪随机事件和一个up事件组成)
pct_motion = False

# 轨迹事件百分比
pct_trackball = False

# “基本”导航事件的百分比(导航事件由来自方向输入设备的up/down/left/right组成)
pct_nav = False

# “主要”导航事件的百分比(这些导航事件通常引发图形接口中的动作，如：5-way键盘的中间按键、回退按键、菜单按键)
pct_majornav = False

# “系统”按键事件的百分比(这些按键通常被保留，由系统使用，如Home、Back、Start Call、End Call及音量控制键)。
pct_syskeys = False

# 启动Activity的百分比。在随机间隔里，Monkey将执行一个startActivity()调用，作为最大程度覆盖包中全部Activity的一种方法
pct_appswitch = 30

# 调整其它类型事件的百分比。它包罗了所有其它类型的事件，如：按键、其它不常用的设备按钮、等等。
pct_anyevent = False

# 指定了一个或几个包，一个“-p”对应一个包。
p_allowed_package_name = False

# 指定了一个或几个类别，一个“-c”对应一个类别。若不指定则将选择下列类别中列出的Activity： Intent.CATEGORY_LAUNCHER或
# Intent.CATEGORY_MONKEY。
c_main_category = False

# 设置此选项，Monkey将执行初始启动，进入到一个测试Activity，然后不会再进一步生成事件
dbg_no_events = False

# 设置此选项，将在Monkey事件序列之前和之后立即生成profiling报告。这将会在data/misc中生成文档(~5Mb)，所以要小心使用它
hprof = True

# 设置此选项，Monkey将在应用程序崩溃或发生任何失控异常时继续向系统发送事件，直到计数完成。
ignore_crashes = False

# 设置此选项，Monkey将在应用程序发生任何超时错误时，继续向系统发送事件，直到计数完成。
ignore_timeouts = True

# 设置此选项，Monkey将在应用程序发生许可错误时，继续向系统发送事件，直到计数完成。
ignore_security_exceptions = False

# 当Monkey由于一个错误而停止时，出错的应用程序将继续处于运行状态。设置此项时，将会通知系统停止发生错误的进程。注意，正常的(成功的)结束，
# 并没有停止启动的进程，设备只是在结束事件之后，简单地保持在最后的状态。
kill_process_after_error = False

# 监视并报告Android系统中本地代码的崩溃事件。如果设置了--kill-process-after-error，系统将停止运行。
monitor_native_crashes = False

# 停止执行中的Monkey，直到有调试器和它相连接.
wait_dbg = False

# 白名单，在/data/white.txt中指定需要测试的APK
whitelist = False

# 黑名单，在/data/black.txt中指定不需要测试的APK
blacklist = True

# -------------------------------*Logging*-------------------------------
# 创建一个logger
logger = logging.getLogger('MonkeyTest')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('Reports.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
# -------------------------------*Logging*-------------------------------

adb_command = ''
local_path = sys.path[0]
logger.info("Local path：{}".format(local_path))

# 格式化Log等级，一个-v最低，三个-v最高
if log_lev is 3:
    adb_command += '-v -v -v '
elif log_lev is 2:
    adb_command += '-v -v '
else:
    adb_command += "-v "

# If you 're-run' the Monkey with the same seed value,
# it will generate the same sequence of events.
if seed is False:
    pass
else:
    adb_command += '-s ' + str(seed) + " "

# Black/white list, white list with a higher priority.
if whitelist is True:
    push_white = 'adb push {}/data/white.txt /sdcard/white.txt'.format(local_path)
    if os.system(push_white) == 0:
        adb_command += '--pkg-whitelist-file /sdcard/white.txt '
elif blacklist is True:
    push_black = 'adb push {}/data/black.txt /sdcard/black.txt'.format(local_path)
    if os.system(push_black) == 0:
        adb_command += '--pkg-blacklist-file /sdcard/black.txt '


# formart time interval between events.
if throttle is False:
    pass
else:
    adb_command += '--throttle ' + str(throttle) + " "

# formart profiling report.
if hprof is False:
    pass
else:
    adb_command += '--hprof' + " "

# formart timeouts
if ignore_timeouts is False:
    pass
else:
    adb_command += '--ignore-timeouts' + " "

# formart app switch percentage.
if pct_appswitch is False:
    pass
else:
    adb_command += '--pct-appswitch ' + str(pct_appswitch) + " "

# formart 'anyevent'
if pct_anyevent is False:
    pass
else:
    adb_command += '--pct-anyevent ' + str(pct_anyevent) + " "


def cur_times(dateFormat):
    '''
    date：Get the current date，e.g. 20130808
    time：Get the current time，e.g. 135035
    datetime：Get the current datetime，e.g. 20130808-135035
    '''
    if dateFormat is 'date':
        dateFormat = time.strftime('%Y%m%d', time.localtime(time.time()))
        return dateFormat
    elif dateFormat is 'time':
        dateFormat = time.strftime('%H%M%S', time.localtime(time.time()))
        return dateFormat
    elif dateFormat is 'datetime':
        dateFormat = time.strftime(
            '%Y%m%d-%H%M%S', time.localtime(time.time()))
        return dateFormat
    else:
        logger.warning('The time parameter is valid')


def md_path(logDir):
    '''
    Create log path.
    '''
    if os.path.exists(logDir):
        logger.info('log dir is exist...')
    else:
        logger.info('log dir is not exist, Create it now...')
        os.makedirs(logDir)
        logger.info('Created.')


def testDone():
    '''
    works done.
    '''
    ctime = time.time() - start_time
    logger.info('Test Termination: Test time to: %s', ctime)
    # logger.info('%s %s %s', *('Tested ', n - 1, ' times.'))
    logger.info('Tested %s times.', (n - 1))
    logger.info('Test is done.')


def chkPower(device):
    '''
    Use the "adb shell dumpsys battery" command to get battery level, return int value.
    '''
    cmd = ['adb', '-s', device, 'shell', 'dumpsys', 'battery', '|', 'grep', 'level']
    run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    battery = bytes.decode(run.stdout.read())
    if "level" not in battery:
        # logger.warning("Query battery information failed!")
        return False
    else:
        getvalue = battery.split(':')[1].strip()
        # logger.info("Battery level : {}".format(getvalue))
        return int(getvalue)


# ------------------Test start, mark start time.--------------------
# 定义测试开始的时间
start_time = time.time()

now = cur_times('datetime')
Result_path = '{}/MonkeyResult/{}'.format(local_path, now)
logger.info('Result path: {}'.format(Result_path))

# set start times.
n = 1
# Test loop.
while int(time.time() - start_time) <= Run_Time * 3600:
    device = MTOFF.check_devices()
    batt_level = chkPower(device)
    if device == None:
        logger.warning('Please check device is already connected.')
        sys.exit()  # Currently, multi-device operation is not supported.
    else:
        logger.info('Connected device: {}'.format(device))
    if batt_level < 1:  # check Android power.
        logger.info('The battery level is %s, start charge.', batt_level)
        os.system('adb shell input keyevent POWER')
        time.sleep(1800)
        os.system('adb shell input keyevent POWER')
    elif not batt_level:
        logger.warning("Query battery information failed!")
        sys.exit()

    # Creat log dir.
    md_path(Result_path)
    logger.info('Times: %s ', n)
    Event_Log = Result_path.replace('\\', '/') + \
        '/MonkeyEvents_{}.log'.format(cur_times('time'))
    Event_Log_Flie = open(Event_Log, 'w')
    # -------------use subprocess run command--------------
    run_monkey = 'adb shell monkey {}{}'.format(adb_command, events)
    logger.info('Monkey Command is: %s', run_monkey)
    start = subprocess.Popen(run_monkey.split(),
                             stdout=Event_Log_Flie,
                             stderr=Event_Log_Flie)
    start.wait()
    start.terminate()

    # snap screen.
    logger.info("Find Exception, snap screen.")
    snap.androidScreencap(device, Result_path)
    # take bugreport.
    logger.info("Pull bugreport ......")
    bugreport = 'adb bugreport {}'.format(Result_path)
    # logger.info(bugreport)
    os.system(bugreport)
    logger.info('Wait a minute.')
    time.sleep(5)
    n += 1
else:
    logger.warning("Set Time To End!")
    sys.exit()
