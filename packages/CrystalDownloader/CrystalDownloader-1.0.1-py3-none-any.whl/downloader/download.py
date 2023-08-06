# -*- coding: utf-8 -*-
import http
import urllib.request
import requests
import threading
from urllib.parse import urlencode
import ssl

import re
import urllib

ssl._create_default_https_context = ssl._create_unverified_context

def urlEncodeNonAscii(b):
    return re.sub(b'[\x80-\xFF]', lambda c: b'%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urllib.parse.urlparse(iri)
    return urllib.parse.urlunparse([urlEncodeNonAscii(part.encode('utf-8')) for  part in parts])


class Downloader:
    def __init__(self, url, download_to, max_block_size=1024*1024*5, thread_num=0):
        url = iriToUri(url)
        self.url = url
        self.name = download_to
        # response = requests.get(self.url)
        req = urllib.request.Request(self.url.decode())
        response = urllib.request.urlopen(req)
        file_size = response.headers['Content-Length']
        print(file_size)
        #  创建一个和要下载文件一样大小的文件
        fp = open(self.name, "wb")
        fp.truncate(int(file_size))
        fp.close()
        self.total = int(file_size)
        # 根据要求或者块大小计算线程个数
        if thread_num:
            self.thread_num = thread_num
        else:
            self.thread_num = (self.total+max_block_size-1)//max_block_size
        print('开启线程数量： ' + str(self.thread_num))
        self.event_list = [threading.Event() for _ in range(self.thread_num)]
        self.event_list[0].set()
        print('File size is %d KB' % (self.total/1024))

    # 划分每个下载块的范围
    def get_range(self):
        ranges = []
        offset = int(self.total/self.thread_num)
        for i in range(self.thread_num):
            if i == self.thread_num-1:
                ranges.append((i*offset, ''))
            else:
                ranges.append((i*offset, (i+1)*offset))
        return ranges

    def download(self, start, end, event_num):
        try:
            headers = {'Range': 'Bytes=%s-%s' % (start, end), 'Accept-Encoding': '*'}
            print(headers)
            res = requests.get(self.url, headers=headers, verify=False)

            # add = urllib.request.Request(url=self.url, headers=headers)
            # res = urllib.request.urlopen(add)
            print('%s:%s chunk starts to download' % (start, end))
            # 写入文件对应位置
            with open(self.name, "r+b") as fp:
                fp.seek(start)
                var = fp.tell()
                fp.write(res.content)
            self.event_list[event_num].wait()
            print("Number[%d] block was written" % event_num)
            if event_num < len(self.event_list)-1:
                self.event_list[event_num+1].set()
        except http.client.IncompleteRead as e:
            print(e)
            # e.partial

    def run(self):
        # import datetime
        # starttime = datetime.datetime.now()
        thread_list = []
        n = 0
        for ran in self.get_range():
            start, end = ran
            print('thread %d Range:%s ~ %s Bytes' % (n, start, end))
            thread = threading.Thread(target=self.download, args=(start, end, n))
            thread.start()
            thread_list.append(thread)
            n += 1
        for t in thread_list:
            t.join()
        # map(lambda thd: thd.join(), thread_list)
        print('download %s load success' % (self.name))
        # endtime = datetime.datetime.now()
        # print((endtime - starttime).seconds)


if __name__ == "__main__":
    import datetime
    starttime = datetime.datetime.now()
    Downloader(url='https://apk.poizon.com/duApp/apk/Android_debug/4.62.0/app_release_test_20201223_1905_社区.apk', download_to='android.apk', thread_num=20).run()
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
