#! /usr/bin/env python
# coding: utf-8
import os
import traceback

from flask import jsonify, request, render_template, redirect, send_from_directory
from config import read_conf
from jy_word.web_tool import send_msg_by_dd, get_host, format_time

from create_app import create_app, sort_request1
from create_auth_code import create_strs, my_file, auth_code_path
from views.generate_report import generate_word


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
    method = request.method
    data = request.args if method == 'GET' else request.json
    url = request.headers.get('API-URL')
    api_service = request.headers.get('API-SERVICE')
    success_status = request.headers.get('SUCCESS-STATUS')
    api_method = request.headers.get('API-METHOD')
    if api_method is not None:
        method = api_method
    response_data = sort_request1(method, url, api_service, data=data)
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


@app.route("/tcm/download/report/", methods=["POST"])
def auth_down_report():
    # file_path = 'sss'
    rq = request.json
    sample_detail, patient_detail, diagnosis = None, None, None
    if rq is not None:
        sample_no = rq.get('sample_no')
        res = sort_request1('POST', '/api/v2/sample/detail/%s/' % sample_no)
        if res is not None:
            sample_detail = res.get('data')
            if sample_detail is not None:
                patient_no = sample_detail.get('patient_no')
                template = sample_detail.get('template')
                res_patient = sort_request1('GET', '/api/v2/patient/detail/%s/' % patient_no)
                if res_patient is not None:
                    patient_detail = res_patient.get('data')
                res_diagnosis = sort_request1('GET', '/api/v2/detection/diagnosis', data={'sample_no': sample_no})
                if res_diagnosis is not None:
                    diagnosis = res_diagnosis.get('data')
    try:
        file_path = generate_word({
            'sample_detail': sample_detail,
            'patient_detail': patient_detail,
            'diagnosis': diagnosis or []
        })
        return jsonify({'file_path': file_path})
    except:
        send_msg_by_dd(traceback.format_exc())
        return '发生故障，已通知管理员，请稍后...'


@app.route('/tcm/download/', methods=["GET", "POST", "PUT", "DELETE", 'OPTIONS'])
def download_file():
    rq = request.args.to_dict()
    file_path = rq.get('file_path')
    dir_name = os.path.dirname(file_path)
    file_name = os.path.relpath(file_path, dir_name)
    # file_name = rq.get('file_name')
    attachment_filename = rq.get('attachment_filename')
    t = format_time(frm='%Y%m%d%H%M%S')
    if attachment_filename is None:
        file_names = file_name.split('.')
        attachment_filename = '%s_%s.%s' % ('.'.join(file_names[:-1]), t, file_names[-1])
    # print dir_name
    # print file_name
    # print attachment_filename
    return send_from_directory(dir_name, file_name, as_attachment=True, attachment_filename=attachment_filename)


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
    text = '/detection/admin/'
    '98a749a93a86d15af5b9634c2db53f71'
    app.run(host=host_info.get('ip'), port=port)
