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
sect_pr_catalog = set_page('A4', footer='rIdFooter1', header='rIdHeader1')


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


def write_header_jingan(page):
    page_type='header'
    if page is None:
        paras = ''
        rels = ''
        rId = '%s_null' % page_type
    else:
        index = page.get('index')
        rId = '%s%s' % (page_type, index)
        text = 'PART %02d %s %s' % (index + 1, page.get('cn'), page.get('en'))
        paras = p.write(p.set(pStyle='a3', pBdr=p.set_pBdr()), r_panel.text(text))
        paras += p.write(p.set(pStyle='a3', pBdr=p.set_pBdr()), r_panel.picture(17.3, 0.66, 'line', text_wrapping='inline'))
        rels = relationship.write_rel('line', target_name='media/line.png')
    return {
        'rId': 'rId%s' % rId.capitalize(),
        'pkg': relationship.about_page(rId, paras, page_type=page_type, rels=rels),
        'rel': relationship.write_rel(rId, page_type)
    }


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
    return p.write(para_setting(spacing=[before, 0], ind=['firstLine', 24], line=18, rule='auto'), runs)


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
    tcs = ''
    for i in range(len(texts)):
        run = r_panel.text(texts[i], size, weight)
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


def write_genes(title, genes):
    paras = ''
    trs = ''
    ww = 9800
    for gene in genes.split('\n'):
        text = gene.split('\t')
        trs += write_gray_tr({
            'text': text,
            'ws': [ww/len(text)] * len(text),
            'border': ['top', 'bottom', 'left', 'right'],
            'size': '小五',
            'weight': 0,
            'color': green,
            'line': 16
        })
    paras += h4_panel(title)
    paras += table.write(trs, insideColor=green, bdColor=green)
    return paras


def write_abstract_drug(data, kind):
    items = [
        [
            {'text': '基因', 'vMerge': '<w:vMerge w:val="restart"/>', 'w': 1200, 'key': 'gene'},
            {'text': '变异', 'vMerge': '<w:vMerge w:val="restart"/>', 'w': 1300, 'key': 'amino_acid_change'},
            {'text': 'FDA/CFDA批准用于本癌种', 'vMerge': '', 'w': 3620, 'key': 'A', 'gridSpan': 2},
            {'text': 'FDA/CFDA批准用于其他癌种', 'vMerge': '<w:vMerge w:val="restart"/>', 'w': 1900, 'key': 'B'},
            {'text': '临床试验药物', 'vMerge': '<w:vMerge w:val="restart"/>', 'w': 1700, 'key': 'amino_acid_change'},
        ],
        [
            {'text': ' ', 'vMerge': '<w:vMerge/>', 'w': 1200, 'key': 'gene'},
            {'text': ' ', 'vMerge': '<w:vMerge/>', 'w': 1300, 'key': 'amino_acid_change'},
            {'text': '靶点获批药物', 'vMerge': '', 'w': 1810, 'key': 'A'},
            {'text': '潜在靶点药物', 'vMerge': '', 'w': 1810, 'key': 'B'},
            {'text': '', 'vMerge': '<w:vMerge/>', 'w': 1900, 'key': 'C'},
            {'text': '', 'vMerge': '<w:vMerge/>', 'w': 1700, 'key': 'D'},
        ]
    ]
    trs = ''
    for tr_item in items:
        tcs = ''
        for tc_item in tr_item:
            tc_item['fill'] = green_bg
            tcs += write_tc_panel(tc_item)
        trs += tr.write(tcs)
    if len(data) == 0:
        data = [{}]
    for d_item in data:
        tcs = ''
        arr = d_item.get(kind) or []
        for tc_item1 in items[1]:
            key = tc_item1['key']
            if key in ['A', 'B', 'C', 'D']:
                arr1 = []
                for x in arr:
                    if x.get('aiyi_level') == key:
                        arr1.append(x.get('drugs'))
                d_item[key] = '\n'.join(arr1)
            tcs += write_tc_panel({
                'text': d_item.get(key) or '/',
                'w': tc_item1.get('w'),
                'weight': 1 if key == 'gene' else 0
            })
        trs += tr.write(tcs)
    return table.write(trs)


def write_result_drug(data1, data2):
    items = [
        {'text': '药物敏感性', 'w': 1500, 'key': 'gene'},
        {'text': '药物名称', 'w': 1300, 'key': 'drug_name'},
        {'text': '用药解析', 'w': 6800, 'key': 'drug_description'},
    ]
    trs = ''
    tcs = ''
    for tc_item in items:
        tc_item['fill'] = green_bg
        tcs += write_tc_panel(tc_item)
    trs += tr.write(tcs)
    datas = [{'title': '潜在获益药物', 'data': data1}, {'title': '潜在耐药药物', 'data': data2}]
    for data11 in datas:
        data = data11.get('data')
        mingan = data11.get('title')
        if len(data) == 0:
            data = [{}]
        for d_index, d_item in enumerate(data):
            tcs = ''
            for tc_index, tc_item1 in enumerate(items):
                key = tc_item1['key']
                vMerge = ''
                text = d_item.get(key) or '/'
                if tc_index == 0 and len(data) > 1:
                    if d_index == 0:
                        vMerge = '<w:vMerge w:val="restart"/>'
                        text = mingan
                    else:
                        vMerge = '<w:vMerge/>'
                        text = ''
                tcs += write_tc_panel({
                    'text': text,
                    'w': tc_item1.get('w'),
                    'weight': 0,
                    'vMerge': vMerge,
                    'bdColor': green
                })
            trs += tr.write(tcs)
    return table.write(trs, tblBorders=[])


def write_result_drug_description(title, data, items):
    trs = ''
    tcs = ''
    for tc_item in items:
        tc_item['fill'] = green_bg
        tcs += write_tc_panel(tc_item)
    trs += tr.write(tcs)
    # datas = [{'title': '潜在获益药物', 'data': data1}, {'title': '潜在耐药药物', 'data': data2}]
    # for data11 in datas:
    #     data = data11.get('data')
    if len(data) == 0:
        data = [{}]
    for d_index, d_item in enumerate(data):
        tcs = ''
        for tc_index, tc_item1 in enumerate(items):
            key = tc_item1['key']
            text = d_item.get(key) or '/'
            tcs += write_tc_panel({
                'text': text,
                'w': tc_item1.get('w'),
                'weight': 0,
                'vMerge': '',
                'bdColor': green
            })
        trs += tr.write(tcs)
    return h4_panel(title) + table.write(trs, tblBorders=[])


def write_abstract_gene(data):
    genes = [
        {'gene': 'EGFR', 'var_type': 'SNV/InDel/CNV'},
        {'gene': 'ALK', 'var_type': 'SNV/InDel/Fusion'},
        {'gene': 'ROSI', 'var_type': 'SNV/InDel/Fusion'},
        {'gene': 'BRAF', 'var_type': 'SNV/InDel'},
        {'gene': 'KRAS', 'var_type': 'SNV/InDel'},
        {'gene': 'ERBB2', 'var_type': 'SNV/InDel/CNV'},
        {'gene': 'RET', 'var_type': 'SNV/InDel/Fusion'},
        {'gene': 'MET', 'var_type': 'SNV/InDel/CNV'}
    ]
    items = [
        {'text': '基因', 'w': 1420, 'key': 'gene'},
        {'text': '变异', 'w': 4100, 'key': 'amino_acid_change'},
        {'text': '检测情况', 'w': 4100, 'key': 'result'},
    ]

    trs = ''
    tcs = ''
    for tc_item in items:
        tc_item['fill'] = green_bg
        tcs += write_tc_panel(tc_item)
    trs += tr.write(tcs)
    for g_item in genes:
        tcs = ''
        gene = g_item.get('gene')
        result = filter(lambda x: x.get('gene') == gene, data.get('stars'))
        result_text = '未检出'
        color = 'auto'
        if len(result):
            result_text = '突变型'
            color = 'red'
        tc_items = [
            {'text': g_item.get('gene'), 'weight': 1, 'w': items[0].get('w')},
            {'text': g_item.get('var_type'), 'weight': 0, 'w': items[1].get('w')},
            {'text': result_text, 'weight': 0, 'w': items[2].get('w'), 'color': color},
        ]
        for tc_item1 in tc_items:
            tcs += write_tc_panel(tc_item1)
        trs += tr.write(tcs)
    return table.write(trs)


def write_result1(data, cat):
    diagnosis = data.get('diagnosis')
    stars = data.get('stars')
    print data.get('huoyi')
    paras = ''
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    size = 10
    p_set = para_setting(spacing=[0, 1.5], line=16, rule='exact')
    CGAT = {
        "C": "胞嘧啶", "G": "鸟嘌呤", "A": "腺嘌呤", "T": "胸腺嘧啶"
    }
    amino = {
        "A": "丙氨酸", "R": "精氨酸", "D": "天冬氨酸", "C": "半胱氨酸",
        "Q": "谷氨酰胺", "E": "谷氨酸", "H": "组氨酸", "I": "异亮氨酸",
        "G": "甘氨酸", "N": "天冬酰胺", "L": "亮氨酸", "K": "赖氨酸",
        "M": "甲硫氨酸", "F": "苯丙氨酸", "P": "脯氨酸", "S": "丝氨酸",
        "T": "苏氨酸", "W": "色氨酸", "Y": "酪氨酸", "V": "缬氨酸",
        "X": "翻译提前终止",
    }

    for report_item in stars:
        gene = report_item.get('gene')
        drug = report_item.get('drug')
        amino_acid_change = report_item.get('amino_acid_change') or ''
        effect = report_item.get('effect')
        exon_number = report_item.get('exon_number')
        p1 = amino_acid_change.split('p.')[-1]

        paras += p.write(
            para_setting(spacing=[0, 1], line=12, rule='auto'),
            r_panel.text('%s %s;' % (gene, amino_acid_change), size, 1)
        )
        run1 = r_panel.text('变异解析：', size, 1)
        for k in ['drug', 'diagnosis']:
            if k not in report_item:
                report_item[k] = '（？？？）'
        jiexi = '患者样本中检出的%s %s为%s，' % (gene, amino_acid_change, effect)
        jiexi += '该突变位于%s基因的第%s号外显子，' % (gene, exon_number)
        if len(p1) > 2:
            t1 = CGAT.get(p1[0])
            no = p1[1:-1]
            t2 = amino.get(p1[-1])
            try:
                jiexi += u'导致该基因编码的蛋白序列的第%s位氨基酸由%s' % (no, t1)
                jiexi += u'替换为%s。' % t2
            except:
                print gene
            jiexi += '该突变是%s基因%s号外显子常见敏感突变。' % (gene, exon_number)
            jiexi += '在%s患者中，携带%s敏感突变的患者可获益于%s等%s酪氨酸激酶抑制剂。' % (diagnosis, gene, drug, gene)
        else:
            jiexi += '导致%s蛋白质功能异常。' % gene

        run1 += r_panel.text(jiexi)
        paras += p.write(p_set, run1)
        paras += p.write(
            p_set,
            r_panel.text('基因描述：', size, 1) + r_panel.text(report_item.get(u'cn_intro'))
        )
    paras += write_result_drug(stars, [])
    paras += p.write(r_panel.text('说明：PMID为PubMed数据库中收录文献的编号，PubMed数据库由美国国家医学图书馆(NLM)所属的国家生物技术信息中心(NCBI)开发，是使用最为广泛的医学文献数据库之一。', '小五'))
    paras += write_result_drug_description('潜在获益药物说明', data.get('huoyi'), [
        {'text': '药物名称', 'w': 1300, 'key': 'drug_name'},
        {'text': '商品名', 'w': 1300, 'key': 'product_name'},
        {'text': '药物类型', 'w': 1300, 'key': 'drug_name'},
        {'text': '审批状态', 'w': 800, 'key': 'drug_name'},
        {'text': '药物说明', 'w': 4900, 'key': 'drug_description'}
    ])
    paras += p.write()
    paras += write_result_drug_description('相关临床研究', stars, [
        {'text': '基因', 'w': 1300, 'key': 'drug_name'},
        {'text': '入组标准', 'w': 1500, 'key': 'drug_name'},
        {'text': '适应症', 'w': 1500, 'key': 'drug_name'},
        {'text': '临床研究\n编号', 'w': 1600, 'key': 'drug_name'},
        {'text': '临床研究\n分期', 'w': 1600, 'key': 'drug_description'},
        {'text': '描述', 'w': 2100, 'key': 'drug_description'},
    ])
    paras += p.write()
    paras += write_result_drug_description('检出变异总表', stars, [
        {'text': '基因', 'w': 1300, 'key': 'gene'},
        {'text': '转录本编号', 'w': 1600, 'key': 'transcript_id'},
        {'text': '核苷酸\n变化', 'w': 1300, 'key': 'nucleotide_change'},
        {'text': '氨基酸\n变化', 'w': 1300, 'key': 'amino_acid_change'},
        {'text': '外显子\n位置', 'w': 1000, 'key': 'exon_number'},
        {'text': '变异类型', 'w': 1500, 'key': 'effect'},
        {'text': '突变比例/\n拷贝数', 'w': 1600, 'key': 'tcn_em'},
    ])
    paras += p.write()
    return paras


def write_result_TMB(tmb_info):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('肿瘤突变负荷（TMB）评估', '小四', weight=1, color=green))
    p_set = para_setting(line=12, rule='auto')
    items = [
        {'label': '突变负荷（TMB; Non-synonymous Mutations per Mb）：', 'result': tmb_info.get('tmb')},
        {'label': '突变负荷在该癌种患者人群中的Percentile Rank：', 'result': '10.25%'},
        {'label': '免疫检查点抑制剂疗效评估：', 'result': '该患者的肿瘤突变负荷程度低于该癌种人群肿瘤突变负荷的平均水平，因此，该患者可能对免疫治疗的应答偏低。'}
    ]
    for item in items:
        run = r_panel.text(item.get('label'), normal_size)
        run += r_panel.text(item.get('result'), normal_size, 1, color=green)
        paras += p.write(p_set, run)
    paras += p.write(para_setting(spacing=[0, 16]), r_panel.picture(12.73, rId='tmb', align=['center', '']))
    paras += p.write(para_setting(spacing=[1, 0.5], line=16, rule='exact'), r_panel.text('临床意义', '小四', 1))
    text = '''肿瘤突变负荷（Tumor Mutation Burden，TMB）通常定义为每个癌症病人全外显子测序或靶向测序每百万碱基（Mb）的非同义突变或所有体细胞突变数目。根据科研报道及本实验室数据统计，高TMB阈值为＞10.4Muts/Mb。
    既往研究表明肿瘤突变负荷TMB可用于定量估计肿瘤基因组编码区的突变总数，不同癌症类型具有不同的肿瘤突变负荷水平。研究表明具有较高水平TMB的肿瘤细胞更容易被免疫系统识别，同时在多项临床研究中已证实对免疫检查点抑制剂如纳武利尤单抗、帕博利珠单抗、Ipilimumab等有更强的免疫应答效果。
    在一项对100，000个人类癌症基因组的分析中揭示了肿瘤突变负荷（TMB）的情况。描述了TMB在100，000个癌症病例的多样化队列中的分布，并测试了100多种肿瘤类型中体细胞改变与TMB之间的关联。发现一部分患者在几乎所有类型的癌症中（肺癌、肾癌、皮肤癌等）都表现出高TMB，包括许多罕见的肿瘤类型[PMID: 28420421]。
    一项基于Foundation one CDx的研究结果于2018年ASCO会议发布，表明在多种实体瘤包括非小细胞肺癌、尿路上皮癌中TMB值大于16 Muts/Mb的患者对阿特珠单抗表现出较高的敏感性[2018 ASCO Abstract No:12000]。
    临床三期研究表明，纳武利尤单抗（Nivolumab）联合依匹单抗（Ipilimumab）用于一线治疗TMB高于10 Muts/Mb的晚期非小细胞肺癌明显优于双铂化疗，1年的无进展生存期为43% vs 13%，中位无进展生存期为7.2 vs 5.5个月[PMID: 29658845; NCT02477826; 2018 ASCO Abstract No:9020]；基于上述研究结果，2018年6月FDA接受纳武利尤单抗联合Ipilimumab用于TMB高于10 Muts/Mb的晚期非小细胞肺癌的一线治疗的新药申请。
    '''
    for t in text.split('\n'):
        paras += p.write(para_setting(spacing=[0, 0.5], line=16, rule='exact', ind=['firstLine', 2]), r_panel.text(t, 11))
    return paras


def write_result_dMMR(report_data):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('错配修复基因缺陷(dMMR)检测', '小四', weight=1, color=green))
    genes = ['POLE', 'MLH1', 'MSH2', 'MSH6', 'PMS2']
    items = []
    for gene in genes:
        item2 = filter(lambda x: x['gene'] == gene, report_data)
        col2 = '未检测到相关基因突变'
        col3 = '/'
        col4 = '/'
        if len(item2) > 0:
            item = item2[0]
            col2 = '检测到突变'
            col3 = item.get('dna_vaf') or '/'
            col4 = item.get('effect')
        items.append({'gene': gene, 'col2': col2, 'col3': col3, 'col4': col4})
    paras += write_result_drug_description('', items, [
        {'text': '基因', 'w': 2000, 'key': 'gene'},
        {'text': '突变', 'w': 2800, 'key': 'col2'},
        {'text': '突变频率', 'w': 2400, 'key': 'col3'},
        {'text': '突变类型', 'w': 2400, 'key': 'col4'},
    ])
    paras += p.write(para_setting(spacing=[1, 0.5], line=16, rule='exact'), r_panel.text('临床意义', '小四', 1))
    text = '''在一项对结直肠癌患者的研究中发现，POLE胚系突变可导致林奇综合征相关表型，且在MMR相关基因IHC阴性的肿瘤组织中检测到高微卫星不稳定性MSI-H[PubMed: 25370038]。而POLE体细胞突变在微卫星稳定和不稳定的肿瘤组织中均被发现过 [PMID: 21157497，PMID: 24209623] 。
    MLH1、MSH2、MSH6和PMS2等错配修复基因的失活突变可造成错配修复缺陷（dMMR），导致微卫星高度不稳定（MSI-H）。MLH1、MSH2、MSH6和PMS2胚系突变常导致林奇综合征，结直肠癌、胃癌、子宫内膜癌等多种癌症的风险增高。同时，多项回顾性研究表明，MMR基因的体细胞突变同样可以造成dMMR/MSI-H，与散发性结直肠癌和子宫内膜癌发生相关 [PMID: 24333619; 25194673]。
    一项2期临床试验表明，帕博利珠单抗用于携带dMMR的结直肠癌患者的客观缓解率（ORR）为40%，用于不携带dMMR的结直肠癌患者的ORR为0% [PMID: 26028255]。另一项2期临床试验表明，纳武利尤单抗用于携带dMMR的结直肠癌患者的中位无进展生存期优于不携带dMMR的患者（5.3月 vs 1.4月）[2016 ASCO: Abstract #3501]。基于上述研究，《NCCN临床实践指南：结肠癌》（2018. V2）推荐帕博利珠单抗和纳武利尤单抗用于携带dMMR/MSI-H的结直肠癌患者。
    一项临床研究表明，帕博利珠单抗用于dMMR/MSI-H的结直肠癌患者的客观缓解率（ORR）为36%，非结直肠癌患者的ORR为46%。基于该研究，FDA已批准帕博利珠单抗用于dMMR/MSI-H的治疗进展后没有合适的替代治疗方案的儿童或者成年实体瘤患者的治疗；或者氟尿嘧啶、奥沙利铂和伊立替康治疗后进展的结直肠癌患者的治疗。
    CheckMate 142的临床研究结果显示，纳武利尤单抗用于dMMR/MSI-H的结直肠癌患者的ORR为28%，包括1例完全缓解和14例部分缓解 [PMID: 28734759]。基于该研究，FDA已批准纳武利尤单抗用于dMMR/ MSI-H的氟尿嘧啶、奥沙利铂和伊立替康为基础治疗进展后的成人和儿童（12岁及以上）的晚期结直肠癌患者。
    '''
    for t in text.split('\n'):
        paras += p.write(para_setting(spacing=[0, 0.3], line=16, rule='exact', ind=['firstLine', 2]), r_panel.text(t, 11))
    return paras


def write_result_MSI(msi_info):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('微卫星不稳定(MSI)数目', '小四', weight=1, color=green))
    items = [{'num': msi_info.get('somatic'), 'col2': msi_info.get('score'), 'col3': '0.4', 'col4': msi_info.get('sign')}]
    paras += write_result_drug_description('', items, [
        {'text': '检测微卫星数目', 'w': 2000, 'key': 'num'},
        {'text': '微卫星不稳定分值', 'w': 2400, 'key': 'col2'},
        {'text': '参考阈值', 'w': 2000, 'key': 'col3'},
        {'text': '微卫星不稳定性评级', 'w': 2800, 'key': 'col4'},
    ])
    paras += p.write(para_setting(spacing=[0, 16]), r_panel.picture(12.73, rId='msi', align=['center', '']))
    paras += p.write(para_setting(spacing=[0, 0.5], line=16, rule='exact'), r_panel.text('临床意义', '小四', 1))
    text = '''微卫星是指分布在人类基因组里的简单重复序列，又被称作短串连重复 （Short Tandem Repeats， STRs） 或简单重复序列 （Simple Sequence Repeat， SSRs）， 是均匀分布于真核生物基因组中的简单重复序列，由2～6个核苷酸的串联重复片段构成，由于重复单位的重复次数在个体间呈高度变异性并且数量丰富，因此微卫星的应用非常广泛。
    MSI是指与正常组织相比，在肿瘤中某一微卫星由于重复单位的插入或缺失而造成的微卫星长度的任何改变，出现新的微卫星等位基因现象。其发生机制主要包括DNA多聚酶的滑动导致重复序列中1个或多个碱基的错配和微卫星重组导致碱基对的缺失或插入。
    在2015年ASCO年会上，来自约翰霍普金斯医院的Le， et al，报道了基于MMR状态指导下的抗PD-1免疫治疗在晚期癌症中的价值。该研究共入组了32例经目前所有标准治疗均失败的晚期CRC患者，包括11例dMMR和21例pMMR，所有人均接受抗PD-1单抗Pembrolizumab（10mg/kg， Q2W）治疗。结果显示，dMMR组和pMMR组的ORR分别为40%和0%，而两组的DCR分别为90%和11%，均具有显著差异；dMMR组的中位PFS和OS均未达到，而pMMR组的中位PFS和OS分别为2.2月（HR， 0.103; 95%CI， 0.029-0.373， p<0.001）和5.0月（HR， 0.216; 95%CI， 0.047-1.1， p=0.02）。因此，研究者认为，对于经目前所有标准治疗均失败、且为dMMR的晚期CRC患者，可给予抗PD-1单抗Pembrolizumab治疗。
    目前FDA批准Pembrolizumab用于dMMR/MSI-H型的转移性实体瘤，Nivolumab用于dMMR/MSI-H的转移性结直肠癌。Science发表了NCT01876511的临床研究结果显示，Pembrolizumab用于治疗MSI-H的晚期肿瘤患者，MSI-H型肿瘤患者ORR高达54%。
    '''
    for t in text.split('\n'):
        paras += p.write(para_setting(spacing=[0, 0.2], line=16, rule='exact', ind=['firstLine', 2]), r_panel.text(t, 11))
    return paras


def write_result_kangyuan(report_data):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('抗原加工复合缺陷检测', '小四', weight=1, color=green))
    genes = ['ERAP1', 'TAPA', 'TAP2']
    items = []
    for gene in genes:
        item2 = filter(lambda x: x['gene'] == gene, report_data)
        col2 = '未检测到相关基因突变'
        col3 = '/'
        col4 = '/'
        if len(item2) > 0:
            item = item2[0]
            col2 = '检测到突变'
            col3 = item.get('dna_vaf')
            col4 = item.get('effect')
        items.append({'gene': gene, 'col2': col2, 'col3': col3, 'col4': col4})
    paras += write_result_drug_description('', items, [
        {'text': '基因', 'w': 2000, 'key': 'gene'},
        {'text': '突变', 'w': 2800, 'key': 'col2'},
        {'text': 'DNA频率', 'w': 2400, 'key': 'col3'},
        {'text': '突变类型', 'w': 2400, 'key': 'col4'},
    ])
    paras += p.write(para_setting(spacing=[1, 0.5], line=16, rule='exact'), r_panel.text('基因简介', '小四', 1))
    items2 = [
        {'gene': 'ERAP1', 'description': '内质网氨基肽酶1（endoplasmic reticulum aminopeptidase 1，ERAP1）是氨基肽酶M1家族中的一个多功能酶，是抗原递呈不可或缺的重要分子基础，在抗原肽的加工处理、提呈中发挥重要作用，ERAP1的突变会影响抗原的加工。如果ERAP发生突变，尤其是会严重影响蛋白质编码的无义突变和移码突变，将会影响肿瘤新生抗原（Neoantigen）的加工处理，从而降低抗原肽的免疫原性及蛋白酶体剪切。'},
        {'gene': 'TAP1/2', 'description': '抗原处理相关转运体蛋白 （transporter associated with antigen processing， TAP）在内源性抗原提呈过程中有重要作用，负责内源性抗原从胞浆到内质网 （ER） 腔的转运。TAP异二聚体由TAP1和TAP2蛋白组成，每个亚基各有一个核酸结合区（NBD）和一个跨膜区（TMD），TAP1和TAP2的突变会影响抗原的呈递。如果TAP1及TAP2基因发生突变，会影响肿瘤新生抗原的转运及MHC亲和力的改变。'}
    ]
    for item2 in items2:
        paras += p.write(para_setting(line=16, rule='exact'), r_panel.text(item2.get('gene'), 11, 1))
        paras += p.write(para_setting(line=16, rule='exact', spacing=[0, 1]), r_panel.text(item2.get('description'), 11))
    paras += p.write(para_setting(spacing=[1, 0.5], line=16, rule='exact'), r_panel.text('临床意义', '小四', 1))
    text = '''作为MHC-I类抗原呈递通路基因的一部分，抗原加工相关转运体（transporter associated with antigen presentation）TAP1和TAP2能够将抗原肽从细胞质转运到内质网。研究表明，TAP1和TAP2基因多态性可能会改变其分子结构，进而改变其功能，最终影响抗原呈递过程。这种抗原加工呈递过程发生缺陷将会导致肿瘤特异性CTL对肿瘤细胞的识别度下降，从而使肿瘤细胞产生免疫逃逸，而导致原发性/继发性的免疫治疗耐药[PMID: 23852952]。
    肿瘤抗原的表达依赖于抗原加工递呈 （antigen processing machinery，APM）的参与。TAP有研究表明，肿瘤细胞通过下调HLA和（或）APM 的表达从而降低肿瘤抗原表达，而这一现象在头颈部鳞癌HNSCC中十分普遍。Ferris等研究发现，超过50%的HNSCC的HLA低表达，这些患者往往具有广泛的淋巴结转移且不良预后。
    '''
    for t in text.split('\n'):
        paras += p.write(para_setting(spacing=[0, 0], line=16, rule='exact', ind=['firstLine', 2]), r_panel.text(t, 11))
    return paras


def write_result_risk(report_data):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('免疫检测点抑制剂使用风险检测', '小四', weight=1, color=green))
    genes = ['DNMT3A', 'EGFR', 'MDM2', 'MDM4', 'ALK', 'JAK1', 'JAK2', 'B2M', 'PTEN', 'STK11']
    items = []
    for gene in genes:
        item2 = filter(lambda x: x['gene'] == gene, report_data)
        col2 = '未检测到相关基因突变'
        col3 = '/'
        col4 = '/'
        if len(item2) > 0:
            item = item2[0]
            col2 = '检测到突变'
            col3 = item.get('tcn_em')
            col4 = item.get('effect')
        items.append({'gene': gene, 'col2': col2, 'col3': col3, 'col4': col4})
    paras += write_result_drug_description('', items, [
        {'text': '基因', 'w': 2000, 'key': 'gene'},
        {'text': '检测结果', 'w': 2800, 'key': 'col2'},
        {'text': '突变频率/拷贝数', 'w': 2400, 'key': 'col3'},
        {'text': '突变类型', 'w': 2400, 'key': 'col4'},
    ])
    paras += p.write(para_setting(spacing=[1, 0.5], line=16, rule='exact'), r_panel.text('临床意义', '小四', 1))
    text = ''' NCCN指南推荐（2019.V1）PD-L1≥50%且EGFR、ALK阴性的晚期NSCLC患者，免疫用药帕博利珠单抗作为首选，免疫治疗联合化疗作为一线用药。
    FDA批准帕博利珠单抗联合培美曲塞和铂作为EGFR阴性和ALK阴性的转移性，非鳞状非小细胞肺癌（NSqNSCLC）患者的一线治疗。
    CFDA批准纳武利尤单抗治疗EGFR阴性和ALK阴性的既往接受过含铂方案化疗方案后疾病进展或不可耐受的局部晚期或转移性非小细胞肺癌成年患者。
    有临床研究表明，在155名患者中，在所有6名携带MDM2 / MDM4扩增的个体中都观察到TTF（治疗失败）<2个月。在抗PD-1 PD-L1 PD-1 / PD-L1单药治疗后，其中4名患者的现有肿瘤大小显著增加（55％至258％），新的大肿块显著加快了进展速度（与免疫治疗前2个月相比呈2.3-，7.1-，7.2-和42.3-倍）。在多变量分析中，MDM2 / MDM4和EGFR改变与TTF <2个月相关。 10例EGFR改变患者中有2例也是过度进展者（肿瘤大小增加53.6％和125％;增加35.7-和41.7-倍）。[PMID: 28351930]。
    DNMT3A是一种存在于人体内的蛋白酶，可以使去甲基化的CpG位点重新甲基化，即参与DNA的从头甲基化。有研究表明在黑色素瘤中DNA甲基化会影响到PD-L1的表达，因此黑素瘤能够逃避抗肿瘤免疫反应[PMID: 30240750]。
    CheckMate 142研究表明在非小细胞肺癌中，携带EGFR驱动基因突变的患者，对PD-1/PD –L1免疫检查点抑制剂的客观反应率（ORR）要低于未突变患者（3.6% vs. 23.3%）[PMID: 27225694; 26645196]。
    一项药物临床前动物实验显示，携带PTEN缺失突变黑色素瘤小鼠会抑制T细胞杀死肿瘤细胞使肿瘤细胞进行免疫逃逸。在患者中，PTEN缺失突变会导致黑色素瘤患者肿瘤部位的肿瘤浸润性淋巴细胞减少，可能会降低PD-L1免疫治疗应答。[PMID: 26645196]。
    一项药物临床前研究显示，携带JAK1/JAK2功能性缺失突变会影响抗原递呈基因B2M的功能下调，从而可能会降低PD-L1免疫治疗的应答率，并且在该研究中3名黑色素瘤患者均在接受免疫治疗后肿瘤复发[PMID: 27433843]。
    在一项药物临床研究中，研究者使用PD-1/PD-L1抑制剂对165个非小细胞肺癌患者进行了治疗，结果显示携带有STK11和KRAS双突变的患者较野生型患者接受治疗的效果较差，两者的mOS分别是15.6个月和6.4个月[DOI: 10.1200/JCO.2017.35.15_suppl.9016]
    '''
    for t in text.split('\n'):
        paras += p.write(para_setting(spacing=[0, 0], line=16, rule='exact', ind=['firstLine', 2]), r_panel.text(t, 11))
    return paras


def write_result_HLA(hla_info):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('HLA分型结果', '小四', weight=1, color=green))

    items = hla_info.get('items')
    paras += write_result_drug_description('', items, [
        {'text': 'HLA Class I', 'w': 2000, 'key': 'col1'},
        {'text': '等位基因1', 'w': 2800, 'key': 'col2'},
        {'text': '等位基因2', 'w': 2400, 'key': 'col3'},
        {'text': '基因型', 'w': 2400, 'key': 'col4'},
    ])
    paras += p.write(para_setting(spacing=[1, 0.5], line=16, rule='exact'), r_panel.text('临床意义', '小四', 1))
    text = '''人类的MHC通常被称为HLA （human leucocyte antigen，HLA），即人类白细胞抗原，与人类的免疫系统功能密切相关。MHC基因（MHC gene），呈高度多态性，其编码的分子表达于不同细胞表面，参与抗原提呈，制约细胞间相互识别及诱导免疫应答。HLA的不同分型与新生抗原的处理和呈递相关。
    HLA I类（HLA Class I）分子突变使细胞质中抗原肽不能呈递给CD8T细胞。临床病例分析表明，膀胱癌，HLA I完全缺失和严重变异与肿瘤复发相关，膀胱癌、非小细胞肺癌、胰腺癌、乳腺癌、胃癌和前列腺癌的HLA I表达缺失越严重，其肿瘤的超进展越高。
    肿瘤细胞表面上也存在 HLA，参与抗原的处理和呈递。HLA 对 CD8+ T Cell 识别肿瘤细胞必不可少。人体大部分细胞含有两套 HLA 分子编码基因：一套基因遗传自母亲，另一套基因遗传自父亲。有时，基因变化能够导致一套基因全部或部分丢失，称为杂合子缺失（LOH）。当 HLA 位点发生 LOH，有可能促进免疫逃避，从而导致免疫治疗耐药。
    2017年12月，纪念斯隆-凯特林癌症中心（MSKCC）团队的一项研究发表在《Science》上，该研究分析了1535名接受免疫检查点抑制剂的晚期癌症患者的HLA I基因型，治疗方式包括CTLA-4单抗、PD-1单抗和PD-L1单抗治疗，结果显示，HLA I杂合型相较纯合型接受免疫检查点抑制剂的疗效较好，且杂合型与纯合型的肿瘤突变负荷没有统计学差异[PMID: 29217585]。
    '''
    for t in text.split('\n'):
        paras += p.write(para_setting(spacing=[0, 0.5], line=16, rule='exact', ind=['firstLine', 2]), r_panel.text(t, 11))
    return paras


def write_result_KANGYUAN_NEW(report_data):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('肿瘤新生抗原', '小四', weight=1, color=green))

    paras += write_result_drug_description('', report_data, [
        {'text': '识别号', 'w': 1600, 'key': 'col1'},
        {'text': '序列', 'w': 1600, 'key': 'col2'},
        {'text': '亲和力', 'w': 1600, 'key': 'col3'},
        {'text': '剪切效率', 'w': 1600, 'key': 'col4'},
        {'text': '稳定性排名（%）', 'w': 1800, 'key': 'col4'},
        {'text': '免疫原性', 'w': 1400, 'key': 'col4'},
    ])
    paras += p.write(para_setting(spacing=[1, 0.5], line=16, rule='exact'), r_panel.text('临床意义', '小四', 1))
    text = '''癌症细胞在基因变异的基础上产生的带有特异性氨基酸序列变异的蛋白被称为“新生抗原”（neoantigen)。癌细胞在发生发展过程中，会产生很多基因突变，而部分基因突变也会产生正常组织、正常细胞所没有的蛋白质，这些蛋白质，很有可能也会激活免疫系统，并引来免疫系统对癌细胞的攻击。这些能激活免疫系统（能被免疫细胞所识别）的、由癌细胞基因突变所产生的异常蛋白质（异常抗原），就是Neoantigen（肿瘤新生抗原）。

    2014年5月，《science》杂志上曾报道过一个利用体外扩增的、能特异性识别癌细胞的淋巴细胞。成功治疗了一例恶性晚期胆管癌患者。该研究团队将所有基因突变导致的异常的蛋白质片段进行人工合成，然后将患者肿瘤组织中分离出来的淋巴细胞，与携带有这些异常蛋白质片段的细胞共培养，并将能识别特定基因突变所产生的异常蛋白质的T淋巴细胞扩增、激活，重新回输到患者体内。第一次回输的细胞里，具有特异性识别能力的细胞大约占25%，细胞回输后，病人的肿瘤明显缩小，并且稳定了大约1年半的时间。该患者的肿瘤再次进展以后，提高回输细胞的纯度。第二次回输的细胞中，95%的细胞都是具有特异性能力的细胞。细胞回输后发现病人身体里全身各处的病灶，再次出现明显的缩小，一段时间后，最终达到了完全缓解，肿瘤完全消失。后靠淋巴细胞回输，就获得了完全缓解，疗效维持了数年，堪称奇迹[PMID: 24812403]。
    
    2015年12月，同一研究团队在《science》上发表重磅文章，他们利用类似的方式，检测了10个消化道肿瘤患者的组织，发现其中9个病友，都能找到1-3个以上的、能被自身免疫系统识别的基因突变导致的异常蛋白质。该研究团队甚至在一个肠癌的患者体内，发现著名的KRAS突变也可以成为为neoantigen（KRAS突变是史上最恶性、最难对付的致癌突变）。因此，学术界估计，绝大多数病友的肿瘤，应该都能找到或多或少的neoantigen。一般而言，患者肿瘤组织中基因突变的总数越多（也就是TMB越高），那么他所携带的neoantigen也越多[PMID: 26516200]。
    
    2017年7月13日，Nature杂志同一天发布了两项基于neoantigen的个性化肿瘤疫苗治疗恶性黑色素瘤的成功案例。德国的Carmen Loquai教授和Özlem tLoqua教授，利用neoantigen所对应的RNA做疫苗，一共治疗了13例病人。在接种了疫苗后，所有患者体内都产生了针对neoantigen的免疫反应。8位局部晚期接受了手术治疗的病友，其无复发生存时间明显延长，疫苗的注射相当于大幅度推迟乃至预防了肿瘤的复发；另外5位患者为晚期恶性黑色素瘤患者，其中的2位在单独接受疫苗注射后，出现了肿瘤明显缩小，达到了客观有效；另外一位病友接受了疫苗联合PD-1抗体治疗，肿瘤完全缓解[PMID: 28678784]。
    
    哈佛大学的Catherine J. Wu教授带领的团队，利用neoantigen所对应的抗原肽做疫苗，也成功报道了治疗恶性黑色素瘤的案例。他们入组了20位局部晚期或者晚期的恶性黑色素瘤患者，在这20位患者中一共找到了97个neoantigen，制备成了个性化肿瘤疫苗，应用给对应的患者。最后一共有6名患者，真正接受了治疗（其他病友拒绝冒险或者由更常规的治疗还可以试一试，没有同意参与这个全新的治疗试验组），4名患者在接受疫苗注射25个月后未出现复发；另外2名出现复发的病友，随后接受了PD-1抗体治疗，均实现了肿瘤完全缓解，并且在他们的身体里检测到了针对neoantigen的特异性免疫细胞。后选择其中2例患者在治疗前后的CT片子，在先后接受neoantigen疫苗和PD-1抗体之后，这两例患者肺部及皮下软组织中的转移灶，均达到了完全缓解，癌细胞不见踪迹[PMID: 28678778]。
    '''
    for t in text.split('\n'):
        paras += p.write(para_setting(spacing=[0, 0], line=16, rule='exact', ind=['firstLine', 2]), r_panel.text(t, 11))
    return paras


def write_result_drug_3(report_data):
    paras = ''
    p_set1 = para_setting(numId=11, pStyle='a5')
    paras += p.write(p_set1, r_panel.text('FDA/CFDA批准的免疫检查点抑制剂药物说明', '小四', weight=1, color=green))
    items = [
        {'drug_name': 'Pembrolizumab\n帕博利珠单抗', 'product_name': 'Keytruda\n可瑞达', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'FAD/CFDA', 'description': '帕博利珠单抗是一种PD-1单克隆抗体。自2014年开始，FDA相继批准该药物用于黑色素瘤、非小细胞肺癌、头颈鳞状细胞癌、尿道上皮癌、dMMR/MSI-H的结直肠癌和实体瘤以及胃癌等癌症。2018年CFDA批准该药物用于一线治疗进展后的局部晚期或转移性黑色素瘤。'},
        {'drug_name': 'Nivolumab\n纳武利尤单抗', 'product_name': 'Opdivo\n欧狄沃', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'FAD/CFDA', 'description': '纳武利尤单抗是一种PD-1单克隆抗体。自2014年开始，FDA相继批准该药用于黑色素瘤、非小细胞肺癌、肾癌、头颈部鳞状细胞癌、尿道上皮癌、dMMR/MSI-H的结直肠癌和肝细胞癌等癌症。2018年，CFDA批准该药物治疗EGFR阴性和ALK阴性的既往接受过含铂方案化疗方案后疾病进展或不可耐受的局部晚期或转移性非小细胞肺癌成年患者。'},
        {'drug_name': 'Atezolizumab\n阿特珠单抗', 'product_name': 'Tecentriq', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'FAD', 'description': '阿特珠单抗（Atezolizumab）是一种人源化单克隆抗体，能与肿瘤细胞或肿瘤浸润性免疫细胞上的PD-L1结合，并阻断其与PD-1和B7.1的相互作用，从而解除PD-1/PD-L1信号通路介导的肿瘤免疫应答抑制。2016年FDA批准该药用于治疗晚期或转移性尿道上皮癌以及转移性非小细胞肺癌。'},
        {'drug_name': 'Avelumab', 'product_name': 'Bavencio', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'FAD', 'description': 'Avelumab是一种全人源IgG1λ型单克隆抗体，可以结合PD-L1并阻止其与受体PD-1和B7.1的结合，从而解除PD-1/PD-L1信号通路介导的肿瘤免疫应答抑制。2017年FDA批准该药物用于治疗Merkel细胞癌和尿道上皮癌。'},
        {'drug_name': 'Durvalumab', 'product_name': 'Imfinzi', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'FAD', 'description': 'Durvalumab是一种PD-L1单克隆抗体。2017年FDA批准该药物用于转移性尿道上皮癌的患者。2018年，FDA批准该药物用于治疗接受标准铂类化疗联合放疗后疾病未进展的，不可手术切除的III期非小细胞肺癌患者。'},
        {'drug_name': 'Ipilimumab', 'product_name': 'Yervoy', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'FAD', 'description': 'Ipilimumab（依匹单抗）是一种全人源IgG1κ型单克隆抗体，能结合人细胞毒性T淋巴细胞相关抗原4（CTLA-4），阻止CTLA-4与其配体（CD80和CD86）的结合，增加T细胞的活性和增殖能力，从而提高抗肿瘤的免疫应答能力。2011年FDA批准该药治疗不可切除的或转移性黑色素瘤。'},
        {'drug_name': 'Cemiplimab-rwlc', 'product_name': 'Libtayo', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'FAD', 'description': 'Cemiplimab-rwlc是一种PD-1单克隆抗体，通过阻断PD-1和其配体之间的相互作用，从而解除PD-1/PD-L1信号通路介导的肿瘤免疫应答抑制。2018年FDA批准该药物用于皮肤鳞状细胞癌（CSCC）的治疗。'},
        {'drug_name': '特瑞普利单抗', 'product_name': '拓益', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'CFDA', 'description': '特瑞普利单抗是一种PD-1受体的全人源单克隆抗体，可通过封闭T淋巴细胞的PD-1，阻断其与肿瘤细胞表面PD-L1结合，解除肿瘤细胞对免疫细胞的免疫抑制，使免疫细胞重新发挥抗肿瘤细胞免疫作用而杀伤肿瘤细胞。2018年12月17日，CFDA批准该药物用于既往接受全身系统治疗失败的不可切除或转移性黑色素瘤的治疗。'},
        {'drug_name': '信迪利单抗', 'product_name': '达伯舒', 'drug_type': 'PD1-1\n单克隆抗体', 'state': 'CFDA', 'description': '信迪利单抗是一种人类免疫球蛋白G4（IgG4）单克隆抗体，能特异性结合T细胞表面的PD-1分子，从而阻断导致肿瘤免疫耐受的 PD-1/程序性死亡受体配体 1（Programmed Cell Death-1 Ligand-1, PD-L1）通路，重新激活淋巴细胞的抗肿瘤活性，从而达到治疗肿瘤的目的。2018年12月27日，CFDA批准该药用于至少经过二线系统化疗的复发或难治性经典型霍奇金淋巴瘤的治疗。'},
    ]

    paras += write_result_drug_description('', items, [
        {'text': '药物名称', 'w': 1600, 'key': 'drug_name'},
        {'text': '商品名', 'w': 1300, 'key': 'product_name'},
        {'text': '药物类型', 'w': 1600, 'key': 'drug_type'},
        {'text': '审批\n状态', 'w': 1000, 'key': 'state'},
        {'text': '药物说明', 'w': 4100, 'key': 'description'}
    ])
    return paras


def write_result2(report_data, cat):
    paras = ''
    tmb_info = report_data.get('tmb_info')
    stars = report_data.get('stars')
    msi_info = report_data.get('msi_info')
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    paras += write_result_TMB(tmb_info) + p_sect_normal
    paras += write_result_dMMR(stars) + p_sect_normal
    paras += write_result_MSI(msi_info) + p_sect_normal
    paras += write_result_risk(stars) + p_sect_normal
    paras += write_result_kangyuan(stars) + p_sect_normal
    return paras


def write_result3(report_data, cat):
    paras = ''
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    paras += write_result_HLA(report_data.get('hla_info')) + p_sect_normal
    paras += write_result_KANGYUAN_NEW([]) + p_sect_normal
    paras += write_result_drug_3(report_data) + p_sect_normal
    return paras


def write_result4(rs_geno, cat):
    drugs = []
    paras = ''
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    paras += p.write(para_setting(line=20, rule='exact', spacing=[0, 1]), r_panel.text('人群基因序列多态性造成相关代谢蛋白功能差异，使化学治疗药物的有效性和毒副作用产生差异，因此进行基因序列多态性检测可以为化疗用药提供参考。患者基因序列多态性信息与化学治疗药物有效性和毒副作用评估如下表所示。'))
    items = [
        {
            'category': '铂类',
            'drug':  [
                {
                    'drug_name': '卡铂',
                    'genes': [
                        {'gene': 'MTHFR', 'rs': 'rs1801133', 'level': 'Level 2A', 'description': '药效减弱'},
                    ]
                },
                {
                    'drug_name': '奥沙利铂',
                    'genes': [
                        {'gene': 'ERCC1', 'rs': 'rs11615', 'level': 'Level 2B', 'description': '毒副作用增强；药效减弱'},
                        {'gene': 'GSTP1', 'rs': 'rs1695', 'level': 'Level 2A', 'description': '毒副作用增强'},
                        {'gene': 'XRCC1', 'rs': 'rs25487', 'level': 'Level 2B', 'description': '药效减弱'},
                    ]
                },
                {
                    'drug_name': '顺铂',
                    'genes': [
                        {'gene': 'ERCC1', 'rs': 'rs3212986', 'level': 'Level 2B', 'description': '毒副作用增强'},
                        {'gene': 'ERCC2', 'rs': 'rs13181', 'level': 'Level 3', 'description': '药效增强'},
                        {'gene': 'ERCC2', 'rs': 'rs1799793', 'level': 'Level 3', 'description': '药效减弱'},
                        {'gene': 'TPMT', 'rs': 'rs1142345', 'level': 'Level 3', 'description': '毒副作用减弱'},
                        {'gene': 'TPMT', 'rs': 'rs1800460', 'level': 'Level 3', 'description': '毒副作用减弱'},
                        {'gene': 'XPC', 'rs': 'rs2228001', 'level': 'Level 1B', 'description': '毒副作用减弱'},
                    ]
                },
            ]
        },
        {
            'category': '蒽环素类',
            'drug':  [
                {
                    'drug_name': '多柔比星',
                    'genes': [
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 3', 'description': '药效减弱'},
                    ]
                },
                {
                    'drug_name': '表柔比星',
                    'genes': [
                        {'gene': 'GSTP1', 'rs': 'rs1695', 'level': 'Level 2A', 'description': '药效增强；毒副作用减弱'},
                    ]
                },
            ]
        },
        {
            'category': '鬼臼素类',
            'drug':  [
                {
                    'drug_name': '依托泊苷',
                    'genes': [
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 3', 'description': '代谢增强'},
                        {'gene': 'DYNC2H1', 'rs': 'rs716274', 'level': 'Level 2B', 'description': '毒副作用减弱'},
                    ]
                }
            ]
        },
        {
            'category': '抗雌激素类',
            'drug':  [
                {
                    'drug_name': '他莫昔芬',
                    'genes': [
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 3', 'description': '药效增强'},
                    ]
                },
            ]
        },
        {
            'category': '抗雌激素类\n嘧啶类似物',
            'drug':  [
                {
                    'drug_name': '他莫昔芬',
                    'genes': [
                        {'gene': 'CYP2D6', 'rs': 'rs3892097', 'level': 'Level 2A', 'description': '药效增强；毒副作用增强'},
                    ]
                },
                {
                    'drug_name': '卡培他滨',
                    'genes': [
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 3', 'description': '毒副作用增强'},
                    ]
                },
            ]
        },
        {
            'category': '嘧啶类似物\n烷化剂',
            'drug':  [
                {
                    'drug_name': '卡培他滨\n吉西他滨',
                    'genes': [
                        {'gene': 'DPYD', 'rs': 'rs3918290', 'level': 'Level 1A', 'description': '药物代谢增强；毒副作用减弱'},
                        {'gene': 'DPYD', 'rs': 'rs55886062', 'level': 'Level 1A', 'description': '毒副作用减弱'},
                        {'gene': 'MTHFR', 'rs': 'rs1801133', 'level': 'Level 3', 'description': '毒副作用增强'},
                        {'gene': 'TYMS', 'rs': 'rs183205964', 'level': 'Level 3', 'description': '毒副作用减弱'},
                        {'gene': 'CDA', 'rs': 'rs1048977', 'level': 'Level 3', 'description': '代谢增强'}
                    ]
                },
                {
                    'drug_name': '吉西他滨\n氟尿嘧啶',
                    'genes': [
                        {'gene': 'CDA', 'rs': 'rs2072671', 'level': 'Level 3', 'description': '毒副作用减弱'},
                        {'gene': 'CDA', 'rs': 'rs60369023', 'level': 'Level 3', 'description': '药物代谢增强；毒副作用减弱'},
                        {'gene': 'RRM1', 'rs': 'rs1042858', 'level': 'Level 3', 'description': '毒副作用减弱'},
                        {'gene': 'RRM1', 'rs': 'rs183484', 'level': 'Level 3', 'description': '药效增强'},
                        {'gene': 'RRM1', 'rs': 'rs9937', 'level': 'Level 3', 'description': '毒副作用增强；药效减弱'},
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 3', 'description': '毒副作用减弱'}
                    ]
                },
                {
                    'drug_name': '氟尿嘧啶\n环磷酰胺',
                    'genes': [
                        {'gene': 'DPYD', 'rs': 'rs67376798', 'level': 'Level 1A', 'description': '药物代谢增强；毒副作用减弱'},
                        {'gene': 'GSTP1', 'rs': 'rs1695', 'level': 'Level 2A', 'description': '药效减弱'},
                        {'gene': 'MTHFR', 'rs': 'rs1801133', 'level': 'Level 3', 'description': '药效减弱'},
                        {'gene': 'GSTP1', 'rs': 'rs1695', 'level': 'Level 2A', 'description': '药效增强；毒副作用减弱'},
                    ]
                },
            ]
        },
        {
            'category': '烷化剂\n喜树碱类',
            'drug':  [
                {
                    'drug_name': '环磷酰胺\n伊立替康',
                    'genes': [
                        {'gene': 'MTHFR', 'rs': 'rs1801133', 'level': 'Level 2A', 'description': '毒副作用减弱'},
                        {'gene': 'UGT1A1', 'rs': 'rs4148323', 'level': 'Level 2A', 'description': '毒副作用减弱'},
                    ]
                }
            ]
        },
        {
            'category': '叶酸类似物',
            'drug':  [
                {
                    'drug_name': '培美曲塞',
                    'genes': [
                        {'gene': 'MTHFR', 'rs': 'rs1801133', 'level': 'Level 3', 'description': '药效减弱'},
                    ]
                },
            ]
        },
        {
            'category': '叶酸类似物\n长春花生物碱类',
            'drug':  [
                {
                    'drug_name': '培美曲塞\n甲氨蝶呤',
                    'genes': [
                        {'gene': 'TYMS', 'rs': 'rs151264360', 'level': 'Level 3', 'description': '药效增强'},
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 2A', 'description': '毒副作用减弱'},
                    ]
                },
                {
                    'drug_name': '甲氨蝶呤\n长春新碱',
                    'genes': [
                        {'gene': 'MTHFR', 'rs': 'rs1801133', 'level': 'Level 2A', 'description': '药效增强；毒副作用减弱'},
                        {'gene': 'SLCO1B1', 'rs': 'rs11045879', 'level': 'Level 2A', 'description': '药物代谢减弱；毒副作用减弱'},
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 3', 'description': '药效减弱'},
                    ]
                },
            ]
        },
        {
            'category': '紫杉烷类',
            'drug':  [
                {
                    'drug_name': '多西他赛',
                    'genes': [
                        {'gene': 'ERCC2', 'rs': 'rs13181', 'level': 'Level 3', 'description': '毒副作用增强'},
                    ]
                },
            ]
        },
        {
            'category': '紫杉烷类\n芳香化酶抑制剂',
            'drug':  [
                {
                    'drug_name': '紫杉醇',
                    'genes': [
                        {'gene': 'ABCB1', 'rs': 'rs1045642', 'level': 'Level 3', 'description': '药效增强'},
                    ]
                },
                {
                    'drug_name': '紫杉醇\n来曲唑',
                    'genes': [
                        {'gene': 'CYP2C8', 'rs': 'rs10509681', 'level': 'Level 4', 'description': '药物代谢增强'},
                        {'gene': 'CYP2C8', 'rs': 'rs11572080', 'level': 'Level 3', 'description': '毒副作用减弱'},
                        {'gene': 'CYP19A1', 'rs': 'rs4646', 'level': 'Level 3', 'description': '药效减弱（绝经后）'},
                    ]
                },
            ]
        },
        {
            'category': '芳香化酶抑制剂',
            'drug':  [
                {
                    'drug_name': '阿那曲唑',
                    'genes': [
                        {'gene': 'CYP19A1', 'rs': 'rs4646', 'level': 'Level 2B', 'description': '药效减弱（绝经前）/药效增强（绝经后）'},
                    ]
                },
            ]
        },
    ]
    thead = [
        {'key': 'category', 'text': '药物类别', 'w': 1320},
        {'key': 'drug_name', 'text': '药物名称', 'w': 1200},
        {'key': 'gene', 'text': '检测基因', 'w': 1400},
        {'key': 'rs', 'text': '检测位点', 'w': 1400},
        {'key': 'genetype', 'text': '基因型', 'w': 1400},
        {'key': 'level', 'text': '证据等级', 'w': 1400},
        {'key': 'description', 'text': '用药提示', 'w': 1600}
    ]
    trs = ''
    tcs0 = ''
    for th in thead:
        th['fill'] = green_bg
        tcs0 += write_tc_panel(th)
    trs += tr.write(tcs0)

    chems = []
    for c_index, item in enumerate(items):
        category = item.get('category')
        drug = item.get('drug') or []
        for d_index, d_item in enumerate(drug):
            drug_name = d_item.get('drug_name')
            genes = d_item.get('genes')
            max_item = {'level': ''}
            for g_index, g_item in enumerate(genes):
                level = g_item.get('level')
                max_level = max_item.get('level')
                vMerge1 = ''
                if len(drug) > 1:
                    vMerge1 = '<w:vMerge w:val="restart"/>' if c_index == 0 and d_index == 0 and g_index == 0 else '<w:vMerge/>'
                vMerge2 = ''
                if len(genes) > 1:
                    vMerge2 = '<w:vMerge w:val="restart"/>' if g_index == 0 else '<w:vMerge/>'
                tcs = ''
                g_item['category'] = category
                g_item['drug_name'] = drug_name
                rs = g_item.get('rs')
                rs_list = filter(lambda x: x[0] == rs, rs_geno)
                if len(rs_list) > 0:
                    rs_item = rs_list[0]
                    g_item['genetype'] = rs_item[1]
                    if max_level == '' or max_level > level:
                        max_item = g_item
                else:
                    g_item['level'] = ''
                    g_item['description'] = ''
                for th_index, th_item in enumerate(thead):
                    key = th_item.get('key')
                    w = th_item.get('w')
                    vMerge = ''
                    weight = 0
                    if th_index == 0:
                        vMerge = vMerge1
                        weight = 1
                    elif th_index == 1:
                        vMerge = vMerge2
                    tcs += write_tc_panel({'text': g_item.get(key), 'w': w, 'vMerge': vMerge, 'weight': weight})
                trs += tr.write(tcs)
            d_item['max_item'] = max_item
            if max_item.get('level'):
                chems.append(d_item)
    paras += table.write(trs)
    paras += p.write(r_panel.text('备注：此处检测结果不具有临床医嘱性质，仅供临床医师参考，不作为直接用药依据。', '小五'))
    return paras, chems


def write_abstract1(data, cat):
    stars = data.get('stars')
    paras = ''
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    paras += h4_panel(u'具有临床意义的基因变异')
    trs = ''
    w = 1200
    keys = [
        {'w': w, 'title': '基因', 'key': 'gene'},
        {'w': w+200, 'title': '转录本编号', 'key': 'transcript_id'},
        {'w': w+300, 'title': '核苷酸变化', 'key': 'nucleotide_change'},
        {'w': w+300, 'title': '氨基酸变化', 'key': 'amino_acid_change'},
        {'w': w+300, 'title': '外显子位置', 'key': 'exon_number'},
        {'w': w+120, 'title': '变异类型', 'key': 'effect'},
        {'w': w+60, 'title': '突变比例/拷贝数', 'key': 'tcn_em'}
    ]
    ws = []
    titles = []
    for key in keys:
        ws.append(key.get('w'))
        titles.append(key.get('title'))
    jc = 'center'
    trs += write_gray_tr({'ws': ws, 'text': titles, 'fill': green_bg, 'jc': jc})
    huoyi = []
    naiyao = []
    for report_item in stars:
        text = []
        mingan = report_item.get('mingan') or []
        if len(mingan) > 0:
            huoyi.append(report_item)
        naiyao1 = report_item.get('naiyao') or []
        if len(naiyao1) > 0:
            naiyao.append(report_item)
        for key2 in keys:
            text.append(report_item.get(key2.get('key')) or 'NA')
        trs += write_gray_tr({'ws': ws, 'text': text, 'jc': jc})
    paras += table.write(trs, ws)
    paras += h4_panel(u'潜在获益药物')
    # vmerge1 = '<w:vMerge w:val="restart"/>' if i == 0 and d == 0 else '<w:vMerge/>'
    paras += write_abstract_drug(data.get('huoyi'), 'mingan')
    paras += h4_panel(u'潜在耐药药物')
    paras += write_abstract_drug(data.get('naiyao'), 'naiyao')
    paras += h4_panel(u'本癌种FDA获批/NCCN指南推荐的靶药基因检出情况')
    paras += write_abstract_gene(data)
    paras += p.write()
    shuoming = '''说明：
    1）基因变异命名规则依据人类基因组变异学会（HGVS）建立的基因变异命名方法。
    2）突变比例：在该位点所有的等位基因中，突变等位基因的占比。 '''
    for s in shuoming.split('\n'):
        paras += p.write(para_setting(line=16, rule='exact'), r_panel.text(s, '小五'))
    return paras


def write_abstract2(data, cat):
    overview = data.get('overview')
    msi_info = data.get('msi_info')
    hla_info = data.get('hla_info')
    paras = ''
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    paras += h4_panel(u'免疫检查点抑制剂治疗适用性较差')
    trs = ''
    theads = [
        {'fill': green_bg, 'w': 1200, 'text': '序号', 'key': 'gene'},
        {'fill': green_bg, 'w': 4920, 'text': '检测指标', 'key': 'zhibiao'},
        {'fill': green_bg, 'w': 3600, 'text': '检测结果', 'key': 'result'}
    ]
    result = {
        'TMB': '%s Muts/Mb' % overview.get('tmb'),
        'MMR': 'pMMR',
        'PDL1': '~10%阳性',
        'MSI': msi_info.get('sign'),
        'gene': '检测到有害突变',
        'loss': '未检测到有害突变',
        'HLA': hla_info.get('hla_type'),
        'neoantigens': '66个',
    }
    items = [
        {'text': '肿瘤突变负荷\n（Tumor mutation Burden， TMB）', 'standard': '评判标准：详见表格下方备注。', 'key': 'TMB'},
        {'text': '错配修复基因\n（mismatch repair, MMR）', 'key': 'MMR', 'standard': '评判标准：pMMR：MMR基因均无功能缺失突变\ndMMR：MMR任一基因存在功能缺失突变'},
        {'text': 'PD-L1（肿瘤细胞）', 'key': 'PDL1', 'standard': '评判标准：TC≥1%为阳性（报告详情见附件二）'},
        {'text': '微卫星不稳定性\n（MicroSatellite Instability， MSI）', 'key': 'MSI', 'standard': '评判标准：根据105个微卫星重复和5个Promega经典微卫星位点进行比对，综合评估微卫星稳定型（MSS）、微卫星低不稳定型（MSI-L）和微卫星高不稳定型（MSI-H）。'},
        {'text': '免疫治疗风险基因', 'key': 'gene', 'standard': '评判标准：相关基因存在有害突变。\n本次检出EGFR基因突变，患者可能无法从免疫治疗中获益；'},
        {'text': '抗原加工复合体缺陷', 'key': 'loss', 'standard': '评判标准：相关基因存在有害突变'},
        {'text': 'HLA分型', 'key': 'HLA', 'standard': '评判标准：杂合型：所有等位基因均为杂合；\n纯合型：任意一对等位基因为纯合。'},
        {'text': '肿瘤新生抗原\n（Tumor Neoantigens）', 'key': 'neoantigens'}
    ]
    trs += write_tr_panel(theads)
    for index, item in enumerate(items):
        tcs = ''
        tcs += write_tc_panel({'text': index+1, 'weight': 1, 'w': theads[0]['w']})
        tcs += write_tc_panel({'text': item.get('text'), 'weight': 1, 'w': theads[1]['w'], 'line': 18, 'rule': 'exact'})
        tcs += write_tc_panel({'text': result.get(item.get('key')), 'weight': 0, 'w': theads[2]['w']})
        trs += tr.write(tcs)
        standard = item.get('standard')
        if standard:
            tcs2 = ''
            tcs2 += write_tc_panel({'text': ' ', 'w': theads[0]['w']})
            tcs2 += write_tc_panel({
                'text': standard, 'weight': 0,
                'w': theads[1]['w'] + theads[2]['w'], 'gridSpan': 2, 'jc': 'left', 'line': 18, 'rule': 'exact'
            })
            trs += tr.write(tcs2)
    paras += table.write(trs)
    run_tip = r_panel.text('备注（TMB评判标准）', 8, 1)
    run_tip += r_panel.text('：肺癌高TMB阈值为＞13.91 Muts/Mb，乳腺癌高TMB阈值为＞6.36Muts/Mb，肝癌高TMB阈值为＞5.28 Muts/Mb，胃癌高TMB阈值为＞7.29 Muts/Mb，直肠癌高TMB阈值为＞6.27 Muts/Mb，胰腺癌高TMB阈值为＞3.97Muts/Mb，宫颈癌高TMB阈值为＞8.4Muts/Mb，头颈部鳞状细胞癌高TMB阈值为＞10.83Muts/Mb，黑色素瘤高TMB阈值为＞27.76Muts/Mb，默克尔细胞癌高TMB阈值为＞22.62Muts/Mb，肾癌高TMB阈值为＞3.9Muts/Mb，尿路上皮癌高TMB阈值为＞12.44Muts/Mb，皮肤鳞状细胞癌高TMB阈值为＞86.07Muts/Mb，泛癌种高TMB阈值为＞10.57Muts/Mb。', 8)
    paras += p.write(para_setting(line=12, rule='auto'), run_tip)
    return paras


def write_abstract3(report_data, cat):
    paras = ''
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    paras += h4_panel(u'鉴定出66个新免疫抗原，为细胞免疫治疗或肿瘤疫苗制备提供序列依据')
    trs = ''
    theads = [
        {'fill': green_bg, 'w': 1400, 'text': '识别号', 'key': 'no'},
        {'fill': green_bg, 'w': 1800, 'text': '序列', 'key': 'index'},
        {'fill': green_bg, 'w': 1400, 'text': '亲和力', 'key': 'qinheli'},
        {'fill': green_bg, 'w': 1400, 'text': '剪切效率', 'key': 'cut'},
        {'fill': green_bg, 'w': 1800, 'text': '稳定性排名（%）', 'key': 'range'},
        {'fill': green_bg, 'w': 1800, 'text': '免疫原性', 'key': 'mianyi'}
    ]

    items = [
        {'no': 'CDx001', 'index': 'TDFGRAKLL', 'qinheli': '20.73', 'cut': '0.96', 'range': '47.0', 'mianyi': -0.02},
        {'no': 'CDx002', 'index': 'RAKLLGAEE', 'qinheli': '38.25', 'cut': '0.93', 'range': '65.0', 'mianyi': 0.03},
        {'no': 'CDx003', 'index': 'VKITDFGRA', 'qinheli': '61.89', 'cut': '0.89', 'range': '39.0', 'mianyi': 0.27},
        {'no': 'CDx004', 'index': 'KITDFGRAK', 'qinheli': '73.05', 'cut': '0.93', 'range': '47.0', 'mianyi': 0.24},
        {'no': 'CDx005', 'index': 'GRAKLLGAE', 'qinheli': '163.53', 'cut': '0.96', 'range': '65.0', 'mianyi': -0.17},
    ]
    trs += write_tr_panel(theads)
    for index, item in enumerate(items):
        tcs = ''
        for th in theads:
            key = th.get('key')
            tcs += write_tc_panel({'text': item.get(key), 'weight': 1 if th == '识别号' else 0, 'w': th['w'], 'line': 10, 'rule': 'auto'})
        trs += tr.write(tcs)
    paras += table.write(trs)
    p_set = para_setting(line=12, rule='auto')
    tips = '''备注:
    1. 报告摘要部分只展示前5名的新免疫抗原，全部新免疫抗原请见结果解读--肿瘤新生抗原鉴定结果部分 
    2.	亲和力是多肽与MHC结合的距离，数值越小结合力越强
    3.	剪切效率是蛋白酶体剪切多肽的效率
    4.	稳定性指多肽的稳定性，数值越小越稳定
    5.	免疫原性是指多肽激发免疫反应的能力，数值越大激发免疫反应的能力越强'''
    for t in tips.split('\n'):
        paras += p.write(p_set, r_panel.text(t, 8))
    return paras


def write_abstract4(chems, cat):
    paras = ''
    primary = '#00A683'
    info = '#0054A6'
    danger = '#FF0000'
    signs = [
        {'text': '√', 'degree': 'primary', 'color': primary, 'size': '四号'},
        {'text': '〇', 'degree': 'info', 'color': info, 'size': '五号'},
        {'text': '×', 'degree': 'danger', 'color': danger, 'size': '三号'}
    ]
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    paras += h4_panel(u'检测到5类综合效果优于平均人群的化疗药物使用方案', jc='center')
    run0 = r_panel.text('化疗用药提示参考最高证据等级的用药提示进行综合判读，将常用化疗药物初步划分为推荐药物（', normal_size)
    run0 += r_panel.text(signs[0].get('text'), size=signs[0].get('size'), color=signs[0].get('color'))
    run0 += r_panel.text('）、可选药物（', normal_size)
    run0 += r_panel.text(signs[1].get('text'), size=signs[1].get('size'), color=signs[1].get('color'))
    run0 += r_panel.text('）和慎用药物（', normal_size)
    run0 += r_panel.text(signs[2].get('text'), size=signs[2].get('size'), color=signs[2].get('color'))
    run0 += r_panel.text('），仅供医生参考，具体的治疗方案须由临床医生根据实际情况而决定。', normal_size)
    paras += p.write(para_setting(line=16, rule='exact', ind=['firstLine', 2], spacing=[0, 0.5]), run0)
    items = [
        {'drug': '卡铂', 'tip': 'primary'},
        {'drug': '奥沙利铂', 'tip': 'primary'},
        {'drug': '顺铂', 'tip': 'primary'},
        {'drug': '多柔比星', 'tip': 'info'},
        {'drug': '表柔比星', 'tip': 'primary'},
        {'drug': '依托泊苷', 'tip': 'primary'},
        {'drug': '他莫昔芬', 'tip': 'primary'},
        {'drug': '卡培他滨', 'tip': 'primary'},
        {'drug': '吉西他滨', 'tip': 'danger'},
        {'drug': '氟尿嘧啶', 'tip': 'primary'},
        {'drug': '环磷酰胺', 'tip': 'primary'},
        {'drug': '伊立替康', 'tip': 'primary'},
        {'drug': '培美曲塞', 'tip': 'primary'},
        {'drug': '甲氨蝶呤', 'tip': 'primary'},
        {'drug': '长春新碱', 'tip': 'primary'},
        {'drug': '多西他赛', 'tip': 'primary'},
        {'drug': '紫杉醇', 'tip': 'primary'},
        {'drug': '来曲唑（绝经后）', 'tip': 'primary'},
        {'drug': '阿那曲唑（绝经前）', 'tip': 'primary'},
        {'drug': '阿那曲唑（绝经后）', 'tip': 'primary'}
    ]
    print chems[0]
    for item in items:
        items2 = filter(lambda x: item.get('drug').split('（')[0] in x.get('drug_name'), chems)
        level_item = {'level': 'zzz'}
        for item2 in items2:
            max_item = item2.get('max_item')
            if max_item.get('level') < level_item.get('level'):
                level_item = max_item
                description = max_item.get('description')
                liaoxiao = None
                duxing = None
                if description is not None:

                    description = description.strip().split('；')
                    for des in description:
                        for d in des.split('/'):
                            if '代谢' in d or '药效' in d:
                                liaoxiao1 = None
                                if d.split('（')[0].endswith('强'):
                                    liaoxiao1 = True
                                elif d.split('（')[0].endswith('弱'):
                                    liaoxiao1 = False
                                else:
                                    print d, 'liaoxiao===='
                                if '绝经前' in item.get('drug'):
                                    if '绝经前' in d:
                                        liaoxiao = liaoxiao1
                                elif '绝经后' in item.get('drug'):
                                    if '绝经后' in d:
                                        liaoxiao = liaoxiao1
                                else:
                                    liaoxiao = liaoxiao1
                            if '毒' in d:
                                if d.endswith('强'):
                                    duxing = True
                                elif d.endswith('弱'):
                                    duxing = False
                                else:
                                    print d, 'duxing===='

                if liaoxiao is True and duxing is False:
                    item['tip'] = 'primary'
                elif liaoxiao is False and duxing is True:
                    item['tip'] = 'danger'
                elif liaoxiao is True or duxing is False:
                    item['tip'] = 'info'
                elif liaoxiao is None and duxing is True:
                    item['tip'] = '药效未知，毒性强'
                elif liaoxiao is False and duxing is None:
                    item['tip'] = '药效弱，毒性未知'
                elif description is None:
                    item['tip'] = '/'
                else:
                    item['tip'] = '不定'
                    print item.get('drug'), liaoxiao, duxing
    trs = ''
    theads = [
        {'fill': green_bg, 'w': 1200, 'text': '序号', 'key': 'gene'},
        {'fill': green_bg, 'w': 1800, 'text': '药物名称', 'key': 'drug'},
        {'fill': green_bg, 'w': 1600, 'text': '用药提示', 'key': 'tip'}
    ]

    row = int(math.floor(len(items) / 2.0))
    trs += write_tr_panel(theads*2)
    for i in range(row):
        tcs = ''
        index2 = i+row
        item1 = items[i]
        item2 = {} if index2 >= len(items) else items[index2]
        item1.update({'index': i})
        item2.update({'index': index2})
        items2 = [item1, item2]
        for item in items2:
            tip1 = item.get('tip')
            result1 = {'weight': 0, 'w': theads[2]['w'], 'text': tip1}
            if tip1:
                sign = filter(lambda x: x['degree'] == tip1, signs)
                if len(sign)> 0:
                    result1.update(sign[0])
            tcs += write_tc_panel({'text': '%02d' % (item.get('index')+1), 'weight': 0, 'w': theads[0]['w']})
            tcs += write_tc_panel({'text': item.get('drug'), 'weight': 0, 'w': theads[1]['w']})
            tcs += write_tc_panel(result1)
        trs += tr.write(tcs)
    paras += table.write(trs)
    paras += p.write(
        para_setting(spacing=[1.5, 0], line=15, rule='exact'),
        r_panel.text('说明：一种化疗药物的疗效或者毒副作用通常受多个基因的单核苷酸多态性（SNP）的影响。化疗药物综合判读规则参考最高证据等级，若最高证据等级用药提示不一致，则显示为不定。某些化疗药物仅有疗效的研究结论或者仅有毒副作用的研究结论，则以单一指标作为参考，另一指标则显示为一般。', '小五')
    )
    p_set = para_setting(line=15, rule='exact', ind=[2.2, 0])
    tips = '''1）推荐药物（√）：最高证据等级用药提示药效增强且毒副作用一般或减弱的化疗药物。
    2）慎用药物（×）：最高证据等级用药提示药效一般或减弱且毒副作用增强的化疗药物。
    3）可选药物（〇）：不满足推荐药物和慎用药物条件的其他化疗药物
    4）没有证据的当做一般处理； 证据等级相同的且相互矛盾的视为不定
    5）用药提示为“/”时，表示受检者携带的基因型尚未见研究报道。'''
    for t in tips.split('\n'):
        runs = []
        for s in signs:
            st = s.get('text')
            if st in t:
                ts = t.split(st)
                for t2 in ts:
                    runs.append(r_panel.text(t2, '小五'))
                runs.insert(1, r_panel.text(st, size=s['size'], color=s['color']))
        if len(runs):
            runt = ''.join(runs)
        else:
            runt = r_panel.text(t, '小五')
        paras += p.write(p_set, runt)
    return paras


def write_abstract5(cat):
    paras = ''
    paras += h2_panel(cat.get('title'), cat.get('bm'), size='小二', jc='center', outline=1)
    p_set = para_setting(line=12, rule='auto', ind=['hanging', 1.5])
    tips = '''1、本检测结果仅对此次送检样本负责。
    2、本检测结果仅报告检测范围内的基因变异，不能评估检测范围以外的基因变异及其影响。
    3、本检测主要用于辅助临床决策，用药推荐仅供医生参考，不具备医嘱性质，具体的治疗方案须由临床医生决定。
    4、本检测结果具有时效性，由于肿瘤发展是一个动态变化的过程，从严格意义上讲本检测只能反映检测样本采集时患者肿瘤的基因突变状态。
    5、本中心对以上检测结果保留最终解释权，如有疑义，请在收到结果后的 7 个工作日内与我们联系。'''
    for t in tips.split('\n'):
        runt = r_panel.text(t, '小五')
        paras += p.write(p_set, runt)
    paras += p.write(para_setting(spacing=[0, 15]))
    items = [
        {'border': [], 'text': '检验者', 'weight': 1, 'w': 1400},
        {'border': [], 'text': ' ', 'weight': 1, 'w': 1800, 'img': r_panel.picture(3.3, rId='suncuifeng', wrap='undertext')},
        {'border': [], 'text': '检验者', 'weight': 1, 'w': 1400},
        {'border': [], 'text': ' ', 'weight': 1, 'w': 1800, 'img': r_panel.picture(3.3, rId='zhouyan')},
        {'border': [], 'text': '检验者', 'weight': 1, 'w': 1400},
        {'border': [], 'text': ' ', 'weight': 1, 'w': 1800, 'img': r_panel.picture(2.56, rId='yujianxian')},

    ]
    trs = write_tr_panel(items)
    paras += table.write(trs, tblBorders=[])
    run_stamp = r_panel.text('本报告签字盖章后生效', 10)
    run_stamp += r_panel.picture(3.97, rId='stamp', posOffset=[1, -1], wrap='undertext')
    paras += p.write(para_setting(spacing=[2, 0]), run_stamp)
    return paras


def write_cover(data):
    data = data or {}
    paras = ''
    paras += p.write(r_panel.picture(19.72, 28.69, rId='cover', relativeFrom=['page', 'page'], wrap='undertext', posOffset=[0,1]))

    paras += write_cover_line('姓    名', text=data.get('patient_name') or '', before=28)
    paras += write_cover_line('报告编号', text=data.get('case_no') or '')
    paras += write_cover_line('送检单位', text=data.get('contacts') or '')
    paras += write_cover_line('报告日期', text=data.get('contacts') or '')
    # paras += p.write(para_setting(spacing=[20, 0], ind=[18, 0]), r_tcm.text('姓名： %s' % data.get('health_record').get('name'), 12))
    # paras += p.write(para_setting(ind=[18, 0]), r_tcm.text('编号： %s' % data.get('sample_id'), 12))
    return paras


def write_oration(sample_detail):
    paras = ''
    first_name = get_first_name(sample_detail)
    paras += p.write(para_setting(line=12, rule='auto', jc='center', spacing=[0, 1]), r_panel.text('致您的一封信', 16, 1, color=green))
    p_set = para_setting(line=20, rule='exact', ind=['firstLine', 2])
    paras += p.write(para_setting(line=20, rule='exact'), r_panel.text('尊敬的%s：' % first_name, normal_size, 1))
    texts = '''
    您好！

    感谢您对青岛菩提慧生医学检验有限公司的信任！菩提检验旨在针对肿瘤治疗提供综合性的诊疗评估报告。我们通过更全面、更权威及更前沿的分子诊断技术对您的送检样本进行检测，为您的肿瘤精准治疗保驾护航！
    
    我们本着科学严谨，认真负责的态度，依据美国国立综合癌症网络(NCCN)临床指南、国内外专家共识、国际癌症临床会议等循证医学证据为您筛选敏感性较高、毒副作用较低的个性化药物治疗方案，帮助医生实现精准治疗，并最大化提升您的治疗获益。
    
    此次检测具体内容由您的主治医生根据您的病情和检测意愿进行选择，并在青岛菩提慧生医学检验有限公司的中心实验室进行，与您个人身份有关的资料我们将妥善保管，并且保证不会泄露给第三方机构。此次检测本质上属于研究性检测，具体检测内容可更好地为您及您的主治医生从核酸水平上提供参考，而不具有直接诊断和治疗的目的，具体疾病干预措施以临床医生意见为准。
    
    随着科学与医学的不断发展，癌症治疗的不断突破，我们有充足的理由相信癌症不再是无法攻克的难题。菩提检验全体将竭诚为您服务，与您携手抗击病魔。
    '''
    for t in texts.split('\n'):
        paras += p.write(p_set, r_panel.text(t, normal_size))
    paras += p.write(p.set(spacing=[4, 0]), r_panel.text('智慧成就健康', normal_size))
    return paras


def write_introduce():
    paras = ''
    paras += write_title('【青岛菩提慧生医学检验有限公司】')
    p_set = para_setting(line=12, rule='auto', ind=['firstLine', 2])
    texts = '''青岛菩提慧生医学检验有限公司是由菩提医疗集团投资建设的独立医学检验实验室，是以肿瘤为特色的智能检验与研发中心。菩提检验按照ISO 15189、CAP、CLIA国际规范标准设计建设，致力于肿瘤、遗传病、感染性疾病、慢病、药物基因组学等的精准智能检测，提供溯源数据、病原学、分项、综合、动态相结合的五级临床检验诊断报告和科学研究服务支持，实现肿瘤等疾病个体化、规范化、精准检测、系统评价的全程管理，建设国际一流系统诊断、人才培养及技术创新平台。
    青岛菩提慧生医学检验有限公司致力于成为中国转化医学的领导者，为个性化医疗保健提供创新的解决方案，改善人民生活。'''
    for t in texts.split('\n'):
        paras += p.write(p_set, r_panel.text(t, normal_size))

    paras += write_title('【BODHI-QUEEN】')
    paras += p.write(p_set, r_panel.text('全面指导肿瘤靶向、免疫治疗及疗效评估特色组合。给患者带来新的希望！', normal_size))

    p_set2 = para_setting(line=12, rule='auto')
    texts2 = [
        {'title': 'Pancancerplex（579大panel）', 'text': '，全面、准确、深度覆盖肿瘤靶向免疫治疗相关基因。即使取不到组织的患者，也可以通过外周血检测ctDNA。'},
        {'title': 'Watson for Genomics', 'text': '，是借助人工智能技术对受检者肿瘤样本高通量测序数据提供针对基因变异检测的数据快速解读服务（包括变异的分类，判断与基因变异相关的治疗手段及药物临床试验信息）。可以更快速、精确、高效地对肿瘤基因突变进行解读，帮助临床精准选择药物，避免遗漏。'},
        {'t_color': green, 'title': '新生抗原预测', 'text': '，能够更好地预测免疫治疗的疗效。我们采用新生抗原预测技术，可预测出高质量的肿瘤新生抗原序列，同时可以为肿瘤疫苗或细胞治疗提供最精确的抗原。'},
        {'t_color': green, 'title': '肿瘤免疫微环境分析', 'text': '，对肿瘤细胞PD-L1表达水平和CD8+巨噬细胞评估。可以更精确的判断治疗药物的有限性。'},
        {'t_color': green, 'title': '血清中IL-8含量监控', 'text': '，用于评估体液免疫应答水平，预测免疫治疗有效性。'}
    ]
    for t2 in texts2:
        run = r_panel.text(t2.get('title'), normal_size, weight=1, color=t2.get('t_color') or 'auto')
        run += r_panel.text(t2.get('text'))
        paras += p.write(p_set2, run)
    return paras


def write_catalog(catalogue):
    # 目   录
    para = p.write(p.set(jc='center', outline=3, line=12, rule='auto'), r_panel.text("目  录", size='小一', weight=1))
    for cat in catalogue:
        para = write_cat(cat, para, spacing=[0, 0.1], pos=9600)
    para += p.write(r_panel.fldChar('end'))
    para += p.write(p.set(sect_pr=sect_pr_catalog))
    return para


def write_patient_info(report_detail, cat):
    paras = ''

    paras += h1_panel(cat.get('title'), cat.get('bm'))
    trs = ''
    w = 3200
    w1 = [w] * 3
    items = [
        {'ws': w1, 'text': [
            '姓  名： %s' % report_detail.get('patient_name') or none_text,
            '性  别： %s' % sex2str(report_detail.get('sex')),
            '年  龄： %s' % report_detail.get('age') or none_text
        ]},
        {'ws': w1, 'text': [
            '联系人：%s' % report_detail.get('contacts') or none_text,
            '联系方式：%s' % report_detail.get('contacts_tel'),
            '检测项目：%s' % report_detail.get('detection_item') or none_text
        ]},
        {'ws': w1, 'text': [
            '送检单位：%s' % report_detail.get('contacts') or none_text,
            '取样来源：%s' % report_detail.get('contacts_tel'),
            ''
        ]},
        {'ws': w1, 'text': [
            '样本编号：%s' % report_detail.get('sample_id') or none_text,
            '样本类型：%s' % report_detail.get('sample_type') or none_text,
            '样本数量：%s' % report_detail.get('sample_count') or none_text
        ]},
        {'ws': w1, 'text': [
            '癌症类型：%s' % report_detail.get('diagnosis_type') or none_text,
            '病理诊断：%s' % report_detail.get('diagnosis') or none_text,
            'TNM分期：%s' % report_detail.get('TNM') or none_text
        ]},
        {'ws': w1, 'text': [
            '治疗史：%s' % report_detail.get('diagnosis_history') or none_text, '', ''
        ]},
        {'ws': w1, 'text': [
            '送检日期：%s' % report_detail.get('detection_date') or none_text,
            '报告日期：%s' % report_detail.get('detection_finished') or none_text,
            ''
        ]}
    ]
    for item in items:
        item['jc'] = 'left'
        item['fill'] = green_bg
        trs += write_gray_tr(item)
    paras += table.write(trs, w1, tblBorders=['top', 'bottom'])
    return paras


def write_abstract(data, cats):
    stars = data.get('stars')
    paras = ''
    cat0 = cats[0]
    paras += h1_panel(cat0.get('title'), cat0.get('bm'))
    huoyi = []
    naiyaos = []
    for tip_item in stars:
        for k in ['gene', 'amino_acid_change']:
            tip_item[k] = tip_item.get(k) or '（？？？）'
        known_db = tip_item.get('known_db') or []
        drug = []
        naiyao = []
        mingan = []
        for known_item in known_db:
            drugs = known_item.get('drugs')
            if drugs not in drug:
                drug.append(drugs)
            evidence_direction = known_item.get('evidence_direction') or ''
            evidence_direction = evidence_direction.strip().capitalize()
            if evidence_direction.endswith('(support)') or evidence_direction.endswith('(supoort)'):
                if evidence_direction.startswith('Resistant'):
                    mingan.append(known_item)
                if evidence_direction.startswith('Responsive'):
                    naiyao.append(known_item)
        tip_item['naiyao'] = naiyao
        tip_item['mingan'] = mingan
        if len(naiyao) >0:
            naiyaos.append(tip_item)
        if len(mingan) > 0:
            huoyi.append(tip_item)
        # for k in drug.keys():
        #     print k,
        tip_item['drug'] = '、'.join(drug)
        tip = u'{gene}的{amino_acid_change}突变是对{drug}治疗的强预测指标'.format(**tip_item)
        paras += p.write(r_panel.text(tip, normal_size))
    data['stars'] = stars
    data['huoyi'] = huoyi
    data['naiyao'] = naiyaos
    paras += write_abstract1(data, cats[1]) + p_sect_normal
    paras += write_abstract2(data, cats[2]) + p_sect_normal
    paras += write_abstract3(stars, cats[3]) + p_sect_normal
    paras += write_abstract4(data.get('chems'), cats[4]) + p_sect_normal
    paras += write_abstract5(cats[5]) + p_sect_normal
    return paras, huoyi, naiyaos


def write_result(data, gene_info, cats):
    paras = ''
    cat0 = cats[0]
    paras += h1_panel(cat0.get('title'), cat0.get('bm'))
    paras += write_result1(data, cats[1]) + p_sect_normal
    paras += write_result2(data, cats[2]) + p_sect_normal
    paras += write_result3(data, cats[3]) + p_sect_normal
    paras += data.get('para_geno') + p_sect_normal
    return paras


def write_affix(report_data, gene_info, cats):
    paras = ''
    cat0 = cats[0]
    paras += h1_panel(cat0.get('title'), cat0.get('bm'))
    genes1 = '''ABL1	AKT1	AKT2	APC	AR	ARAF	ATM	BCL2L11
    CDK4	CDK6	CDKN2A	CDKN2B	CHEK2	CTNNB1	DDR2	ERBB2
    FGFR2	FGFR4	FLT3	GNA11	GNAQ	IDH1	IDH2	IGF1R
    MCL1	MET	MLH1	MSH6	MTOR	MYCN	MYD88	NF1
    PTCH1	PTEN	RB1	SMARCA4	SMARCB1	SMO	SOX2	STK11
    BRCA2	CBL	CCND1	CCND2	CCND3	CCNE1	TSC1	TSC2
    ERBB4	ERCC1	ESR1	FANCA	FANCC	FBXW7	ALK	BRAF
    KDR	KIT	KRAS	LRP1B	MAP2K1	MAP2K2	FGFR1	FGFR3
    NRAS	PIK3CA	PIK3R1	PMS1	PMS2	POLE	NTRK1	PDGFRA
    ROS1	BRCA1	ERBB3	JAK2	NF2	TP53	VHL	EGFR
    MSH2	RET						'''
    genes2 = '''ALK	ATM	ATR	BRCA1	BRCA2	BRIP1	CD274	CHEK2
    EGFR	FANCA	JAK1	JAK2	KRAS	MDM2	PTEN	RAD50
    MDM4	MLH1	MSH2	MSH6	PALB2	PDCD1LG2	PMS2	POLD1
    B2M	HLA-A	HLA-B	CALR	ERAP1	ERAP2	TAP1	TAP2
    TAPBPL	TOP1	TPP2	DNMT3A	TP53	POLE	TAPBP	'''
    genes3 = '''ABCB1	CDA	CYP19A1	CYP2C8	CYP2D6	DPYD	DYNC2H1	ERCC1
    ERCC2	GSTP1	MTHFR	RRM1	SLCO1B1	TPMT	TYMS	UGT1A1
    XPC	XRCC1						'''
    genes4 = '''PTGS2	CD276	ERCC5	HIST1H3F	MAPKAP1	PIM1	SDHB	U2AF1
    EXO1	CD70	ERF	HIST1H3G	MAX	PLCG2	SDHC	UPF1
    HERC1	CD79A	ERG	HIST1H3H	MDC1	PLK2	SDHD	VEGFA
    HMGB1	CD79B	ERRFI1	HIST1H3I	MED12	PMAIP1	SESN1	VTCN1
    HMGN1	CDC42	ETV1	HIST1H3J	MEF2B	PNRC1	SESN2	WT1
    LIG1	CDC73	EZH1	HIST2H3C	MEN1	PPARG	SESN3	WWTR1
    LIG3	CDH1	EZH2	HIST2H3D	MGA	PPM1D	SETD2	XIAP
    MLH3	CDK12	TENT5C	HIST3H3	MITF	PPP2R1A	SF3B1	XPO1
    PCNA	CDK8	FANCG	HNF1A	MPL	PPP4R2	SH2B3	XRCC2
    POLB	CDKN1A	FANCL	HOXB13	MRE11	PPP6C	SH2D1A	YAP1
    TP73	CDKN1B	FAS	HRAS	MSH3	PRDM1	SHOC2	YES1
    COL5A1	CDKN2C	FAT1	HSD3B1	MSI1	PRDM14	SHQ1	ZFHX3
    DMD	CEBPA	FGF10	ICOSLG	MSI2	PREX2	SLX4	ZNF217
    PHF6	CENPA	FGF14	ID3	MST1	PRKAR1A	SMAD2	ZNF703
    ACVR1	CHEK1	FGF19	IFNGR1	MST1R	PRKCI	SMAD3	ETV6
    ACVR1B	CIC	FGF23	IGF1	MUTYH	PRKD1	SMAD4	EWSR1
    AGO2	CREBBP	FGF3	IGF2	MYC	PTP4A1	SMARCD1	KMT2A
    AKT3	CRKL	FGF4	IKBKE	MYCL	PTPN11	SMYD3	MYB
    ALOX12B	CRLF2	FGF6	IKZF1	MYOD1	PTPRD	SNCAIP	NTRK2
    AMER1	CSDE1	FH	IL10	NBN	PTPRS	SOCS1	RAF1
    ANKRD11	CSF1R	FLCN	IL7R	NCOA3	PTPRT	SOS1	RARA
    ARFRP1	CSF3R	FLT1	INHA	NCOR1	QKI	SOX17	ABCB9
    ARID1A	CTCF	FLT4	INHBA	NEGR1	RAB35	SOX9	ACE2
    ARID1B	CTLA4	FOXA1	INPP4A	NFE2L2	RAC1	SPEN	CANX
    ARID2	CTNNA1	FOXL2	INPP4B	NFKBIA	RAC2	SPOP	CTSB
    ARID5B	CUL3	FOXO1	INPPL1	NKX2-1	RAD21	SPRED1	CTSL
    ASXL1	CXCR4	FOXP1	INSR	NKX3-1	RAD51	SRC	CTSS
    ASXL2	CYLD	FUBP1	IRF2	NOTCH1	RAD51B	SRSF2	IDE
    ATRX	CYSLTR2	FYN	IRF4	NOTCH2	RAD51C	STAG2	IFI30
    AURKA	DAXX	GABRA6	IRS1	NOTCH3	RAD51D	STAT3	LGMN
    AURKB	DCUN1D1	GATA1	IRS2	NOTCH4	RAD52	STAT5A	LNPEP
    AXIN1	DICER1	GATA2	JAK3	NPM1	RAD54L	STAT5B	NPEPPS
    AXIN2	DIS3	GATA3	JUN	NSD1	RASA1	STK19	NRDC
    AXL	DNAJB1	GATA4	KDM5A	NTHL1	RBM10	STK40	PDIA3
    BABAM1	DNMT1	GATA6	KDM5C	NTRK3	RECQL	SUFU	TNF
    BAP1	DNMT3B	GID4	KDM6A	NUF2	RECQL4	SUZ12	VSIR
    BARD1	DOT1L	GLI1	KEAP1	NUP93	REL	SYK	CD200
    BBC3	DROSHA	GNA13	KEL	PAK1	COP1	TBX3	CD40
    BCL10	DUSP4	GNAS	KLF4	PARP1	RHEB	TCF3	CD40LG
    BCL2	E2F3	GPS2	KLHL6	PAX5	RHOA	TCF7L2	CD48
    BCL2L1	EED	GREM1	KMT2B	PBRM1	RICTOR	TEK	CD80
    BCL2L2	EGFL7	GRIN2A	KMT2C	PDCD1	RIT1	TERT	CD86
    BCL6	EIF1AX	GRM3	KMT2D	PDGFRB	RNF43	TET1	ITGAV
    BCOR	EIF4A2	GSK3B	KNSTRN	PDK1	RPS6KA4	TET2	ITGB3
    BCORL1	EIF4E	H3F3A	LATS1	PDPK1	RPS6KB2	TGFBR1	LGALS9
    BIRC3	ELF3	H3F3B	LATS2	PGR	RPTOR	TGFBR2	MICA
    BLM	EP300	H3F3C	LMO1	PHOX2B	RRAGC	TMEM127	MICB
    BMPR1A	EPAS1	HGF	LYN	PIK3C2B	RRAS	TMPRSS2	TNFRSF9
    BRD4	EPCAM	HIST1H1C	MALT1	PIK3C2G	RRAS2	TNFAIP3	TNFSF14
    BTG1	EPHA3	HIST1H2BD	MAP2K4	PIK3C3	RTEL1	TNFRSF14	TNFSF18
    BTK	EPHA5	HIST1H3A	MAP3K1	PIK3CB	RUNX1	TP53BP1	TNFSF4
    CARD11	EPHA7	HIST1H3B	MAP3K13	PIK3CD	RXRA	TP63	TNFSF9
    CARM1	EPHB1	HIST1H3C	MAP3K14	PIK3CG	RYBP	TRAF2	ABL2
    CASP8	ERCC3	HIST1H3D	MAPK1	PIK3R2	SDHA	TRAF7	EMSY
    CBFB	ERCC4	HIST1H3E	MAPK3	PIK3R3	SDHAF2	TSHR	CHD2
    CHD4	ABRAXAS1	CCNQ	FANCD2	FANCE	FANCF	FRS2	ADGRA2
    HSP90AA1	KAT6A	LZTR1	MAGI2	MRE11	PAK3	PAK5	PRKN
    PRKDC	PRSS8	RANBP2	RUNX1T1	KMT5A	SLIT2	SOX10	SPTA1
    STAT4	TAF1	ELOC	TOP2A	NSD2	NSD3	CCN6	XRCC5
    ZBTB2							'''
    paras += h2_panel(cats[1].get('title'), cats[1].get('bm'))
    paras += write_genes('靶向用药基因', genes1)
    paras += write_genes('免疫治疗检测基因', genes2)
    paras += write_genes('化疗用药检测基因', genes3) + p_sect_normal
    paras += write_genes('其他肿瘤相关基因', genes4) + p_sect_normal
    cat = cats[2]
    paras += h2_panel(cat.get('title'), cat.get('bm'))
    file_path = os.path.join(dir_name, 'panel_genes.txt')
    gene_no_path = os.path.join(dir_name, 'gene_no.json')
    rs_path = os.path.join(dir_name, 'rs.json')
    # gene_nos = my_file.read(gene_no_path)

    panel_genes = my_file.read(file_path).strip('\n').split('\n')
    gene_index = 0
    items2 = []
    items = []
    rs = []
    pic = []
    gene_nos = []

    for t_index, t in enumerate(panel_genes):
        t = t.strip().strip('\t').strip().strip('\r').strip('\n\r').strip('^M').strip('\xe2\x80\x83\n')
        if len(t) > 0:
            # items.append(t)
            # if t in genes1 + genes2 + genes3 + genes4:
            #     print t_index, t, 'gene'
            #     if gene_index > 0:
            #         paras += p_sect_normal
            #     paras += p.write(p.set(jc='center', spacing=[0, 0.5]), r_panel.text(t, '小四', 1))
            #     gene_index += 1
            if t == '参考文献':

                # i_gene = items[len(rs)]
                # item2 = {
                #     'gene': panel_genes[i_gene],
                #     'description': panel_genes[i_gene+1, t_index - 2],
                #     'tip': panel_genes[t_index-1],
                #     'reference': ''
                # }
                rs.append(t_index)
                # pic.append(t_index-1)
            if len(t) < 20 and '图' not in t and t != '参考文献':
    #             print t_index, t
    #             gene_index += 1
                gene_nos.append(t_index)
    #             paras += p.write(p.set(jc='center', spacing=[0, 0.5]), r_panel.text(t, '小四', 1))
    for i_gene_no, gene_no in enumerate(gene_nos):
        i_rs = rs[i_gene_no]
        i_tip = i_rs - 1
        if i_gene_no < len(gene_nos) -1:
            next_no = gene_nos[i_gene_no+1]
        else:
            next_no = len(gene_nos)

        if i_gene_no in [2]:
            i_tip = i_rs
        tip = panel_genes[i_tip]
        if i_tip == i_rs:
            tip = ''
        print i_gene_no, panel_genes[gene_no], panel_genes[i_rs], tip
        gene = panel_genes[gene_no]
        description = panel_genes[gene_no+1: i_tip]
        reference = panel_genes[i_rs+1: next_no]
        item2 = {
            'gene': gene,
            'description': description,
            'tip': tip,
            'reference': reference
        }
        items2.append(item2)
        paras += p.write(p.set(jc='center', spacing=[0, 0.5]), r_panel.text(gene, '小四', 1))
        for d in description:
            paras += p.write(p.set(line=19.2, rule='exact'), r_panel.text(d))
        paras += p.write(p.set(spacing=[0, 18]), r_panel.picture(cy=10, rId=gene.replace('-', '_').split('(')[0], align=['center', ''], posOffset=[0, 0.5]))
        paras += p.write(p.set(jc='center'), r_panel.text(tip, '小五'))
        paras += p.write(p.set(line=19.2, rule='exact', ind=['hanging', 1]), r_panel.text('参考文献', weight=1))
        for rr in reference:
            paras += p.write(p.set(line=18, rule='exact', ind=['hanging', 1]), r_panel.text(rr))
        paras += p_sect_normal
    print gene_index
    my_file.write(file_path[:-3] + 'json', items2)
    # my_file.write(gene_no_path, items)
    my_file.write(rs_path, rs)
    paras += p_sect_normal
    return paras


def write_shuoming(cat0):
    paras = ''
    paras += h1_panel(cat0.get('title'), cat0.get('bm'))
    text = '''1.	BODHI-QUEEN能为您提供：
    BODHI-QUEEN是菩提检验针对肿瘤精准治疗独立研发的，通过对肿瘤组织（血液）的靶向区域和转录组高深度测序数据综合分析，全面、精准地评估肿瘤治疗方式的多组学检测产品。
    
    2.	BODHI-QUEEN的适用人群包括：
    有靶向治疗、免疫治疗和化疗需求的癌症患者。
    
    3.	肿瘤突变负荷：
    肿瘤突变负荷（Tumor Mutation Burden, TMB）是指肿瘤组织每兆碱基中突变的总数。肿瘤突变负荷（TMB）越高，那么可能相应的肿瘤相关的致癌突变越多，每个肿瘤的个性就越突出，越不同于正常细胞。临床试验结果表明，免疫检验点抑制剂（如PD-1和PD-L1抗体）在治疗过程中只对部分患者有效。进一步的研究显示，肿瘤突变负荷可以用来评估免疫检验点抑制剂的治疗适用性，肿瘤突变负荷超过一定阈值的患者对免疫检验点抑制剂治疗会比较敏感。
    
    4.	肿瘤新生抗原：
    癌症细胞在基因变异的基础上产生的带有特异性氨基酸序列变异的蛋白被称为“新生抗原”（Neoantigen)。肿瘤新生抗原具有肿瘤特异性，能够被T细胞识别病引起免疫应答。一般而言，患者肿瘤组织中基因突变的总数越多（也就是TMB越高），那么他所携带的neoantigen也越多。越来越多的研究数据表明，肿瘤新生抗原是临床免疫治疗的关键因素，是免疫治疗中重要的生物标志物和靶点。'''
    for t in text.split('\n'):
        size = '五号'
        color = 'auto'
        if t.endswith('：'):
            size = 11
            color = green
        paras += p.write(para_setting(line=20, rule='exact'), r_panel.text(t, size, color=color))
    return paras


def write_reference(cat0):
    paras = ''
    paras += h1_panel(cat0.get('title'), cat0.get('bm'))
    title = '▎药品说明书及临床指南'
    text = '''1)	ado-trastuzumab emtansine_Revised:04/2016
    2)	afatinib_Revised:04/2016
    3)	alectinib_Revised:12/2015
    4)	cobimetinib_Revised: 11/2015
    5)	crizotinib_Revised:04/2016
    6)	dabrafenib_Revised:06/2016
    7)	dinutuximab_Revised:03/2015
    8)	erlotinib_Revised:06/2016
    9)	gefitinib_Revised:07/2015
    10)	ibrutinib_Revised:06/2016
    11)	imatinib_Revised:01/2015
    12)	lapatinib_Revised:02/2015
    13)	lumacaftor_Revised:05/2016
    14)	olaparib_Revised:12/2014
    15)	osimertinib_Revised:11/2015
    16)	pertuzumab_Revised:03/2016
    17)	rucaparib_Revised:12/2016
    18)	ruxolitinib_Revised:03/2016 
    19)	trametinib_Revised:11/2015
    20)	trastuzumab_Revised:03/2016
    21)	vemurafenib_Revised:06/2016
    22)	NCCN Guideline: Colon Cancer v.2.2018
    23)	NCCN Guideline: Esophageal and Esophagogastric Junction Cancers v.2.2018
    24)	NCCN Guideline: Melanoma v.2.2018
    25)	NCCN Guideline: Non-Small Cell Lung Cancer (NSCLC) v.6.2018
    26)	NCCN Guideline: Soft Tissue Sarcoma v.1.2018
    27)	NCCN Guideline: Pancreatic Adenocarcinoma v.1.2018
    28)	NCCN Guideline: Gastric Cancer v.2.2018
    29)	NCCN Guideline: Rectal Cancer v.2.2018
    30)	NCCN Guideline: Breast Cancer v.1.2018'''
    title1 = '▎ 会议及临床共识意见'
    text1 = '''1)	AACR 2014 (abstr CT103)
    2)	Annals of Oncology (2016) 27 (6): 416-454. 10.1093/annonc/mdw383
    3)	ASCO 2015 (abstr e15516)
    4)	ASH meeting, Dec 2014, abstract #389
    5)	Cancer Res 2016;76(14 Suppl):Abstract nr 1249
    6)	Cancer Res October 1, 2014 74:CT326
    7)	DOI: 10.1200/JCO.2017.35.18_suppl.LBA2501
    8)	DOI: http://dx.doi.org/10.1016/S1556-0864(16)30324-0
    9)	DOI:10.1158/1538-7445.AM2013-LB-64
    10)	DOI:10.1158/1538-7445.AM2016-CT007
    11)	ENA 2014 (abstr 373)
    12)	ESMO 2015 (abstract 302)
    13)	J Clin Oncol 29: 2011 (suppl; abstr 8061)
    14)	J Clin Oncol 32:5s, 2014 (suppl; abstr 8031)
    15)	J Clin Oncol 32:5s, 2014 (suppl; abstr 8077)
    16)	J Clin Oncol 33, 2015 (suppl; abstr 2540)
    17)	J Clin Oncol 33, 2015 (suppl; abstr 2545)
    18)	J Clin Oncol 33, 2015 (suppl; abstr 7003)
    19)	J Clin Oncol 33, 2015 (suppl; abstr 8015)
    20)	J Clin Oncol 33, 2015 (suppl; abstr TPS5608)
    21)	J Clin Oncol 34, 2016 (suppl; abstr 4517)
    22)	J Clin Oncol 34, 2016 (suppl; abstr 9009)
    23)	JCO, Vol 33, No 15_suppl (May 20 Supplement), 2015: 2540
    24)	guideline:CSCO 胃肠间质瘤专家委员会.临床肿瘤学杂志.2013,18(11)
    25)	中国埃克替尼治疗非小细胞肺癌专家共识（2016 年版）
    26)	CSCO 黑色素瘤专家委员会，人民卫生出版社 2017 版'''
    p_set = para_setting(line=12*1.1, rule='auto', spacing=[0, 1.5])
    p_set1 = para_setting(line=12*1.09, rule='auto', spacing=[0, 0.15])
    paras += p.write(p_set, r_panel.text(title, normal_size))
    for t in text.split('\n'):
        paras += p.write(p_set1, r_panel.text(t, normal_size))
    paras += p_sect_normal
    paras += p.write(p_set, r_panel.text(title1, normal_size))
    for t1 in text1.split('\n'):
        paras += p.write(p_set1, r_panel.text(t1, normal_size))
    return paras


def write_produce(cat0):
    paras = ''
    paras += h1_panel(cat0.get('title'), cat0.get('bm'))
    text = '''	报告阅读
    本报告主要检测肿瘤治疗相关基因的变异情况。报告给出的变异信息（和无变异信息）可为临床医生对受检者的治疗提供参考，受检者请在临床医生的指导下阅读本报告。
    
    	基因变异和药物说明
    一个生物标志物变异的发现并不意味着必定会对某一药物或疗法有效，同样没有检测到生物标志物也不代表一定会对任何药物或疗法都无效。本报告中任何一个标志变异和潜在有效或无效药物均不按照先后顺序排名。潜在临床受益或无效药物的证据来源或等级不做评估。
    
    	治疗方案由医生决策
    本报告提及到的药物可能对某一特定患者并不适应。任何一个或所有潜在有效药物的选取或无效药物的弃选都由医生慎重决定。临床医生在给出推荐治疗方案时，需要综合考虑本检测报告细信息和患者其他相关信息。
    
    	次生危害不予赔偿
    在检测过程中及知晓检测结果后，因自身心理或生理因素可能引起受检者出现不同程度的精神压力和负担，由此产生的次生危害，检测机构不承担任何责任。
    
    	信息保密
    菩提检验将妥善保存与受检者个人身份有关的资料，并且保证不会泄露给第三方机构。
    
    患者的治疗决策必须基于医生的医学判断，并遵照医院给出的护理标准。医生的决策不能仅依赖于某一单个监测，如此次检测和本报告中给出的信息。本报告不是临床诊断报告，不具备医嘱性质，供医生参考治疗方案由医生决策
    '''
    for t in text.split('\n'):
        size = 10
        color = 'auto'
        weight = 0
        wingdings = False
        t = t.strip()
        if t.startswith(''):
            size = 11
            color = green
            weight = 1
            wingdings = True
        paras += p.write(para_setting(line=20, rule='exact'), r_panel.text(t, size, weight=weight, color=color, wingdings=wingdings))
    return paras


def write_body(data):
    para = ''
    for key in data['para_keys']:
        para += data[key]
    return '<w:body>%s</w:body>' % para


def sort_panel_data(data):
    # img_info_path = data['img_info']
    # r_tcm.img_info_path = img_info_path
    pkgs = ''
    rels = ''
    chapters = ''
    sample_detail = data.get('sample_detail') or {}
    report_data = data.get('variant_list') or []
    gene_info = data.get('gene_info') or []
    imgs, files = [], []

    catelogs = get_catalog()
    # , huoyi, naiyaos
    para_geno, chems = write_result4(data.get('rs_geno'), catelogs[11])
    data['chems'] = chems
    para_abstract, huoyi, naiyaos = write_abstract(data, catelogs[1: 7])
    data['huoyi'] = huoyi
    data['naiyao'] = naiyaos
    data['para_geno'] = para_geno
    para_result = write_result(data, gene_info, catelogs[7: 12])
    return {
        'other_page': (pkgs, rels),
        'cover': write_cover(sample_detail) + p_sect_normal,
        'oration': write_oration(sample_detail) + p_sect_normal,
        'introduce': write_introduce() + p_sect_normal,
        'catalog': write_catalog(catelogs),
        'chapters': chapters,
        'common': write_patient_info(sample_detail, catelogs[0]) + p_sect_normal,
        'abstract': para_abstract,
        'result': para_result,
        'affix': write_affix(report_data, gene_info, catelogs[12: 15]),
        'shuoming': write_shuoming(catelogs[15]) + p_sect_normal,
        'reference': write_reference(catelogs[16]) + p_sect_normal,
        'produce': write_produce(catelogs[17]) + p_sect_normal,
        'files': files,
        'imgs': imgs,
        'para_keys': [
            'cover',
            'oration',
            'introduce',
            'catalog',
            'common',
            'abstract',
            'result',
            'affix',
            'shuoming',
            'reference',
            'produce',
        ]
    }


def down_common(data, sort_func):
    # my_file.write(file_name.split('.')[0] + '.json', data)

    img_dir = os.path.join(dir_name, 'panel_demo', 'word', 'media')
    img_info_path = os.path.join(dir_name, 'img_info_%s.json' % 'panel')
    gene_info_path = os.path.join(dir_name, 'OncoKB_gene_info.json')

    patient_detail = data.get('sample_detail')
    patient_name = None
    if patient_detail:
        patient_name = patient_detail.get('patient_name')
    item_name = data.get('item_name')
    report_time = format_time(frm='%Y%m%d%H%M%S')
    action_name = u'%s_%s_检测报告' % (patient_detail.get('sample_id'), patient_name)
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
    if item_name == 'aiyi':
        from views.tumor.report_aiyi import get_report_core
        pkg = get_report_core(data)
    else:
    # if env.startswith('Development'):
        if os.path.exists(img_info_path):
            os.remove(img_info_path)
        imgs = get_imgs(img_dir)
        my_file.write(img_info_path, imgs)
        r_panel.img_info_path = img_info_path
        data['img_info'] = imgs
        data['pic'] = r_panel
        data['gene_info'] = my_file.read(gene_info_path) or []
        report_data = sort_func(data)
        body = write_body(report_data)
        imgs = report_data.get('imgs') or imgs
        imgs2 = []
        for img in imgs:
            if img not in imgs2:
                imgs2.append(img)
        pkg = write_pkg_parts(imgs2, body, other=report_data.get('other_page'))
    status = False
    while status != 5:
        status = my_file.download(pkg, file_name)
    print file_name
    return file_name


def down_panel(data):
    return down_common(data, sort_panel_data)


if __name__ == "__main__":
    # generate_word(get_dignosis() or [])
    # down_common({}, sort_panel_data)
    down_panel({})
    # print __file__
    pass
    

