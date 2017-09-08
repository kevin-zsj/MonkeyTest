# -*- coding: utf-8 -*-
'''
__author__  = 'Kevin'
Email = 'kevin@ishow.me'
'''
import logging
import os
import subprocess
import sys
import time

import SnapScreen as snap

# hours
Run_Time = 10
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
pct_appswitch = 50

# 调整其它类型事件的百分比。它包罗了所有其它类型的事件，如：按键、其它不常用的设备按钮、等等。
pct_anyevent = 0

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
cpath = sys.path[0]

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
    push_white = 'adb push {}/data/white.txt /sdcard/white.txt'.format(cpath)
    if os.system(push_white) == 0:
        adb_command += '--pkg-whitelist-file /sdcard/white.txt '
elif blacklist is True:
    push_black = 'adb push {}/data/black.txt /sdcard/black.txt'.format(cpath)
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


def chkPower():
    '''
    检查样机电量的百分比，返回一个int类型的数值
    '''
    cmd = ['adb', 'shell', 'dumpsys', 'battery', '|', 'grep', 'level']
    run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    batt = run.stdout.read()
    if "level" not in batt:
        print "Query battery information failed!"
        return False
    else:
        getvalue = batt.split(':')[1].strip()
        print "Battery level : " + getvalue
        return int(getvalue)


def chkDevices():
    '''
    使用‘adb devices’命令获取设备连接信息，若有Android设备连接则返回一个值：
    0 ：无设备连接
    1 ：有一台设备连接
    2 ：有两台或两台以上的设备连接
    '''
    cmd = ['adb', 'devices']
    run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    getvalue = run.stdout.readlines()
    count = len(getvalue)
    # print getvalue
    if count == 3:
        sn = getvalue[1].split('device')[0].strip()
        # print sn
        logger.info('Device ID: %s', sn)
        return 1
    elif count > 3:
        logger.warning('Multiple devices connected.')
        for i in getvalue[1:-1]:
            # print "----------", i
            # sn = getvalue[1].split('device')[0].strip()
            logger.info(i)
        return 2
    else:
        logger.warning('No devices is connected.')
        # return 0


# ------------------Test start, mark start time.--------------------
# 定义测试开始的时间
start_time = time.time()

now = cur_times('datetime')
Result_path = '{}/MonkeyResult/{}'.format(cpath, now)
print 'Result path:', Result_path

# set start times.
n = 1
# Test loop.
while int(time.time() - start_time) <= Run_Time * 3600:
    devices = chkDevices()
    batt_level = chkPower()
    if devices != 1:
        logger.warning(
            'please check device is already connected, or more devices.')
        sys.exit()  # Currently, multi-device operation is not supported.
    if batt_level < 10:  # check Android power.
        logger.info('The battery level is %s, start charge.', batt_level)
        os.system('adb shell input keyevent POWER')
        time.sleep(1800)
        os.system('adb shell input keyevent POWER')
    else:
        logger.warning("Query battery information failed!")
        sys.exit()

        # Creat log dir.
        md_path(Result_path)
        logger.info('Times: %s ', n)
        events_log_name = 'MonkeyEvents_{}.log'.format(cur_times('time'))
        logger.info('Log_name: %s', events_log_name)
        # last MonkeyTest command.
        run_monkey = 'adb shell monkey {}{} > {}\\{}'.format(adb_command,
                                                             events,
                                                             Result_path,
                                                             events_log_name)
        logger.info('Run Command: %s', run_monkey)

        # Test running.
        os.system(run_monkey)
        # snap screen.
        snap.androidScreencap(Result_path)
        # take bugreport.
        bugreport = 'adb bugreport {}'.format(Result_path)
        logger.info(bugreport)
        # os.system(bugreport)
        logger.info('Wait a minute.')
        time.sleep(5)
    n += 1
