# -*- coding: utf-8 -*-
'''
__author__  = 'Kevin'
__version__ = '0.8'
'''
import os
import time
import logging
import logAnalysis
import adbCmd

# hours
run_time = 0.1

# 发送Event数量
events = 500

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
whitelist = True

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
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
# -------------------------------*Logging*-------------------------------

adb_command = ''

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
    os.system('adb push %s/data/white.txt /data/white.txt' % os.getcwd())
    adb_command += '--pkg-whitelist-file /data/white.txt '
elif blacklist is True:
    os.system('adb push %s/data/black.txt /data' % os.getcwd())
    adb_command += '--pkg-blacklist-file /data/black.txt '
else:
    pass

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


def cur_times(x):
    '''
    date：Get the current date，e.g. 20130808
    time：Get the current time，e.g. 135035
    datetime：Get the current datetime，e.g. 20130808-135035
    '''
    if x is 'date':
        x = time.strftime('%Y%m%d', time.localtime(time.time()))
        return x
    elif x is 'time':
        x = time.strftime('%H%M%S', time.localtime(time.time()))
        return x
    elif x is 'datetime':
        x = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        return x
    else:
        logger.warning('The time parameter is valid')


def md_path(x):
    '''
    Create log path.
    '''
    if os.path.exists(x):
        logger.info('log dir is exist...')
    else:
        logger.info('log dir is not exist, Create it now...')
        os.makedirs(x)
        logger.info('Created.')


def testDone():
    '''
    works done.
    '''
    logger.info('Test Termination: Test time to: %s' %
                (time.time() - start_time))
    logger.info('%s %s %s', *('Tested ', n - 1, ' times.'))
    logger.info('Test is done.')

# ------------------Test start,mark start time.--------------------
start_time = time.time()

# set start times.
n = 1
now = cur_times('datetime')
Result_path = './MonkeyResult/%s' % now

# Test loop.
while int(time.time() - start_time) <= run_time * 3600:
    r = adbCmd.adbSerialno('adb get-serialno')
    if r[0] == 'unknown':
        logger.warning('No devices is connected.')
        break
    elif len(r) > 1:
        logger.warning('Multiple devices connected.')
    else:
        logger.info('Connected devices : %s' % r[0])
        # Creat log dir.
        md_path(Result_path)
        logger.info('当前测试次数：第 %s 次' % n)
        events_log_name = 'MonkeyEvents_%s.log' % cur_times('time')
        logger.info('%s %s' % ('Log_name:', events_log_name))
        # last MonkeyTest command.
        run_monkey = 'adb shell monkey %s%s > %s\\%s' % (adb_command,
                                                         events,
                                                         Result_path,
                                                         events_log_name)
        logger.info('%s %s', *('Run Command:', run_monkey))

        # Test running.
        os.system(run_monkey)

        time.sleep(1)
    n += 1
else:
    fl = logAnalysis.traverse(Result_path)
    analy = logAnalysis.crashlist(fl)
    # print analy
    results = logAnalysis.xTable(analy)
    if results:
        logger.info('PackageName --- Crashed times')
        for k in results:
            logger.info('->%s --- %s times' % (k, results[k]))
    else:
        logger.info('No crashed app is fond.')
    testDone()

# use explorer open log dir.
# os.system(r'explorer /select,%s' %(Result_path))
