#! /usr/bin/env python
# coding: utf-8
import base64
import json
import os
import requests

from flask import jsonify, request, render_template
from config import read_conf
from jy_word.web_tool import send_msg_by_dd, get_host, format_time

from create_app import create_app
from create_auth_code import create_strs, my_file, auth_code_path


app = create_app()
restart_time = format_time(frm='%Y%m%d%H%M%S')


@app.route('/')
def hello_world():
    return render_template('index.html', restart_time=restart_time)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', restart_time=restart_time)


@app.route("/tcm/api/", methods=["GET", "POST", "PUT", "DELETE"])
def tcm_api():
    # 配置文件
    conf = read_conf()
    ports = conf.get('ports')
    endpoint = conf.get('endpoint')
    env = conf.get('env')
    # 请求相关
    method = request.method
    data = request.args if method == 'GET' else request.json
    url = request.headers.get('API-URL')
    api_service = request.headers.get('API-SERVICE')
    success_status = request.headers.get('SUCCESS-STATUS')
    api_method = request.headers.get('API-METHOD')
    if api_method is not None:
        method = api_method
    auth = request.headers.get('Authorization')
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
        api_url = endpoint + ':' + ports[api_service] + url
        request_params = {'json': data} if method != 'GET' else {'params': data}
        headers = {'Content-Type': 'application/json'}
        if auth:
            headers['Authorization'] = auth
        request_params['headers'] = headers
        try:
            response = requests.request(method, api_url, **request_params)
        except Exception, e:
            error_message = '%s\n' % str(e)
            response = None
        if response is not None:
            if response.status_code != 200:
                error_message = "%s %s %d %s\n" % (api_url, "POST", response.status_code, response.text)
            else:
                response_data = response.json()
                status = response_data.get('status')
        error_message += u'【请求服务】：%s\n' % api_service
        error_message += u'【api】：%s\n' % api_url
    error_message += u'【访问ip】：%s\n' % request.remote_addr
    error_message += u'【访问地址】：%s\n' % request.url
    error_message += u'【请求方式】：%s\n' % method
    error_message += u'【请求数据】：%s\n' % json.dumps(data)
    if status is not None:
        error_message += u'【状态码】:%d\n' % status
    error_message += u'【返回数据】：%s\n' % json.dumps(response_data)
    try:
        sss = base64.b64decode(auth).decode()
        error_message += u'【用户名】：%s\n' % sss.split(':')[0]
    except:
        error_message += ''
    # if self.is_print:
    #     print error_message
    if 'success' not in error_message.lower():
        try:
            send_msg_by_dd(error_message, env=env)
        except:
            print(error_message)
    return jsonify(response_data)


@app.route("/tcm/upload/file/", methods=["POST", 'OPTIONS'])
def upload_report():
    try:
        conf = read_conf()
        if isinstance(conf, str):
            return conf
        file_dir = conf.get('file_dir')
        if file_dir is None:
            return 'file_dir not in config.conf'
        if len(request.files) == 0:
            return jsonify({"success": False, "message": 'select file'})
        for k in request.files:
            f = request.files[k]
            name_array = f.filename.split('.')
            dir_path = os.path.join(file_dir, name_array[-1])
            if os.path.exists(dir_path) is False:
                os.makedirs(dir_path)
            path = os.path.join(dir_path, '.'.join(name_array[-2:]))
            f.save(path)
            return jsonify({'path': path, "message": 'success'})
        return jsonify({'len': len(request.files)})
    except Exception, e:
        send_msg_by_dd(str(e))
        return jsonify({'message': str(e)})


@app.route("/tcm/auth/code/", methods=["GET", "POST", 'OPTIONS'])
def auth_code():
    items = create_strs(1000)
    return jsonify(items)


@app.route("/tcm/code/crud/", methods=["GET", "POST", "PUT", "DELETE"])
def auth_code_crud():
    items = create_strs(1000)
    rq = request.args.to_dict() if request.method == 'GET'else request.json
    if request.method == 'POST':
        items = create_strs(len(items) + int(rq.get('num')), rq.get('belong'))
        return jsonify(items)
    f_items = filter(lambda x: x['code'] == rq.get('code'), items)
    if len(f_items) == 0:
        return jsonify({'message': '邀请码不存在'})
    f_item = f_items[0]
    if request.method == 'GET':
        return jsonify(f_item)
    if request.method == 'PUT':
        f_item.update(rq)
    my_file.write(auth_code_path, items)
    return jsonify(f_item)


if __name__ == '__main__':
    port = 9002
    host_info = get_host(port)
    app.run(host=host_info.get('ip'), port=port)
