#! /usr/bin/env python
# coding: utf-8
import chardet
import os
import sys
import subprocess
import traceback
import json

from flask import jsonify, request, render_template, send_from_directory, redirect
from config import read_conf
from jy_word.web_tool import send_msg_by_dd, format_time, zip_dir
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
restart_time = format_time(frm='%Y-%m%d-%H:%M:%S')
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
    return render_template('index.html',
                           static_dir=static_dir.rstrip('/'),
                           restart_time=restart_time, system_name=system_name, conf=conf)


@app.errorhandler(404)
def page_not_found(e):
    conf = read_conf()
    system_name = conf.get('system_name')
    # print 'system_name', system_name
    return render_template('index.html', static_dir=static_dir.rstrip('/'), restart_time=restart_time, system_name=system_name, conf=conf)


@app.route("/en/tcm/api/", methods=["GET", "POST", "PUT", "DELETE"])
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
            file_name = '%s%s.%s' % ('.'.join(name_array[0:-1]), t, name_array[-1])
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
        print path
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
    chemotherapy = []
    hotspots = []
    variant_list_all = []
    hotspots_all = []
    if rq is not None:
        sample_no = rq.get('sample_no')
        item_name = rq.get('item_name')
        res = sort_request1('POST', '/api/v2/sample/detail/%s/' % sample_no)
        if res is not None:
            sample_detail = res.get('data') or {}

        res2 = sort_request1('GET', '/api/v2/tumor/variants/?sample_no=%s&fil_status=1' % sample_no)
        if res2 is not None:
            variant_list_all = res2.get('data') or []
            variant_list = filter(lambda x: x.get('fil_status') == 0, variant_list_all)
        res2hotspot = sort_request1('GET', '/api/v2/tumor/hotspot/variants/?sample_no=%s&fil_status=1' % sample_no)
        if res2hotspot is not None:
            hotspots_all = res2hotspot.get('data') or []
            hotspots = filter(lambda x: x.get('fil_status') == 0, hotspots_all)
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
        if item_name == 'weizhi':
            res_chemotherapy = sort_request1('GET', '/api/v2/tumor/chemotherapy/', data={'sample_no': sample_no})
            if res_chemotherapy is not None:
                chemotherapy = res_chemotherapy.get('data') or []

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
    hotspots_stars = filter(lambda x: x['add_star'] > 1, hotspots)
    for h in hotspots_stars:
        h['add_star'] -= 1
    variant_stars += hotspots_stars
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
            'variant_list_all': variant_list_all,
            'cnvs': cnvs,
            'svs': svs,
            'stars': stars,
            'hotspots_stars': hotspots_stars,
            'variant_stars': variant_stars,
            'stars0': stars0,
            'cnv_stars': cnvs_stars,
            'sv_stars': svs_stars,
            'rs_geno': rs_geno or [],
            'chemotherapy': chemotherapy,
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
    if file_path is None:
        return 'Sorry, no path.'
    dir_name = os.path.dirname(file_path)
    file_name = os.path.relpath(file_path, dir_name)
    # file_name = rq.get('file_name')
    attachment_filename = rq.get('attachment_filename')
    t = format_time(frm='%Y%m%d%H%M%S')
    if '..' in dir_name or 'password' in file_path:
        return 'Sorry, unavailable path.'
    if 'passwd' in file_path:
        return 'Sorry, unavailable path.'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    env = conf.get('env')
    if env and env == 'KOBARS':
        if file_path not in ['/gpfs/www/kobas3/site/kobas-2.1.1/kobas-2.1.1.tar.gz',
                             '/gpfs/www/kobas3/site/kobas-2.1.1/kobas-3.0.3.tar.gz']:
            if dir_name.startswith('/gpfs/user/budc/kobas_2019/data/example') is False \
                    and dir_name.startswith('/gpfs/user/budc/kobas_2019/data/online') is False \
                    and dir_name.startswith('/gpfs/user/budc/app/app_data/output/') is False:
                return 'Sorry, unavailable path.'
    if attachment_filename is None:
        file_names = file_name.split('.')
        attachment_filename = '%s_%s.%s' % ('.'.join(file_names[:-1]), t, file_names[-1])
    if os.path.exists(file_path) is False:
        return 'Sorry, file_path dose not exists.'
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
        return cmd, [dir1]
    return tumor_app('pheatmap', '/public/jingdu/budechao/scripts/run_pheatmap_colTree.R', sort_pheatmap)


@app.route('/tumor/table2matrix/', methods=['GET', 'POST'])
def table2matrix():
    def sort_pheatmap(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        dir1 = os.path.dirname(input_file1)
        cmd = 'Rscript %s %s %s %s %s %s' % (
            r_path,
            input_file1,
            output,
            rq.get('source_node'),
            rq.get('target_node'),
            rq.get('relationship'),
        )
        return cmd, [dir1]
    return tumor_app('table2matrix', '/public/jingdu/budechao/lecture/lec5_table2matrix/table2matrix.R', sort_pheatmap)


@app.route('/tumor/herbScore/', methods=['GET', 'POST'])
def herbScore():
    shPath = '/public/jingdu/zss/Rscript-zss/app/herb/run_herb_interaction.sh'
    def sort_pheatmap(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        dir1 = os.path.dirname(input_file1)
        cmd = 'sh %s %s %s %s %s' % (
            r_path,
            '/public/jingdu/zss/Rscript-zss/app/herb/',
            '/public/jingdu/zss/Rscript-zss/app/herb',
            input_file1,
            output
        )
        return cmd, [dir1]
    return tumor_app('table2matrix', shPath, sort_pheatmap)


@app.route('/tumor/herbVisualization/', methods=['GET', 'POST'])
def herbVisualization():
    rPath = '/public/jingdu/zss/Rscript-zss/app/herb/run3_herbHeatmap.R'
    def sort_pheatmap(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        dir1 = os.path.dirname(input_file1)
        cmd = 'Rscript %s %s %s' % (
            r_path,
            input_file1,
            output
        )
        return cmd, [dir1]
    return tumor_app('table2matrix', rPath, sort_pheatmap, output_postfix='png')


@app.route('/tumor/ternaryPlot/', methods=['GET', 'POST'])
def tumor_ternaryPlot():
    rPath = '/public/jingdu/zss/Rscript-zss/app/ternaryplot/run_ternaryPlot.R'
    def sort_pheatmap(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        dir1 = os.path.dirname(input_file1)
        cmd = 'Rscript %s %s %s' % (
            r_path,
            input_file1,
            output
        )
        return cmd, [dir1]
    return tumor_app('ternaryPlot', rPath, sort_pheatmap, output_postfix='png')


@app.route('/tumor/signature/', methods=['GET', 'POST'])
def tumor_signature():
    rPath = '/public/jingdu/zss/Rscript-zss/app/signature/new/run_signature96_auto.sh'
    rPathDir = os.path.dirname(rPath)
    def sort_pheatmap(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
        dir1 = os.path.dirname(input_file1)
        BSg_type = rq.get('BSg_type')
        # sample_ids = rq.get('sample_ids')
        cmd = 'sh %s %s %s %s %s %s' % (
            r_path,
            input_file1,
            'freq96.tsv',
            BSg_type,
            output[:-4],
            rPathDir
        )
        return cmd, [dir1, rPathDir]
    return tumor_app(
        'signature',
        rPath,
        sort_pheatmap,
        output_postfix='zip',
        bio='bc_deconstructsigs'
    )


@app.route('/tumor/siRNA/', methods=['GET', 'POST'])
def tumor_siRNA():
    rPath = '/data/siRNA/run_siRNA_auto.sh'
    def sort_pheatmap(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', '/data/userdata', t)
        dir1 = os.path.dirname(input_file1)
        cmd = 'sh %s %s %s %s /data/siRNA' % (
            r_path,
            rq.get('filter_freq'),
            input_file1,
            result_dir
        )
        return cmd, [dir1]
    return tumor_app_siRNA('siRNA', rPath, sort_pheatmap, output_postfix='png')


def sort_app_file(key, file_key, result_dir, t):
    rq = request.json
    input_file1 = rq.get(file_key)
    if input_file1 is None:
        input_file1 = os.path.join(result_dir, '%s_%s.txt' % (file_key, t))
        my_file.write(input_file1, rq.get(key))
    return input_file1


def tumor_app(app_name, r_path, sort_func, output_postfix='txt', order1='--rm', bio='bio_r'):
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
    t = format_time(frm='%Y%m%d%H%M%S')
    items = []
    msg = ''
    # a + 5
    if request.method == 'POST':
        rq = request.json
        output_file = '%s.output.%s.%s' % (app_name, t, output_postfix)
        output = output_dir.rstrip('/') + '/' + output_file
        cmd_dev, dirs = sort_func(rq, r_path, output, output_dir, t)
        dirs += [output_dir, r_dir]
        # docker run -rm -v data_dir:/data -w /data bio_r
        cmd = 'docker run %s' % order1
        for i in list(set(dirs)):
            cmd += ' -v %s:%s' % (i, i)
        cmd += ' %s ' % bio
        if env and env.startswith('Development'):
            cmd = ''
        cmd += cmd_dev
        fileDir = output[:-4]
        isZip = output_postfix == 'zip'
        if isZip:
            if os.path.exists(fileDir) is False:
                os.makedirs(fileDir)
        print cmd
        try:
            code = os.system(cmd)
            # print code, t
            if code:
                # 获取错误日志
                try:
                    # scheduler_order = "top -u ybtao"
                    # os.system(cmd)
                    return_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    # next_line = return_info.stdout.readline()
                    # msg = next_line.decode("utf-8", "ignore")
                    # while True:
                    #     next_line = return_info.stdout.readline()
                    #     return_line = next_line.decode("utf-8", "ignore")
                    #     if return_line == '' and return_info.poll() is not None:
                    #         break
                    #     if return_line:
                    #         msg = return_line
                    #         print 'ssdfdf', msg
                    #         # break
                    # returncode = return_info.wait()
                    # if returncode:
                    #     print 'read', return_info.stdout.read()
                    #     raise subprocess.CalledProcessError(returncode, return_info)
                    msg = return_info.communicate()[0].decode('utf-8', 'ignore')
                except Exception, e:
                    print 'Exception', e
                    msg = traceback.format_exc()
                    send_msg_by_dd('app\n\n%s' % msg)
                    if isZip:
                        os.removedirs(fileDir)
                    # msg = traceback.format_exc()
        except Exception, e:
            # traceback.print_exc()
            msg = cmd + traceback.format_exc()
        rq.update({
            'output': output,
            'add_time': t,
        })


        # print app.logger.error()
        # # demo signature zip start
        # for i in range(3):
        #     os.makedirs(os.path.join(fileDir, 's%s' % i))
        #     fp = open(os.path.join(fileDir, '%s.txt' % i), 'w+')
        #     fp.write('sdfdgkdfjgk%s' % i)
        #     fp.close()
        # # demo signature zip end
        if isZip and os.path.exists(fileDir):
            while True:
                zipStatus = zip_dir('', fileDir, output)
                if zipStatus == 5:
                    break

        if os.path.exists(output):
            # data = my_file.read(output)
            return jsonify({'data': {
                'file_path': output, 'dir': output_dir, 'file_name': output_file,
                'cmd': cmd,
                'msg': msg
            }, 'message': 'success', 'status': 100001})
        return jsonify({'message': u'输出文件生成失败: %s' % msg, 'cmd': cmd})
    return jsonify({'data': items, 'message': 'success'})


def tumor_app_siRNA(app_name, r_path, sort_func, output_postfix='txt'):
    env_key = 'AY_USER_DATA_DIR'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    env = conf.get('env')
    r_dir = os.path.dirname(r_path)

    t = format_time(frm='%Y%m%d%H%M%S')
    items = []
    msg = ''

    # a + 5
    if request.method == 'POST':
        rq = request.json
        dirname = rq.get('taskid')
        # output_dir = os.path.join('/data/output', dir_name)
        output_dir = '/data/output/%s' % dirname
        output = ''
        cmd_dev, dirs = sort_func(rq, r_path, output, output_dir, t)
        # docker run -rm -v data_dir:/data -w /data bio_r
        cmd = 'docker run -d --rm --name %s -v /data:/data bc_biosoft ' % dirname
        if env and env.startswith('Development'):
            cmd = ''
        cmd += cmd_dev
        print cmd
        try:
            code = os.system(cmd)
            # print code, t
            if code:
                # 获取错误日志
                try:
                    # scheduler_order = "top -u ybtao"
                    # os.system(cmd)
                    return_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    # next_line = return_info.stdout.readline()
                    # msg = next_line.decode("utf-8", "ignore")
                    # while True:
                    #     next_line = return_info.stdout.readline()
                    #     return_line = next_line.decode("utf-8", "ignore")
                    #     if return_line == '' and return_info.poll() is not None:
                    #         break
                    #     if return_line:
                    #         msg = return_line
                    #         print 'ssdfdf', msg
                    #         # break
                    # returncode = return_info.wait()
                    # if returncode:
                    #     print 'read', return_info.stdout.read()
                    #     raise subprocess.CalledProcessError(returncode, return_info)
                    msg = return_info.communicate()[0].decode('utf-8', 'ignore')
                except Exception, e:
                    print 'Exception', e
                    msg = traceback.format_exc()
                    # msg = traceback.format_exc()
        except Exception, e:
            # traceback.print_exc()
            msg = cmd + traceback.format_exc()
        rq.update({
            'output': output,
            'add_time': t,
        })

        # print app.logger.error()

        if os.path.exists(output_dir):
            # data = my_file.read(output)
            return jsonify({'data': {'file_path': output, 'dir': output_dir, 'task_id': dirname}, 'message': 'success', 'status': 100001})
        return jsonify({'message': u'输出文件生成失败: %s' % msg, 'cmd': cmd})
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


@app.route("/jyweb/<action_name>/crud/", methods=["GET", "POST", "PUT", "DELETE"])
def upgrade_crud(action_name):
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    file_dir = conf.get('file_dir')
    if file_dir is None:
        return 'file_dir not in config.conf'
    dir_name = os.path.join(file_dir, action_name)
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name)
    method = request.headers.get('API-METHOD') or request.method
    t = format_time(frm='%Y%m%d%H%M%S')
    if method == 'POST':
        rq = request.json
        rq['add_time'] = t
        path_new = os.path.join(dir_name, '%s_%s.json' % (action_name, t))
        my_file.write(path_new, rq)
    if method.lower() == 'delete':
        rq = request.json
        add_time = rq.get('add_time')
        path_delete = os.path.join(dir_name, '%s_%s.json' % (action_name, add_time))
        if os.path.exists(path_delete):
            item_delete = my_file.read(path_delete)
            if item_delete.get('account') == rq.get('account'):
                os.remove(path_delete)
    if method.lower() == 'put':
        rq = request.json
        add_time = rq.get('add_time')
        path_put = os.path.join(dir_name, '%s_%s.json' % (action_name, add_time))
        if os.path.exists(path_put):
            item_put = my_file.read(path_put)
            item_put.update(rq)
            my_file.write(path_put, item_put)
    items = []
    for i in os.listdir(dir_name):
        path = os.path.join(dir_name, i)
        item = my_file.read(path)
        items.append(item)
    account = request.args.get('account') if method == 'GET' else request.json.get('account')
    items = filter(lambda x: x.get('account') == account, items)
    items.reverse()
    return jsonify(items)


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
    if account:
        items = filter(lambda x: x.get('account') == account, items)
    items.reverse()
    return jsonify(items)


@app.route('/tcm/file/', methods=['POST'])
def get_file():
    rq = request.json
    query_path = rq.get('query_path') or ''
    postfix = rq.get('postfix') or []
    root_path = rq.get('root_path') or ''
    root_dir = rq.get('root_dir') or ''
    env_key = rq.get('env_key') or 'AY_USER_DATA_DIR'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    # print conf
    # JINGD_DATA_ROOT = os.environ.get('JINGD_DATA_ROOT') or conf.get('jingd_data_root')
    JINGD_DATA_ROOT = os.environ.get(env_key) or conf.get('jingd_data_root') or ''
    if root_dir:
        JINGD_DATA_ROOT = root_dir
        if root_path and root_path.startswith(root_dir):
            root_path = root_dir[len(root_dir):]
    path = os.path.join(JINGD_DATA_ROOT, root_path, query_path)
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
    rq = request.json or {}
    dir_name = rq.get('dir') or ''
    file_name = rq.get('file_name') or ''
    to_json = True
    if 'to_json' in rq:
        to_json = rq.get('to_json')
    path = os.path.join(dir_name, file_name)
    if os.path.exists(path) is False:
        return 'Path not exists, %s' % path
    data = my_file.read(path, to_json=to_json)
    try:
        encoding = chardet.detect(data[0])['encoding']
        # print encoding
        data = data.decode(encoding, 'ignore').encode('utf-8')
    except:
        traceback.print_exc()

    return json.dumps({'message': 'success', 'data': data, 'file_path': path})


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
    # if file_path.endswith('.pdf'):
    #     with open(file_path, 'rb') as f:
    #         str64 = base64.b64decode(f.read())
    #         encoding = chardet.detect(str64[0])['encoding']
    #         print encoding
    #         str64 = str64.decode(encoding, 'ignore').encode('utf-8')
    #         print str64
    # else:
    #     str64 = pic_b64encode(file_path)
    str64 = pic_b64encode(file_path)
    data = {'img': str64, 'file_path': file_path}
    import json
    return json.dumps(data)


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


@app.route('/kobas3/annotate/visualization/', methods=['POST'])
def post_annotate_visualization():
    rq = request.json or {}
    dataSource = rq.get('dataSource') or []
    out_dir = rq.get('out_dir') or ''
    fileKey = rq.get('fileKey') or 'output_identify_clu'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    output_identify_clu = conf.get(fileKey)
    if output_identify_clu is None:
        return '%s not in config.conf' % fileKey
    path = os.path.join(out_dir, output_identify_clu)
    print path
    import csv
    with open(path, 'w') as f:
        tsv_test = csv.writer(f, delimiter='\t', lineterminator='\n')
        # tsv_test.writerow(dataSource)
        if len(dataSource) > 0:
            th = dataSource[0].keys()
            th = 'Term	Database	ID	Input number	Background number	P-Value	Corrected P-Value	Input	Hyperlink'.split('\t')
            if fileKey == 'output_identify_edge':
                th = 'pathway1	pathway2	cor	pathway1_ID	input1_number	background1_number	pvalue1	qvalue1	pathway2_ID	input2_number	background2_number	pvalue2	qvalue2'.split('\t')
            # tsv_test.writerow('\t'.join(th))
            tsv_test.writerow(th)
            for item in dataSource:
                # tsv_test.writerow('\t'.join(item.values()))
                tr = [item[k.replace(' ', '')] for k in th]
                tsv_test.writerow(tr)
    # my_file.write('sss.json', items3)
    return jsonify({'data': path, 'message': 'success'})


def update_static(project_dir, postfix1=''):
    import shutil
    dist_dir = os.path.join(project_dir, 'dist')
    for postfix in ['js', 'css']:

        src = os.path.join(dist_dir, 'umi.%s' % postfix)
        src_file_name = 'umi'
        file_name = src_file_name

        if postfix1:
            file_name = 'umi_%s' % (postfix1)
        des = os.path.join(static_dir, '%s.%s' % (file_name, postfix))
        if os.path.exists(src):
            print src, des
            shutil.copy(src, des)
    for i in os.listdir(os.path.join(dist_dir, 'static')):
        src = os.path.join(dist_dir, 'static', i)
        des = os.path.join(static_dir, i)
        if os.path.exists(src):
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
    update_static(os.path.join(project_dir, 'KOBASWeb'), 'kobars')
    update_static(os.path.join(project_dir, 'ncFANs'), 'ncFANs')
    # shutil.copytree(r'D:\pythonproject\KOBARSWeb\dist', r'D:\pythonproject\TCMWeb\templates\kobars')
    app.run(host=host_ip, port=port)
