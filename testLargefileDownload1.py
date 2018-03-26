import json, os, sys, shutil, subprocess, re, glob, uuid, time, datetime, filecmp, urllib, urllib2, ftplib, inspect, zipfile, errno, socket, httplib, json, collections
import xml.etree.ElementTree as ET
from functools import partial
from collections import defaultdict
from maya import cmds, mel

url = 'http://192.168.0.210/wms/app/pipeline/script/download_work.php'
attach
prjid = 'pipeline__storage_test__asset'
process = 'rigging'
name = 'test2'
typ = 'attach'
data = urllib.urlencode({
    'project_id' : prjid,
    'wid' : process+'__'+name,
    'type' : typ
})
print url
print '0'
resp = urllib2.urlopen(url, data)
print '1'
# 다운로드 파일 경로 설정
contents = resp.info().getheader('Content-Disposition')
print '2'
if not contents:
    # 헤더 없음. 해당 작업이 없을 가능성이 크지만 다른 가능성도 생각하자.
    raise RuntimeError("work not found: " + name)
fn = re.match('attachment; filename="(.+)"', contents).group(1)
dstf = upd+'/'+fn
print dstf
# 다운로드
try:
    os.remove(dstf)
except OSError:
    pass
fsize = int(resp.info().getheader('Content-Length'))
print fsize
# -attach.zip 파일의 경우 파일이 0 바이트일 가능성이 존재한다.
# 이때 이 작업파일을 풀면 에러가 나게 된다.
if fsize == 0:
    return None
pgwin = ProgressWindow('download : ' + dstf, fsize)
print pgwin
n = 8192
with open(dstf, 'ab') as fd:
    buf = resp.read(n)
    while buf:
        fd.write(buf)
        pgwin.advance(n)
        buf = resp.read(n)
pgwin.close()
# 검사
if os.stat(dstf).st_size != fsize:
    raise RuntimeError('File not downloaded correctly.')