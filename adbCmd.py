# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE


def adbSerialno(s):
    resp = Popen(s, shell=True, stdout=PIPE, stderr=PIPE).stdout.readlines()
    a = []
    for i in resp:
        a.append(i.strip('\r\n'))
    return a

if __name__ == '__main__':
    r = adbSerialno('adb get-serialno')
    if r[0] == 'unknown':
        print 'No devices is connected.'
    elif len(r) == 1:
        print r[0]
    else:
        print 'Multiple devices connected.'
