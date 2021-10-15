#! /usr/bin/env python
# coding: utf-8
import chardet
import os
import sys
import subprocess
import traceback
import json

from flask import jsonify, request, render_template, send_from_directory, redirect
# from celery import Celery
from config import read_conf
from jy_word.web_tool import send_msg_by_dd, format_time, zip_dir
from jy_word.File import File
from jy_word.Word import pic_b64encode

from create_app import create_app, sort_request1
from create_auth_code import create_strs, my_file, auth_code_path
from views.generate_report import generate_word
from views.tcm.report_study import down_study
from views.tumor.report_panel import down_panel
from views.tumor.report_aiyi import filter_sv, float2percent
from views.tumor.apps.app import *

reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app()

# # 配置消息代理的路径，如果是在远程服务器上，则配置远程服务器中redis的URL
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# # 要存储 Celery 任务的状态或运行结果时就必须要配置
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# # 初始化Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# # 将Flask中的配置直接传递给Celery
# celery.conf.update(app.config)

restart_time = format_time(frm='%Y-%m%d-%H:%M:%S')
dir_name = os.path.dirname(__file__)
static_dir = os.path.join(dir_name, 'static')
project_dir = os.path.dirname(dir_name)


@app.route('/kobas3/')
@app.route('/kobas3')
@app.route('/kobas')
@app.route('/')
# @app.route('')
def hello_world():
    conf = read_conf()
    full_path = request.full_path
    system_name = conf.get('system_name')
    return render_template('index.html',
                           static_dir=static_dir.rstrip('/'),
                           restart_time=restart_time, system_name=system_name, conf=conf)


@app.errorhandler(404)
def page_not_found(e):
    conf = read_conf()
    system_name = conf.get('system_name')
    print request.path
    # print 'system_name', system_name
    return render_template('index.html', static_dir=static_dir.rstrip('/'), restart_time=restart_time, system_name=system_name, conf=conf)


@app.route("/kobas3/tcm/api/", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/kobas/tcm/api/", methods=["GET", "POST", "PUT", "DELETE"])
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
        # print request.json.get('file')
        if len(request.files) == 0:
            return jsonify({"success": False, "message": 'select file'})
        for k in request.files:
            f = request.files[k]
            name_array = f.filename.split('.')
            dir_path = os.path.join(file_dir, name_array[-1])
            if os.path.exists(dir_path) is False:
                os.makedirs(dir_path)
            # t = format_time(frm='%Y%m%d%H%M%S')
            file_name = f.filename
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
        file_name = rq.get('file_name') or ''

        file_name = '%s%s.txt' % (file_name, format_time(frm='%Y%m%d%H%M%S'))
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
        msg = traceback.format_exc()
        print msg
        send_msg_by_dd(msg)
        return '发生故障，已通知管理员，请稍后...%s' % msg


@app.route("/tcm/download/study/report/", methods=["POST"])
def tcm_download_study():
    rq = request.json
    try:
        file_path = down_study(rq or {})
        return jsonify({'file_path': file_path})
    except:
        message = '下载报告遇到问题，已通知管理员。%s' % traceback.format_exc()
        traceback.print_exc()
        send_msg_by_dd(message)
        return {'message': message}


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
    if env and env in ['KOBARS']:
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


@app.route('/tumor/app/<order>/1/', methods=['GET', 'POST'])
def tumor_app_order1(order):
    JY_SX_REF_DIR = os.environ.get('JY_SX_REF_DIR')
    app_items = {
        'merge': {
            'rPath': '/public/jingdu/budechao/lecture/lec1_merge/merge_demo.R',
            'sortFunc': sort_merge,
        },
        'tapply': {
            'rPath': '/public/jingdu/budechao/lecture/lec2_tapply/tapply_demo.R',
            'sortFunc': sort_tapply
        },
        'reorder': {
            'rPath': '/public/jingdu/budechao/lecture/lec3_reorder/reorder_col.R',
            'sortFunc': sort_reorder
        },
        'join': {
            'rPath': '/public/jingdu/budechao/lecture/lec4_join/join_demo.R',
            'sortFunc': sort_join
        },
        'pheatmap': {
            'rPath': '/public/jingdu/budechao/scripts/run_pheatmap_colTree.R',
            'sortFunc': sort_pheatmap
        },
        'table2matrix': {
            'rPath': '/public/jingdu/budechao/lecture/lec5_table2matrix/table2matrix.R',
            'sortFunc': sort_table2matrix
        },
        'herbScore': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/herb/run_herb_interaction.sh',
            'sortFunc': sort_herbScore
        },
        'herbVisualization': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/herb/run3_herbHeatmap.R',
            'sortFunc': sort_herbVisualization,
            'output_postfix': 'png'
        },
        'ternaryPlot': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/ternaryplot/run_ternaryPlot.R',
            'sortFunc': sort_test_app,
            'output_postfix': 'png'
        },
        'signature': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/signature/new/run_signature96_auto.sh',
            'sortFunc': sort_signature,
            'output_postfix': 'zip',
            'bio': 'bc_deconstructsigs'
        },
        'randomForest': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/randomForest/randomForest.R',
            'sortFunc': sort_randomForest,
            'output_postfix': 'zip',
        },
        'dcTree': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/dctree/dcTree.R',
            'sortFunc': sort_dcTree,
            'output_postfix': 'zip',
        },
        'cox': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/cox/cox.R',
            'sortFunc': sort_cox,
            'output_postfix': 'zip',
        },
        'fisherTest': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/fisher_chisqTest/fisherTest/fisherTest.R',
            'sortFunc': sort_test_app,
            'output_postfix': 'out'
        },
        'chisqTest': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/fisher_chisqTest/chisqTest/chisqTest.R',
            'sortFunc': sort_test_app,
            'output_postfix': 'out'
        },
        'ttest': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/wilcox_tTest/ttest/tTest.R',
            'sortFunc': sort_ttest,
        },
        'wilcoxonTest': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/wilcox_tTest/wilcoxTest/wilcoxonTest.R',
            'sortFunc': sort_ttest,
        },
        'anova': {
            'script_name': 'multGroups_diff.R',
            'sortFunc': sort_annova,
            'output_postfix': 'tsv'
        },
        'surv_group': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/survival/surv_group/surv_group.R',
            'sortFunc': sort_surv_group,
            'output_postfix': 'pdf'
        },
        'surv_cox': {
            'rPath': '/public/jingdu/zss/Rscript-zss/app/survival/surv_cox/surv_cox.R',
            'sortFunc': sort_surv_cox,
            'output_postfix': 'tsv'
        },
        'vcf2maf': {
            'script_name': 'run_vcf2maf.sh',
            'sortFunc': sort_vcf2maf,
            'output_postfix': 'maf',
            'bio': 'bc_vcf2maf',
            'order1': '-v %s:/db' % JY_SX_REF_DIR
        },
        'probe2gene': {
            'script_name': 'probe2gene/probe2gene.R',
            'sortFunc': sort_probe2gene,
            'output_postfix': 'zip',
        },
        'ssGSEA': {
            'script_name': 'ssGSEA/ssGSEA.R',
            'sortFunc': sort_annova,
            'output_postfix': 'tsv'
        },
        'naivebayes': {
            'script_name': 'naivebayes/run_naivebayes.R',
            'sortFunc': sort_naivebayes,
            'output_postfix': 'zip'
        },
        'TCGAanalyze_DEA': {
            'script_name': 'TCGAanalyze_DEA/TCGAanalyze_DEA.R',
            'sortFunc': sort_TCGAanalyze_DEA,
        },
        'CMS': {
            'script_name': 'cms/APP.CMS.R',
            'sortFunc': sort_CMS,
            'output_postfix': 'zip',
        },
        'dcTree2': {
            'script_name': 'dctree/APP.dctree.R',
            'sortFunc': sort_dcTree2,
            'output_postfix': 'tsv',
        },
        'pathway_DI': {
            'script_name': 'APP_pathway_DI/APP_pathway_DI.R',
            'sortFunc': sort_pathway_DI,
            'output_postfix': 'tsv',
        },
        'zscore_scale': {
            'script_name': 'zscore/zscore_scale.R',
            'sortFunc': sort_zscore_scale,
            'output_postfix': 'tsv',
        },
        'mcpcounter': {
            'script_name': 'mcpcounter/mcpCounter.R',
            'sortFunc': sort_mcpcounter,
            'output_postfix': 'tsv',
        },
        'pathway_mut': {
            'script_name': 'Pathway_Mut/APP.cal_pathway_mut.R',
            'sortFunc': sort_pathway_mut,
            'output_postfix': 'zip',
        },
        'igraph_layout_coor': {
            'script_name': 'igraph_layout/get_coor_igraph.R',
            'sortFunc': sort_igraph_layout_coor,
            'output_postfix': 'tsv',
        },
        'mut2matrix': {
            'script_name': 'mut2matrix/APP_mut2matrix.R',
            'sortFunc': sort_mut2matrix,
            'output_postfix': 'tsv',
        },
        'matrix2mut': {
            'script_name': 'matrix2mut/APP_matrix2mut.R',
            'sortFunc': sort_mut2matrix,
            'output_postfix': 'tsv',
        },
        'mut_pair': {
            'script_name': 'mut_pair/APP_mut_pair.R',
            'sortFunc': sort_mut_pair,
            'output_postfix': 'zip',
        },
        'pathway_di_samples': {
            'script_name': 'pathway_di_samples/APP_pathway_DI_samples.R',
            'sortFunc': sort_pathway_di_samples,
            'output_postfix': 'tsv',
        },
        'rank_gene_cluster': {
            'script_name': 'RankGeneCluster/RankGeneCluster.R',
            'sortFunc': sort_rank_gene_cluster,
            'output_postfix': 'zip',
        },
        'intersected_bed': {
            'script_name': 'intersectBed/intersectBed.sh',
            'sortFunc': sort_intersected_bed,
            'output_postfix': 'bed',
            'bio': 'docker.io/meisanggou/bc'
        },
    }
    if order in ['diffTest', 'fisherTest']:
        order = request.json.get('method')
    try:
        if order in app_items:
            app_item = app_items[order]
            conf = read_conf()
            if isinstance(conf, str):
                return conf
            scripts_dir = conf.get('scripts_dir')
            if scripts_dir:
                rPath = app_item.get('rPath')
                if rPath is not None:
                    rDir = os.path.dirname(rPath)
                    fileName = os.path.relpath(rPath, rDir)
                else:
                    fileName = app_item.get('script_name')
                app_item['rPath'] = os.path.join(scripts_dir, fileName)
            return tumor_app1(order, **app_item)
        return jsonify({'message': 'app%s尚未开发' % order})
    except:
        return jsonify({'message': 'app%s运行出错：%s' % (order, traceback.format_exc())})


@app.route('/tumor/app/<order>/2/', methods=['GET', 'POST'])
def tumor_app_order2(order):
    try:
        return tumor_app2()
    except:
        return jsonify({'message': 'app%s运行出错：%s' % (order, traceback.format_exc())})


@app.route('/tumor/siRNA/', methods=['GET', 'POST'])
def tumor_siRNA():
    rPath = '/data/siRNA/run_siRNA_auto.sh'
    def sort_siRNA(rq, r_path, output, result_dir, t):
        input_file1 = sort_app_file('input1', 'input_file1', '/data/userdata', t)
        dir1 = os.path.dirname(input_file1)
        cmd = 'sh %s %s %s %s /data/siRNA' % (
            r_path,
            rq.get('filter_freq'),
            input_file1,
            result_dir
        )
        return cmd, [dir1]
    return tumor_app_siRNA('siRNA', rPath, sort_siRNA, output_postfix='png')


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
    if request.method == 'PUT':
        items2 = rq.get('items')
        if isinstance(items2, list):
            for item2 in items2:
                f2 = filter(lambda x: x['code'] == item2.get('code'), items)
                f2[0].update(item2)
            my_file.write(auth_code_path, items)
        else:
            if len(f_items) == 0:
                return jsonify({'message': '邀请码不存在'})
            f_item = f_items[0]
            f_item.update(rq)
            my_file.write(auth_code_path, items)
            return jsonify(f_item)
    if request.method == 'GET':
        if len(f_items) == 0:
            return jsonify({'message': '邀请码不存在'})
        f_item = f_items[0]
        return jsonify(f_item)
    return jsonify(items)


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
    rq = request.args if method == 'GET' else request.json
    rq = rq or {}
    if method == 'POST':
        rq['add_time'] = t
        path_new = os.path.join(remark_dir, 'remark_%s.json' % t)
        my_file.write(path_new, rq)
    if method.lower() == 'delete':
        add_time = rq.get('add_time')
        path_delete = os.path.join(remark_dir, 'remark_%s.json' % add_time)
        if os.path.exists(path_delete):
            item_delete = my_file.read(path_delete)
            if item_delete.get('account') == rq.get('account'):
                os.remove(path_delete)
    if method.lower() == 'put':
        add_time = rq.get('add_time')
        path_put = os.path.join(remark_dir, 'remark_%s.json' % add_time)
        if os.path.exists(path_put):
            item_put = my_file.read(path_put)
            item_put.update(rq)
            my_file.write(path_put, item_put)
    items = []
    for i in os.listdir(remark_dir):
        path = os.path.join(remark_dir, i)
        try:
            item = my_file.read(path)
            items.append(item)
        except:
            send_msg_by_dd('remark\n%s\n%s' % (path, traceback.format_exc()))
    account = rq.get('account')
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
    data['data']['create_time'] = int(os.path.getctime(path) * 1000)
    data['data']['data_root'] = JINGD_DATA_ROOT
    data['data']['sep'] = os.path.sep
    return jsonify(data)


@app.route('/zip/dir/', methods=['POST'])
def zip_dir_rq():
    rq = request.json or {}
    dir_name = rq.get('dir') or ''
    parent_dir = os.path.dirname(dir_name)
    file_name = rq.get('file_name') or ''
    zip_name = os.path.relpath(dir_name, parent_dir) + '_'+ file_name
    file_list = rq.get('file_list')
    zip_path = os.path.join(parent_dir, zip_name)
    # zip_path = parent_dir + '/' + zip_name
    if os.path.exists(zip_path) is False:
        while True:
            zipStatus = zip_dir(parent_dir, dir_name, zip_name, file_list)
            if zipStatus == 5:
                break
    return json.dumps({'message': 'success',  'file_path': zip_path})


@app.route('/file/content/', methods=['POST'])
def get_file_content():
    rq = request.json or {}
    dir_name = rq.get('dir') or ''
    file_name = rq.get('file_name') or ''
    to_json = True
    if 'to_json' in rq:
        to_json = rq.get('to_json')
    to_string = False
    if 'to_string' in rq:
        to_string = rq.get('to_string')
    path = os.path.join(dir_name, file_name)
    if os.path.exists(path) is False:
        return json.dumps({'message': 'Path not exists, %s' % path})
    data = my_file.read(path, to_json=to_json, to_string=to_string)
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


@app.route('/avai/taxonomy/', methods=['GET'])
@app.route('/kobas/avai/taxonomy/', methods=['GET'])
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


@app.route('/annotate/visualization/', methods=['POST'])
@app.route('/kobas3/annotate/visualization/', methods=['POST'])
@app.route('/kobas/annotate/visualization/', methods=['POST'])
def post_annotate_visualization():
    rq = request.json or {}
    dataSource = rq.get('dataSource') or []
    out_dir = rq.get('out_dir') or ''
    fileKey = rq.get('fileKey') or 'output_identify_clu'
    kobas_app = rq.get('app')
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    output_identify_clu = conf.get(fileKey)
    if output_identify_clu is None:
        return '%s not in config.conf' % fileKey
    path = os.path.join(out_dir, output_identify_clu)
    try:
        import csv
        with open(path, 'w') as f:
            tsv_test = csv.writer(f, delimiter='\t', lineterminator='\n')
            # tsv_test.writerow(dataSource)
            if len(dataSource) > 0:
                th = 'Term	Database	ID	Input number	Background number	P-Value	Corrected P-Value	Input	Hyperlink'.split('\t')
                if kobas_app == 'exp_data':
                    if fileKey in ['output_identify_edge', 'output_edge_tmp']:
                        th = 'pathway1	pathway2	cor	pathway1_ID	pathway2_ID'.split('\t')
                    else:
                        th = 'GENE_SET	NAME	ENRICHMENT_RES	PROBABILITY	ENRICH_SCORE'.split('\t')
                elif fileKey == 'output_identify_edge' or fileKey == 'output_edge_tmp':
                    th = 'pathway1	pathway2	cor	pathway1_ID	input1_number	background1_number	pvalue1	qvalue1	pathway2_ID	input2_number	background2_number	pvalue2	qvalue2'.split('\t')
                # tsv_test.writerow('\t'.join(th))
                tsv_test.writerow(th)
                for item in dataSource:
                    # tsv_test.writerow('\t'.join(item.values()))
                    tr = [item[k.replace(' ', '')] for k in th]
                    tsv_test.writerow(tr)
        # my_file.write('sss.json', items3)
        return jsonify({'data': path, 'message': 'success'})
    except:
        msg = traceback.format_exc()
        send_msg_by_dd(msg)
        return jsonify({'message': msg})


def update_static(src_dir, postfix1=''):
    import shutil
    src_dist_dir = os.path.join(src_dir, 'dist')
    src_static_dir = os.path.join(src_dist_dir, 'static')
    for postfix in ['js', 'css']:
        src = os.path.join(src_dist_dir, 'umi.%s' % postfix)
        src_file_name = 'umi'
        file_name = src_file_name
        if postfix1:
            file_name = 'umi_%s' % (postfix1)
        des = os.path.join(static_dir, '%s.%s' % (file_name, postfix))
        if os.path.exists(src):
            print src, des
            shutil.copy(src, des)
    if os.path.exists(src_static_dir):
        for i in os.listdir(src_static_dir):
            src = os.path.join(src_static_dir, i)
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
    update_static(os.path.join(project_dir, 'ncfansgit'), 'ncFANs')
    update_static(os.path.join(project_dir, 'CRC'), 'CRC')
    update_static(os.path.join(project_dir, 'DeepTCM'), 'DeepTCM')
    # shutil.copytree(r'D:\pythonproject\KOBARSWeb\dist', r'D:\pythonproject\TCMWeb\templates\kobars')
    app.run(host=host_ip, port=port)

