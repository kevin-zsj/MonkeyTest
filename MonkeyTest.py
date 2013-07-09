# coding = utf-8
'''
__author__ = 'Kevin'
'''
import os
import time

run_times                       = 350000     #发送Event数量
log_lev                         = 3         #3为最高，1为最低
seed                            = False     #传说中可以回归到相同的Event事件序列，暂未验证
throttle                        = 200       #插入固定延时
pct_touch                       = False     #触摸事件百分比
pct_motion                      = False     #调整动作事件百分比（动作事件由屏幕上某处的一个down事件、一系列的伪随机事件和一个up事件组成)
pct_trackball                   = False     #轨迹事件百分比
pct_nav                         = False     #“基本”导航事件的百分比(导航事件由来自方向输入设备的up/down/left/right组成)
pct_majornav                    = False     #“主要”导航事件的百分比(这些导航事件通常引发图形接口中的动作，如：5-way键盘的中间按键、回退按键、菜单按键)
pct_syskeys                     = False     #“系统”按键事件的百分比(这些按键通常被保留，由系统使用，如Home、Back、Start Call、End Call及音量控制键)。
pct_appswitch                   = False     #启动Activity的百分比。在随机间隔里，Monkey将执行一个startActivity()调用，作为最大程度覆盖包中全部Activity的一种方法
pct_anyevent                    = False     #调整其它类型事件的百分比。它包罗了所有其它类型的事件，如：按键、其它不常用的设备按钮、等等。
p_allowed_package_name          = False     #指定了一个或几个包，一个“-p”对应一个包。
c_main_category                 = False     #指定了一个或几个类别，一个“-c”对应一个类别。若不指定则将选择下列类别中列出的Activity： Intent.CATEGORY_LAUNCHER或Intent.CATEGORY_MONKEY。
dbg_no_events                   = False     #设置此选项，Monkey将执行初始启动，进入到一个测试Activity，然后不会再进一步生成事件
hprof                           = True      #设置此选项，将在Monkey事件序列之前和之后立即生成profiling报告。这将会在data/misc中生成文档(~5Mb)，所以要小心使用它
ignore_crashes                  = False     #设置此选项，Monkey将在应用程序崩溃或发生任何失控异常时继续向系统发送事件，直到计数完成。
ignore_timeouts                 = True      #设置此选项，Monkey将在应用程序发生任何超时错误(如“Application Not Responding”对话框)时，继续向系统发送事件，直到计数完成。
ignore_security_exceptions      = False     #设置此选项，Monkey将在应用程序发生许可错误(如启动一个需要某些许可的Activity)时，继续向系统发送事件，直到计数完成。
kill_process_after_error        = False     #当Monkey由于一个错误而停止时，出错的应用程序将继续处于运行状态。设置此项时，将会通知系统停止发生错误的进程。注意，正常的(成功的)结束，并没有停止启动的进程，设备只是在结束事件之后，简单地保持在最后的状态。
monitor_native_crashes          = False     #监视并报告Android系统中本地代码的崩溃事件。如果设置了--kill-process-after-error，系统将停止运行。
wait_dbg                        = False     #停止执行中的Monkey，直到有调试器和它相连接.
whitelist                       = False     #白名单，在/data/white.txt中指定需要测试的APK
blacklist                       = True      #黑名单，在/data/black.txt中指定不需要测试的APK

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

#↓↓↓函数：获取当前日期时间↓↓↓
def cur_times(x):
    if x is 'date':
        cur_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        return cur_date
    elif x is 'time':
        cur_time = time.strftime('%H%M%S',time.localtime(time.time()))
        return cur_time
    else:
        print('Please enter a valid time parameter!')

# #↓↓↓函数创建指定路径，如果不存在就创建↓↓↓
def md_path(x):
    if os.path.exists(x):
        print('log dir is exist...')
    else:
        print('log dir is not exist, Create it now...')
        os.makedirs(x)

for i in range(100):
    # os.system('adb remount')
    log_path = 'D:\\log\\%s\\%s\\' %(cur_times('date'),cur_times('time'))
    #创建log目录
    md_path(log_path)
    log_name = 'MonkeyEvent_%s.log' %cur_times('time')
    #↓↓↓格式化成最终的MonkeyTest命令↓↓↓
    run_monkey = "adb shell monkey %s%s " %(adb_command,run_times) +'> ' + log_path + log_name

    #↓↓↓打印monkey命令↓↓↓
    print(run_monkey)
    #↓↓↓Remount Adb并执行命令↓↓↓
    os.system(run_monkey)
    #Copy log from device to PC.
    os.system("adb pull /data/local/logs %s\\%s" %(log_path,cur_times('time')))
    #循环间隔，同时避免两次测试获取时间cur_times('time')相同时结果被覆盖
    time.sleep(1)

#use explorer open log dir.
os.system(r'explorer /select,%s' %(log_path))