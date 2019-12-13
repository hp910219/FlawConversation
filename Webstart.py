#! /usr/bin/env python
# coding: utf-8
import os
import traceback

from flask import jsonify, request, render_template, send_from_directory
from config import read_conf
from jy_word.web_tool import send_msg_by_dd, format_time
from jy_word.File import File
from jy_word.Word import pic_b64encode

from create_app import create_app, sort_request1
from create_auth_code import create_strs, my_file, auth_code_path
from views.generate_report import generate_word
from views.tumor.report_panel import down_panel


app = create_app()
restart_time = format_time(frm='%Y%m%d%H%M%S')


@app.route('/')
def hello_world():
    conf = read_conf()
    system_name = conf.get('system_name')
    return render_template('kobars/index.html', restart_time=restart_time, system_name=system_name, conf=conf)


@app.errorhandler(404)
def page_not_found(e):
    conf = read_conf()
    system_name = conf.get('system_name')
    # print 'system_name', system_name
    return render_template('index.html', restart_time=restart_time, system_name=system_name, conf=conf)


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


@app.route("/tumor/download/report/", methods=["POST"])
def tumor_download_panel():
    # file_path = 'sss'
    rq = request.json
    sample_detail, variant_list, overview, item_name = {}, [], {}, ''
    cnvs = []
    svs = []
    rs_geno = []
    if rq is not None:
        sample_no = rq.get('sample_no')
        item_name = rq.get('item_name')
        res = sort_request1('GET', '/api/v2/sample/report/%s/' % sample_no)
        if res is not None:
            sample_detail = res.get('data') or {}

        res2 = sort_request1('GET', '/api/v2/tumor/variants/?sample_no=%s' % sample_no)
        if res2 is not None:
            variant_list = res2.get('data') or []
        res3 = sort_request1('GET', '/api/v2/tumor/overview/?sample_no=%s' % sample_no)
        if res3 is not None:
            overview = res3.get('data') or {}
        # patient_no = sample_detail.get('patient_no')
        # patient_detail = {}
        # if patient_no:
        #     patient_detail = get_api('/api/v2/patient/detail/%s/' % patient_no) or {}
        # report_detail = get_api('/api/v2/sample/report/%s/' % sample_no) or {}
        res_cnvs = sort_request1('GET', '/api/v2/tumor/cnvs/', data={'sample_no': sample_no})
        if res_cnvs is not None:
            cnvs = res_cnvs.get('data') or []
        res_svs = sort_request1('GET', '/api/v2/tumor/svs/', data={'sample_no': sample_no})
        if res_svs is not None:
            svs = res_svs.get('data') or []
        res_geno = sort_request1('GET', '/api/v2/tumor/genotype/', data={'sample_no': sample_no})
        if res_geno is not None:
            rs_geno = res_geno.get('data') or []

    variant_stars = filter(lambda x: x['add_star'] > 0, variant_list)
    cnvs_stars = filter(lambda x: x['add_star'] > 0, cnvs)
    svs_stars = filter(lambda x: x['add_star'] > 0, svs)
    stars = sorted(variant_stars, key=lambda x: x['add_star'])

    w_sum = 10200

    msi_sort_paired_total = overview.get('msi_sort_paired_total')
    msi_sort_paired_somatic = overview.get('msi_sort_paired_somatic')
    msi_score = int(msi_sort_paired_somatic/float(msi_sort_paired_total) * 10000) / 100.0

    msi_info = {
        'total': msi_sort_paired_total,
        'somatic': msi_sort_paired_somatic,
        'score': msi_score,
        'text': 'MSS微卫星稳定',
        'effect': 'PD1等免疫检查点抗体可能效果不显著',
        'level': '',
        'w': 2000
    }
    if msi_score < 3.5:
        msi_info['sign'] = 'MSS'
    elif msi_score < 10:
        msi_info['text'] = 'MSS微卫星低不稳定'
        msi_info['sign'] = 'MSI-L'
    elif msi_score >= 10:
        msi_info['text'] = 'MSS微卫星高不稳定'
        msi_info['effect'] = 'PD1等免疫检查点抗体可能有效'
        msi_info['level'] = 'A'
        msi_info['sign'] = 'MSI-H'
    diagnose = sample_detail.get('diagnose')
    tmb = overview.get('tmb')
    tmb_info = {
        'tmb': tmb,
        'w': w_sum-300-2000,
        'text': '',
        'effect': '',
        'level': 'C'
    }
    if tmb <= 20:
        tmb_info['text'] = '肿瘤突变负荷TMB低 （%s个突变/Mb，大于该癌种%s%%人群，%s于该癌种突变负荷拐点）' % (tmb, 85, '低')
        tmb_info['level'] = 'B' if diagnose == '非小细胞肺癌' else 'C'
    elif tmb > 20:
        tmb_info['text'] = '肿瘤突变负荷TMB高 （%s个突变/Mb，大于该癌种%s%%人群，%s于该癌种突变负荷拐点）' % (tmb, 85, '高')
        tmb_info['level'] = 'A' if diagnose == '非小细胞肺癌' else 'B'

    hla_genes = ['HLA-A', 'HLA-B', 'HLA-C']
    hla_items = []
    hla_type = '杂合型'
    for gene in hla_genes:
        # col2 =
        key1 = gene.replace('-', '_') + '1'
        key2 = gene.replace('-', '_') + '2'
        col2 = overview.get(key1.lower())
        col3 = overview.get(key2.lower())
        col4 = '杂合型'
        if col2 == col3:
            col4 = '纯合型'
            hla_type = '纯合型'
        hla_items.append({'col1': gene, 'col2': col2, 'col3': col3, 'col4': col4})
    hla_info = {
        'genes': hla_genes,
        'items': hla_items,
        'hla_type': hla_type
    }
    try:
        file_path = down_panel({
            'item_name': item_name,
            'overview': overview or {},
            'diagnose': diagnose,
            'sample_detail': sample_detail,
            'variant_list': variant_list,
            # 'report_detail': report_detail or {},
            # 'patient_detail': patient_detail,
            'cnvs': cnvs,
            'svs': svs,
            'stars': stars,
            'variant_stars': variant_stars,
            'cnv_stars': cnvs_stars,
            'sv_stars': svs_stars,
            'rs_geno': rs_geno or [],
            'msi_info': msi_info,
            'tmb_info': tmb_info,
            'hla_info': hla_info
        })
        return jsonify({'file_path': file_path})
    except:
        traceback.print_exc()
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


@app.route('/tcm/file/', methods=['POST'])
def get_file():
    rq = request.json
    pre = rq.get('query_path') or ''
    postfix = rq.get('postfix') or []
    root_path = rq.get('root_path') or ''
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    # print conf
    JINGD_DATA_ROOT = os.environ.get('JINGD_DATA_ROOT') or conf.get('jingd_data_root')
    path = os.path.join(JINGD_DATA_ROOT, root_path, pre)
    if os.path.exists(path) is False:
        return 'Path not exists, %s' % path
    file2 = File(path)
    data = file2.get_file_list('s', '', postfix=postfix)
    data['data']['data_root'] = JINGD_DATA_ROOT
    data['data']['sep'] = os.path.sep
    return jsonify(data)


@app.route('/transfer/img/', methods=['POST'])
def transfer_img():
    rq = request.json
    if rq is None:
        return jsonify({'message': '请求错误'})

    file_path = rq.get('file_path')
    if file_path is None:
        return jsonify({'message': 'file_path: %s' % file_path})
    if os.path.exists(file_path) is False:
        return jsonify({'message': 'file not exists: %s' % file_path})
    data = {'img': pic_b64encode(file_path), 'file_path': file_path}
    return jsonify(data)


if __name__ == '__main__':
    port = 9003
    from jy_word.web_tool import get_host
    host_info = get_host(port)
    text = '/detection/admin/'
    '98a749a93a86d15af5b9634c2db53f71'
    host_ip= host_info.get('ip')
    from jy_word.web_tool import killport
    # killport(9005)
    killport(port)
    # host_ip = '192.168.105.66'
    src = r'D:\pythonproject\TCM3\dist\umi.js'
    des = r'D:\pythonproject\TCMWeb\static\umi.js'
    src_kobars = r'D:\pythonproject\KOBARSWeb\dist\umi.js'
    des_kobars = r'D:\pythonproject\TCMWeb\static\umi_kobars.js'
    import shutil
    shutil.copy(src, des)
    shutil.copy(src_kobars, des_kobars)
    # shutil.copytree(r'D:\pythonproject\KOBARSWeb\dist', r'D:\pythonproject\TCMWeb\templates\kobars')
    app.run(host=host_ip, port=port)
