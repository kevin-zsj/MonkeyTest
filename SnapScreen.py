# -*- coding:utf-8 -*-
import os
import sys
import time


def androidScreencap(path=0):
    localTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    remote_obj = '/sdcard/%s.png' % localTime
    if path:
        local_obj = path
    else:
        local_obj = sys.path[0]

    print remote_obj, local_obj
    snap = 'adb shell screencap -p %s' % remote_obj
    pullPic = 'adb pull %s %s' % (remote_obj, local_obj)
    print "run command: ", pullPic

    os.system(snap)
    os.system(pullPic)

    print 'OK.'


if __name__ == '__main__':
    androidScreencap()
