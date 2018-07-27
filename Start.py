# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import sys
import os
import subprocess

local_path = sys.path[0]
print('Pushing Test tools ...')
os.system('adb push {}/startMonkey.sh /sdcard/'.format(local_path))
print('Pushing black names ...')
os.system('adb push {}/data/black.txt /sdcard/'.format(local_path))
print('Run test ...')
cmd = 'adb shell "sh /sdcard/startMonkey.sh &"'
run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# print('STDOUT: ', run.stdout.read())
# print('STDERR: ', run.stderr.read())
print('Test is running ...')