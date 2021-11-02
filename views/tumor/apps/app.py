#! /usr/bin/env python
# coding: utf-8
import os
import sys
import subprocess
import traceback

from flask import jsonify, request
from config import read_conf
from jy_word.web_tool import send_msg_by_dd, format_time, zip_dir

from create_auth_code import my_file

reload(sys)
sys.setdefaultencoding('utf-8')


def sort_merge(rq, rPath, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    input_key1 = rq.get('input_key1')
    input_key2 = rq.get('input_key2')
    way = rq.get('way')
    cmd = 'Rscript %s %s %s %s %s %s %s' % (
        rPath,
        input_file1, input_key1,
        input_file2, input_key2,
        output, way
    )
    return cmd, [os.path.dirname(input_file1), os.path.dirname(input_file2)]


def sort_tapply(rq, rPath, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_key1 = rq.get('input_key1')
    cmd = 'Rscript %s %s %s %s %s %s %s' % (
        rPath,
        input_file1, input_key1,
        rq.get('start'), rq.get('end'),
        output, rq.get('method')
    )
    return cmd, [os.path.dirname(input_file1)]


def sort_reorder(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    order_file = sort_app_file('order', 'order_file', result_dir, t)
    cmd = 'Rscript %s %s %s %s' % (
        r_path,
        input_file1,
        order_file,
        output
    )
    return cmd, [os.path.dirname(input_file1), os.path.dirname(order_file)]


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


def sort_table2matrix(rq, r_path, output, result_dir, t):
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


def sort_herbScore(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    r_path_dir = os.path.dirname(r_path)
    dir1 = os.path.dirname(input_file1)
    cmd = 'sh %s %s %s %s %s %s' % (
        r_path,
        result_dir,
        r_path_dir,
        input_file1,
        output,
        rq.get('top_value')
    )
    return cmd, [dir1, result_dir, r_path_dir]


def sort_vcf2maf(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    cmd = '/bin/bash %s %s %s %s %s' % (
        r_path,
        input_file1,
        rq.get('tumor_id'),
        rq.get('normal_id'),
        output,
    )
    return cmd, [dir1]


def sort_herbVisualization(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    cmd = 'Rscript %s %s %s' % (
        r_path,
        input_file1,
        output,
    )
    return cmd, [dir1]


def sort_signature(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    BSg_type = rq.get('BSg_type')
    rPathDir = os.path.dirname(r_path)
    # sample_ids = rq.get('sample_ids')
    cmd = 'sh %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        'freq96.tsv',
        BSg_type,
        output[:-4],
        rPathDir
    )
    return cmd, [dir1]


def sort_test_app(rq, rPath, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    cmd = 'Rscript %s %s %s' % (
        rPath,
        input_file1,
        output
    )
    return cmd, [dir1]


def sort_TCGAanalyze_DEA(rq, rPath, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    cmd = 'Rscript %s %s %s %s %s %s %s' % (
        rPath,
        input_file1,
        input_file2,
        rq.get('group1_name'),
        rq.get('group2_name'),
        output,
        rq.get('type'),
    )
    return cmd, [dir1, dir2]


def sort_randomForest(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    output_dir = output[:-4]
    # sample_ids = rq.get('sample_ids')
    # train_pd.txt test_pd.txt weights.txt output.pdf
    # print result_dir
    cmd = 'Rscript %s %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        os.path.join(output_dir, 'train_pd.txt'),
        os.path.join(output_dir, 'test_pd.txt'),
        os.path.join(output_dir, 'weights.txt'),
        os.path.join(output_dir, 'output.pdf'),
    )
    return cmd, [dir1, dir2]


def sort_dcTree(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    output_dir = output[:-4]
    cmd = 'Rscript %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        os.path.join(output_dir, 'train.pd.prune.txt'),
        os.path.join(output_dir, 'train.pd.nopr.txt'),
        os.path.join(output_dir, 'test.pd.prune.txt'),
        os.path.join(output_dir, 'test.pd.nopr.txt'),
        os.path.join(output_dir, 'tree_nopr.png'),
        os.path.join(output_dir, 'tree_prune2.png'),
        os.path.join(output_dir, 'roc_nopr.png'),
        os.path.join(output_dir, 'roc_prune.png'),
        os.path.join(output_dir, 'test_roc_nopr.png'),
        os.path.join(output_dir, 'test_roc_prune.png'),
        os.path.join(output_dir, 'out_cp.txt'),
        (rq.get('cp_value') or '0.015'),
    )
    return cmd, [dir1, dir2]


def sort_CMS(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    output_dir = output[:-4]
    cmd = 'Rscript %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        os.path.join(output_dir, 'alterations.clustering.pdf'),
        os.path.join(output_dir, 'alterations.pheatmap.pdf'),
        os.path.join(output_dir, 'samples.clustering.tsv'),
    )
    return cmd, [dir1, dir2]


def sort_dcTree2(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    r_dir = os.path.dirname(r_path)
    cmd = 'Rscript %s %s %s %s' % (
        r_path,
        input_file1,
        output,
        r_dir
    )
    return cmd, [dir1, r_dir]


def sort_pathway_DI(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    r_dir = os.path.dirname(r_path)
    cmd = 'Rscript %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        output,
    )
    return cmd, [dir1, dir2]


def sort_zscore_scale(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    cmd = 'Rscript %s %s %s' % (
        r_path,
        input_file1,
        output,
    )
    return cmd, [dir1]


def sort_mcpcounter(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    cmd = 'Rscript %s %s %s %s %s' % (
        r_path,
        input_file1,
        output,
        rq.get('data_type'),
        rq.get('gene_type'),
    )
    return cmd, [dir1]


def sort_pathway_mut(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    output_dir = output[:-4]
    cmd = 'Rscript %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        os.path.join(output_dir, 'pathway.out.matrix.tsv'),
        os.path.join(output_dir, 'pathway.out.table.tsv'),
        os.path.join(output_dir, 'pathway.out.pair.tsv'),
    )
    return cmd, [dir1, dir2]


def sort_mut_pair(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    output_dir = output[:-4]
    cmd = 'Rscript %s %s %s %s' % (
        r_path,
        input_file1,
        os.path.join(output_dir, 'out_mut_table.tsv'),
        os.path.join(output_dir, 'out_mut_matrix.tsv'),
    )
    return cmd, [dir1]


def sort_rank_gene_cluster(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    input_file3 = sort_app_file('input3', 'input_file3', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    dir3 = os.path.dirname(input_file3)
    output_dir = output[:-4]  #zip
    cmd = 'Rscript %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        input_file3,
        output_dir + '/',
        rq.get('pre_name')
    )
    return cmd, [dir1, dir2, dir3]


def sort_pathway_di_samples(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    input_file3 = sort_app_file('input3', 'input_file3', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    dir3 = os.path.dirname(input_file3)
    cmd = 'Rscript %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        input_file3,
        output
    )
    return cmd, [dir1, dir2, dir3]


def sort_igraph_layout_coor(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    cmd = 'Rscript %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        rq.get('method'),
        output
    )
    return cmd, [dir1, dir2]


def sort_mut2matrix(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    cmd = 'Rscript %s %s %s' % (
        r_path,
        input_file1,
        output
    )
    return cmd, [dir1]


def sort_cox(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    output_dir = output[:-4]
    cmd = 'Rscript %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        os.path.join(output_dir, 'cox.test.gene.tsv'),
        os.path.join(output_dir, 'merge.gene.tsv'),
    )
    return cmd, [dir1, os.path.dirname(input_file2)]


def sort_ttest(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    cmd = 'Rscript %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        rq.get('groupA_name'),
        rq.get('groupB_name'),
        output
    )
    return cmd, [dir1, dir2]


def sort_annova(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    cmd = 'Rscript %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        output
    )
    return cmd, [dir1, dir2]


def sort_surv_group(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    variable = rq.get('variable')
    cmd = 'Rscript %s %s %s %s' % (
        r_path,
        input_file1,
        output,
        variable
    )
    return cmd, [dir1]


def sort_surv_cox(rq, r_path, output, result_dir, t):
    exp_file = sort_app_file('input1', 'input_file1', result_dir, t)
    surv_file = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(exp_file)
    dir2 = os.path.dirname(surv_file)
    cmd = 'Rscript %s %s %s %s %s %s' % (
        r_path,
        exp_file,
        surv_file,
        output,
        rq.get('time'),
        rq.get('status'),
    )
    return cmd, [dir1, dir2]


def sort_probe2gene(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    output_dir = output[:-4]
    cmd = 'Rscript %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        os.path.join(output_dir, 'out_symbol.tsv'),
        os.path.join(output_dir, 'out_entrez.tsv')
    )
    return cmd, [dir1, dir2]


def sort_naivebayes(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    output_dir = output[:-4]
    cmd = 'Rscript %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        os.path.join(output_dir, 'out_train.tsv'),
        os.path.join(output_dir, 'out_test.tsv'),
        rq.get('laplace')
    )
    return cmd, [dir1, dir2]


def sort_intersected_bed(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    cmd = '/bin/bash %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        output
    )
    return cmd, [dir1, dir2]


def sort_cnv_seg2gene(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    input_file2 = sort_app_file('input2', 'input_file2', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    dir2 = os.path.dirname(input_file2)
    cmd = 'Rscript %s %s %s %s %s %s' % (
        r_path,
        input_file1,
        input_file2,
        output,
        rq.get('amp_fold'),
        rq.get('del_fold'),
    )
    return cmd, [dir1, dir2]


def sort_colon_cancer(rq, r_path, output, result_dir, t):
    input_file1 = sort_app_file('input1', 'input_file1', result_dir, t)
    dir1 = os.path.dirname(input_file1)
    cmd = '/bin/bash %s %s %s' % (
        r_path,
        input_file1,
        output,
    )
    return cmd, [dir1]


def sort_app_file(key, file_key, result_dir, t):
    rq = request.json
    input_file1 = rq.get(file_key)
    if input_file1 is None:
        input_file1 = os.path.join(result_dir, '%s_%s.txt' % (file_key, t))
        my_file.write(input_file1, rq.get(key))
    return input_file1


def tumor_app1(app_name, rPath='', sortFunc=None, output_postfix='txt', order1='--rm', bio='bio_r', **kwargs):
    env_key = 'AY_USER_DATA_DIR'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    env = conf.get('env')
    JINGD_DATA_ROOT = os.environ.get(env_key) or conf.get('jingd_data_root')
    r_dir = os.path.dirname(rPath)
    output_dir = os.path.join(JINGD_DATA_ROOT, 'app', 'output', app_name)
    if os.path.exists(output_dir) is False:
        os.makedirs(output_dir)
        # return jsonify({'message': 'Path not exists, %s' % path})
    t = format_time(frm='%Y%m%d%H%M%S')
    items = []
    msg = ''
    # a + 5
    if request.method == 'POST':
        rq = request.json
        taskid = rq.get('taskid')
        if taskid:
            output_dir = os.path.join(output_dir, taskid)
        if os.path.exists(output_dir) is False:
            os.makedirs(output_dir)
        output_file = '%s.output.%s.%s' % (app_name, t, output_postfix)
        output = output_dir.rstrip('/') + '/' + output_file
        cmd_dev, dirs = sortFunc(rq, rPath, output, output_dir, t)
        dirs += [output_dir, r_dir]
        # docker run -rm -v data_dir:/data -w /data bio_r
        cmd = 'docker run %s' % order1
        for i in list(set(dirs)):
            cmd += ' -v %s:%s' % (i, i)
        cmd += ' %s ' % bio
        if env and env.startswith('Development'):
            cmd = ''
        cmd += cmd_dev
        return jsonify({'data': {
            'app_name': app_name,
            'postfix': output_postfix,
            'file_path': output,
            'dir': output_dir, 'file_name': output_file,
            'cmd': cmd,
            'msg': msg
        }, 'message': 'success', 'status': 100001})
    return jsonify({'data': items, 'message': 'success'})


def tumor_app2():
    msg = ''
    rq = request.json
    output = rq.get('file_path')
    cmd = rq.get('cmd')
    output_dir = rq.get('dir')
    file_name = rq.get('file_name')

    zip_file_dir = output[:-4]
    output_postfix = rq.get('postfix')
    isZip = output_postfix == 'zip'
    if isZip:
        if os.path.exists(zip_file_dir) is False:
            os.makedirs(zip_file_dir)
        # print fileDir
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
                    os.removedirs(zip_file_dir)
                # msg = traceback.format_exc()
    except Exception, e:
        # traceback.print_exc()
        msg = cmd + traceback.format_exc()



    # print app.logger.error()
    # # demo signature zip start
    # for i in range(3):
    #     os.makedirs(os.path.join(fileDir, 's%s' % i))
    #     fp = open(os.path.join(fileDir, '%s.txt' % i), 'w+')
    #     fp.write('sdfdgkdfjgk%s' % i)
    #     fp.close()
    # # demo signature zip end
    if isZip and os.path.exists(zip_file_dir):
        while True:
            zipStatus = zip_dir('', zip_file_dir, output)
            if zipStatus == 5:
                break

    if os.path.exists(output):
        # data = my_file.read(output)
        return jsonify({'data': {
            'file_path': output, 'dir': output_dir, 'file_name': file_name,
            'cmd': cmd,
            'msg': msg
        }, 'message': 'success', 'status': 100001})
    return jsonify({'message': u'输出文件生成失败: %s' % msg, 'cmd': cmd})


def tumor_app(app_name, rPath='', sortFunc=None, output_postfix='txt', order1='--rm', bio='bio_r', **kwargs):
    env_key = 'AY_USER_DATA_DIR'
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    env = conf.get('env')
    JINGD_DATA_ROOT = os.environ.get(env_key) or conf.get('jingd_data_root')
    r_dir = os.path.dirname(rPath)
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
        taskid = rq.get('taskid')
        if taskid:
            output_dir = os.path.join(output_dir, taskid)
        if os.path.exists(output_dir) is False:
            os.makedirs(output_dir)
        output_file = '%s.output.%s.%s' % (app_name, t, output_postfix)
        output = output_dir.rstrip('/') + '/' + output_file
        cmd_dev, dirs = sortFunc(rq, rPath, output, output_dir, t)
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
            # print fileDir
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


if __name__ == '__main__':
    print 'tumor app'
