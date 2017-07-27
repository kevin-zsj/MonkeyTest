# -*- coding: utf-8 -*-
import os
import re


def traverse(path):
    '''
    遍历指定路径下的所有文件
    '''
    filesName = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            filesName.append(os.path.join(root, fn))
    return filesName


def reCrash(s):
    '''
    正则匹配提取出crashed package name
    如：从// CRASH: com.wandoujia.phoenix2 (pid 3903)中提取出com.wandoujia.phoenix2
    '''
    m = '//\sCRASH:\s(.*)\s[(]pid\s(.*)[)]'
    n = re.match(m, s)
    if n:
        return n.group(1)
    else:
        return None


def crashlist(filesList):
    crashCount = []
    for filesName in filesList:
        try:
            for line in open(filesName):
                mCrash = reCrash(line)
                if mCrash:
                    crashCount.append(mCrash)
        except:
            print('Faild to open file the %s.' % filesName)
    return crashCount


def xTable(l):
    res = {}
    for i in l:
        res[i] = res.get(i, 0) + 1
    return res


if __name__ == '__main__':
    filesList = traverse(r'D:\log\MonkeyTest\20130908-171150')
    m = crashlist(filesList)
    results = xTable(m)
    print 'PackageName --- Crashed times'
    for k in results:
        print '->%s --- %s times' % (k, results[k])
    print
    raw_input('Press any key to continue...')
