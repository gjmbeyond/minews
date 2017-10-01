#coding=utf8
import scrapy
from scrapy.spiders import Spider
from win32api import *
from win32gui import *
import win32api, win32con
import sys, os
import struct
import time
import multiprocessing
import winsound
import json

reload(sys)
sys.setdefaultencoding('utf8')

def show_msg_box(title, msg):
    win32api.MessageBox(0, msg, title, win32con.MB_OK)

class IthomeSpider(Spider):
    name = 'IthomeSpider'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "BEC=DD6D195E2C1060E7C26D2140DE587438|Wc+hs|Wc+gK; Hm_lvt_cfebe79b2c367c4b89b285f412bf9867=1505024681,1506779226; Hm_lpvt_cfebe79b2c367c4b89b285f412bf9867=1506779616",
        "Host": "www.ithome.com",
        "If-Modified-Since": "Sat, 30 Sep 2017 13:49:09 GMT",
        "If-None-Match": 'W/"8228e8e3f239d31:0"',
        "Referer": "https://www.ithome.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }
    targets = [u'小米', u'红米']
    result = []

    def __init__(self, param1=None, *args, **kwargs):
        super(IthomeSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.ithome.com/blog.htm']
    
    def start_requests(self):
        yield scrapy.FormRequest(self.start_urls[0], headers=self.headers, callback=self.parse_content)

    def parse_content(self, response):
        print "enter %s" % (self.parse_content.__name__, )
        base_path = '//ul[@class="ulcl"]'
        lis_path = base_path + '/li'
        for i in range(0, len(response.xpath(lis_path))):
            title_path = lis_path + '[' + str(i+1) + ']/div/h2'
            title = response.xpath(title_path).xpath('string(.)').extract()[0]
            title = title.replace(' ', '')
            thread_path = lis_path + '[' + str(i+1) + ']/div/h2/a/@href'
            thread_url = response.xpath(thread_path).extract()[0]
            (matched, cat) = self.is_match(title)
            if matched:
                print 'title=%s; match_keyword=%s; url=%s' % (title, cat, thread_url, )
                r = {
                    'title': title,
                    'url': thread_url,
                    'category': cat
                }
                self.result.append(r)
        output_dir = 'output/'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        print 'dir: %s exists: %s' % (output_dir, os.path.exists(output_dir), )
        with open(output_dir+'result.json', 'w') as fd:
            fd.write(json.dumps(self.result, ensure_ascii=False))
                # winsound.Beep(600,1000)
                # p = multiprocessing.Process(target=show_msg_box, args=(u"新闻提醒", 'title=%s; match_keyword=%s' % (title, cat), ))
                # p.start()
                # win32api.MessageBox(0, 'title=%s; match_keyword=%s' % (title, cat), u"新闻提醒", win32con.MB_OK)
                # w = WindowsBalloonTip(
                #     u"新闻提醒".encode('gbk'),
                #     ('title=%s; match_keyword=%s' % (title, cat)).encode('gbk')
                # )

    def is_match(self, title):
        for s in self.targets:
            try:
                if title.index(s) > -1:
                    return (True, s)
            except:
                continue
        return (False, None)

class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",title,200,msg))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

