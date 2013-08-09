# -*- coding: utf-8 -*
'''
__author__ = 'Kevin'
'''
import os
import time
import re
from subprocess import Popen, PIPE

#hours
run_time                        = 12

#发送Event数量
events                          = 216000

#3为最高，1为最低
log_lev                         = 3

#传说中可以回归到相同的Event事件序列
seed                            = False

#插入固定延时
throttle                        = 200

#触摸事件百分比
pct_touch                       = False

#调整动作事件百分比（动作事件由屏幕上某处的一个down事件、一系列的伪随机事件和一个up事件组成)
pct_motion                      = False

#轨迹事件百分比
pct_trackball                   = False

#“基本”导航事件的百分比(导航事件由来自方向输入设备的up/down/left/right组成)
pct_nav                         = False

#“主要”导航事件的百分比(这些导航事件通常引发图形接口中的动作，如：5-way键盘的中间按键、回退按键、菜单按键)
pct_majornav                    = False

#“系统”按键事件的百分比(这些按键通常被保留，由系统使用，如Home、Back、Start Call、End Call及音量控制键)。
pct_syskeys                     = False

#启动Activity的百分比。在随机间隔里，Monkey将执行一个startActivity()调用，作为最大程度覆盖包中全部Activity的一种方法
pct_appswitch                   = False

#调整其它类型事件的百分比。它包罗了所有其它类型的事件，如：按键、其它不常用的设备按钮、等等。
pct_anyevent                    = False

#指定了一个或几个包，一个“-p”对应一个包。
p_allowed_package_name          = False

#指定了一个或几个类别，一个“-c”对应一个类别。若不指定则将选择下列类别中列出的Activity： Intent.CATEGORY_LAUNCHER或Intent.CATEGORY_MONKEY。
c_main_category                 = False

#设置此选项，Monkey将执行初始启动，进入到一个测试Activity，然后不会再进一步生成事件
dbg_no_events                   = False

#设置此选项，将在Monkey事件序列之前和之后立即生成profiling报告。这将会在data/misc中生成文档(~5Mb)，所以要小心使用它
hprof                           = True

#设置此选项，Monkey将在应用程序崩溃或发生任何失控异常时继续向系统发送事件，直到计数完成。
ignore_crashes                  = False

#设置此选项，Monkey将在应用程序发生任何超时错误(如“Application Not Responding”对话框)时，继续向系统发送事件，直到计数完成。
ignore_timeouts                 = True

#设置此选项，Monkey将在应用程序发生许可错误(如启动一个需要某些许可的Activity)时，继续向系统发送事件，直到计数完成。
ignore_security_exceptions      = False

#当Monkey由于一个错误而停止时，出错的应用程序将继续处于运行状态。设置此项时，将会通知系统停止发生错误的进程。注意，正常的(成功的)结束，并没有停止启动的进程，设备只是在结束事件之后，简单地保持在最后的状态。
kill_process_after_error        = False

#监视并报告Android系统中本地代码的崩溃事件。如果设置了--kill-process-after-error，系统将停止运行。
monitor_native_crashes          = False

#停止执行中的Monkey，直到有调试器和它相连接.
wait_dbg                        = False

#白名单，在/data/white.txt中指定需要测试的APK
whitelist                       = False

#黑名单，在/data/black.txt中指定不需要测试的APK
blacklist                       = True

Result_path                     = 'D:\\log\\MonkeyTest\\'
get_log                         = '/data/local/logs'

adb_command = ''

#↓↓↓格式化Log等级，一个-v最低，三个-v最高↓↓↓
if log_lev is 3:
    adb_command += '-v -v -v '
elif log_lev is 2:
    adb_command += '-v -v '
else:
    adb_command += "-v "

#↓↓↓格式化seed，一般为了多次执行同一组Event才会用到↓↓↓
if seed is False:
    pass
else:
    adb_command += '-s '+str(seed)+" "

#↓↓↓黑、白名单功能,白名单优先级最高，即当白名单为True时，无论黑名单是否为True都执行白名单↓↓↓
if whitelist is True:
    os.system('adb push %s/data/white.txt /data'%os.getcwd())
    adb_command += '--pkg-whitelist-file /data/white.txt '
elif blacklist is True:
    os.system('adb push %s/data/black.txt /data'%os.getcwd())
    adb_command += '--pkg-blacklist-file /data/black.txt '
else:
    pass

#↓↓↓设定Event延时，也就是每个Event之间的间隔↓↓↓
if throttle is False:
    pass
else:
    adb_command += '--throttle '+str(throttle) +" "

#↓↓↓生成profiling报告↓↓↓
if hprof is False:
    pass
else:
    adb_command += '--hprof'+" "

#↓↓↓格式化‘忽略超时’命令↓↓↓
if ignore_timeouts is False:
    pass
else:
    adb_command += '--ignore-timeouts'+" "


def cur_times(x):
    '''
    获取当前日期时间:
    形参为date：获取当前日期，如20130808
    形参为time：获取当前时间，如135035
    形参为datetime：获取当前日期时间，20130808-135035
    '''
    if x is 'date':
        x = time.strftime('%Y%m%d',time.localtime(time.time()))
        return x
    elif x is 'time':
        x = time.strftime('%H%M%S',time.localtime(time.time()))
        return x
    elif x is 'datetime':
        x = time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
        return x
    else:
        print('Please enter a valid time parameter!')

def md_path(x):
    '''
    函数创建指定路径，如果不存在就创建
    '''
    if os.path.exists(x):
        print('log dir is exist...')
    else:
        print('log dir is not exist, Create it now...')
        os.makedirs(x)
        print('Done.')

def testDone():
    '''
    测试完成时的输出
    '''
    fp = open('%sResult.txt' %(Result_path),'a')
    print('Test Termination: Test time to:',time.time()-start_time,file=fp)
    print('Test Termination: Test time to:',time.time()-start_time)
    print('已完成测试：%s 次'%n,file=fp)
    print('已完成测试：%s 次'%n)
    fp.close()
    print('Test is done.')

#------------------Test start,mark start time.--------------------
start_time = time.time()

# log Analysis Function.
# crash_count = []

# set start times.
n = 1

#Test loop.
while int(time.time()-start_time) <= run_time*3600:
    #Set the directory to save log.
    # events_log = '%s' %(Result_path)
    #创建log目录
    md_path(Result_path)

    #use 'adb remount' check devices and remount.
    cmd = 'adb remount'
    resp = Popen(cmd, shell=True,stdout=PIPE, stderr=PIPE).stdout.readlines()
    # print(resp)
    #Judgment resp returned results.
    if resp == []:
        print('error: device not found.')
        testDone()
        break
    else:
        #Creat result log.
        fp = open('%sResult.txt' %(Result_path),'a')
        result = str(resp)[3:-6]
        print('当前测试次数：第 %s 次' %n,file=fp)
        print('当前测试次数：第 %s 次' %n)
        print(result,file=fp) #return 'remount succeeded'
        print(result)
        events_log_name = 'MonkeyEvents_%s.log' %cur_times('time')
        print('Log_name:',events_log_name)
        #格式化成最终的MonkeyTest命令
        run_monkey = 'adb shell monkey %s%s ' %(adb_command,events) +'> ' + Result_path + events_log_name
        print('Run Command:',run_monkey,file=fp)
        print('Run Command:',run_monkey)
        #Run adb command.
        os.system(run_monkey)
        #Set the directory to save logcat.
        logcat = '%sLogcat_%s' % (Result_path,cur_times('datetime'))
        print('Logcat save to :',logcat)
        pull_log = "adb pull %s %s%s" %(get_log,logcat,cur_times('time'))
        print('Get logcat:',pull_log)
        #pull log to PC form target device.
        os.system(pull_log)
        # print('Start analyzing log')
        print('Ready next test.')
        n += 1
    fp.close()
    time.sleep(10)
else:
    testDone()
    break

#use explorer open log dir.
os.system(r'explorer /select,%s' %(Result_path))