# coding: utf-8

import os
import re
import execjs
import requests
from operator import itemgetter
from urlparse import urljoin


pattern = re.compile(r'(/xml/sub/\d+/\d+.xml).*?rate.*?:.*?(\d+)')
filepattern = re.compile(r'local_downfile\(this,.*?(\d+)\)')
shtg_filehash = 'duei7chy7gj59fjew73hdwh213f'
ctx = execjs.compile('function shtg_calcfilehash(a){function b(j){var g="";for(var f=0;f<j.length;f++){var h=j.charCodeAt(f);g+=(h+47>=126)?String.fromCharCode(" ".charCodeAt(0)+(h+47)%126):String.fromCharCode(h+47)}return g}function d(g){var j=g.length;j=j-1;var h="";for(var f=j;f>=0;f--){h+=(g.charAt(f))}return h}function c(j,h,g,f){return j.substr(j.length-f+g-h,h)+j.substr(j.length-f,g-h)+j.substr(j.length-f+g,f-g)+j.substr(0,j.length-f)}if(a.length>32){switch(a.charAt(0)){case"o":return(b((c(a.substr(1),8,17,27))));break;case"n":return(b(d(c(a.substr(1),6,15,17))));break;case"m":return(d(c(a.substr(1),6,11,17)));break;case"l":return(d(b(c(a.substr(1),6,12,17))));break;case"k":return(c(a.substr(1),14,17,24));break;case"j":return(c(b(d(a.substr(1))),11,17,27));break;case"i":return(c(d(b(a.substr(1))),5,7,24));break;case"h":return(c(b(a.substr(1)),12,22,30));break;case"g":return(c(d(a.substr(1)),11,15,21));case"f":return(c(a.substr(1),14,17,24));case"e":return(c(a.substr(1),4,7,22));case"d":return(d(b(a.substr(1))));case"c":return(b(d(a.substr(1))));case"b":return(d(a.substr(1)));case"a":return b(a.substr(1));break}}return a}')


def get_movie_url(query):
    url = 'http://shooter.cn/api/qhandler.php?t=sub&e=UTF-8&q=%s' % query
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return ''
        rs = pattern.findall(r.content)
        if not rs:
            return ''
        rs = [(u, int(r)) for u, r in rs]
        rs = sorted(rs, key=itemgetter(1), reverse=True)
        path, rate = rs[0]
        return urljoin('http://shooter.cn', path)
    except:
        return ''


def parse_page(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return ''
        file_id = filepattern.findall(r.content)[0]
        r = requests.get('http://shooter.cn/files/file3.php?hash=duei7chy7gj59fjew73hdwh213f&fileid=%s' % file_id, timeout=10)
        if r.status_code != 200:
            return ''
        path = ctx.call('shtg_calcfilehash', r.content)
        return urljoin('http://file1.shooter.cn', path)
    except:
        return ''


def do_download(query):
    page_url = get_movie_url(query)
    if not page_url:
        return
    download_url = parse_page(page_url)
    o = requests.get(download_url, timeout=10)
    with open('%s.rar' % query, 'w') as f:
        f.write(o.content)


if __name__ == '__main__':
    do_download('逆转未来')
