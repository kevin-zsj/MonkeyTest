# -*- coding:utf-8 -*-
# Author: Kevin.Zhang
# E-Mail: testcn@vip.qq.com

import sys
import os
import subprocess


def check_devices():
    cmd = 'adb devices'
    run = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    output = run.stdout.readlines()
    # print(output)
    # print(len(output))
    devices_lst = []
    for i in output:
        to_str = bytes.decode(i)
        # print(to_str)
        if to_str.strip().endswith('device'):
            devices_lst.append(to_str.split('\t')[0])
    # print(devices_lst)
    if len(devices_lst) > 1:
        print('Devices list: ')
        for k, v in enumerate(devices_lst):
            print(k, '：', v)
        option = input('Enter a ID for your device: ')
        if int(option) in range(len(devices_lst)):
            device = devices_lst[int(option)]
        else:
            device = None
            print('Wrong option entered! ')
    elif len(devices_lst) == 0:
        print('No devices if fond.')
        device = None
    else:
        device = devices_lst[0]
        print('Devices is: {}'.format(device))
    return device

def push_test_files(device):
    if device is None:
        device = ''
    local_path = sys.path[0]
    print('Pushing Test tools ...')
    os.system('adb -s {} push {}/startMonkey.sh /sdcard/'.format(device, local_path))
    print('Pushing black names ...')
    os.system('adb -s {} push {}/data/black.txt /sdcard/'.format(device, local_path))


def run_test(device):
    if device is None:
        device = ''
    # local_path = sys.path[0]
    print('Run test ...')
    cmd = 'adb -s {} shell "sh /sdcard/startMonkey.sh >/dev/null 2>&1 &"'.format(device)
    run = subprocess.run(cmd, shell=True)
    if run.returncode == 0:
        print('Test is running ...')
    else:
        print('Test Failed.')

if __name__ == '__main__':
    device = check_devices()
    push_test_files(device)
    run_test(device)