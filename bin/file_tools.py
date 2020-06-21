import os
import fnmatch

def find_files(dir, filter='*', recursiv=False):
    res = []
    list = os.listdir(dir)
    flist = fnmatch.filter(list, filter)
    l = len(flist)
    i = 0
    while i < l:
        file = dir + '/' + flist[i]
        file = file.replace('/../', '/').replace('/./', '/')
        if os.path.isfile(file):
             res.append(file)
        i += 1
    return res
