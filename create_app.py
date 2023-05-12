#! /usr/bin/env python
# coding: utf-8
import base64
import json
import requests
from flask import Flask, request
from flask_cors import CORS
from jy_word.web_tool import send_msg_by_dd
from config import read_conf


def create_app():
    my_app = Flask(__name__)
    my_app.config.update(
        MAX_CONTENT_LENGTH=50 * 1024 * 1024 * 1024
    )
    CORS(my_app, supports_credentials=True)
    return my_app


def sort_request1(method, url, api_service='api', auth=None, data=None, remote_addr='', rq_url='', files=None):
    # 配置文件
    conf = read_conf()
    ports = conf.get('ports')
    endpoint = conf.get('endpoint')
    env = conf.get('env')
    # 请求相关
    success_status = request.headers.get('SUCCESS-STATUS')
    api_method = request.headers.get('API-METHOD')
    if api_method is not None:
        method = api_method
    if auth is None:
        auth = request.headers.get('Authorization')
    xAuth = request.headers.get('X-Authorization')
    # start
    error_message = ''
    response_data = None
    status = None
    if isinstance(conf, str):
        error_message = conf
    if ports is None:
        error_message = 'No ports found in config.conf'
    elif api_service not in ports:
        error_message = u'暂无此服务：%s. 目前服务有：%s\n' % (api_service, ports.keys())
    else:
        port = ports[api_service]
        if conf.get('port'):
            port = conf.get('port')
        if conf.get(api_service):
            port = conf.get(api_service)
        if url.startswith('http://') or url.startswith('https://'):
            api_url = url
        else:
            api_url = endpoint + ':' + port + url
        data = data or {}
        request_params = {'json': data} if method != 'GET' else {'params': data}
        headers = {'Content-Type': 'application/json'}
        if auth:
            headers['authorization'] = auth
        if xAuth:
            headers['X-Authorization'] = xAuth

        if files:
            request_params = {'data': data} if method != 'GET' else {'params': data}
            request_params['files'] = files
        else:
            request_params = {'json': data} if method != 'GET' else {'params': data}
            # headers = {}
            # headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        request_params['headers'] = headers
        request_params['stream'] = data.get('stream')

        try:
            response = requests.request(method, api_url, **request_params)
        except Exception, e:
            error_message = '%s\n' % str(e)
            response = None
        if response is not None:
            if response.status_code != 200:
                # print 'body', response.text.body
                error_message = "%s %s %d %s\n" % (api_url, "POST", response.status_code, response.text)
            else:
                try:
                    response_data = response.json()
                except:
                    return {'data': response.text}
                status = response_data.get('status')
        error_message += u'【请求服务】：%s\n' % api_service
        error_message += u'【api】：%s\n' % api_url
    if remote_addr:
        error_message += u'【访问ip】：%s\n' % remote_addr
    if rq_url:
        error_message += u'【访问地址】：%s\n' % rq_url
    error_message += u'【请求方式】：%s\n' % method
    error_message += u'【请求数据】：%s\n' % json.dumps(data)
    if status is not None:
        error_message += u'【状态码】:%d\n' % status
    error_message += u'【返回数据】：%s\n' % json.dumps(response_data)
    try:
        sss = base64.b64decode(str(auth).split(' ')[-1]).decode()
        error_message += u'【用户名】：%s\n' % sss.split(':')[0]
    except:
        import traceback
        # traceback.print_exc()
        error_message += ''
    # if self.is_print:
    #     print error_message
    # print headers
    # print error_message
    # if 'success' not in error_message.lower():
    #     try:
    #         send_msg_by_dd(error_message, env=env)
    #     except:
    #         print(error_message)
    if response_data is None:
        response_data = {'message': '请求接口返回异常：\n%s' % error_message, 'status': -1}
    return response_data