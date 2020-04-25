#! /usr/bin/env python
# coding: utf-8
import os
import sys
import traceback

from flask import jsonify, request, render_template, send_from_directory, redirect
from config import read_conf
from jy_word.web_tool import send_msg_by_dd, format_time
from jy_word.File import File
from jy_word.Word import pic_b64encode

from create_app import create_app, sort_request1
from create_auth_code import create_strs, my_file, auth_code_path
from views.generate_report import generate_word
from views.tumor.report_panel import down_panel
from views.tumor.report_aiyi import filter_sv, float2percent

reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app()
restart_time = format_time(frm='%Y%m%d%H%M%S')
dir_name = os.path.dirname(__file__)
static_dir = os.path.join(dir_name, 'static')
project_dir = os.path.dirname(dir_name)

@app.route('/kobas3/')
@app.route('/kobas3')
@app.route('/')
# @app.route('')
def hello_world():
    conf = read_conf()
    system_name = conf.get('system_name')
    return render_template('index.html', restart_time=restart_time, system_name=system_name, conf=conf)


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
            t = format_time(frm='%Y%m%d%H%M%S')
            file_name = '%s.%s' % (t, name_array[-1])
            path = os.path.join(dir_path, file_name)
            f.save(path)
            return jsonify({'path': path, "message": 'success'})
        return jsonify({'len': len(request.files)})
    except Exception, e:
        traceback.print_exc()
        send_msg_by_dd(traceback.format_exc())
        return jsonify({'message': str(e)})


@app.route("/tcm/save/file/", methods=["POST", 'OPTIONS'])
def save_file():
    try:
        conf = read_conf()
        if isinstance(conf, str):
            return conf
        file_dir = conf.get('file_dir')
        if file_dir is None:
            return 'file_dir not in config.conf'
        rq = request.json
        if rq is None:
            return 'nothing is requested'
        content = rq.get('content')
        dir_path = os.path.join(file_dir, 'annotate', 'input')
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
        file_name = rq.get('file_name')
        if file_name is None:
            file_name = '%s.txt' % format_time(frm='%Y%m%d%H%M%S')
        path = os.path.join(dir_path, file_name)
        my_file.write(path, content)
        return jsonify({'path': path, "message": 'success'})
    except Exception, e:
        traceback.print_exc()
        send_msg_by_dd(traceback.format_exc())
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
                res_diagnosis = sort_request1('GET', '/api/v2/detection/diagnosis/', data={'sample_no': sample_no})
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
        traceback.print_exc()
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
    neoantigens = []
    if rq is not None:
        sample_no = rq.get('sample_no')
        item_name = rq.get('item_name')
        res = sort_request1('POST', '/api/v2/sample/detail/%s/' % sample_no)
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
        res_neoantigens = sort_request1('GET', '/api/v2/tumor/neoantigens/', data={'sample_no': sample_no})
        # neoantigens = get_api('/api/v2/tumor/neoantigens/', {'sample_no': sample_no}) or []
        if res_neoantigens is not None:
            neoantigens = res_neoantigens.get('data') or []

    w_sum = 10200
    diagnose = sample_detail.get('diagnosis') or ''
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

    variant_stars = filter(lambda x: x['add_star'] > 0, variant_list)
    cnvs_stars = filter(lambda x: x['add_star'] > 0, cnvs)
    svs_stars0 = filter(lambda x: x['add_star'] > 0, svs)
    svs_stars = filter(lambda x: filter_sv(x), svs)
    stars = sorted(variant_stars + cnvs_stars+svs_stars, key=lambda x: x['add_star'], reverse=True)
    # stars = sorted(variant_stars, key=lambda x: x['add_star'], reverse=True)
    stars0 = sorted(variant_stars + cnvs_stars+svs_stars0, key=lambda x: x['add_star'], reverse=True)

    msi_sort_paired_total = overview.get('msi_sort_paired_total')
    msi_sort_paired_somatic = overview.get('msi_sort_paired_somatic')
    try:
        msi_score = int(msi_sort_paired_somatic / float(msi_sort_paired_total) * 10000) / 100.0
    except:
        msi_score = 0

    msi_info = {
        'index': 'MSI',
        'total': msi_sort_paired_total,
        'somatic': msi_sort_paired_somatic,
        'score': msi_score,
        'text': 'MSS微卫星稳定',
        'effect': 'PD1等免疫检查点抗体可能效果不显著',
        'level': '',
        'w': 3000
    }
    if msi_score < 3.5:
        msi_info['sign'] = 'MSS'
    elif msi_score < 10:
        msi_info['text'] = 'MSI-L微卫星低不稳定'
        msi_info['sign'] = 'MSI-L'
    elif msi_score >= 10:
        msi_info['text'] = 'MSI-H微卫星高不稳定'
        msi_info['effect'] = 'PD1等免疫检查点抗体可能有效(A)'
        msi_info['level'] = 'A'
        msi_info['sign'] = 'MSI-H'

    tmb = overview.get('tmb')
    try:
        tmb = float(tmb)
    except:
        tmb = tmb
    tmb_tip = '注：NSCLC未经选择人群PD抗体有效率，具吸烟史为22%，无吸烟史为10%'
    if diagnose in '结直肠癌':
        tmb_tip = '注：MSS微卫星稳定结直肠癌患者PD1抗体有效率为0%；MSI-H微卫星不稳定结直肠癌患者有效率为29.6%。'
    tmb_percentage = overview.get('tmb_percentage')
    # print tmb_percentage, type(tmb_percentage)
    tmb_percentage = float2percent(tmb_percentage, 1)

    tmb_info = {
        'index': 'TMB',
        'w': w_sum-300-3000,
        'result': 'TMB肿瘤突变负荷低 （%s个突变/Mb）' % (tmb),
        'level': '',
        'tmb_tip': '',
        'effect': 'PD1等免疫检查点抗体治疗可能效果不显著',
        'tmb_percentage': tmb_percentage,
        'tmb': tmb
    }

    tmb_percentage_text = ''
    if tmb_percentage:
        tmb_percentage_text = '，大于该癌种%s人群' % tmb_percentage
    tmb_effect = '低'
    if tmb >= 10 and tmb < 20:
        if diagnose not in ['结直肠癌', '胰腺癌']:
            tmb_info['level'] = 'B' if diagnose == '非小细胞肺癌' else 'C'
            tmb_effect = '高'
    elif tmb >= 20:
        tmb_effect = '高'
        if diagnose in ['结直肠癌', '胰腺癌']:
            tmb_info['level'] = 'C'
        elif diagnose in ['非小细胞肺癌']:
            tmb_info['level'] = 'A'
        else:
            tmb_info['level'] = 'B'
    tmb_info['result'] = 'TMB肿瘤突变负荷%s （%s个突变/Mb）' % (tmb_effect, tmb)
    tmb_info['text'] = '肿瘤突变负荷TMB%s（%s个突变/Mb%s）' % (tmb_effect, tmb, tmb_percentage_text)
    if tmb_info['level']:
        tmb_info['effect'] = 'PD1等免疫检查点抗体治疗可能有效（%s）' % tmb_info['level']
    try:
        file_path = down_panel({
            'item_name': item_name,
            'overview': overview or {},
            'diagnosis': diagnose,
            'sample_detail': sample_detail,
            'variant_list': variant_list,
            'cnvs': cnvs,
            'svs': svs,
            'stars': stars,
            'variant_stars': variant_stars,
            'stars0': stars0,
            'cnv_stars': cnvs_stars,
            'sv_stars': svs_stars,
            'rs_geno': rs_geno or [],
            'neoantigens': neoantigens or [],
            'msi_info': msi_info,
            'tmb_info': tmb_info,
            'hla_info': hla_info
        })
        return jsonify({'file_path': file_path})
    except:
        message = '下载报告遇到问题，已通知管理员。%s' % traceback.format_exc()
        traceback.print_exc()
        send_msg_by_dd(message)
        return {'message': message}


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
    if '..' in dir_name or 'password' in file_path:
        return 'Sorry, unavailable path.'
    # print dir_name
    # print file_name
    # print attachment_filename
    return send_from_directory(dir_name, file_name, as_attachment=True, attachment_filename=attachment_filename)


@app.route('/tumor/merge/excel/', methods=['GET', 'POST'])
def tumor_merge():
    def sort_merge(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
        input_key1 = rq.get('input_key1')
        input_key2 = rq.get('input_key2')
        way = rq.get('way')
        cmd = 'Rscript %s %s %s %s %s %s %s' % (
            r_path,
            input_file1, input_key1,
            input_file2, input_key2,
            output, way
        )
        return cmd, [os.path.dirname(input_file1), os.path.dirname(input_file2)]
    return tumor_app('merge', '/public/jingdu/budechao/lecture/lec1_merge/merge_demo.R', sort_merge)


@app.route('/tumor/tapply/', methods=['GET', 'POST'])
def tumor_tapply():
    def sort_tapply(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        input_key1 = rq.get('input_key1')
        cmd = 'Rscript %s %s %s %s %s %s %s' % (
            r_path,
            input_file1, input_key1,
            rq.get('start'), rq.get('end'),
            output, rq.get('method')
        )
        return cmd, [os.path.dirname(input_file1)]
    return tumor_app('tapply', '/public/jingdu/budechao/lecture/lec2_tapply/tapply_demo.R', sort_tapply)


@app.route('/tumor/reorder/', methods=['GET', 'POST'])
def reorder_col():
    def sort_reorder(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        order_file = sort_app_file('order', 'order_file', result_dir, t)
        cmd = 'Rscript %s %s %s %s' % (
            r_path,
            input_file1, order_file,
            output
        )
        return cmd, [os.path.dirname(input_file1), os.path.dirname(order_file)]
    return tumor_app('reorder', '/public/jingdu/budechao/lecture/lec3_reorder/reorder_col.R', sort_reorder)


@app.route('/tumor/join/', methods=['GET', 'POST'])
def join_table():
    def sort_join(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
        dir1 = os.path.dirname(input_file1)
        dir2 = os.path.dirname(input_file2)
        cmd = 'Rscript %s %s %s %s %s' % (
            r_path,
            input_file1, input_file2,
            output, rq.get('id')
        )
        return cmd, [dir1, dir2]
    return tumor_app('join', '/public/jingdu/budechao/lecture/lec4_join/join_demo.R', sort_join)


@app.route('/tumor/pheatmap/', methods=['GET', 'POST'])
def pheatmap_colTree():
    def sort_pheatmap(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        dir1 = os.path.dirname(input_file1)
        ftsize_row = rq.get('ftsize_row')
        ftsize_col = rq.get('ftsize_col')
        cluster_method = rq.get('cluster_method')
        output_file = '%spdf' % output[:-3]
        cmd = 'Rscript %s %s %s %s %s %s %s' % (
            r_path,
            input_file1, output_file, ftsize_row, ftsize_col,
            cluster_method, output
        )
        print cmd
        return cmd, [dir1]
    return tumor_app('pheatmap', '/public/jingdu/budechao/scripts/run_pheatmap_colTree.R', sort_pheatmap)


def sort_app_file(key, file_key, result_dir, t):
    rq = request.json
    input_file1 = rq.get(file_key)
    if input_file1 is None:
        input_file1 = os.path.join(result_dir, '%s_%s.txt' % (file_key, t))
        my_file.write(input_file1, rq.get(key))
    return input_file1


def tumor_app(app_name, r_path, sort_func, output_postfix='txt'):
    env_key = 'AY_USER_DATA_DIR'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    env = conf.get('env')
    JINGD_DATA_ROOT = os.environ.get(env_key) or conf.get('jingd_data_root')
    r_dir = os.path.dirname(r_path)
    output_dir = os.path.join(JINGD_DATA_ROOT, app_name)
    if os.path.exists(output_dir) is False:
        os.makedirs(output_dir)
        # return jsonify({'message': 'Path not exists, %s' % path})
    tapply_info = os.path.join(output_dir, '%s_app_info.json' % app_name)
    t = format_time(frm='%Y%m%d%H%M%S')
    items = my_file.read(tapply_info) or []
    if request.method == 'POST':
        rq = request.json
        output_file = '%s.output.%s.%s' % (app_name, t, output_postfix)
        output = os.path.join(output_dir, output_file)
        cmd_dev, dirs = sort_func(rq, r_path, output, output_dir, t)
        dirs += [output_dir, r_dir]
        # docker run -rm -v data_dir:/data -w /data bio_r
        cmd = 'docker run --rm'
        for i in list(set(dirs)):
            cmd += ' -v %s:%s' % (i, i)
        cmd += ' bio_r '
        if env and env.startswith('Development'):
            cmd = ''
        cmd += cmd_dev
        try:
            os.system(cmd)
        except:
            return jsonify({'message': traceback.format_exc()})
        rq.update({
            'output': output,
            'add_time': t,
        })
        items.insert(0, rq)
        my_file.write(tapply_info, items)
        if os.path.exists(output):
            # data = my_file.read(output)
            return jsonify({'data': {'file_path': output, 'dir': output_dir, 'file_name': output_file}, 'message': 'success', 'status': 100001})
        return jsonify({'message': u'输出文件生成失败', 'cmd': cmd})
    return jsonify({'data': items, 'message': 'success'})


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


@app.route("/tcm/remark/crud/", methods=["GET", "POST", "PUT", "DELETE"])
def remark_crud():
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    file_dir = conf.get('file_dir')
    if file_dir is None:
        return 'file_dir not in config.conf'
    remark_dir = os.path.join(file_dir, 'remark')
    if os.path.exists(remark_dir) is False:
        os.makedirs(remark_dir)

    method = request.headers.get('API-METHOD') or request.method
    t = format_time(frm='%Y%m%d%H%M%S')
    if method == 'POST':
        rq = request.json
        rq['add_time'] = t
        path_new = os.path.join(remark_dir, 'remark_%s.json' % t)
        my_file.write(path_new, rq)
    if method.lower() == 'delete':
        rq = request.json
        add_time = rq.get('add_time')
        path_delete = os.path.join(remark_dir, 'remark_%s.json' % add_time)
        if os.path.exists(path_delete):
            item_delete = my_file.read(path_delete)
            if item_delete.get('account') == rq.get('account'):
                os.remove(path_delete)
    if method.lower() == 'put':
        rq = request.json
        add_time = rq.get('add_time')
        path_put = os.path.join(remark_dir, 'remark_%s.json' % add_time)
        if os.path.exists(path_put):
            item_put = my_file.read(path_put)
            item_put.update(rq)
            my_file.write(path_put, item_put)
    items = []
    for i in os.listdir(remark_dir):
        path = os.path.join(remark_dir, i)
        item = my_file.read(path)
        items.append(item)
    account = request.args.get('account') if method == 'GET' else request.json.get('account')
    items = filter(lambda x: x.get('account') == account, items)
    items.reverse()
    return jsonify(items)


@app.route('/tcm/file/', methods=['POST'])
def get_file():
    rq = request.json
    pre = rq.get('query_path') or ''
    postfix = rq.get('postfix') or []
    root_path = rq.get('root_path') or ''
    env_key = rq.get('env_key') or 'AY_USER_DATA_DIR'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    # print conf
    # JINGD_DATA_ROOT = os.environ.get('JINGD_DATA_ROOT') or conf.get('jingd_data_root')
    JINGD_DATA_ROOT = os.environ.get(env_key) or conf.get('jingd_data_root')
    path = os.path.join(JINGD_DATA_ROOT, root_path, pre)
    if os.path.exists(path) is False:
        os.makedirs(path)
        return jsonify({'message': 'Path not exists, %s' % path})
    file2 = File(path)
    data = file2.get_file_list('s', '', postfix=postfix)
    data['data']['data_root'] = JINGD_DATA_ROOT
    data['data']['sep'] = os.path.sep
    return jsonify(data)


@app.route('/file/content/', methods=['POST'])
def get_file_content():
    rq = request.json
    dir_name = rq.get('dir') or ''
    file_name = rq.get('file_name') or ''
    path = os.path.join(dir_name, file_name)
    if os.path.exists(path) is False:
        return 'Path not exists, %s' % path
    data = my_file.read(path)
    import chardet
    try:
        encoding = chardet.detect(data[0])['encoding']
        data = data.decode(encoding, 'ignore').encode('utf-8')
    except:
        traceback.print_exc()
    return jsonify({'message': 'success', 'data': data, 'file_path': path})


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


@app.route('/kobas3/avai/taxonomy/', methods=['GET'])
def get_avi_taxonomy():
    dir_name = os.path.dirname(__file__)
    static_dir = os.path.join(dir_name, 'static')
    json_dir = os.path.join(static_dir, 'json')
    file_path = os.path.join(json_dir, 'avai_taxonomy.txt')
    lines = my_file.read(file_path).strip('\n').split('\n')
    items = []
    kinds1 = []
    kinds2 = []
    for line in lines:
        line = line.split('\t')
        kind1 = line[-2]
        kind2 = line[-1]
        dict3 = {'value': line[0], 'label': line[2], 'kind1': kind1, 'kind2': kind2}
        if kind1 not in kinds1:
            kinds1.append(kind1)
        if kind2 not in kinds2:
            kinds2.append(kind2)
        items.append(dict3)
    items3 = []
    # print kinds1
    kinds1 = ['Animals', 'Plants', 'Fungi', 'Protists', 'Bacteria', 'Archaea']
    for k1 in kinds1:
        items4 = []
        for k2 in kinds2:
            arr12 = filter(lambda x: x.get('kind1') == k1 and x.get('kind2') == k2, items)
            if len(arr12) > 0:
                arr12.sort(key=lambda x:x.get('label'))
                items4.append({'value': k2, 'label': k2, 'children': arr12})
        if len(items4) > 0:
            items4.sort(key=lambda x: x.get('label'))
            items3.append({'value': k1, 'label': k1, 'children': items4})
    # my_file.write('sss.json', items3)
    return jsonify({'data': items3, 'message': 'success'})


def update_static(project_dir, postfix1=''):
    import shutil
    dist_dir = os.path.join(project_dir, 'dist')
    for postfix in ['js', 'css']:
        src_file_name = 'umi.%s' % postfix
        file_name = src_file_name
        if postfix1:
            file_name = 'umi_%s.%s' % (postfix1, postfix)
        src = os.path.join(dist_dir, src_file_name)
        des = os.path.join(static_dir, file_name)
        if os.path.exists(src):
            # print src, des
            shutil.copy(src, des)


if __name__ == '__main__':

    from jy_word.web_tool import get_host, killport
    port = 9003
    host_info = get_host(port)
    text = '/detection/admin/'
    '98a749a93a86d15af5b9634c2db53f71'
    host_ip = host_info.get('ip')
    # killport(9005)
    killport(port)    # host_ip = '192.168.105.66'

    update_static(os.path.join(project_dir, 'TCM'))
    update_static(os.path.join(project_dir, 'KOBARSWeb'), 'kobars')
    # shutil.copytree(r'D:\pythonproject\KOBARSWeb\dist', r'D:\pythonproject\TCMWeb\templates\kobars')
    app.run(host=host_ip, port=port)
