#coding=utf8
from flask import Flask
from flask import render_template
import json
from task_manager import IthomeSpiderProcess
import os
import logging
from minews.settings import LOG_LEVEL
print 'log level is %s' % (LOG_LEVEL, )
logging.basicConfig(level=LOG_LEVEL)

app = Flask(__name__)

info = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grab_ithome')
def grab_ithome():
    # item = {
    #     'title': '测试',
    #     'url': '#',
    #     'category': '小米'
    # }
    process = IthomeSpiderProcess()
    process.start()
    process.join()
    fp = 'output/result.json'
    logging.debug('file: %s exists: %s' % (fp, os.path.exists(fp), ))
    if os.path.exists(fp):
        items = json.load(open(fp, 'r'))
        for item in items:
            append_flag = True
            for i in info:
                if i.has_key('url'):
                    if i['url'] == item['url']:
                        append_flag = False
                        break
            if append_flag:
                info.append(item)
    return json.dumps(info)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)