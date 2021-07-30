# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2019/8/1 0001
__author__ = 'huohuo'
import json
import math
import os
import shutil
from string import Template

from jy_word.File import File
from jy_word.Word import Run, HyperLink, Paragraph, Set_page, Table, Tc, Tr
from jy_word.Word import write_cat, write_pkg_parts, get_img_info, get_imgs, bm_index0
from jy_word.web_tool import test_chinese, format_time, sex2str, float2percent, get_first_name

# from report_aiyi import

from config import read_conf
my_file = File()

r_panel = Run(family='微软雅黑')
hyperlink = HyperLink()
p = Paragraph()
set_page = Set_page().set_page
table = Table()
tr = Tr()
tc = Tc()

# 初号=42磅
# 小初=36磅
# 一号=26磅
# 小一=24磅
# 二号=22磅
# 小二=18磅
# 三号=16磅
# 小三=15磅
# 四号=14磅
# 小四=12磅
# 五号=10.5磅
# 小五=9磅
# 六号=7.5磅
# 小六=6.5磅
# 七号=5.5磅
# 八号=5磅


# ##################下载报告所需方法######################
dir_name = os.path.dirname(__file__)
page_margin = [2.4, 0.67, 0.49, 1.23, 2, 0]
gray = 'EEEEEE'
green = '#385623'
green_bg = '#A8D08D'
normal_size = 10.5  # 五号
none_text = 'NA'
w_sum = 9620
p_sect_normal = p.write(p.set(sect_pr=set_page(page_margin=[2.54, 1.9, 2.54, 1.9, 1.5, 1.75])))
sect_pr_catalog = set_page('A4', footer='rIdFooter1')


def get_dignosis():
    data = my_file.read('diagnosis.json')
    if data is None:
        return data
    return data.get('data')


def get_catalog():
    # {"title": cat[0], 'left': cat[1], 'page': cat[2], 'style': cat[3], 'bm': bm_index0 + index}
    #[title, left, page, style]
    catalogue = [
        [u"基本信息", 0, 1, 10],
        [u"报告摘要", 0, 1, 10],
        [u"靶向治疗药物使用建议", 2, 1, 23],
        [u"免疫治疗药物使用建议", 2, 1, 23],
        [u"新肿瘤免疫抗原预测", 2, 1, 23],
        [u"化疗药物使用建议", 2, 1, 23],
        [u"检测声明", 0, 1, 10],
        [u"结果解读", 0, 1, 10],
        [u"靶向用药基因检测结果", 2, 1, 23],
        [u"免疫用药基因检测结果", 2, 1, 23],
        [u"肿瘤新生抗原鉴定结果", 2, 1, 23],
        [u"化疗用药基因检测结果", 2, 1, 23],
        [u"附录", 0, 3, 10],
        [u"基因检测列表", 2, 4, 23],
        [u"癌症相关的基因背景介绍", 2, 5, 23],
        [u"报告说明", 0, 5, 10],
        [u"参考文献", 0, 5, 10],
        [u"产品声明", 0, 5, 10],
        # [u"附件", 2, 6, 23],
        # [u"IL-8 附件一", 2, 6, 23],
        # [u"CD8+PDL1 附件二", 2, 6, 23],
        # [u"IBMWatsonforGenomics 附件三", 2, 6, 23]
    ]
    items = []
    for index, cat in enumerate(catalogue):
        item = {"title": cat[0], 'left': cat[1], 'page': cat[2], 'style': cat[3], 'bm': bm_index0 + index}
        items.append(item)
    return items


def para_sect(**setting):
    return p.write(p.set(sect_pr=set_page(**setting)))


def para_setting(**settings):
    default_options = {
        'spacing': [0, 0],
        'ind': [0, 0],
        'jc': 'left',
        'line': 19.2,
        'rule': 'exact'
    }
    default_options.update(settings)
    return p.set(**default_options)


def write_title(title, jc='left'):
    return p.write(para_setting(jc=jc, line=12, rule='auto', spacing=[0, 1]), r_panel.text(title, 10.5, 1, color=green))


def header_panel(title, bm_name='', line=12, size='三号', spacing=[0, 0], jc='left'):
    return p.write(
        para_setting(jc=jc, line=line, rule='auto', spacing=spacing),
        r_panel.text(title, size, 1),
        bm_name
    )


def h1_panel(title, bm_name=''):
    return p.write(
        para_setting(jc='center', line=12*2.41, rule='auto', spacing=[0, 1], outline=1),
        r_panel.text(title, '二号', 1),
        bm_name
    )


def h2_panel(title, bm_name='', size='三号', jc='left', outline=2):
    return p.write(
        para_setting(jc=jc, line=12*1.73, rule='auto', spacing=[0, 1], outline=outline),
        r_panel.text(title, size, 1),
        bm_name
    )


def h4_panel(title, bm_name='', color=green, jc='left'):
    return p.write(
        para_setting(line=12, rule='auto', spacing=[1, 0], jc=jc),
        r_panel.text(title, '小四', 1, color=color),
        bm_name
    )


def write_cover_line(title, before=0, text=''):
    runs = r_panel.text('%s：' % title, 12, 0, color=green)
    runs += r_panel.text('%s' % text, 12, 1, color=green)
    return p.write(para_setting(spacing=[before, 0], ind=['firstLine', 11], line=18, rule='auto'), runs)


run_border = r_panel.text('□', 19)


def write_gray_tr(item):
    ws = item.get('ws')
    texts = item.get('text') or [''] * len(ws)
    fill = item.get('fill') or ''
    size = item.get('size') or 11
    weight = item.get('weight') if 'weight' in item else 1
    jc = item.get('jc') or 'center'
    line = item.get('line') or 12
    color = item.get('color') or 'auto'
    tcBorders = item.get('border') or []
    none = item.get('none')

    tcs = ''
    for i in range(len(texts)):
        run = r_panel.text(texts[i] or none, size, weight)
        para = p.write(para_setting(line=line, rule='auto', jc=jc), run)
        tcs += tc.write(para, tc.set(ws[i], tcBorders=tcBorders, fill=fill, gridSpan=ws[i]/1200, color=color))
    return tr.write(tcs)


def write_tr_panel(items):
    tcs = ''
    for item in items:
        tcs += write_tc_panel(item)
    return tr.write(tcs)


def write_tc_panel(item):
    w = item.get('w')
    fill = item.get('fill') or ''
    size = item.get('size') or 11
    weight = item.get('weight') if 'weight' in item else 1
    jc = item.get('jc') or 'center'
    color = item.get('color') or 'auto'
    text = item.get('text') or none_text
    line = item.get('line') or 10
    rule = item.get('rule') or 'auto'
    border = item.get('border') or ['top', 'bottom', 'left', 'right']
    img = item.get('img') or ''
    para = ''
    for t in str(text).split('\n'):
        run = r_panel.text(t, size, weight, color=color)
        run += img
        para += p.write(para_setting(line=line, rule=rule, jc=jc), run)
    return tc.write(
        para,
        tc.set(
            w, tcBorders=border,
            fill=fill, gridSpan=item.get('gridSpan') or 1,
            vMerge=item.get('vMerge') or '',
            color=item.get('bdColor') or ''
        )
    )


def write_cover(data):
    paras = ''
    # paras += p.write(r_panel.picture(19.72, 28.69, rId='cover', relativeFrom=['page', 'page'], wrap='undertext', posOffset=[0,1]))
    paras += p.write(p.set(spacing=[9, 0], jc='center'), r_panel.text('名医处方学习报告', '初号', 1, color=green))
    paras += write_cover_line('姓    名', text=data or '', before=18)
    paras += write_cover_line('报告日期', text=format_time())
    return paras


def write_introduce(data):
    paras = ''
    items = data.get('items') or data.get('test_detail')
    n = len(items)
    average_score = data.get('average_score') or data.get('score')
    taste_time = data.get('taste_time')

    tag = get_score_tag(average_score)
    paras += write_title('本次学习医案%s份，平均得分%s， 用时%s， 成绩%s。' % (n, average_score, taste_time, tag))
    p_set = para_setting(line=12, rule='auto')

    for i, item in enumerate(items):
        item = item or {}
        rq = item.get('rq') or item
        answer = item.get('answer') or {}
        score1 = item.get('score') or answer.get('score')
        tag1 = get_score_tag(score1)
        paras += write_title('医案%s (%s分， %s)' % (i+1, score1, tag1))
        paras += p.write(p_set, r_panel.text('四诊信息: %s' % item.get('diagnostic')))
        sss = [
            {'title': '证型', 'key': 'tcm_type'},
            {'title': '治法', 'key': 'treatment_method'},
            {'title': '方剂', 'key': 'recipe_name'},
        ]
        run = ''
        run1 = ''
        for s in sss:
            title = s.get('title')
            key = s.get('key')
            run += r_panel.text('%s: %s  ' % (title, rq.get(key)), space=True)
            run1 += r_panel.text('%s: %s  ' % (title, answer.get(key)), space=True, color='red')
        paras += p.write(p_set, run)
        paras += p.write(p_set, run1)
        paras += p.write(p_set, r_panel.text('名医处方信息：%s' % answer.get('recipe'), color='red'))
        paras += p.write(p_set, r_panel.text('您的处方信息：%s' % rq.get('recipe')))
    return paras


def write_body(data):
    para = ''
    for key in data['para_keys']:
        para += data[key]
    return '<w:body>%s</w:body>' % para


def sort_study_data(data):
    # img_info_path = data['img_info']
    # r_tcm.img_info_path = img_info_pagth
    pkgs = ''
    rels = ''
    chapters = ''
    account = data.get('account')
    return {
        'other_page': (pkgs, rels),
        'cover': write_cover(account) + p_sect_normal,
        'introduce': write_introduce(data),
        'para_keys': [
            'cover',
            'introduce',
        ]
    }


def down_common(data, sort_func):
    # my_file.write(file_name.split('.')[0] + '.json', data)
    report_time = format_time(frm='%Y%m%d%H%M%S')
    account = data.get('account')
    action_name = u'%s_学习报告' % account
    conf = read_conf()
    if isinstance(conf, dict):
        file_dir = conf.get('file_dir') or '/tmp'
    else:
        file_dir = '/tmp'
    report_dir = os.path.join(file_dir, 'report')
    if os.path.exists(report_dir) is False:
        os.makedirs(report_dir)
    data['report_time'] = format_time(frm="%Y-%m-%d")
    file_name = os.path.join(report_dir, u'%s_%s.doc' % (action_name, report_time))
    report_data = sort_func(data)
    body = write_body(report_data)

    pkg = write_pkg_parts([], body)
    status = False
    while status != 5:
        status = my_file.download(pkg, file_name)
    print file_name
    return file_name


def down_study(data):
    return down_common(data, sort_study_data)


def get_score_tag(score):
    if score >= 90:
        return '优秀'
    if score >= 80:
        return '良好'
    if score >= 60:
        return '及格'
    return '不及格'


if __name__ == "__main__":
    # generate_word(get_dignosis() or [])
    # down_common({}, sort_panel_data)
    down_study({})
    # print __file__
    pass
    

