#! /usr/bin/env python
# coding: utf-8
__author__ = 'huo'
import math
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import Image
from jy_word.web_tool import test_chinese
from jy_word.Word import bm_index0, get_imgs, uniq_list, get_img, get_img_info
from jy_word.File import File
from jy_word.Word import Paragraph, Run, Set_page, Table, Tc, Tr, HyperLink, Relationship, SDT
from jy_word.Word import write_cat, write_pkg_parts
from jy_word.web_tool import sex2str, format_time
from config import dir_name, static_dir

gray = 'E9E9E9'
gray_lighter = 'EEEEEE'
blue = '00ADEF'
bg_blue = 'EFFBFF'
dark_blue = '002060'
white = 'FFFFFF'
red = 'ED1C24'
red_lighter = 'FF8B8B'
orange = 'F14623'
colors = ['2C3792', '3871C1', '50ADE5', '37AB9C', '27963C', '40B93C', '80CC28']
borders = ['top', 'right', 'bottom', 'left']
title_cn, title_en = u'多组学临床检测报告', 'AIomics1'

# 初始化
aiyi_dir = os.path.join(static_dir, 'aiyi')
base_dir = os.path.join(aiyi_dir, 'base_data')
img_dir = os.path.join(aiyi_dir, 'images')
my_file = File()
base_file = File(base_dir)
img_info_path = os.path.join(img_dir, 'img_info.json')

r_aiyi = Run(img_info_path)
r_heiti = Run(family='黑体')
r_kaiti = Run(family='楷体')
hyperlink = HyperLink()
p = Paragraph()
set_page = Set_page().set_page
table = Table()
tr = Tr()
tc = Tc()
sdt = SDT()
page_margin = [3.5, 1.5, 2.54, 1.5, 1.5, 1.75]
page_margin4 = [4, 1.5, 2.54, 1.5, 1.5, 1.75]
p_set_tr = p.set(line=12*1.15)
sect_pr_cover = set_page('A4', header='rIdHeadertitle', footer='rIdCover')
w_sum = 10000+200

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
dark = '000000'


def get_report_core(data):
    sample_detail = data.get('sample_detail') or {}
    overview = data.get('overview') or {}
    other_pic = []
    img_info = get_imgs_weizhi(img_dir, is_refresh=True, others=other_pic)
    body = write_body(data)
    pages = write_pages(data.get('report_time'), sample_detail.get('sample_id'))
    pkgs1 = write_pkg_parts(img_info, body, other=pages)
    return pkgs1


def write_body(data):
    body = ''
    body += write_chapter0(data)
    return body


def write_table_title(title, gridSpan=0, sub_title=''):
    tcs = ''
    run = r_aiyi.text(title, '五号', weight=1)
    if sub_title:
        run += r_aiyi.text(sub_title, '小五', color=white)
    para = p.write(p.set(line=12, jc='left'), run)
    tcs += tc.write(para, tc.set(w_sum, tcBorders=['top', 'bottom'], gridSpan=gridSpan, fill=gray))
    return tr.write(tcs)


def write_chapter0(data):
    sample_detail = data.get('sample_detail')
    para = ''
    para += p.write(p.set(jc='center', spacing=[0, 0]), r_aiyi.text('地中海贫血基因检测报告单', '小四', weight=1))
    trs = ''
    w = 1200
    vStart = '<w:vMerge w:val="restart"/>'
    vMerge = '<w:vMerge/>'
    items = [
        {
            'title': '样品信息',
            'items': [
                [
                    {'text': '姓名:', 'w': w},
                    {'text': sample_detail.get('patient_name'), 'w': w},
                    {'text': '性别:', 'w': w},
                    {'text': sex2str(sample_detail.get('sex')), 'w': w},
                    {'text': '年龄:', 'w': w},
                    {'text': sample_detail.get('patient_name'), 'w': w},
                    {'text': '籍贯:', 'w': w},
                    {'text': sample_detail.get('native'), 'w': w},
                ],
                [
                    {'text': '送检机构:', 'w': w},
                    {'text': sample_detail.get('patient_name'), 'w': w * 2, 'gridSpan': 2},
                    {'text': '部门:', 'w': w},
                    {'text': sample_detail.get('inspection_department'), 'w': w},
                    {'text': '送检人:', 'gridSpan': 2},
                    {'text': sample_detail.get('patient_name'), 'w': w},
                ],
                [
                    {'text': '样本类型:', 'gridSpan': 2},
                    {'text': sample_detail.get('sample_type'), 'w': w * 2, 'gridSpan': 2},
                    {'text': '接收时间:', 'gridSpan': 2},
                    {'text': sample_detail.get('date_created'), 'w': w * 2, 'gridSpan': 2},
                ]
            ]
        },
        {
            'title': '检测项目',
            'items': [
                [
                    {'text': '项目名称', 'w': w},
                    {'text': sample_detail.get('patient_name'), 'gridSpan': 7},

                ],
                [
                    {'text': '检测方法:', 'w': w},
                    {'text': 'PCR-sequencing', 'gridSpan': 7},
                ]
            ]
        },
        {
            'title': '基因型',
            'items': [
                [
                    {'text': 'α地贫：                             β地贫：', 'gridSpan': 8},
                ],
                [
                    {'text': '本检测结果仅对检测标本负责，供临床参考。检测结果的解释及疾病诊断，请咨询相关医院专科医师。', 'gridSpan': 8},
                ]
            ]
        },
        {
            'title': '',
            'items': [
                [
                    {'text': '检测结论：', 'gridSpan': 8, 'weight': 1},
                ]
            ]
        },
        {
            'title': '检测内容',
            'items': [
                [
                    {'text': '常见α+β地贫基因检测（23种）', 'vMerge': vStart},
                    {'text': '3种缺失型α地贫', 'gridSpan': 3},
                    {'text': '--SEA; -α3.7; -α4.2', 'gridSpan': 4},
                ],
                [
                    {'text': '', 'vMerge': vMerge},
                    {'text': '3种点突变型α地贫', 'gridSpan': 3},
                    {'text': 'Hb WS；Hb QS；Hb CS', 'gridSpan': 4},
                ],
                [
                    {'text': '', 'vMerge': vMerge},
                    {'text': '17种点突变型β地贫', 'gridSpan': 3},
                    {'text': '-32(C>A)；-30(T>C)；-29(A>G)；-28(A>G)；CAP+1(A>C)；CAP+43_+40(-AAAC)；起始密码子(ATG>AGG)；CD14/15(+G)；CD17(A>T)；CD26(G>A)；CD27/28(+C)；IVS-I-1(G>T)；IVS-I-5(G>C)；CD31(-C)；CD41/42(-TTCT)；CD43(G>T)；CD71/72(+A)；IVS-II-654(C>T)', 'gridSpan': 4},
                ],
                [
                    {'text': '临床α+β地贫基因检测（47种）', 'vMerge': vStart},
                    {'text': '常见23种α+β地贫基因突变，加上如下国际常见突变：', 'gridSpan': 7},
                ],
                [
                    {'text': '', 'vMerge': vMerge},
                    {'text': '5种缺失型α地贫', 'gridSpan': 3},
                    {'text': '--FIL；--Thai；-α2.4；-α27.6；--34.6', 'gridSpan': 4},
                ],
                [
                    {'text': '', 'vMerge': vMerge},
                    {'text': '1种点突变型α地贫', 'gridSpan': 3},
                    {'text': 'Poly(A) AATAAA>AATGAA', 'gridSpan': 4},
                ],
                [
                    {'text': '', 'vMerge': vMerge},
                    {'text': '15种点突变型β地贫', 'gridSpan': 3},
                    {'text': '-91(A>G)；-38(G>A)；CAP+1(A>C)；CD5(-CT)；CD8/9 (+G)；CD10(C>A)；CD15(G>A)；CD16(-C)；CD22(A>G)；CD30(A>G)；CD30(-A)；CD30(G>C)；CD39(G>T)；IVS-II-5(G>C)；CD130(T>G)；', 'gridSpan': 4},
                ],
                [
                    {'text': '', 'vMerge': vMerge},
                    {'text': '3种缺失型β地贫', 'gridSpan': 3},
                    {'text': '缺失型Gγ(Aγδβ)0；SEA-HPFH；Del 619', 'gridSpan': 4},
                ],
                [
                    {'text': '全套α+β地贫基因检测', 'vMerge': vStart},
                    {'text': '临床47种α+β地贫基因突变，加上罕少见突变：', 'gridSpan': 7},
                ],
                [
                    {'text': '', 'vMerge': vMerge},
                    {'text': '罕少见突变', 'gridSpan': 3},
                    {'text': 'CD15/16(+G)；CD19(A>G)；IVS-I-2 (T>C)；IVS-I-128 (T>G)；CD37 (G>A)；CD38(-A)；CD40/41 (+T)；CD53(-T)；CD71/72 (+T)等', 'gridSpan': 4},
                ],
                [
                    {'text': '检测者', 'vMerge': '', 'gridSpan': 1},
                    {'text': '', 'vMerge': '', 'gridSpan': 1},
                    {'text': '审核者', 'vMerge': '', 'gridSpan': 1},
                    {'text': '', 'vMerge': '', 'gridSpan': 2},
                    {'text': '报告时间', 'vMerge': '', 'gridSpan': 1},
                    {'text': '', 'vMerge': '', 'gridSpan': 2},
                ],
            ]
        },
    ]
    for item in items:
        title = item.get('title')
        if title:
            trs += write_table_title(title, 8)
        items2 = item.get('items')
        for item2 in items2:
            for item23 in item2:
                item23['w'] = (item23.get('gridSpan') or 1) * w
            trs += write_tr_weizhi(item2)
    para += table_weizhi(trs)
    para += sect_pr_cover
    return para


def write_tr_weizhi(items, cantSplit=''):
    if len(items) == 0:
        return ''
    tcs = ''
    for item in items:
        tcs += write_tc_weizhi(item)
    return tr.write(tcs, tr.set(cantSplit=cantSplit))


def write_tc_weizhi(item):
    text = item.get('text') or ''
    jc = item.get('jc') or 'left'
    pPr = item.get('pPr') or p.set(jc=jc, spacing=[0.2, 0.2])
    size = item.get('size') or '小五'
    weight = item.get('weight') or 0
    wingdings = item.get('wingdings') or False
    para = ''
    tcFill = item.get('tcFill') or ''
    tcColor = item.get('tcColor') or dark
    level = item.get('level')
    w = item.get('w') or w_sum

    tcBorders = item.get('tcBorders') or ['top', 'bottom', 'left', 'right']
    gridSpan = item.get('gridSpan') or 0
    lineSize = item.get('lineSize') or 8
    for t in text.split('\n'):
        run = r_aiyi.text(' ' + t, size=size, weight=weight, wingdings=wingdings, space=True)
        para += p.write(pPr, run)
    return tc.write(para, tc.set(w=w,
                                 fill=tcFill, tcBorders=tcBorders,
                                 gridSpan=gridSpan, vMerge=item.get('vMerge') or '',
                                 color=tcColor, lineSize=lineSize))


def write_pages(t, sample_id):
    relationship = Relationship()
    pkg_parts, relationshipss = '', ''
    # 页脚-cover
    page_type = 'footer'
    footer_id_cover = 'cover'
    size = 9
    paras_cover = ''
    # paras += p.write(p.set(jc='right'), sdt.write())
    paras_cover += p.write(p.set(jc='left'), r_aiyi.text('地址：广西南宁市双拥路6号广西医科大学第一附属医院', size))
    relationshipss += relationship.write_rel(footer_id_cover, page_type)
    pkg_parts += relationship.about_page(footer_id_cover, paras_cover, page_type=page_type)
    # 页头
    page_type = 'header'
    footer_id = 'headertitle'
    paras = ''
    paras += p.write(p.set(jc='center', line=18),
                     r_aiyi.text('广西医科大学第一附属医院地中海贫血防治重点实验室', '小四', weight=1))
    relationshipss += relationship.write_rel(footer_id, page_type)
    pkg_parts += relationship.about_page(footer_id, paras, page_type=page_type)
    # return footer, relationships
    return pkg_parts, relationshipss


def table_weizhi(trs2):
    return table.write(trs2) + p.write(p.set(line=1, rule='exact'))


def float2percent(p, n=2):
    try:
        p = float(p)
    except:
        print p
        return p
    return '%s%%' % (round(p*100, n))


def get_imgs_weizhi(path, is_refresh=False, others=[]):
    return []