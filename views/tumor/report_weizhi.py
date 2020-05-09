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
from jy_word.Word import write_pkg_parts
from jy_word.web_tool import sex2str
from config import static_dir

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
weizhi_dir = os.path.join(static_dir, 'weizhi')
base_dir = os.path.join(aiyi_dir, 'base_data')
img_dir = os.path.join(aiyi_dir, 'images')
my_file = File()
base_file = File(base_dir)
gene_list12 = base_file.read('1.2gene_list.json')
gene_list53 = base_file.read('5.3gene_list.xlsx', sheet_name='Sheet2')
signature_cn = base_file.read('signature_cn.txt')
img_info_path = os.path.join(img_dir, 'img_info.json')

r_aiyi = Run(img_info_path)
r_heiti = Run(family='黑体')
r_kaiti = Run(family='楷体')
r_yahei = Run(family='微软雅黑')
hyperlink = HyperLink()
p = Paragraph()
set_page = Set_page().set_page
table = Table()
tr = Tr()
tc = Tc()
sdt = SDT()
page_margin = [3.5, 1.5, 2.54, 1.5, 1.5, 1.75]
page_margin4 = [4, 1.5, 2.54, 1.5, 1.5, 1.75]
p_set_tr = p.set(line=12, spacing=[0.2, 0.2])
p_set_tr_center = p.set(line=12, spacing=[0.2, 0.2], jc='center')
sect_pr_catalog = set_page('A4', footer='rIdFooter1')
# sect_pr_catalog = set_page('A4', footer='rIdFooter1', header='rIdHeader1')
sect_pr_cover = set_page('A4', header='rIdHeadercover', footer='rIdCover')
sect_pr_overview = set_page('A4', header='rIdHeader2', footer='rIdReport_time')
sect_pr_catalog1 = set_page('A4', header='rIdHeader2', footer='rIdFooter1')
sect_pr_content = set_page('A4', footer='rIdFooter1', pgNumType_s=1, header='rIdHeader2')
con1 = p.write(p.set(rule='exact', line=12, sect_pr=set_page(type='continuous', cols=1)))
con2 = p.write(p.set(rule='exact', line=12, sect_pr=set_page(type='continuous', cols=2, space=40)))
page_br = p.write(set_page(page_margin=page_margin))
sect_pr1 = set_page('A4', page_margin=page_margin, footer='rIdFooter2', header='rIdHeader2', type='continuous', cols=1)
# sect_pr2 = set_page('A4', page_margin=page_margin, footer='rIdReport_time', header='rIdHeader2', pgNumType_s=1)

outline1 = {'wingdings': False, 'spacing': [0, 0.5], 'size': 12, 'outline': 2, 'rule': 'auto', 'line': 12, 'weight': 1}
outline2 = {'wingdings': True, 'spacing': [1, 0.5], 'size': 11, 'outline': 2, 'rule': 'auto', 'line': 12}
outline21 = {'wingdings': False, 'spacing': [1, 0.5], 'size': 11, 'outline': 2, 'rule': 'auto', 'line': 12}
outline3 = {'wingdings': True, 'spacing': [0.5, 0.2], 'ind': ['hanging', 0.5], 'size': 10.5, 'outline': 3, 'rule': 'auto', 'line': 12}
outline4 = {'spacing': [0.5, 0], 'ind': ['hanging', 0.5], 'size': 10, 'outline': 4, 'rule': 'auto', 'line': 12}
outline5 = {'wingdings': True, 'spacing': [0.5, 0], 'ind': ['hanging', 0.5], 'size': '小五', 'outline': 5, 'rule': 'auto', 'line': 12, 'weight': 0}

w_sum = 18 * 567

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
blue_d = '71BAE3'

green = '3EAE95'
green_lighter = 'B6E8DB'
cnv_genes = [
    'MEF2B', 'FGF4', 'KEAP1', 'ESR1', 'MAPK1', 'TSC2', 'MGA', 'AGO2', 'PIK3R2', 'CCND1', 'GLI1', 'CDKN1B', 'MLH1', 'BCL6', 'MSH2', 'MSH6', 'TNFAIP3', 'DUSP4', 'CXCR4', 'FLT3',
    'CDKN1A', 'SOX9', 'SMO', 'FOXA1', 'RAF1', 'LATS1', 'BTG1', 'KRAS', 'VHL', 'PDGFRA', 'APC', 'HNF1A', 'CDK4', 'BRIP1', 'FGFR3', 'BARD1', 'CCND2', 'CDH1', 'PDGFRB', 'SMAD2',
    'RHEB', 'KMT2C', 'AXIN1', 'CREBBP', 'CCNE1', 'CDKN2C', 'INPP4B', 'SMARCB1', 'EP300', 'EED', 'BRD4', 'AKT3', 'KDR', 'PIK3CA', 'CTCF', 'CBL', 'DNMT3A', 'MSH3', 'RAD50', 'CDK6',
    'PMS2', 'ERBB3', 'RB1', 'TP53', 'ERBB2', 'PIK3R1', 'RASA1', 'EGFR', 'CDKN2B', 'NOTCH1', 'ATM', 'MYCN', 'FBXW7', 'FLT1', 'YAP1', 'KIT', 'BRAF', 'PIK3CB', 'FGFR4', 'FGF19',
    'NPM1', 'SOX17', 'RAD21', 'TSC1', 'RUNX1', 'ANKRD11', 'KMT2D', 'AXL', 'CDKN2A', 'PPM1D', 'MAP2K1', 'BCL2L1', 'TERT', 'HRAS', 'ERCC4', 'AURKA', 'WHSC1L1', 'EZH2', 'CIITA', 'ARID1A',
    'SHQ1', 'STK11', 'SMAD3', 'DNMT3B', 'RBM10', 'IKZF1', 'FGF3', 'ARID2', 'EPHA3', 'MEN1', 'NF2', 'SMAD4', 'DICER1', 'SMARCA4', 'ARID1B', 'GATA3', 'AKT1', 'PTPN11', 'MITF', 'NKX2-1',
    'RAC1', 'PAK1', 'PTPRD', 'BCL11B', 'RICTOR', 'BRCA1', 'PAX5', 'SRC', 'NF1', 'CASP8', 'FGFR2', 'MAX', 'TGFBR2', 'XRCC2', 'FH', 'PARP1', 'IKBKE', 'MDM4', 'CDC73', 'RFWD2',
    'DDR2', 'ROS1', 'MCL1', 'PRDM1', 'CD58', 'NRAS', 'BCL10', 'JUN', 'PTEN', 'CCND3', 'ATRX', 'TET1', 'MED12', 'DAXX', 'AR', 'TGFBR1', 'SDHB', 'SDHD', 'ASXL1', 'ERRFI1',
    'KDM6A', 'MYC', 'BCOR', 'TET2', 'BRCA2', 'MTAP', 'CDK8', 'CD274', 'JAK2', 'TP53BP1', 'LATS2', 'ALK', 'FANCA', 'ERCC2', 'AKT2', 'BCL2L11', 'PBRM1', 'CARD11', 'PDCD1LG2', 'MET',
    'KDM5A', 'ETV1', 'SETD2', 'RHOA', 'FGFR1', 'RELN', 'ASXL2', 'FAT1', 'CDK12', 'BBC3', 'BAP1', 'MDM2', 'RAD51B', 'VEGFA', 'NTRK1', 'KMT2A', 'B2M', 'CIC', 'FOXP1', 'REL',
    'NCOA3', 'TTF1', 'GSTP1', 'BIRC7', 'RSF1', 'TOP1', 'TYMS', 'ABCC3', 'ASNS', 'LRP1B', 'NTRK3', 'TLK2',
]
level_tips_wz = [
    {'text': 'A', 'tip': 'FDA/NCCN推荐药物', 'color': '#007CC8', 'x': 1.4},
    {'text': 'B', 'tip': '专家共识药物', 'color': '#5ABADA', 'x': 4.2},
    {'text': 'C', 'tip': '临床证据药物', 'color': '#95D8EB', 'x': 6.15},
    {'text': 'D', 'tip': '临床前证据药物', 'color': '#BFE8F3', 'x': 8.15}
]


def get_report_core(data):
    sample_detail = data.get('sample_detail') or {}
    overview = data.get('overview') or {}
    other_pic = []
    for pic_k in ['signature_pic', 'tmb_pic']:
        pic_path = overview.get(pic_k)
        if pic_path and os.path.exists(pic_path):
            pic_info = get_img_info(pic_path)
            other_pic.append(pic_info)
    img_info = get_imgs_weizhi(img_dir, is_refresh=True, others=other_pic)
    body = write_body(title_cn, title_en, data)
    body = body.replace('免疫检查点抗体', '免疫检查点抑制剂')
    pages = write_pages(data.get('report_time'), sample_detail.get('sample_id'))
    pkgs1 = write_pkg_parts(img_info, body, other=pages)
    return pkgs1


def write_body(title_cn, title_en, data):
    diagnose = data.get('diagnosis')
    variant_list = data.get('variant_list')
    report_detail = data.get('report_detail')
    overview = data.get('overview')
    stars0 = data.get('stars0')
    stars = data.get('stars')

    sample_detail = data.get('sample_detail')
    sequencing_type = sample_detail.get('sequencing_type') or ''
    #关于hrd
    hrd_hisens_loh = overview.get('hrd_hisens_loh') or 0
    hrd_hisens_tai = overview.get('hrd_hisens_tai') or 0
    hrd_hisens_lst = overview.get('hrd_hisens_lst') or 0
    hrd = hrd_hisens_loh + hrd_hisens_lst + hrd_hisens_tai
    paras_hr, items_hr = write_hrd(sequencing_type, data, [0.5, 0])
    # print len(variant_list), report_detail.keys()
    #  KRAS、NRAS野生型,  都没有发生突变的话，A级推荐西妥昔单抗和帕尼单抗
    yesheng = []
    if diagnose in ['结直肠癌']:
        for gene in ['KRAS', 'NRAS']:
            arr = filter(lambda x: x.get('gene') == gene, variant_list)
            if len(arr) == 0 and gene not in yesheng:
                yesheng.append(gene)
    # yesheng = ['KRAS', 'NRAS']
    data['yesheng'] = yesheng
    if 'panel' in sequencing_type.lower():
        action1 = ''
        if len(items_hr) > 0:
            col2 = '致病突变'
            hrd_index = 0
            title = 'HR通路相关基因发现明确致病突变'
            action1 = title
        else:
            col2 = '未发现致病突变'
            hrd_index = len(stars)
            title = 'HR通路相关基因未发现明确致病突变'
        if hrd_index >= 0:
            data['paras_hr'] = paras_hr
            stars0.insert(hrd_index, {'col1': 'HR通路相关基因', 'col2': col2, 'hr': title, 'action1': action1})
    else:
        # if hrd > 42:
        col1 = 'HRD评分'
        col2 = ''
        hrd_score = 'LOH=%s、TAI=%s、LST=%s' % (hrd_hisens_loh, hrd_hisens_tai, hrd_hisens_lst)
        action1 = ''
        if hrd > 42:
            col2 = '高（%s, > 42, %s）' % (hrd, hrd_score)
            hrd_index = 0
            action1 = 'HRD高'
        elif diagnose in ['卵巢癌', '乳腺癌', '前列腺癌']:
            col2 = '低（%s, < 42, %s）' % (hrd, hrd_score)
            hrd_index = len(stars)
            action1 = 'HRD低'
        else:
            hrd_index = -1
        if hrd_index >= 0:
            if diagnose not in ['卵巢癌', '乳腺癌', '前列腺癌']:
                hrd_index = len(stars)
            data['paras_hr'] = paras_hr
            data['hrd_tip'] = action1.replace('HRD', 'HRD评分')
            data['hrd_index'] = hrd_index
            stars0.insert(hrd_index, {'col1': col1, 'col2': col2, 'hrd': hrd, 'action1': action1})
    msi_info = data.get('msi_info')
    tmb_info = data.get('tmb_info')
    ploidy = overview.get('ploidy')
    try:
        ploidy = round(float(ploidy), 1)
    except:
        ploidy = ploidy
    data['ploidy'] = ploidy
    data['target_tips'] = stars0, False, []
    paras3, chem_drugs = write_chapter3(5, data.get('chemotherapy'))
    para_ddr, tip_ddr, tip_ddr1, level_ddr = write_chapter_ddr(stars if diagnose == '泌尿上皮癌' else variant_list, diagnose)
    para_mingan, tip_mingan, tip_mingan1, level_mingan = write_chapter_mingan(stars, diagnose, ploidy)
    para_naiyao, tip_naiyao, tip_naiyao1, level_naiyao = write_chapter_naiyao(data, ploidy)
    para_chaojinzhan, tip_chaojinzhan, tip_chaojinzhan1, level_chaojinzhan = write_chapter_chaojinzhan(data, ploidy)
    para_hla, tip_hla, tip_hla1, level_hla = write_chapter_hla(overview, diagnose)

    para_signature, tip_signature, level_signature = write_chapter_signature(overview.get('signature_30') or [])
    para_yichuan, tip_yichuan, tip_yichuan1, level_yichuan = write_chapter_yichuan()
    data['immun_tip'] = [
        msi_info,
        tmb_info,
        {'index': 'DDR', 'tip1': tip_ddr1, 'text': tip_ddr, 'level': level_ddr, 'w': (w_sum-300) / 2},
        {'index': '免疫敏感驱动基因', 'tip1': tip_mingan1, 'text': tip_mingan, 'level': level_mingan, 'w': (w_sum-300) / 2},
        {'index': '免疫耐药驱动基因', 'tip1': tip_naiyao1, 'text': tip_naiyao, 'level': level_naiyao, 'w': (w_sum-300) / 2},
        {'index': '免疫超进展', 'tip1': tip_chaojinzhan1, 'text': tip_chaojinzhan, 'level': level_chaojinzhan, 'w': (w_sum-300) / 2},
        {'index': 'HLA分型', 'tip1': tip_hla1, 'text': tip_hla, 'level': level_hla, 'w': w_sum}
    ]
    data['chem_tip'] =  '可能有效且毒副作用低的药物：%s' % ('无' if len(chem_drugs) == 0 else ', '.join(chem_drugs))
    data['yichuan'] = {
        'text': tip_yichuan, 'level': level_yichuan, 'title': '肿瘤遗传性检测结果', 'line': 0
    }

    data['para_ddr'] = para_ddr
    data['para_mingan'] = para_mingan
    data['para_naiyao'] = para_naiyao
    data['para_chaojinzhan'] = para_chaojinzhan
    data['para_hla'] = para_hla
    data['para_signature'] = para_signature
    data['para_yichuan'] = para_yichuan
    body = ''
    body += write_cover(data)
    body += write_chapter0(title_cn, data)
    body += write_catalog()
    body += write_chapter1(data)
    body += write_chapter2(4, data)
    body += paras3
    body += write_chapter4(6, data)
    body += write_chapter5(7, data)
    body += write_chapter_affix(8, data)
    return body


def write_cover(data):
    para = ''
    sample_detail = data.get('sample_detail')
    report_time = data.get('report_time')
    para += p.write(
        r_aiyi.picture(20.5, rId='cover_weizhi',  wrap='undertext',
                       relativeFrom=['page', 'page'], align=['center', ''], posOffset=[0, 0.26])
    )
    # para += p.write(
    #     r_aiyi.picture(20.5, rId='cover_weizhi2',  wrap='undertext', relativeFrom=['page', 'page'], align=['center', ''])
    # )
    para += p.write(p.set(jc='center', spacing=[5, 0]),
                    r_aiyi.text('肿瘤个体化诊疗基因检测', '小初', weight=1, color=RGB_to_Hex('33,89,104')))
    para += p.write(p.set(jc='center', spacing=[0.5, 4]),
                    r_aiyi.text('Precision Oncology & Personalized Treatment', '小三', weight=1, color=RGB_to_Hex('75,172,198')))
    texts = [
        {'label': '项目名称', 'value': u'实体瘤680基因检测'},
        {'label': '患者姓名', 'key': 'patient_name'},
        {'label': '样本编号', 'key': 'sample_id'},
        {'label': '送检医院', 'key': 'inspection_department'},
        {'label': '收样日期'},
        {'label': '报告日期', 'value': report_time},
    ]
    size = '小四'
    trs = ''
    ws = [int(2.75*567), int(5.5 * 567)]
    for t_item in texts:
        label = t_item.get('label')
        key = t_item.get('key')
        value = t_item.get('value') or sample_detail.get(key) or ''
        # value = u'中文'

        tcs = ''
        p_set = {
            'size': size, 'weight': 1,
            'pPr': p.set(line=12, spacing=[0.9, 0], jc='center'),
            'color': '#595959'
        }

        n = 24
        len_cn = test_chinese(value)
        # value = value.encode('utf-8')
        kongge = n - len(value) - len_cn
        left = kongge/2
        right = kongge - left
        text2 = '%s%s%s' % (' ' * left, value, ' ' * right)
        # run += r_aiyi.text('%s%s%s' % (' ' * left, value, ' ' * right), size, 1, space=True, underline='single')
        #指定高度1厘米；单元格居中；第1列指定宽度2.75厘米，第2列指定宽度5.5厘米；，加粗，小四，颜色RGB89,89,89.
        # 第2列单元格均有下划线等齐
        item1 = {'text': '%s：' % label, 'w': ws[0], 'tcColor': white, 'tcBorders': []}
        item2 = {'text': value, 'w': ws[1], 'tcColor': RGB_to_Hex('89,89,89'), 'tcBorders': ['bottom'], 'lineSize': 12}
        item1.update(p_set)
        item2.update(p_set)
        tcs += write_tc_weizhi(item1)
        tcs += write_tc_weizhi(item2)
        trs += tr.write(tcs, tr.set(trHeight=567))
    para += table.write(trs, tblBorders=[])
    para += p.write(p.set(sect_pr=sect_pr_cover))
    return para


def write_catalog():
    # 目   录
    para = p.write(
        p.set(spacing=[0, 0], jc='center', outline=3, line=24, rule='auto'),
        r_aiyi.text("目录", size=18, color=white) +
        r_aiyi.picture(17.42, rId='content_weizhi', relativeFrom=['page', 'page'], align=['center', 'center'])
    )
    para += p.write(p.set(sect_pr=sect_pr_catalog1))
    return para


def write_chapter0(title_cn, data):
    para = ''
    sample_detail = data.get('sample_detail') or {}
    para += write_patient_info(data)
    para += write_target_tip(data) + p.write()
    para += write_immun_tip_weizhi(data.get('immun_tip'))
    chem_fill = '#95D8EB'
    if data['chem_tip'].endswith('无'):
        chem_fill = ''
    tip_items = [
        {'title': '化学治疗提示', 'text': data['chem_tip'], 'line': 15, 'tcFill': chem_fill},
        data['yichuan']
    ]
    for tip_item in tip_items:
        trs_tip0 = write_table_title(tip_item.get('title'))
        tip_item['tcBorders'] = ['bottom']
        tip_item['jc'] = 'center'
        trs_tip0 += write_tr_weizhi([tip_item])
        para += table_weizhi(trs_tip0, line=tip_item.get('line'))
    run = r_aiyi.text('附注： 以上靶向、免疫、化学和最新研究进展治疗提示部分与后面附录信息遵循', '小五')
    run += r_aiyi.text('A、B、C、D', '小五', weight=1)
    run += r_aiyi.text('四个证据等级以及对应', '小五')
    run += r_aiyi.text('颜色标识', '小五', weight=1)
    run += r_aiyi.text('。', '小五')
    para += p.write(p.set(spacing=[0.5, 0.5]), run)
    tcs_level = ''
    for level_item in level_tips_wz:
        text = level_item.get('text')
        tcs_level += write_tc_weizhi({'text': text, 'tcFill': level_item.get('color'), 'w': 450, 'tcBorders': [], 'jc': 'center'})
        tcs_level += write_tc_weizhi({'text': level_item.get('tip'), 'w': 2000 if text == 'A' else 1600, 'tcBorders': []})
    tcs_level += write_tc_weizhi({'text': '提示可能有效', 'weight': 1, 'w': 1600, 'tcBorders': []})
    tcs_level1 = ''
    tcs_level1 += write_tc_weizhi({'text': ' ', 'weight': 1, 'w': 450, 'tcBorders': ['top', 'bottom', 'left', 'right'], 'tcColor': gray})
    tcs_level1 += write_tc_weizhi({'text': '提示可能无效', 'weight': 1, 'w': 2000, 'tcBorders': []})
    tcs_level1 += write_tc_weizhi({'text': ' ', 'weight': 1, 'w': 450, 'tcBorders': [], 'tcFill': gray})
    tcs_level1 += write_tc_weizhi({'text': '提示可能耐药', 'weight': 1, 'w': 1600, 'tcBorders': []})
    tcs_level1 += write_tc_weizhi({'text': ' ', 'weight': 1, 'w': w_sum-4500, 'tcBorders': [], 'gridSpan': 5})
    para += table.write(tr.write(tcs_level) + tr.write(tcs_level1), tblBorders=[]) + p.write()
    technology = '本检测基于第二代测序技术，捕获680个与癌症发生发展的生物学原理及个性化治疗方案高度相关的基因的重要外显子及部分内含子区域，以及其他50个基因在实体肿瘤中高发突变的热点区域，进行高深度测序，测量这些基因中出现的来自组织或循环肿瘤DNA的突变、重排、拷贝数增加等变异事件，从而对靶向、免疫、化学或其他可能的治疗方式根据证据等级进行提示。'
    overview = data.get('overview') or {}
    purity = float2percent(overview.get('purity'), 0)
    tumor_mean_target_coverage = overview.get('tumor_mean_target_coverage')
    try:
        tumor_mean_target_coverage = float(tumor_mean_target_coverage)
        tumor_mean_target_coverage = round(tumor_mean_target_coverage, 1)
    except:
        tumor_mean_target_coverage

    tips = [
        {'title': '关于检测项目', 'text': technology + '\n相关局限性说明：由于肿瘤异质性等原因，本检测报告仅对本样本负责，患者诊疗决策需在临床医生指导下进行'}
    ]
    for tip_item in tips:
        trs_tip = write_table_title(tip_item.get('title'))
        texts = tip_item.get('text').split('\n')
        for text in texts:
            trs_tip += write_tr_weizhi([{'text': text, 'tcBorders': ['bottom'], 'pPr': p.set(spacing=[0.2, 0.2])}])
        para += table_weizhi(trs_tip) + p.write()
    trs_qc = write_table_title('样本和数据质控信息', 4)
    qcs = [
        {'weight': 1, 'items': ['质量参数', '数值', '质控标准', '质控结果']},
        {'weight': 0, 'items': ['DNA总量（ng）', ' ', '≥50', '合格']},
        {'weight': 0, 'items': ['预文库总量（ng）', ' ', '≥300', '合格']},
        {'weight': 0, 'items': ['平均测序深度（X）', tumor_mean_target_coverage, '≥500', '合格' if tumor_mean_target_coverage >= 500 else '不合格']},
        {'weight': 0, 'items': ['深度＞（0.1X目标测序深度）占比', ' ', '≥90%', '合格']},
    ]
    for qc in qcs:
        tcs_qc = ''
        for qc_index,t in enumerate(qc.get('items')):
            w_qc = 6.75 if qc_index == 0 else 3.75
            tcs_qc += write_tc_weizhi({
                'text': t, 'size': 10, 'w': int(w_qc * 567), 'tcBorders': [], 'weight': qc.get('weight')
            })
        trs_qc += tr.write(tcs_qc)
    para += table_weizhi(trs_qc) + p.write()
    admins = ['测序操作人', '', '数据分析人', '', '报告审核人', '']
    tcs_admins = ''
    for admin_index, admin in enumerate(admins):
        w_admin = 2.5 if admin_index % 2 == 0 else 3.5
        tcs_admins += write_tc_weizhi({
            'text': admin, 'size': 10, 'color': green_lighter, 'w': int(w_admin * 567)
        })
    para += table_weizhi(tr.write(tcs_admins, tr.set(trHeight=2*567)), ['top', 'bottom'])
    para += p.write(p.set(sect_pr=sect_pr_overview))
    return para


def write_chapter1(data):
    cats = get_catalog()[0: 4]
    para = ''

    trs1 = tr.write(
        tc.write(
            p.write(
                p.set(spacing=[1, 0]),
                r_aiyi.text('说明：报告中采用统一颜色标识对基因突变信息进行标注，其中：', 10)
            ),
            tc.set(w_sum, tcBorders=[], gridSpan=5)
        ),
        # tr.set(trHeight=567)
    )
    tcs1 = ''
    tcs1 += write_tc_weizhi({'jc': 'center', 'tcBorders': [], 'text': '红色', 'color': white, 'tcFill': red, 'size': 10, 'weight': 1, 'w': (567*1.5)})
    tcs1 += write_tc_weizhi({'tcBorders': [], 'text': '表示明确致病突变位点', 'size': 9, 'w': (567*4)})
    tcs1 += write_tc_weizhi({'jc': 'center', 'tcBorders': [], 'text': '浅红色', 'color': white, 'tcFill': red_lighter, 'size': 10, 'weight': 1, 'w': (567*1.5)})
    tcs1 += write_tc_weizhi({'tcBorders': [], 'text': '表示未明意义突变位点', 'size': 9, 'w': (567*4)})
    tcs1 += write_tc_weizhi({'tcBorders': [], 'text': '', 'size': 9, 'w': (567*7)})
    # para += table_weizhi(tr.write(tcs1, tr.set(trHeight=(0.7*567))), [], jc='left')
    trs1 += tr.write(tcs1)
    # para += table.write(trs1, tblBorders=[], jc='left', ind=0.2)
    para += table_weizhi(trs1, [], line=5)
    para += h4_aiyi(cat=cats[1], **outline1)
    para1 = ''
    para1 += h4_aiyi(cat=cats[2], **outline3)
    target_tips, show_extra, extra_item = data['target_tips']
    genes = {}
    action = []
    for i, item in enumerate(target_tips):
        gene = item.get('gene') or item.get('gene1')
        action1 = item.get('action1')
        action2 = '%s%s' % (gene or '', action1)
        tcn_em = item.get('tcn_em')  # 拷贝数
        ccf_expected_copies_em = item.get('ccf_expected_copies_em') or item.get('clone_proportion') or '' # 肿瘤细胞比例
        dna_vaf = item.get('dna_vaf')
        cc = ''
        if ccf_expected_copies_em:
            cc = '，肿瘤细胞比例%s' % float2percent(ccf_expected_copies_em)
        elif dna_vaf:
            cc = '，突变丰度%s' % float2percent(dna_vaf)
        vars = genes.get(gene) or []
        if item not in vars:
            vars.append(item)
        genes[gene] = vars

        # para11 = p.write(
        #     p.set(line=24),
        #     r_aiyi.text('  变异事件%s:  ' % (i + 1), space=True) +
        #     r_aiyi.text(' %s(%s%s) ' % (gene, action1, cc), color=white, fill=red, space=True)
        # )
        # tc1 = tc.write(para11, tc.set(w_sum, color=blue, fill=bg_blue))
        # para1 += table.write(tr.write(tc1), tblBorders=[])
        # action_name =
        action_name = ' %s(%s%s) ' % (gene, action1, cc)
        para_hrd = ''
        if item.get('hrd'):
            para_hrd = data.get('paras_hr')
            action_name = ' HRD评分%s' % item.get('col2')
            # action.append(data.get('hrd_tip'))
            para1 += table_weizhi(write_table_title(action_name))
        elif item.get('hr'):
            para_hrd = data.get('paras_hr')
        else:
            if action2 and action2 not in action:
                action.append(action2)
            para1 += table_weizhi(write_table_title('驱动变异%s:%s' % (i + 1, action_name)))

        para_index = 1
        pPr = p.set(line=15, spacing=[0, 1])
        para_eve = ''
        oncogenicity_variant_summary = item.get('oncogenicity_variant_summary')
        if oncogenicity_variant_summary:
            para_eve += p.write(pPr, r_aiyi.text(oncogenicity_variant_summary, 9))
        aiyi_db = item.get('known_db')
        para_eve += write_evidence1(gene, aiyi_db)
        if para_eve:
            para1 += h4_aiyi(' 该驱动变异关键循证医学证据', wingdings=True) + para_eve
            para_index += 1
        # para1 += para1
        # if len(items) == 0:

        # 原癌和抑癌
        para_gene = ''
        xingzhi = []
        oncogene = item.get('oncogene')
        tumor_suppressor_gene = item.get('tumor_suppressor_gene')
        if oncogene == 1:
            xingzhi.append('原癌')
        if tumor_suppressor_gene == 1:
            xingzhi.append('抑癌')
        if len(xingzhi) > 0:
            para_gene += p.write(p.set(line=12*1.25, spacing=[0, 0.5]), r_aiyi.text('%s %s基因' % (gene, '、'.join(xingzhi)), '小五', 1))
        summary = item.get('summary_cn')
        if summary:
            para_gene += p.write(p.set(line=12), r_aiyi.text(summary, 9))
        cn_intro = item.get('cn_intro')
        if cn_intro:
            para_gene += p.write(p.set(line=12), r_aiyi.text(cn_intro, 9))
        if para_gene:
            para1 += h4_aiyi(' 该基因临床治疗说明', **outline3)
            para1 += para_gene
        # else:
        #     para1 += p.write()
        para1 += para_hrd

    # tip = tip
    yesheng = data.get('yesheng')
    yesheng_text = ''
    if len(yesheng) == 2:
        yesheng_text = '发现%s野生型，' % ('、'.join(yesheng))
    hrd_tip = data.get('hrd_tip')
    hrd_index = data.get('hrd_index')
    if hrd_tip and hrd_index == 0:
        if yesheng_text == '':
            yesheng_text += '发现'
        yesheng_text = '%s，' % hrd_tip
    if len(action) == 0:
        run_tip = r_aiyi.text('本次检测未找到驱动基因变异事件', 10, 1)
    else:
        run_tip = r_aiyi.text('本次检测%s共找到%d个驱动基因的变异事件：' % (yesheng_text, len(genes.keys())), 10, 1)
        run_tip += r_aiyi.text('、'.join(action[:-1]), 10.5)
        if len(action) > 1:
            run_tip += r_aiyi.text('和', 10, 1)
        run_tip += r_aiyi.text(action[-1], 10.5, 1)
    if hrd_tip and 'HRD' not in yesheng_text:
        run_tip += r_aiyi.text('，%s' % hrd_tip, 10.5, 1)
    common_tip, common_para = write_common_diagnosis(data)
    paras = para
    paras += p.write(run_tip + r_aiyi.text('。' + common_tip, 10, 1))
    paras += common_para
    paras += p.write(p.set(line=18, rule='exact'), r_aiyi.text('注：驱动变异是靶向治疗提示的基础和前提条件，此处仅呈现通过数据库、文献等各方面数据和规则判断为驱动突变的肿瘤变异事件。', '小五'))
    paras += para1
    paras += write_chapter13(cats[3])
    paras += p.write(p.set(sect_pr=set_page(page_margin=page_margin4, header='rIdHeader3', footer='rIdFooter2', pgNumType_s=1)))
    return paras


def write_chapter2(index, data):
    n, start, bm0 = 11, 5, 453150350
    cats = get_catalog()[start-1: start + n]
    para = ''
    immun_tip = data.get('immun_tip') or []
    text = '、'.join([(x.get('tip1') or x.get('text') or '' )for x in immun_tip])

    para += h4_aiyi(cat=cats[1], spacing=[0, 0.5], size=12, weight=1, outline=1)
    para += p.write(p.set(spacing=[0, 0.5]), r_aiyi.text('本次检测显示该患者%s。' % text, 10, weight=1))

    msi_info = data.get('msi_info')
    tmb_info = data.get('tmb_info')
    msi_sort_paired_total = msi_info.get('total')
    msi_sort_paired_somatic = msi_info.get('somatic')
    msi_score = msi_info.get('score')

    chs = [
        {
            'cat': cats[2],
            'note_before': 0,
            'img_id': 'msi_score',
            'data': msi_info,
            'note': '注：肿瘤组织-正常样本配对分析的模式',
            'before': 8,
            'cy': 4.19,
            'w': 3600,
            'infos': [
                {'title': '结果说明', 'text':
                    'MSI是指与正常组织相比，在肿瘤中某一微卫星由于重复单位的插入或缺失而造成的微卫星长度的任何改变，出现新的微卫星等位基因现象。' +
                    '其发生机制主要包括DNA多聚酶的滑动导致重复序列中1个或多个碱基的错配和微卫星重组导致碱基对的缺失或插入。' +
                    '该结果采用经FDA批准的MSIsensor算法获得。本次检测采用肿瘤组织-正常样本配对分析的模式，' +
                    '共分析了%s个微卫星位点，' % msi_sort_paired_total +
                    '其中%s个微卫星位点为具有显著差异的体细胞变异点，' % msi_sort_paired_somatic +
                    '比例为%s%%，' % msi_score +
                    '即MSIsensor评分为%s。' % msi_score +
                    '研究表明，MSIsensor评分免疫治疗疗效正相关，也与错义突变和插入缺失突变总量显著正相关（PMID:31048490）。'},
                {'title': '检测意义',
                 'text': '目前FDA批准Pembrolizumab用于dMMR/MSI-H型的转移性实体瘤，Nivolumab用于dMMR/MSI-H的转移性结直肠癌。Science发表了NCT01876511的临床研究结果显示，Pembrolizumab用于治疗MSI-H的晚期肿瘤患者，MSI-H型肿瘤患者ORR高达54%。MSI-H在结直肠癌、胃癌、子宫内膜癌中较多，其他多种癌种都有一定量的分布。MSI是MMR（错配修复系统）的一个反映标志，MMR是人体细胞DNA修复的一种方式之一，MMR缺陷导致DNA出错的概率大规模提升，进而导致该类型肿瘤细胞具有非常高的突变量，而高的突变负荷进一步导致肿瘤细胞高概率采用PD1等通路的免疫逃逸机制。因此，PD1抗体对MSI-H/dMMR肿瘤更可能有效。'
                 }
            ] },
        {
            'cat': cats[3],
            'before': 0, 'note_before': 13,
            'img_id': 'tmb',
            'cy': 7,
            'note': tmb_info.get('tmb_tip'),
            'data': tmb_info,
            'w': 3200,
            'infos': [
                {'title': '结果说明', 'text': '该结果通过680个基因的panel获得，该panel实际大小为2.4M，核算CDS区域为1.29M。TMB肿瘤突变负荷指平均每M（兆）区域，肿瘤细胞发生的非同义突变的个数。（证据级别说明：常规以10个突变/Mb标准时非小细胞肺癌证据级别为B级，结直肠癌和胰腺癌由于免疫治疗有效率低，常规阈值为20，其他所有癌种均为C级；当TMB大于20，高于绝大多数情况阈值时，非小细胞肺癌更新为A级，其他癌种（结直肠癌和胰腺癌除外）更新为B级。'},
                {'title': '检测意义', 'text': 'TMB在多项临床研究中均被证明能够有效区分PD1抗体、CTLA4抗体等免疫检查点抑制剂治疗是否有效的人群。综合型研究表明，在不同肿瘤中，不同患者的PD1抗体治疗有效性的差异55%可以由TMB的差异解释。TMB是不同肿瘤间体细胞突变量的评估。一般情况下，TMB越高，该肿瘤可能会拥有更多的肿瘤新生抗原，该肿瘤也越有可能在经过免疫检查点抑制剂解除肿瘤免疫逃逸之后，被患者自身的免疫系统所识别，相关治疗在该患者身上也就越可能有效。'},
            ]
        }
    ]
    for ch in chs:
        para += write_chapter21(ch)
    para += h4_aiyi(cat=cats[4], **outline21) + data.get('para_ddr')
    para += h4_aiyi(cat=cats[5], **outline21) + data.get('para_mingan')
    para += h4_aiyi(cat=cats[6], **outline21) + data.get('para_naiyao')
    para += h4_aiyi(cat=cats[7], **outline21) + data.get('para_chaojinzhan')
    para += h4_aiyi(cat=cats[8], **outline21) + data.get('para_hla')
    para += h4_aiyi(cat=cats[9], **outline21) + write_kangyuan(data.get('neoantigens'))

    para += h4_aiyi(cat=cats[10], **outline21)
    para += h4_aiyi('免疫治疗与肿瘤免疫', **outline3)
    para_set = p.set()
    para_set1 = p.set(spacing=[0, 0.5])
    para += p.write(para_set, r_aiyi.text('自2012年，约翰霍普金斯大学PD1抗体临床试验结果发表在《新英格兰医学杂志》之后，免疫治疗真正进入临床医生和产业界的视野，并迅速取代靶向治疗成为肿瘤治疗最新最主流的治疗研究方向。CTLA4、PD1抗体以惊人的产业化速度和疗效，迅速在多个癌种中获批，并在肺癌中成为一线治疗药物。PDL1表达、微卫星不稳定迅速成为有效协助患者药物筛选的分子标志物，肿瘤突变负荷TMB、新抗原负荷、肿瘤CD8+T淋巴细胞浸润状态等在各种数据中证明具有筛选有效患者的能力，然而，新型免疫治疗手段以超越基础研究的速度在发展，免疫治疗人群筛选和联合治疗时机选择远远没有到达完美，新的标志物层出不求', '小五'))
    para += p.write(para_set, r_aiyi.text('肿瘤免疫治疗是通过协助免疫系统发挥被抑制或者缺失的免疫能力，进而实现肿瘤治疗的手段。更好的理解肿瘤免疫过程，能够协助我们对各种新型肿瘤免疫治疗手段和新型标志物形成更好的全局性理解，以便我们更好的采取与化疗、放疗、靶向治疗的联合治疗手段，优化免疫治疗时机和方式的选择。肿瘤免疫周期理论是由Mellman等人提出来的肿瘤免疫过程框架，目前已经成为肿瘤免疫学研究和临床应用的思维框架。', '小五'))
    para += h4_aiyi('肿瘤免疫周期理论', **outline3)
    # para += p.write(r_aiyi.picture(cy=10, rId='2.4.2', align=['center', ''], posOffset=[0, 0.5]))
    para += write_pic_center(10, '2.4.2')
    # para += p.write(para_set) * 16
    para += p.write(para_set, r_aiyi.text('肿瘤免疫治疗是通过协助免疫系统发挥被抑制或者缺失的免疫能力，进而实现肿瘤治疗的手段。更好的理解肿瘤免疫过程，能够协助我们对各种新型肿瘤免疫治疗手段和新型标志物形成更好的全局性理解，以便我们更好的采取与化疗、放疗、靶向治疗的联合治疗手段，优化免疫治疗时机和方式的选择。肿瘤免疫周期理论是由Mellman等人提出来的肿瘤免疫过程框架，目前已经成为肿瘤免疫学研究和临床应用的思维框架。', '小五'))
    para += h4_aiyi('1）肿瘤细胞死亡并释放肿瘤特异抗原', **outline5)
    para += p.write(para_set, r_aiyi.text('从某种意义上说，肿瘤是由基因突变积累形成的疾病，同时，肿瘤基因突变也是肿瘤免疫过程发生的主要驱动因素。各种原因形成的肿瘤基因突变，部分情况下会让肿瘤细胞表达出与未突变基因不一样的蛋白质，其中部分突变蛋白的肽段会被身体的免疫系统识别为“外源”抗原，即所谓的“新抗原”。当肿瘤因为各种原因死亡后，含有新抗原的蛋白就会从肿瘤细胞中释放出来，进而驱动肿瘤免疫反应。所以，部分情况下，放疗、化疗、靶向治疗等治疗手段会跟免疫检查点抑制剂治疗形成协同增强作用，也是因为该原因引起。最新部分研究甚至发现，不管PDL1表达状态，PD通路抗体联合化疗的疗效远高于单独化疗。微卫星高不稳定、肿瘤突变负荷高的肿瘤患者，一般情况下免疫检查点抑制剂具有更好的疗效，也均是因为一般情况下，更高的突变负荷，意味着更多的新抗原可能性。', '小五'))
    para += h4_aiyi('2）抗原提呈细胞摄取并处理肿瘤新抗原', **outline5)
    para += p.write(para_set, r_aiyi.text('抗原提呈细胞摄取含有新抗原的突变蛋白，并将水解为可以结合到MHC（主要组织相容性复合物，又称为HLA人类白细胞抗原）的肽段。抗原提呈细胞需要有包括促炎症细胞因子和肿瘤细胞死亡释放的信号因子在内的多种免疫原性信号才能够有效启动，因此，不同免疫状态下的肿瘤，新抗原的提呈效率是不一样的。不同人的MHC具有异质性，所以，不同患者哪些新抗原能够被提呈是不一样的。目前通过生物信息手段，新抗原能够以一定的准确性被预测出来。目前有研究通过预测的新抗原进行个性化治疗疫苗设计，促进抗原提呈过程，并取得了相当惊人的效果。', '小五'))
    para += h4_aiyi('3）抗原提呈细胞进入淋巴结激活T细胞', **outline5)
    para += p.write(para_set, r_aiyi.text('（抗原提呈细胞被新抗原激活后，进入淋巴结激活初始T细胞。初始T细胞在共刺激分子的协同作用下诱导T细胞增殖并分化成为激活免疫杀伤的效应T细胞和抑制免疫杀伤的调节性T细胞，并通过两者比例的精确控制达成免疫反应性质确定和平衡。重组白细胞介素2（IL-2）即通过该环节调节肿瘤免疫反应。', '小五'))
    para += h4_aiyi('4）激活的T细胞离开淋巴结进入循环系统', **outline5)
    para += p.write(para_set, r_aiyi.text('激活的T细胞基于细胞黏附分子组分变化的原因，脱离淋巴结进入循环系统。', '小五'))
    para += h4_aiyi('5）T细胞穿过血管壁浸润到肿瘤微环境', **outline5)
    para += p.write(para_set, r_aiyi.text('肿瘤细胞死亡等原因引起的局部免疫反应会让周围组织跟炎症反应一样释放细胞因子和趋化因子，结合该部位血管内皮细胞由于炎症反应表达量增加的附着蛋白，让循环系统中的T细胞通过与血管内皮细胞锚定后进入肿瘤微环境中。初步研究结果表明，抗血管生成治疗与免疫治疗能够起到非常好的协同作用，部分临床试验中甚至提高将近一倍的治疗效果。', '小五'))
    para += h4_aiyi('6）T细胞通过特异性受体识别肿瘤细胞', **outline5)
    para += p.write(para_set, r_aiyi.text('肿瘤细胞和一般体细胞一样，在核糖体进行蛋白质翻译的过程中，会有一定比例的缺陷蛋白并会被水解成肽段，其中能够被MHC结合的潜在抗原会被提呈到细胞膜表面。T细胞通过特异性受体（TCR）识别肿瘤细胞表面的新抗原。有研究表明，部分肿瘤中，肿瘤细胞MHC缺失对于免疫逃逸的发生贡献重要意义。目前CAR-T和TCR-T是重点研究方向，并在部分肿瘤中发挥惊人的治疗效果。CAR-T治疗又称人工合成嵌合抗原受体T细胞治疗，直接取代T细胞识别肿瘤细胞的方式，而TCR-T则是通过筛选分离针对肿瘤特定抗原的TCR，将原来未能识别肿瘤细胞的T细胞改造成能够识别肿瘤细胞的T细胞。', '小五'))
    para += h4_aiyi('7）肿瘤细胞被T细胞识别并溶解消灭', **outline5)
    para += p.write(para_set, r_aiyi.text('当效应T细胞识别出肿瘤细胞表面的特异性抗原后，胞浆内储存的效应分子将朝目标方向释放，在不影响周围正常细胞的情况下溶解肿瘤细胞。CD8+T细胞是最重要的执行细胞杀伤的效应T细胞，所以，一般情况下，其肿瘤微环境浸润情况与免疫治疗疗效正相关。同时，PD1和CTLA-4是T细胞表面的抑制性受体，肿瘤细胞通过相应配体的表达，抑制T细胞的免疫杀伤作用。', '小五'))
    para += h4_aiyi('肿瘤免疫表型理论', **outline3)
    para += write_pic_center(7, '2.4.3.1')
    # para += p.write(r_aiyi.picture(cy=10, rId='2.4.3.1', align=['center', ''], posOffset=[0, 0.5]))
    # para += p.write(para_set) * 16
    para_mianyi = ''
    # para += p.write(
    #     p.set(spacing=[0, 0.5], ind=[0, 18]),
    #     r_aiyi.text('肿瘤免疫表型理论是由Mellman在肿瘤免疫周期的基础上，进一步根据最新的研究成果，细化发展出来的一套肿瘤免疫分型体系。该分型体系根据相应的生物学机制，将肿瘤分成免疫沙漠型（棕色）、免疫豁免型（蓝色）和炎症型（红色）三种，并进一步根据宿主基因、微生物组、环境因素、治疗药物和癌症共五个维度，将影响免疫原性的多种研究进展整合成如下图所示，与免疫治疗疗效和免疫原性相关的癌症-免疫设定点。', '小五')
    #     + r_aiyi.picture(6, rId='2.4.3.2', posOffset=[16, -1], align=['', ''])
    # )
    para_mianyi += p.write(
        p.set(spacing=[0, 0.5], ind=[0, 0]),
        r_aiyi.text('肿瘤免疫表型理论是由Mellman在肿瘤免疫周期的基础上，进一步根据最新的研究成果，细化发展出来的一套肿瘤免疫分型体系。该分型体系根据相应的生物学机制，将肿瘤分成免疫沙漠型（棕色）、免疫豁免型（蓝色）和炎症型（红色）三种，并进一步根据宿主基因、微生物组、环境因素、治疗药物和癌症共五个维度，将影响免疫原性的多种研究进展整合成如下图所示，与免疫治疗疗效和免疫原性相关的癌症-免疫设定点。', '小五')
    )
    # para += p.write() * 5
    para_mianyi += p.write(p.set(ind=[0, 0]), r_aiyi.text('癌症免疫设定点是指产生有效癌症免疫原性所需克服的阈值，为指导免疫治疗临床应用和研究提供一个系统性框架。该设定点可以理解为理解为刺激因子、抑制因子和TCR结合信号（T细胞抗原受体与新抗原、癌症相关抗原等癌症抗原的亲和力）的平衡。癌症免疫治疗主要是针对肿瘤部位，通过增加的刺激因子、减少抑制因子或者增加TCR结合信号这三种方式进行的。', '小五'))
    tcs_mianyi = tc.write(para_mianyi, tc.set(567 * 12, tcBorders=[]))
    tcs_mianyi += tc.write(
        p.write(r_aiyi.picture(cy=6, rId='2.4.3.2', align=['right', ''])), tc.set(567 * 6, tcBorders=[])
    )
    para += table.write(tr.write(tcs_mianyi), tblBorders=[])
    para += h4_aiyi('免疫检查点抑制剂疗联合传统治疗研究进展', **outline3)
    para += p.write(para_set, r_aiyi.text('免疫检查点抑制剂单药治疗虽然在临床治疗中显示出广泛的抗癌效果，不同癌种的总体有效率基本在20%左右，即使通过多种标志物进行预测可一定程度上减少无效人群，但其获益人群一样有限。从肿瘤免疫过程上看，将免疫阻隔型和免疫沙漠型的“冷”肿瘤，转变成免疫炎症型的“热”肿瘤，扩大免疫检查点抑制剂的获益人群，可以通过联合治疗的方式进行。对PDL1、MSI、TMB等各类型标志物预测检查位点抗体单药治疗效获益可能性较低的患者，最好进行检查位点抗体与其他治疗方式的联合治疗。多项研究发现放疗、化疗和靶向治疗等传统治疗联合免疫检查点抑制剂治疗能够获得惊人的效果，中位生存期、无疾病进展生存期和有效率等疗效指标翻倍的情况。同时，值得注意的是，联合治疗会成倍甚至多倍的提高毒副反应。基于对肿瘤免疫过程理解的加深，特异性针对特定肿瘤免疫过程的免疫治疗是联合治疗的更优选择。', '小五'))
    para += h4_aiyi('新型免疫治疗手段研究进展', **outline3)
    para += p.write(para_set1, r_aiyi.text('免疫治疗是癌症治疗有史以来最激动人心的治疗领域，甚至有的医生认为，癌症免疫治疗让人类真正真正看到了癌症被治愈的希望。随着PD1抗体在各癌种中的攻城略地，新型的免疫治疗手段也展现出未来的王者之相。', '小五'))
    para += h4_aiyi('1）个性化癌症治疗疫苗', **outline5)
    para += p.write(para_set, r_aiyi.text('癌症疫苗，这种通过主动免疫去扩大肿瘤特异性T细胞反应的治疗方式，一直被认为是癌症免疫治疗的有效手段。尽管大家能够清晰看到癌症疫苗的合理性，但是，过去在临床方面的尝试都是不成功的。不同患者之间的肿瘤抗原具有强烈的多样性，因此，个性化癌症疫苗的发展是必要的。随着二代测序和生物信息工具的逐步完善，癌症疫苗的核心环节，新抗原预测逐渐成熟，该技术在最近的研究中取得突破性的进展，且由于安全性较好，是最值得跟进参与的新型癌症免疫治疗手段之一。', '小五'))
    # para += p.write(r_aiyi.picture(cy=11, rId='2.4.5.1', align=['center', ''], posOffset=[11.12, 0.76]))
    para += write_pic_center(8, '2.4.5.1')
    # para += p.write(para_set) * 17
    para += h4_aiyi('2）免疫检查点抑制剂相关抗体', **outline5)
    para += p.write(para_set, r_aiyi.text('肿瘤免疫检查点不仅仅PD1和CTLA-4，还有至少几十种免疫检查点。目前该领域，IDO抑制剂、LAG3抑制剂在早期临床试验中显示出相当好的疗效，与PD1联合用药的情况下，部分结果甚至成倍提升有效率，其中IDO抑制剂，已经进入三期临床临床试验（注：IDO抑制剂Epacadostat与Keytruda联用的关键三期临床试验ECHO-301失败）。', '小五'))
    para += h4_aiyi('3）CAR-T和TCR-T治疗', **outline5)
    para += p.write(para_set, r_aiyi.text('CAR-T和TCR-T都属于细胞治疗的范畴，主要通过对患者自身的T细胞进行工程化改造，让其能够发挥肿瘤细胞的杀灭功能。CAR-T，又称嵌合抗原受体T细胞治疗，是通过人工合成的受体使患者自身的T细胞能够进行肿瘤细胞识别，进而发挥肿瘤细胞杀伤效果。由于CAR-T细胞在实体瘤中的浸润能力相对较差，目前临床主要应用于血液肿瘤中。随着技术进展，如通过提升CAR-T中对增强T细胞浸润能力相关基因的表达，未来应该也能够在实体瘤治疗中发挥重要作用。TCR-T，又称T细胞识别受体（TCR）工程化改造T细胞治疗，是通过将对特定抗原亲和力强的TCR移植到患者自身的T细胞上使患者自身的T细胞发挥肿瘤细胞杀伤效果。其中特异性TCR-T，是指针对患者特异的新抗原进行设计的TCR-T治疗方式，是未来最有价值的癌症治疗手段，相比通过个性化疫苗诱导形成肿瘤杀伤T细胞，从原理上来说，特异性TCR-T治疗属于更靠后的免疫周期中的环节，可能具有更好的治疗效果。', '小五'))
    para += h4_aiyi('4）溶瘤病毒', **outline5)
    para += p.write(para_set, r_aiyi.text('溶瘤病毒是一群倾向于感染和杀伤肿瘤细胞的病毒。溶瘤病毒治疗是指将本身对身体伤害较低的溶瘤病毒经工程化改造减毒处理和治疗效果提升后，感染肿瘤患者的治疗方式。这种治疗思路和方法，是多年前发现和临床实践过的方法，且2005年中国CFDA批准了一种溶瘤腺病毒。但是，单药治疗效果有限，并未引起广泛关注。随着PD1抗体治疗的普及，临床研究发现，溶瘤病毒联合PD1治疗能够大幅度提高PD1抗体治疗的有效率，2015年，溶瘤病毒治疗T-Vec批准用于黑色素瘤。溶瘤病毒在提高PDL1表达、逆转肿瘤相关免疫抑制等多个层面，均能够与PD1抗体治疗形成非常好的协同效果。', '小五'))
    para += p.write(r_aiyi.picture(cy=10, rId='2.4.5.2', align=['center', ''], posOffset=[0, 0.3]))
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    return para


def write_chapter3(index, chem_items):
    n, start = 2, 10+6
    cats = get_catalog()[start-1: start + n]
    trs1 = ''
    ws1 = [8*567, 3 * 567, 3.5*567, 3.5 * 567]
    pPr = p.set(spacing=[0.1, 0.05], jc='center')
    trs1 += write_thead51(['化疗药物', '敏感性', '毒副作用', '检测结果'], ws=ws1, tcFill=gray, pPr=pPr, size='小五', weight=1)
    chem_tips = [
        {'text': u'推荐使用', 'color': RGB_to_Hex('255,0,0')},
        {'text': u'常规使用', 'color': RGB_to_Hex('54,95,245')},
        {'text': u'谨慎使用', 'color': ''},
    ]
    # chem_items = []

    chem_drugs = []
    trs2 = ''
    ws2 = [2*567, 1.9 * 567, 2.1 * 567, 4 *567, 2* 567, 4 * 567, 2* 567]
    trs2 += write_thead51(['化疗药物', '基因名称', '检测位点', '疾病', '检测结果', '判断结果', '等级'],
                          ws=ws2, tcFill=gray, pPr=pPr, size='小五', inline=['left', 'top', 'bottom'], weight=1)
    if len(chem_items) == 0:
        trs1 += write_tr51(['无'] * len(ws1), ws1)
        trs2 += write_tr51(['无'] * len(ws2), ws2)

    for i in range(len(chem_items)):
        item = chem_items[i]
        result = item.get('result')
        result_colors = filter(lambda x: x.get('text') == result, chem_tips)
        result_color = '' if len(result_colors) == 0 else result_colors[0].get('color')
        tcs1 = ''
        items1 = [
            {'text': item.get('drug')},
            {'text': item.get('sensibility')},
            {'text': item.get('side_reaction')},
            {'text': item.get('result'), 'color': result_color},
        ]
        if result == '推荐使用':
            chem_drugs.append(item.get('drug'))
        for i1_index, item1 in enumerate(items1):
            item1.update({'w': ws1[i1_index], 'pPr': pPr})
            tcs1 += write_tc_weizhi(item1)
        trs1 += tr.write(tcs1)
        rs_list0 = item['detail']
        for rs_index, rs_item0 in enumerate(rs_list0):
            # print rs_item0
            vMergeStart = '<w:vMerge w:val="restart"/>'
            vMerge = '<w:vMerge/>'
            items = [
                {'text': item.get('drug') if rs_index == 0 else '', 'vMerge': vMergeStart if rs_index == 0 else vMerge},
                {'text': rs_item0.get('gene')},
                {'text': rs_item0.get('rs_no')},
                {'text': rs_item0.get('disease')},
                {'text': rs_item0.get('genotype')},
                {'text': rs_item0.get('result')},
                {'text': rs_item0.get('level')},
            ]
            tcs2 = ''
            for i_index, item in enumerate(items):
                item['w'] = ws2[i_index]
                item['pPr'] = p.set(jc='center')
                if i_index > 0:
                    item['tcBorders'] = ['left', 'top', 'bottom']
                # item['jc'] = 'center'
                tcs2 += write_tc_weizhi(item)
            trs2 += tr.write(tcs2)
    para = ''
    para += h4_aiyi(cat=cats[1], spacing=[0, 0.5], outline=1, line=24, rule='auto', size=11, ind=['hanging', 1])
    para += p.write(
        p.set(spacing=[0.5, 0.2]),
        r_aiyi.text(' 化疗药物检测结果', '五号', 1, wingdings=True, space=True)
    )
    tr_shuoming = tr.write(
        tc.write(
            p.write(pPr, r_aiyi.text('说明', 10, 1)),
            tc.set(gridSpan=len(ws1), fill=gray, tcBorders=[], color=gray)
        )
    )
    trs1 += tr_shuoming
    text1 = '''1. 疗效预测（药物敏感性较高/低和毒副作用风险较高/低）根据证据等级综合判断获得。
    2. 此处检测结果不具有临床医嘱性质，仅供临床医师参考，不作为直接用药依据，具体用药方案请遵医嘱。
    3. “-”表示没有药物敏感性位点或毒副作用位点等的相关资料，不进行临床指导。'''
    paras1 = ''
    for t in text1.split('\n'):
        paras1 += p.write(p.set(spacing=[0.2, 0]), r_aiyi.text(t, '小五'))
    trs1 += tr.write(
        tc.write(paras1, tc.set(18 * 567, gridSpan=4, color=gray, tcBorders=[]))
    )
    para += table_weizhi(trs1)
    para += p.write(
        p.set(spacing=[0.5, 0.2]),
        r_aiyi.text(' 化疗药物检测详细结果', '五号', 1, wingdings=True, space=True)
    )
    trs2 += tr.write(
        tc.write(
            p.write(pPr, r_aiyi.text('说明', 10, 1)),
            tc.set(gridSpan=len(ws2), fill=gray, tcBorders=[], color=gray)
        )
    )
    texts21 = '''1. 基因名称：均采用 HGNC 里的官方命名。
    2. rs 号：NCBI 里对所提交的 snp 给予的编号。
    3. 对应疾病：为 PharmGKB 数据库中相关药物的对应疾病研究。
    4. 等级划分：参考https://www.pharmgkb.org/page/clinAnnLevels。'''
    texts22 = '''1A：注释基于被医学会认可的指南或经某些重大卫生系统的认可；
    1B：注释基于多项有统计显著的研究；
    2A：注释基于多项重复研究，故药效关系很有可能是有意义的；
    3：注释仅基于 1 项有显著差异的研究（未重复）或多项研究但缺乏明显药效关联性；
    4：注释仅基于少量病例、非权威研究或体外的分子功能研究。'''
    texts23 = '''5. 检测结果只对本次送检样品负责，样品只进行 DNA 水平检测，不涉及 RNA 和蛋白质水平。
    6. 检测结果不具有临床医嘱性质，仅供临床医师参考。
    7. 如对报告有疑义，请在收到报告后 7 个工作日内与我们联系。'''
    paras2 = ''
    paras2 += p.write(
        p.set(line=1, rule='exact'),
        r_aiyi.picture(2.23, rId='level3', align=['right', ''], wrap='undertext'))
    for t in texts21.split('\n'):
        paras2 += p.write(p.set(spacing=[0.2, 0]), r_aiyi.text(t, '小五'))
    for t in texts22.split('\n'):
        paras2 += p.write(p.set(spacing=[0.2, 0], ind=[3, 0]), r_aiyi.text(t, '小五'))
    for t in texts23.split('\n'):
        paras2 += p.write(p.set(spacing=[0.2, 0], ind=[0, 0]), r_aiyi.text(t, '小五'))

    trs2 += tr.write(
        tc.write(paras2, tc.set(18 * 567, gridSpan=len(ws2), color=gray, tcBorders=[]))
    )
    para += table_weizhi(trs2)
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index, page_margin=[4, 1.5, 2.54, 1.5, 1.5, 1.75])))
    return para, chem_drugs


def write_chapter4(index, data):
    cats = get_catalog()[18: 22]
    para = ''
    # print cats[0].get('title'), '==='
    para += h4_aiyi(cat=cats[0], spacing=[0, 0.5], outline=1, size=12, ind=['hanging', 1])
    para += data['para_yichuan']
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    return para


def write_chapter5(index, data):
    s, n = 21, 6
    cats = get_catalog()[s: s+n]
    para = ''
    # para += h4_aiyi(cat=cats[0], **outline2)
    para += h4_aiyi(cat=cats[0], spacing=[0, 0.5], outline=1, size=12, ind=['hanging', 1])
    para += write_chapter51(cats[1].get('title'), data) + p.write()
    para += write_chapter_cnvs(cats[2].get('title'), data)
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))

    return para


# '3EA6C2'
def write_chapter_affix(index, data):
    s, n = 21, 6
    cats = get_catalog()[s: s+n]
    para = ''
    para += p.write(
        p.set(spacing=[0.2, 0.2], jc='center', line=1.45*12), r_aiyi.text('附  录', 12, weight=1))
    genes1 = '''ABL1	ACVR1	ACVR1B	ACVR2A	AGO2	AKT1	AKT2	AKT3	ALK
    ALOX12B	AMER1	ANKRD11	APC	AR	ARAF	ARFRP1	ARID1A	ARID1B
    ARID2	ARID5B	ASXL1	ASXL2	ATM	ATR	ATRX	AURKA	AURKB
    AXIN1	AXIN2	AXL	B2M	BABAM1	BAP1	BARD1	BBC3	BCL10
    BCL2	BCL2L1	BCL2L11	BCL2L2	BCL6	BCOR	BCORL1	BCR	BIRC3
    BIRC5	BLK	BLM	BMPR1A	BRAF	BRCA1	BRCA2	BRD4	BRIP1
    BTG1	BTK	C11orf30	CALR	CARD11	CARM1	CASP8	CBFB	CBL
    CCND1	CCND2	CCND3	CCNE1	CD19	CD22	CD274	CD276	CD38
    CD3D	CD3E	CD3G	CD52	CD74	CD79A	CD79B	CDC42	CDC73
    CDH1	CDK12	CDK2	CDK4	CDK6	CDK8	CDK9	CDKN1A	CDKN1B
    CDKN2A	CDKN2B	CDKN2C	CEBPA	CENPA	CHD4	CHEK1	CHEK2	CIC
    CREBBP	CRKL	CRLF2	CSDE1	CSF1R	CSF3R	CSK	CTCF	CTLA4
    CTNNA1	CTNNB1	CUL3	CUL4A	CXCR4	CYLD	CYP2C8	CYP2E1	CYSLTR2
    DAXX	DCUN1D1	DDR1	DDR2	DICER1	DIS3	DNAJB1	DNMT1	DNMT3A
    DNMT3B	DOT1L	DROSHA	DUSP4	E2F3	EED	EGF	EGFL7	EGFR
    EIF1AX	EIF4A2	EIF4E	ELF3	EML4	EP300	EPAS1	EPCAM	EPHA2
    EPHA3	EPHA5	EPHA7	EPHB1	ERBB2	ERBB3	ERBB4	ERCC1	ERCC2
    ERCC3	ERCC4	ERCC5	ERF	ERG	ERRFI1	ESR1	ETV1	ETV4
    ETV6	EWSR1	EZH1	EZH2	EZR	FAM175A	FAM46C	FAM58A	FANCA
    FANCC	FANCD2	FANCE	FANCF	FANCG	FANCI	FANCL	FAS	FAT1
    FBXW7	FGF1	FGF10	FGF12	FGF14	FGF19	FGF2	FGF23	FGF3
    FGF4	FGF5	FGF6	FGF7	FGF8	FGF9	FGFR1	FGFR2	FGFR3
    FGFR4	FGR	FH	FLCN	FLT1	FLT3	FLT4	FOXA1	FOXL2
    FOXO1	FOXP1	FUBP1	FYN	GABRA6	GATA1	GATA2	GATA3	GATA4
    GATA6	GID4	GLI1	GNA11	GNA13	GNAQ	GNAS	GPS2	GREM1
    GRIN2A	GRM3	GSK3B	H3F3A	H3F3B	H3F3C	HCK	HGF	HIST1H1C
    HIST1H2BD	HIST1H3A	HIST1H3B	HIST1H3C	HIST1H3D	HIST1H3E	HIST1H3F	HIST1H3G	HIST1H3H
    HIST1H3I	HIST1H3J	HIST2H3C	HIST2H3D	HIST3H3	HLA-A	HLA-B	HNF1A	HOXB13
    HRAS	HSD3B1	HSP90AA1	ICOSLG	ID3	IDH1	IDH2	IFNGR1	IGF1
    IGF1R	IGF2	IKBKE	IKZF1	IL10	IL2RA	IL2RB	IL2RG	IL6
    IL7R	INHA	INHBA	INPP4A	INPP4B	INPPL1	INSR	IRF2	IRF4
    IRS1	IRS2	ITK	JAK1	JAK2	JAK3	JUN	KCNJ5	KDM5A
    KDM5C	KDM6A	KDR	KEAP1	KEL	KIT	KLF4	KLHL6	KMT2A
    KMT2B	KMT2C	KMT2D	KNSTRN	KRAS	LATS1	LATS2	LCK	LIMK1
    LMO1	LRP1B	LTK	LYN	MALT1	MAP2K1	MAP2K2	MAP2K4	MAP2K7
    MAP3K1	MAP3K13	MAP3K14	MAPK1	MAPK3	MAPKAP1	MAX	MCL1	MDC1
    MDM2	MDM4	MED12	MEF2B	MEN1	MERTK	MET	MGA	MITF
    MLH1	MPL	MRE11A	MS4A1	MSH2	MSH3	MSH6	MST1R	MTOR
    MUTYH	MYC	MYCL	MYCN	MYD88	MYOD1	NBN	NCOA3	NCOR1
    NEGR1	NF1	NF2	NFE2L2	NFKBIA	NKX2-1	NKX3-1	NOTCH1	NOTCH2
    NOTCH3	NOTCH4	NPM1	NRAS	NSD1	NT5C2	NTHL1	NTRK1	NTRK2
    NTRK3	NUF2	NUP93	PAK1	PAK3	PAK7	PALB2	PARK2	PARP1
    PARP2	PAX5	PBRM1	PCBP1	PDCD1	PDCD1LG2	PDGFRA	PDGFRB	PDK1
    PDPK1	PGR	PHOX2B	PIK3C2B	PIK3C2G	PIK3C3	PIK3CA	PIK3CB	PIK3CD
    PIK3CG	PIK3R1	PIK3R2	PIK3R3	PIM1	PLCG2	PLK2	PMAIP1	PMS1
    PMS2	PNRC1	POLD1	POLE	PPARG	PPM1D	PPP2R1A	PPP2R2A	PPP4R2
    PPP6C	PRDM1	PRDM14	PREX2	PRKAR1A	PRKCI	PRKD1	PTCH1	PTEN
    PTK6	PTP4A1	PTPN11	PTPRD	PTPRS	PTPRT	QKI	RAB35	RAC1
    RAC2	RAD21	RAD50	RAD51	RAD51B	RAD51C	RAD51D	RAD52	RAD54L
    RAF1	RARA	RASA1	RB1	RBM10	RECQL	RECQL4	REL	RET
    RFWD2	RHEB	RHOA	RICTOR	RIT1	RNF43	ROCK1	ROS1	RPS6KA4
    RPS6KB2	RPTOR	RRAGC	RRAS	RRAS2	RTEL1	RUNX1	RXRA	RYBP
    SBDS	SDC4	SDHA	SDHAF2	SDHB	SDHC	SDHD	SESN1	SESN2
    SESN3	SETD2	SETD8	SF3B1	SGK1	SH2B3	SH2D1A	SHOC2	SHQ1
    SLAMF7	SLC34A2	SLX4	SMAD2	SMAD3	SMAD4	SMARCA4	SMARCB1	SMARCD1
    SMO	SMYD3	SNCAIP	SOCS1	SOS1	SOX10	SOX17	SOX2	SOX9
    SPEN	SPOP	SPRED1	SPRY2	SRC	SRD5A2	SRMS	SRSF2	STAG2
    STAT3	STAT5A	STAT5B	STK11	STK19	STK40	SUFU	SUZ12	SYK
    TAP1	TAP2	TBX3	TCEB1	TCF3	TCF7L2	TEK	TERT	TET1
    TET2	TGFBR1	TGFBR2	TIPARP	TMEM127	TMPRSS2	TNFAIP3	TNFRSF14	TNFRSF8
    TNFSF11	TOP1	TP53	TP53BP1	TP63	TRAF2	TRAF7	TSC1	TSC2
    TSHR	TYRO3	U2AF1	UGT1A1	UPF1	VEGFA	VHL	VTCN1	WAS
    WHSC1	WHSC1L1	WISP3	WT1	WWTR1	XIAP	XPC	XPO1	XRCC1
    XRCC2	YAP1	YES1	ZFHX3	ZNF217	ZNF703			'''
    title1 = '573个基因全外显子（点突变、短片段拆入/缺失、拷贝数变异）'

    gene_infos = [
        [title1, genes1],
        ['45个基因部分外显子（点突变、短片段拆入/缺失、拷贝数变异）', '''ABCB1	ABCC2	ABCC4	ABCG2	ADGRA2	CHST3	CSNK1A1	CYP17A1	CYP1A1
CYP1B1	CYP2C19	DPYD	DSCAM	DYNC2H1	ELOC	EMSY	FANCB	FCGR3A
FRK	GALNT14	HDAC1	KAT6A	KMT5A	LRIG3	LRP2	MAP4K5	MRE11
MSI1	MTHFR	NOS3	NRG1	NSD2	PAK5	PRKDC	PRKN	PTK2
RANBP2	RPL13	RRM1	SIK1	SLC22A2	SLCO1B1	SLCO1B3	STAT4	TYK2'''],
        ['37个基因部分内含子（融合/重排）', '''ALK	BCL2	BCR	BRAF	BRCA1	BRCA2	CD74	ERC	ETV1
ETV4	ETV5	ETV6	EWSR1	EZR	FGFR1	FGFR2	FGFR3	KIT
KMT2A	MET	MSH2	MYB	MYC	NOTCH2	NTRK1	NTRK2	NUTM1
PDGFRA	RAF1	RARA	RET	ROS1	RSPO2	SDC4	SLC34A2	TERT
TMPRSS2	 	 	 	 	 	 	 	 '''],
        ['37个MSI基因', '''ACTC	ATM	ATM-15	BAT-25	BAT-26	BAT-34c4	BAT-40	BRCA2	CBL-17
CUL-22	D10S197	D17S250	D17S261	D17S799	D18S35	D18S55	D18S58	D1S2883
D2S123	D5S346	MET	MITF-14	MONO-27	MSH2	MSH6	NF1-26	NR-21
NR-22	NR-24	NR-27	PMS2	POLE	PTK-16	PTPN-17	RET-14	SDHC
TGF-βRII								'''],
        ['41个化疗基因', '''ABCB1	ABCG2	C8orf34	CBR3	CDA	COMT	CYP19A1	CYP1B1	CYP2B6
CYP2C19	CYP2C8	CYP2D6	CYP3A4	CYP3A5	CYP4B1	CYP4F2	DPYD	DYNC2H1
EGFR	ERCC1	ERCC2	FASTKD3	GSTM1	GSTP1	GSTT1	MTHFR	NQO1
NT5C2	NUDT15	RRM1	SEMA3C	SLC28A3	SLCO1B1	SOD2	TP53	TPMT
TYMS	UGT1A1	UMPS	XPC	XRCC1				'''],
    ]
    para += p.write(
        p.set(spacing=[0, 0.2], line=12),
        r_aiyi.text(' 基因检测列表', '小四', 1, wingdings=True, color='3EA6C2', space=True)
    )
    for gene_info in gene_infos:
        para += p.write(
            p.set(spacing=[0.2, 0.2], line=12),
            r_aiyi.text(gene_info[0], 10, weight=1)
        )
        trs1 = ''
        for items in gene_info[1].split('\n'):
            tcs1 = ''
            for t_index, t in enumerate(items.lstrip('\t').split('\t')):
                tcs1 += write_tc_weizhi({
                    'text': t.strip('\n').strip(),
                    'italic': True,
                    'size': '小五',
                    'w': (2.1 if t_index == 0 else 2) * 567,
                    'tcBorders': [],
                    'pPr': p.set(spacing=[0, 0])
                })
            trs1 += tr.write(tcs1)
        para += table_weizhi(trs1, ['top', 'bottom'], bdColor='3EA6C2')
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))

    para += write_chapter53(data)
    para += write_references()
    return para


def write_backcover():
    return ''


def write_read_guide():
    para = ''
    para += p.write(
        p.set(jc='center', spacing=[0, 1]),
        r_heiti.text('报告标识与颜色说明', '二号', 1)
    )
    figures1 = [
        {
            'cy': 0.51,
            'title': '证据等级说明',
            'f': [
                {"title": "A级：FDA/NCCN推荐级别", "text": '具体指以下两种情况：\n1、针对某一特定癌症，经过FDA批准的；\n2、针对某一特定癌种，专业指南推荐的；', 'rId': 'rIdA'},
                {"title": "B级：专家共识级别", "text": '具体指基于高水平研究，相关领域专家意见一致；', 'rId': 'rIdB'},
                {"title": "C级：临床证据级别", "text": '具体指以下三种情况：\n1、同一分子标志物，FDA批准用于其他癌症；\n2、作为临床试验纳入标准；\n3、多项小型研究形成的一些共识；', 'rId': 'rIdC'},
                {"title": "D级：临床前证据级别", "text": '具体指临床前研究或者少量案例报道，结果不确定。', 'rId': 'rIdD'},
            ],
            'tip': '以上为ASCO、AMP和CAP共同发布的证据级别定义，其中A级和B级证据相关变异为具有强烈临床意义的一类变异，C级和D级证据相关变异为具有潜在临床意义的二类变异。'
        },
        {
            'cy': 0.45,
            'title': '药物疗效预测说明',
            'f': [
                {"text": '可能耐药：xxxxxxxxxxxxxx', 'rId': 'rIdGray_block'},
                {"text": '可能无效：xxxxxxxxx', 'rId': 'rIdWhite_block'}
            ]
        }
    ]
    ind=[4, 4]
    for fig in figures1[:1]:
        para += h4_aiyi(fig['title'], spacing=[1.5, 0.5], ind=ind, jc='left', size='四号')
        for i in range(len(fig['f'])):
            item = fig['f'][i]
            text = item.get('text').split('\n')
            para += p.write(
                p.set(ind=ind, spacing=[0.8, 0]),
                r_heiti.text(item.get('title'), weight=1)
            )
            for t in text:
                para += p.write(
                    p.set(ind=[ind[0]+2.5, ind[1]], line=18, rule='exact'),
                    r_aiyi.text(t, '小五')
                )
        para += p.write(
            p.set(ind=ind, spacing=[0.8, 0]),
            r_aiyi.text(fig['tip'], '小五')
        )
    for fig in figures1[1:]:
        para += h4_aiyi(fig['title'], spacing=[1.5, 0.5], ind=ind, jc='left', size='四号')
        r_a = ''
        r_gray = ''
        left = 2.39
        cx = 0.6
        posy = -0.1
        kongge = [3, 5, 5, 4]
        lefts = [0, 1.97, 4, 5.72]
        for t_n, t in enumerate(level_tips_wz):
            level = t.get('text')
            r_a += r_aiyi.picture(cx, rId=level, wrap='undertext', posOffset=[left+lefts[t_n], posy])
            text2 = '%s%s' % (' ' * kongge[t_n], level)
            r_gray += r_aiyi.text(text2, '小二', color=white, space=True)
            r_gray += r_aiyi.picture(cx, rId='gray_block', wrap='undertext', posOffset=[left+lefts[t_n], posy+0.35])

        para += p.write(
            p.set(ind=ind, spacing=[0, 0]),
            r_heiti.text('可能有效：证据为阳性', weight=1)
        )
        para += p.write(
            p.set(line=18, ind=[ind[0]+2.5, ind[1]]),
            r_aiyi.text('具体指相关药物可能敏感或有效果，图示如下：', '小五')
        )
        para += p.write(
            p.set(line=18, ind=ind),
            r_a
        )
        para += p.write(
            p.set(ind=ind, spacing=[0, 0]),
            r_heiti.text('可能耐药：证据为阳性', weight=1)
        )
        para += p.write(
            p.set(line=12, ind=[ind[0]+2.5, ind[1]]),
            r_aiyi.text('具体指相关药物可能耐药或超进展，图示如下：', '小五')
        )
        para += p.write(
            p.set(line=12, ind=ind),
            r_gray
        )
        para += p.write(
            p.set(ind=ind, spacing=[0, 0]),
            r_heiti.text('可能无效：证据为阴性', weight=1)
        )
        para += p.write(
            p.set(line=18, ind=[ind[0]+2.5, ind[1]]),
            r_aiyi.text('     具体指相关药物可能无效或效果较差', '小五', space=True) +
            r_aiyi.picture(cx, rId='white_block', wrap='undertext', posOffset=[left, 0.1])
        )
        # para += p.write(
        #     p.set(line=18, ind=ind),
        #     r_aiyi.text('表示相应级别证据阳性，提示相关药物可能耐药或者超进展', '小五')
        # )
        # para += p.write(
        #     p.set(line=18, ind=ind),
        #     r_white
        # )
        # para += p.write(
        #     p.set(line=18, ind=ind),
        #     r_aiyi.text('表示相应级别证据阴性，提示相关药物可能无效或效果较差', '小五')
        # )
    para += h4_aiyi('基因变异说明', spacing=[1.5, 0.5], ind=ind, jc='left', size='四号')
    para += p.write(p.set(ind=[ind[0]+2.5, ind[1]]),
                    r_aiyi.text(' ', space=True, fill=red, size='二号')
                    + r_aiyi.text('  提示该基因变异事件阳性', '小五', space=True))
    para += p.write(p.set(sect_pr=set_page('A4', footer='rIdReport_time', header='rIdHeader2')))
    return para


def write_common_diagnosis(data):
    # https://mubu.com/doc/VQgYbsTdC
    diagnosis = data.get('diagnosis')
    if diagnosis == '非小细胞肺癌':
        d_genes = [
            {'db': 'variant_stars', 'gene': 'EGFR', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'KRAS', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'BRAF', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'HER2', 'text': '突变'},
            {'db': 'sv_stars', 'gene': 'ALK', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'ROS1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'RET', 'text': '融合'},
            {'db': 'cnv_stars', 'gene': 'MET', 'text': '扩增'},
            {'db': 'variant_stars', 'gene': 'MER', 'text': ' exon14 skipping'},
            {'db': 'sv_stars', 'gene': 'NTRK1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK3', 'text': '融合'},
        ]
    elif diagnosis == '结直肠癌':
        #  KRAS、NRAS野生型,  都没有发生突变的话，A级推荐西妥昔单抗和帕尼单抗
        d_genes = [
            {'db': 'variant_stars', 'gene': 'KRAS', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'NRAS', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'BRAF', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'PIK3CA', 'text': '突变'},
            {'db': 'cnv_stars', 'gene': 'HER2', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'MET', 'text': '扩增'},
            {'db': 'sv_stars', 'gene': 'ALK', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'ROS1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK3', 'text': '融合'},
        ]
    elif diagnosis == '乳腺癌':
        d_genes = [
            {'db': 'cnv_stars', 'gene': 'HER2', 'text': '扩增'},
            {'db': 'variant_stars', 'gene': 'PIK3CA', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'BRCA1', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'BRCA2', 'text': '突变'},
            {'db': 'cnv_stars', 'gene': 'FGFR1', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'FGFR2', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'FGFR3', 'text': '扩增'},
            {'db': 'sv_stars', 'gene': 'NTRK1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK3', 'text': '融合'},
        ]
    elif diagnosis == '胃癌':
        d_genes = [
            {'db': 'cnv_stars', 'gene': 'HER', 'text': '扩增', 'gene1': 'ERBB2'},
            {'db': 'cnv_stars', 'gene': 'MET', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'FGFR1', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'FGFR2', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'FGFR3', 'text': '扩增'},
            {'db': 'variant_stars', 'gene': 'CDH1', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'KRAS', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'ARID1A', 'text': '突变'},
            {'db': 'sv_stars', 'gene': 'NTRK1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK3', 'text': '融合'},
        ]
    elif diagnosis == '黑色素瘤':
        d_genes = [
            {'db': 'variant_stars', 'gene': 'BRAF', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'NRAS', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'NF1', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'KIT', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'PDGFRA', 'text': '突变'},
            {'db': 'sv_stars', 'gene': 'NTRK1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK3', 'text': '融合'},
        ]
    elif diagnosis == '胃肠道间质瘤':
        d_genes = [
            {'db': 'variant_stars', 'gene': 'KIT', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'PDGFRA', 'text': '突变'},
            {'db': 'sv_stars', 'gene': 'NTRK1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK3', 'text': '融合'},
        ]
    elif diagnosis == '胰腺癌':
        d_genes = [
            {'db': 'variant_stars', 'gene': 'KRAS', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'BRCA1', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'BRCA2', 'text': '突变'},
            {'db': 'sv_stars', 'gene': 'NTRK1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'NTRK3', 'text': '融合'},
        ]
    elif diagnosis == '胆道肿瘤':
        d_genes = [
            {'db': 'sv_stars', 'gene': 'FGFR1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'FGFR2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'FGFR3', 'text': '融合'},
            {'db': 'cnv_stars', 'gene': 'FGFR1', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'FGFR2', 'text': '扩增'},
            {'db': 'cnv_stars', 'gene': 'FGFR3', 'text': '扩增'},
        ]
    elif diagnosis in ['膀胱癌', '尿路上皮癌', '膀胱/尿路上皮癌']:
        d_genes = [
            {'db': 'sv_stars', 'gene': 'FGFR1', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'FGFR2', 'text': '融合'},
            {'db': 'sv_stars', 'gene': 'FGFR3', 'text': '融合'},
            {'db': 'variant_stars', 'gene': 'FGFR1', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'FGFR2', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'FGFR3', 'text': '突变'},
        ]
    elif diagnosis in ['卵巢癌', '输卵管癌', '卵巢癌/输卵管癌']:
        # BRCA1胚系（体细胞）突变BRCA2胚系（体细胞）突变
        d_genes = [
            {'db': 'variant_stars', 'gene': 'BRCA1', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'BRCA2', 'text': '突变'},
        ]
    elif diagnosis in ['子宫内膜癌']:
        # 子宫内膜癌
        # PTEN突变
        # PIK3CA突变
        # POLE突变
        d_genes = [
            {'db': 'variant_stars', 'gene': 'PTEN', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'PIK3CA', 'text': '突变'},
            {'db': 'variant_stars', 'gene': 'POLE', 'text': '突变'},
        ]
    elif diagnosis in ['脑胶质瘤']:
        # 脑胶质瘤
        # IDH1突变
        # 1p19q共缺失
        # TERT启动子突变未检测
        # MGMT甲基化未检测
        d_genes = [
            {'db': 'variant_stars', 'gene': 'IDH1', 'text': '突变'},
            {'db': 'variant_stars', 'gene': '1p19q', 'text': '共缺失'},
            {'db': 'variant_stars', 'gene': 'TERT', 'text': '启动子突变'},
            {'db': 'variant_stars', 'gene': 'MGT', 'text': '甲基化'},
        ]
    else:
        return '', ''
    d_items = []
    for d_item in d_genes:
        jihe = data[d_item.get('db')]
        g = d_item.get('gene')
        g1 = d_item.get('gene1') or g
        text = d_item.get('text')
        d_items2 = filter(lambda x: x.get('gene') == g1 or (x.get('gene1') and x.get('gene1').split('(') == g), jihe)
        fill = ''
        d_text = g + text
        if len(d_items2) > 0:
            fill = red
            if g == 'MER' and diagnosis == '非小细胞肺癌':
                d_text = 'MET exon 14 skipping 阳性'
        else:
            d_text = g + '未发生' + text
            if g == 'MER' and diagnosis == '非小细胞肺癌':
                d_text = 'MET exon 14 skipping 未发生'
        item = {'text': d_text, 'fill': fill}
        if item not in d_items:
            d_items.append(item)
    paras = ''
    tip = '%s常见癌种驱动基因检测结果说明:' % diagnosis
    col = 4
    items2 = []
    for i in range(0, len(d_items), col):
        items2.append(d_items[i: i+col])
    paras += write_mingan(items2, col)
    return tip, paras


def write_hrd(sequencing_type, data, ind):
    paras = ''
    p_set = p.set(line=15, spacing=[0, 0.5])
    index = 1
    variant_stars = data.get('variant_stars')
    paras_hr, items_hr = write_genes_hr(variant_stars)
    text = '在临床试验中，NOVA研究中发现，在铂类敏感的复发高级别卵巢癌中，HRD评分高的患者，PARP抑制剂niraparib治疗组相比安慰剂组，PFS为12.9m vs 3.8m（PMID：27717299）。然而，HRD评分并非总能预测PARP抑制剂治疗效果，今年ASCO上报道的GeparOLA研究发现，HRD评分高、BRCA1/2突变的早期乳腺癌患者中，奥拉帕尼组与化疗组（卡铂联合紫杉醇）疗效类似，（pCR率55.1% vs 48.6%（2019 ASCO abstract 506）。'
    if 'panel' not in sequencing_type.lower():
        paras += h4_aiyi('HRD评分说明', **outline3)
        index += 1
        paras += p.write(p_set, r_aiyi.text('奥拉帕尼等PARP抑制剂主要通过协同致死的方式对肿瘤细胞起到杀伤作用，同源重组修复缺陷HRD是PARP抑制剂发挥作用的生物学基础。由于HRD涉及到多个基因的突变、甲基化等多种状态，目前无法直接检测，HRD评分通过检测肿瘤基因组的三个特征杂合性缺失（LOH）、端粒等位基因不平衡（TAI），和大规模的状态转换（LST）作为HRD的标志物。HRD评分为LOH、TAI和LST三个评分的总和，既往回顾性研究将HRD评分＞42作为HRD状态的阈值。（注：本检测采用WES数据评估HRD评分，与通过SNP芯片或者专门设计的捕获芯片检测的结果有少量差异。', 9))
        text += 'HR通路相关基因变异与肿瘤的HRD状态密切相关。'
    else:
        tip = ''
    paras += paras_hr
    paras += h4_aiyi(' 检测意义', **outline3)
    paras += p.write(p_set, r_aiyi.text(text, 9))
    return paras, items_hr


def filter_sv(x):
    # only_pr=-1时，somatic，其他为candidate
    only_pr = x.get('only_pr')
    add_star = x.get('add_star')
    if add_star > 0:
        return True
    if only_pr != -1:
        reads_support = x.get('reads_support')
        fusion = x.get('fusion') or ''
        # 支持reads数≥10
        # 且
        # 融合列包含Protein Fusion: in frame、Protein Fusion: mid-exon或者Protein Fusion: out of frame这三种情况的任一情况
        if reads_support >= 10 and (
                'Protein Fusion: in frame' in fusion or
                'Protein Fusion: mid-exon' in fusion or
                'Protein Fusion: out of frame' in fusion
        ):
            return True
    return False


def write_explains(content, p_set=None):
    para = ''
    if p_set is None:
        p_set = p.set(line=1, rule='exact')
    for text in content.split('\n'):
        if text.strip():
            texts = text.split('：')
            if len(texts) > 1:
                para += write_explain({'title': '%s：' % texts[0], 'text': '：'.join(texts[1:])}, p_set=p_set)
            else:
                para += p.write(p_set, r_aiyi.text(text))
    return para


def write_chapter13(cat):
    p_set = p.set()
    para = h4_aiyi(cat=cat, **outline21)
    para += h4_aiyi('靶向治疗与驱动基因', **outline3)
    para += p.write(p_set, r_aiyi.text('靶向治疗药物是针对特定的肿瘤发生发展相关特定基因设计的药物。传统化疗主要针对快速分裂的细胞，既杀伤肿瘤细胞、又杀伤正常细胞，毒副作用大，而靶向治疗更精准的针对肿瘤特定特征或者肿瘤微环境，所以毒副作用相对较低。', '小五'))
    para += p.write(p_set, r_aiyi.text('实际临床应用中，靶向药初步可以分成针对肿瘤抗血管生成及多靶点相关的靶向药和针对肿瘤细胞特定基因变异的靶向药。抗血管生成及多靶点相关的靶向药现阶段大多没有特定的基因变异可以预测其疗效。针对肿瘤细胞特定基因变异的靶向药，一般情况下仅对该类突变患者有效。此类特定基因，包含在肿瘤驱动基因范畴中。', '小五'))
    para += h4_aiyi('驱动基因及突变形式说明', **outline3)
    para += h4_aiyi('a. 驱动基因说明', **outline4)
    para += p.write(p_set, r_aiyi.text('在肿瘤发生发展中扮演重要角色，能够“驱动”癌症疾病进程的基因称为驱动基因。乘客基因则是指对肿瘤发生发展重要性不高的基因，但是，重要性目前只是一个相对概念而不是绝对概念，所以，虽目前有多种方式进行驱动基因的鉴定，但是并没有统一的完整标准。驱动基因又分成发生激活突变后具有促进癌症发生发展的原癌基因和功能正常情况下抑制癌症发生的抑癌基因。驱动基因上的基因变异，可以是驱动突变，也可以是乘客突变。驱动突变可以是原癌基因的激活突变，也可以是抑癌基因的失活突变。一般情况下，肿瘤靶向治疗针对驱动基因中的原癌基因激活突变进行抑制，如EGFR Tkis抑制EGFR突变，或者针对抑癌基因的失活突变进行相关信号通路的协同致死，如PARP抑制剂治疗BRCA1、2基因变异肿瘤。', '小五'))
    para += h4_aiyi('b. 原癌基因和激活突变', **outline4)
    para += p.write(p_set, r_aiyi.text('原癌基因指正常功能情况下，在细胞信号传导等多个层面扮演重要角色，但是发生激活突变后会促进癌症发生发展的基因。激活突变一般情况下发生在原癌基因经常发生突变的热点位置上，如下图的PIK3CA和IDH1基因，且突变以错义突变为主。', '小五'))
    para += h4_aiyi('c. 抑癌基因和失活突变', **outline4)
    para += p.write(
        p.set(spacing=[0, 0]),
        r_aiyi.text('抑癌基因指正常功能下，扮演着DNA修复等抑制癌症发生发展过程的基因。抑癌基因发生失活突变会导致身体抑制癌症的功能降低。抑癌突变一般情况下热点突变较少，可发生在基因近乎任何区域，如下图的RB1和VHL基因，且会出现更多的截断突变。', '小五')
        # +r_aiyi.picture(10, rId='1.3.3', align=['center', ''], posOffset=[0, 3])
    )
    para += write_pic_center(10, '1.3.3')
    # para += p.write(p.set(jc='center', spacing=[0, 12]), run=r_aiyi.picture(13.34, rId='1.3.3', align=['center', '']))
    # para += p.write(p.set(sect_pr=set_page()))
    para += h4_aiyi('肿瘤数据解读证据级别说明', **outline3)
    para += p.write(p_set, r_aiyi.text('通过二代测序技术，特别是本报告采用的组学检测技术，每个肿瘤患者会找到几十个、几百个甚至于几千个肿瘤基因变异。不同基因变异具有不同的临床指导意义。美国临床肿瘤协会（ASCO）、美国病理学家联合学会会（CAP）和分子病理协会（AMP）共同发布了相关的标准和指南。该指南首先把变异根据临床意义等级分成四类：等级Ⅰ，强临床意义的变异；等级Ⅱ，潜在临床意义的变异；等级Ⅲ，不清楚临床意义的变异；等级Ⅳ，良性和可能良性的变异。其中，又根据变异的证据级别，等级Ⅰ和等级Ⅱ的变异进一步细化分成Level A、B、C、D四个级别。', '小五'))
    para += p.write(p_set, r_aiyi.text('Level A：1、针对某一特定癌症，经过FDA批准的；2，针对某一特定癌种，专业指南推荐的；', '小五'))
    para += p.write(p_set, r_aiyi.text('Level B：基于高水平研究，相关领域专家意见一致；', '小五'))
    para += p.write(p_set, r_aiyi.text('Level C：1、同一分子标志物，FDA批准用于其他癌症；2、作为临床试验纳入标准', '小五'))
    para += p.write(p_set, r_aiyi.text('Level D：临床前研究，结果不确定', '小五'))
    para += write_db_info(outline3, outline4)
    return para


def write_pic_center(cy, img_id):
    tc_pic = tc.write(
        p.write(
            run=r_aiyi.picture(cy=cy, rId=img_id, posOffset=[0, 0.5], align=['center', ''])
        ),
        tc.set(w_sum, tcBorders=[])
    )
    return table_weizhi(tr.write(tc_pic), [])


def write_chapter21(ch):
    para = ''
    info = ch.get('data')
    text = info.get('text')
    effect = info.get('effect')
    level = info.get('level')
    para += h4_aiyi(cat=ch.get('cat'), **outline21)
    para += write_immun_table([text, effect], level)
    para += write_pic_center(ch['cy'], ch['img_id'])
    if ch['note']:
        para += p.write(p.set(jc='center'), r_aiyi.text(ch['note'], size=8.5))
    for i in ch['infos']:
        para += write_explain_new(i)
    return para


def write_chapter_ddr(variants, diagnosis):
    ddr = write_genes_ddr(variants, diagnosis)
    para = write_immun_table([ddr['tr1'], ddr['tr2']], ddr['level']) + p.write()
    para += ddr['para']
    para += write_explain_new({'title': '结果说明', 'text': 'DDR基因突变患者更可能从免疫检查点抑制剂治疗中获益。细胞内正常的代谢活动与环境因素均会引起DNA损伤，初步估算，每个正常细胞每天产生1000-1000000处分子损伤。肿瘤细胞由于基因组等异常，大部分情况下DNA损伤的速率远高于正常细胞。DNA损伤反应基因主要包括错配修复、同源重组修复等DNA修复相关基因（DDR基因），也包括细胞周期检查点、染色质重塑等其他基因，据一篇专家手工注释研究表明，DDR基因大约有450个。DNA损伤反应跟免疫系统之间具有非同寻常的关系，如召集免疫细胞聚集，对T细胞杀伤更敏感等。以上是根据目前最新研究，将已有证据证明相关基因突变与免疫检查点疗效直接相关的DDR基因子集。该基因列表可能会随着DDR基因的研究进展逐步扩大。'})
    para += write_evidence_new([
        {
            'disease': '泌尿上皮癌',
            'title': 'DDR基因明确致病突变泌尿上皮癌患者PD1抗体治疗反应率为80%，意义未明突变患者有效率为54%（2018《JCO》）',
            'text': '60例泌尿上皮癌患者入组相关PD1抗体治疗前瞻性临床实验。DDR基因（共34个基因）突变患者28例（47%），其中明确致病突变患者15例（25%）。出现任意DDR基因突变的患者与更高的治疗反应率相关(67.9% v 18.8%; P<0.001)。 其中明确致病突变患者治疗反应率为80%，意义不明突变患者有效率为54%，显著高于DDR基因野生型患者（19%，P<0.001）(PMID：29489427)'
        },
        {
            'disease': '非小细胞肺癌',
            'title': '468例NSCLC患者研究发现DDR基因明确致病突变患者ICIs治疗ORR、PFS和OS均显著高于野生型患者（2019 Asco）',
            'text': '468例接受ICIs治疗和NGS检测的NSCLC患者中，242例患者DDR基因发生变异，其中74例定义为DDR阳性(DDR基因致病突变，分别为ATM(41.9%)、MLH1/MSH2/MSH6(18.9%)、BRCA1/2(16.2%)、CHEK1/2(9.4%)、FANC基因(9.4%)、BAP1(5.4%)、RAD基因(5.4%)、ERCC4/6(4.0%)、POLE(2.7%)、ATR(2.7%)，DDR阳性组的TMB中位值明显高于DDR阴性组(12.1 vs 9.8突变/MG, P = 0.007)。各组间PD-L1中位肿瘤比例评分差异无统计学意义(30% vs 25%， P = 0.33)。DDR阳性组(N = 394)相比DDR阴性组有明显高于客观缓解率(31.1%比19.1%,P = 0.03)、更长的平均无进展生存(4.3 vs 2.6个月, P = 0.02)和总生存期(16.3 vs 9.8个月, P = 0.009)。(2019 ASCO abstract 9077)'
        },
        {
            'disease': '前列腺癌',
            'title': '15例前列腺癌患者研究发现DDR基因明突变患者ICIs治疗PFS均显著高于野生型患者（2019 Asco）',
            'text': '在一项包含15例AR-V7阳性的前列腺癌前瞻性2期临床试验发现，6例患者出现DDR基因突变（3例BRCA2、2例ATm和1例ERCC4，明确致病突变和预测致病突变），DDR阳性组和阴性组在PFS水平具有显著差异。（ PFS (HR 0.31; P=0.01, 显著)， PSA-PFS (HR 0.19; P<0.01, 显著, PSA 反应 (33% vs. 0%; P=0.14, 非显著), ORR (40% vs. 0%; P=0.46,非显著)), , and OS (HR 0.41; P=0.11, 非显著)）（PMID:29983880 ）'
        }
    ])
    return para, ddr['tip'], ddr['tr1'], ddr['level']


def write_genes_ddr(variants, diagnosis):
    col = 9
    genes = [
        {
            'title': '同源重组修复基因', 'color': colors[0],
            'genes': ['BRCA1', 'MRE11A', 'NBN', 'RAD50', 'RAD51', 'RAD51B', 'RAD51D', 'RAD52', 'RAD54L']
        },
        {
            'title': '范可尼贫血通路基因', 'color': colors[1],
            'genes': ['BRCA2', 'BRIP1', 'FANCA', 'FANCC', 'PALB2', 'RAD51C', 'BLM']
        },
        {
            'title': '碱基切除修复基因', 'color': colors[2],
            'genes': ['ERCC2', 'ERCC3', 'ERCC4', 'ERCC5', 'ERCC6']
        },
        {
            'title': '错配修复基因', 'color': colors[3],
            'genes': ['MLH1', 'MSH2', 'MSH6', 'PMS1', 'PMS2']
        },
        {
            'title': '细胞周期检查点基因', 'color': colors[4],
            'genes': ['ATM', 'ATR', 'CHEK1', 'CHEK2', 'MDC1']
        },
        {
            'title': '其他基因', 'color': colors[5],
            'genes': ['POLE', 'MUTYH', 'PARP1', 'RECQL4', 'BAP1']
        }
    ]
    trs2 = ''
    ws = [int(3.6*567)] + [int(1.6*567)] * 9
    pPr = p.set(line=12, rule='auto', jc='center')
    reds = []
    oranges = []
    var_items = []
    for k in range(len(genes)):
        gene = genes[k]
        gene_list = gene['genes']
        gene_list += [''] * (col-len(gene_list))
        tcs = ''
        fill = ''
        if 'title' in gene:
            para = p.write(pPr, r_aiyi.text(gene['title'], size='小五', weight=1))
            tcs += tc.write(para, tc.set(w=ws[k], fill=RGB_to_Hex('233,233,233'), color=gray))
        for j in range(len(gene_list)):
            gene = gene_list[j]
            fill1, var_item = get_var_color_ddr(gene, variants, diagnosis)
            if var_item is not None and var_item not in var_items:
                var_items.append(var_item)
            color, text, var_text = '000000', gene, ''
            if fill1 not in ['', gray]:
                color = white
                if fill1 == red:
                    reds.append(gene)
                elif fill1 == red_lighter:
                    oranges.append(gene)
            para = p.write(pPr, r_aiyi.text(text, color=color, size='小五', fill=fill1, italic=True)) + var_text
            tcs += tc.write(para, tc.set(w=ws[j+1], fill=fill, color=gray))
        trs2 += tr.write(tcs, tr.set(trHeight=0.9*567))
    tr1 = 'DDR基因无变异'
    tr2 = 'PD1等免疫检查点抑制剂等免疫治疗可能不显著'
    tr11 = tr1
    level = ''
    tip = tr1
    if len(reds + oranges) > 0:
        tr1 = 'DDR基因中发现'
        if len(reds) > 0:
            tr1 += '%s基因突变' % ('、'.join(reds))
        if len(oranges) > 0:
            # 表示未明意义突变位点
            tr1 += '和%s未明意义突变' % ('、'.join(oranges))
        postfix = '' if len(reds + oranges) == 1 else '等事件'
        tip = 'DDR基因中发现%s突变%s' % (reds[0], postfix)
        tr11 = tr1 + '。'
        tr2 = 'PD1等免疫检查点抑制剂等免疫治疗可能有效'
        level = 'C'
        if diagnosis in ['泌尿上皮癌', '非小细胞肺癌', '前列腺癌']:
            level = 'C-同癌种证据'
        tr2 += '(%s)' % level
    paras = table_weizhi(trs2)
    paras += write_detail_table(var_items, [], [], '')
    return {'para': paras, 'tr1': tr11, 'tr2': tr2, 'tip': tip, 'level': level}


def write_genes_hr(variant_stars):
    col = 8
    genes = '''BRCA1	BRCA2	ATM	ATR	ATRX	NBN	PALB2	RAD50
    BARD1	BLM	BRIP1	CHEK1	CHEK2	RAD51C	RAD51D	RAD52
    FANCA	FANCC	FANCD2	FANCE	FANCF	RAD51	RAD51B	BAP1
    FANCG	FANCI	FANCL	FANCM	MRE11A	RAD54L	RPA1	WRN'''.split('\n')
    trs2 = ''
    ws = [(w_sum-400)/col] * col
    var_items = []
    for k in range(len(genes)):
        line = genes[k]
        gene_list = line.strip('\t').strip().split('\t')
        gene_list += [''] * (col-len(gene_list))
        tcs = ''
        fill = ''
        for j in range(len(gene_list)):
            gene = gene_list[j]
            fill1, tip, var_item = get_var_color(gene, variant_stars)
            color, text, var_text = '000000', gene, ''
            if fill1 not in ['', gray]:
                color = white
                if fill1 == red:
                    var_items.append(var_item)
            para = p.write(p_set_tr_center, r_aiyi.text(text, color=color, size=9, fill=fill1, italic=True)) + var_text
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, tcBorders=[]))
        trs2 += tr.write(tcs)
    if len(var_items) > 0:
        title = 'HR通路相关基因发现明确致病突变'
    else:
        title = 'HR通路相关基因未发现明确致病突变'
    trs2 = write_table_title(title, col) + trs2
    paras = table_weizhi(trs2)
    if len(var_items) > 0:
        paras += write_detail_table(var_items, [], [], '')
    return paras, var_items


def get_var_color_ddr(gene, vars, diagnosis=''):
    # 1.突变：加星  红色
    # 2.未明意义突变：未明意义突变显示规则（仅在癌种为泌尿上皮癌时呈现，其他癌种均不呈现）：①突变比例：肿瘤细胞比例≥50%，肿瘤细胞比例不可获得时，突变丰度vaf≥0.1
    # 【ccf_expected_copies_em】肿瘤细胞比例，
    # 【dna_vaf】突变丰度，
    for item in vars:
        if gene == item.get('gene'):
            add_star = item.get('add_star')
            if add_star > 0:
                return red, item
            if diagnosis == '泌尿上皮癌':
                ccf_expected_copies_em = item.get('ccf_expected_copies_em')
                if ccf_expected_copies_em is None:
                    dna_vaf = item.get('dna_vaf')
                    if dna_vaf >= 0.1:
                        return red_lighter, item
                if ccf_expected_copies_em >= 0.5:
                    return red_lighter, item
    return '', None


def write_chapter_mingan(stars, diagnose, ploidy):
    # 匹配规则：
    # 1、注意基因同名现象：PDL1基因在列表中应为CD274，PDL2基因应为PDCD1LG2，由驱动性加星过来；
    # 2、POLE和POLD1虽然均为抑癌基因，但是这两个基因为热点突变驱动，仅与数据库匹配的突变才是驱动突变，由驱动性加星过来；
    # 3、CDK12、TP53、KRAS、ATM、PBRM1、SMARCA4和ARID1A均为常规的驱动基因规则，由加星过来；  且满足二者之一
    #   ①，拷贝数为0，纯合缺失且肿瘤细胞比例大于80%以上时；
    #   ②、>90%、lcn_em = 0
    # 4、SERPINB3、SERPINB4和TET1这三个基因均为任意突变即可，但是对突变比例有限制：肿瘤细胞比例≥50%，肿瘤细胞比例不可获得时，突变丰度vaf≥0.1

    # 证据规则：
    # PDL1/2、基因扩增、 POLE/POLD1热点突变在任意癌种出现均为B级，其他所有基因均为C级，
    # 同时CDK12阳性且为前列腺癌时，呈现“C-同癌种证据”，
    # TP53合并KRAS突变、TP53合并ATM突变、ARID1A突变阳性且为非小细胞肺癌是，呈现“C-同癌种证据”；
    # PBRM1阳性且为肾癌时，呈现“C-同癌种证据”。

    genes_red = []
    tr1 = '免疫治疗敏感驱动基因无变异'
    tr2 = 'PD1等免疫检查点抑制剂可能效果不显著'
    var_items = []
    cnv_items = []
    # sv_items = [] 敏感未涉及到融合基因
    items00 = []
    items01 = []
    items02 = []
    items03 = []
    items04 = []
    items10 = []
    items11 = []
    items12 = []
    items13 = []
    items14 = []
    for star in stars:
        gene = star.get('gene')
        # gene = 'PDL1'
        ccf_expected_copies_em = star.get('ccf_expected_copies_em') or star.get('clone_proportion') # 肿瘤细胞比例
        tcn_em = star.get('tcn_em')  # 拷贝数
        lcn_em = star.get('lcn_em')  # 低拷贝数
        dna_vaf = star.get('dna_vaf')  # 突变丰度
        is_match3 = (tcn_em == 0 and ccf_expected_copies_em > 0.8) or (lcn_em == 0 and ccf_expected_copies_em > 0.9)
        is_match4 = (ccf_expected_copies_em is None and dna_vaf >= 0.1) or ccf_expected_copies_em >= 0.5
        if gene in ['PDL1', 'CD274']:
            if '1' not in items00:
                items00.append('1')
                cnv_items.append(star)
        if gene in ['PDL2', 'PDCD1LG2']:
            if '2' not in items00:
                items00.append('2')
                cnv_items.append(star)
        if gene in ['POLE', 'POLD1']:
            if gene not in items01:
                items01.append(gene)
                var_items.append(star)
        if gene in ['CDK12']:
            if is_match3:
                items02.append(gene)
        if gene in ['TP53', 'KRAS']:
            if gene not in items03:
                if is_match3:
                    if star not in var_items:
                        var_items.append(star)
                    items03.append(gene)
        if gene in ['TP53', 'ATM']:
            if gene not in items04:
                if is_match3:
                    if star not in var_items:
                        var_items.append(star)
                    items04.append(gene)
        if gene in ['PBRM1'] and gene not in items10:
            if is_match3:
                var_items.append(star)
                items10.append(gene)
        if gene in ['SMARCA4'] and gene not in items11:
            if is_match3:
                var_items.append(star)
                items11.append(gene)
        if gene in ['ARID1A'] and gene not in items12:
            if is_match3:
                var_items.append(star)
                items12.append(gene)
        if gene in ['SERPINB3', 'SERPINB4']:
            if gene[-1] not in items13:
                if is_match4:
                    var_items.append(star)
                    items13.append(gene[-1])
        if gene in ['TET1']:
            if gene not in items14:
                if is_match4:
                    var_items.append(star)
                    items14.append(gene)

    items21 = []
    level = ''
    if len(items00) == 0:
        items200 = {'text': 'PDL1/2基因未扩增', 'color': gray}
    else:
        text00 = 'PDL%s基因扩增' % ('/'.join(items00))
        items200 = {'text': text00, 'color': red}
        level = 'B'
        genes_red.append(text00)
    if len(items01) == 0:
        items201 = {'text': 'POLE/POLD1基因无热点突变', 'color': gray}
    else:
        text01 = '%s基因发生热点突变' % ('/'.join(items01))
        items201 = {'text': text01, 'color': red}
        level = 'B'
        genes_red.append(text01)
    if len(items02) == 0:
        items202 = {'text': 'CDK12基因未发生失活变异', 'color': gray}
    else:
        text02 = '%s基因发生失活变异' % ('/'.join(items02))
        items202 = {'text': text02, 'color': red}
        if diagnose == '前列腺癌':
            level = 'C-同癌种证据'
        genes_red.append(text02)
    if len(items03) < 2:
        for v_index, v in enumerate(var_items[::-1]):
            if v.get('gene') in ['TP53', 'KRAS']:
                del var_items[v_index]
        items203 = {'text': 'TP53合并KRAS突变未发生', 'color': gray}
    else:
        text03 = '%s突变发生' % ('合并'.join(items03))
        items203 = {'text': text03, 'color': red}
        if diagnose == '非小细胞肺癌':
            level = 'C-同癌种证据'
        genes_red.append(text03)
    if len(items04) < 2:
        for v_index, v in enumerate(var_items[::-1]):
            if v.get('gene') in ['TP53', 'ATM']:
                del var_items[v_index]
        items204 = {'text': 'TP53合并ATM突变未发生', 'color': gray}
    else:
        if diagnose == '非小细胞肺癌':
            level = 'C-同癌种证据'
        text04 = '%s突变发生' % ('合并'.join(items04))
        items204 = {'text': text04, 'color': red}
        genes_red.append(text04)
    items1 = [items10, items11, items12]
    for nn, gene3 in enumerate(['PBRM1', 'SMARCA4', 'ARID1A']):
        if len(items1[nn]) == 0:
            items21.append({'text': '%s基因未发生失活变异' % gene3, 'color': gray})
        else:
            text10 = '%s基因发生失活变异' % ('/'.join(items1[nn]))
            items21.append({'text': text10, 'color': red})
            if (gene3 == 'ARID1A' and diagnose == '非小细胞肺癌') or (gene3 == 'PBRM1' and diagnose == '肾癌'):
                level = 'C-同癌种证据'
            genes_red.append(text10)
    if len(items13) < 1:
        items213 = {'text': 'SERPINB3/4基因未发生突变', 'color': gray}
    else:
        text13 = 'SERPINB%s基因发生突变' % ('/'.join(items13))
        items213 = {'text': text13, 'color': red}
        genes_red.append(text13)

    if len(items14) < 1:
        items214 = {'text': 'TET1基因未发生突变', 'color': gray}
    else:
        text14 = '%s发生突变' % ('/'.join(items14))
        items214 = {'text': text14, 'color': red}
        genes_red.append(text14)
    items2 = [
        [items200, items201, items202],
        [items203, items204] + items21,
        [items213, items214]
    ]
    tip = tr1
    if len(genes_red) > 0:
        tr1 = '发现免疫治疗敏感相关%s' % concat_str(genes_red)
        tip = '发现免疫治疗敏感相关%s%s' % (genes_red[0], '' if len(genes_red) == 1 else '等事件')
        if level == '':
            level = 'C'
        tr2 = 'PD1等免疫检查点抑制剂等免疫治疗可能有效(%s)' % level
    data = [tr1, tr2]
    para = write_immun_table(data, level)
    para += p.write()
    para += write_mingan(items2, 3)
    para += write_detail_table(var_items, cnv_items, [], ploidy)
    para += write_explain_new({
        'title': '结果说明',
        'text': '多种肿瘤驱动基因变异状态与免疫检查点治疗疗效密切相关，'
                '且通过迥然不同的作用机制导致对免疫检查点治疗敏感。PDL1/2（'
                '该基因位于9p24.1，该区域同时具有PDL2和JAK2基因）扩增主要用肿瘤细胞内生性的PDL1/2高表达相关。'
                '既往研究发现，实体瘤中PDL1扩增是极其罕见的事件，发生率大约是0.7%，虽然目前仅少量案例报道，但是其有效率高达66.7%。'
                '同时，发病机制类似的霍奇金淋巴瘤是PD1治疗有效率最高（＞70%）的肿瘤类型，同样具有9p24.1扩增。'
                'POLE/POLD1是DNA聚合酶的亚基，均具有核酸外切酶结构域。热点突变与超高突变负荷相关，同事与免疫治疗敏感相关。'
                'CDK12双等位基因失活和缺失的前列腺癌患者基因组不稳定、局部串联重复增加、基因融合、新抗原负荷和T细胞浸润增加，'
                '能够从免疫检查点治疗中获益。TP53合并KRAS突变、TP53合并ATM突变则与高突变负荷、T细胞浸润增加相关。'
                'PBRM1、SMARCA4和ARID1A同属SWI/SNF染色质重塑复合物相关基因。'
                'SWI/SNF染色质重塑复合物通过调节基因组结构影响免疫治疗效果，相关基因的失活与免疫治疗敏感相关。'
                'SERPINB3/4是与自身免疫和过敏相关的卵清蛋白的同源基因，相关基因突变在肿瘤早期激发了免疫反应，'
                '进而能够被免疫检查点抑制剂重新激活。'
                'TET1是一个DNA去甲基化酶，是在21个与DNA甲基化密切相关的关键基因中突变频率最高的基因，'
                '且TET1突变在免疫检查点治疗反应组中显著富集。'
    })
    para += write_evidence_old([
        {
            'disease': '乳腺癌、头颈肿瘤、肺鳞癌等多种肿瘤与PDL1/2扩增',
            'title': '66.7% PDL1扩增实体瘤患者经免疫检查点治疗有效（2018《JAMA Oncology》）',
            'text': '118187例肿瘤样本中，PDL1扩增（该基因位于9p24.1，该区域同时具有PDL2和JAK2基因）患者共843例，发生率为0.7%，绝大多数（84.8%）PDL1扩增患者具有较低的TMB。PDL1扩增与免疫组化分析的PDL1表达并非完全相关。在一个单中心研究中，66.7%（9例患者中的6例）患者对免疫检查点治疗客观反应，所有治疗患者的中位PFS为15.2月，有效的患者包括脑胶质瘤1例（PFS≥5.2月），头颈肿瘤2例（PFS≥9和15.2月），转移性基底细胞癌2例（PFS为3.8和≥24.1月）和尿路上皮癌1例（PFS≥17.8月） (PMID：29902298) '
        },
        {
            'disease': '皮肤癌、子宫内膜癌、结直肠癌等多种肿瘤与POLE/POLD1突变',
            'title': 'POLE/POLD1突变免疫检查点治疗患者总生存期显著高于野生型患者（2019《JAMA Oncology》）',
            'text': 'cBioPortal数据库47721例肿瘤样本中，纳入包含错义、移码、终止、无终止、剪切位点等所有POLE/POLD1变异， 2.79%和1.37%的患者发生POLE和POLD1突变。在绝大多数肿瘤中，突变患者TMB显著高于野生型患者。纳入一个1644例经ICI治疗的队列研究发现，POLE或者POLD1突变患者总生存期显著高于野生型人群（34月vs 18月，p=0.004） (PMID：31415061)',
        },
        {
            'disease': '结直肠癌与POLE热点突变',
            'title': '四例POLE热点突变的高突变负荷结直肠癌患者对PD1抗体治疗反应为CR和PR（2019《JCO precision oncology》）',
            'text': '4例POLE热点突变（V411L和P286R）结直肠癌患者TMB为117-220/MB,其中2例患者为PDL1阴性，1例为PDL1弱阳性，经PD1抗体治疗后，两例患者为CR（缓解时间分别为28月和12月），两例患者为PR（缓解时间分别为14月和7月）。 (https://doi.org/10. 1200/PO.18.00214) '
        },
        {
            'disease': '脑胶质瘤与POLE热点突变',
            'title': '一例POLE胚系变异的脑胶质瘤患者对PD1抗体治疗影像学客观反应的案例报道（2016《Cancer Discovery》）',
            'text': '一例POLE胚系变异伴随高突变负荷多形性脑胶瘤患者经PD1治疗后发现颅内病灶影像学客观反应，进一步分析治疗后病灶发现大量的免疫细胞浸润。 (PMID：27683556) '
        },
        {
            'disease': '子宫内膜癌与POLE热点突变',
            'title': '一例POLE突变的子宫内膜癌患者对PD1治疗对PD1抗体治疗超预期反应（维持14个月）的案例报道（2016《JCI》）',
            'text': '一例POLE突变（V41L（外切酶区域）和R114*）的子宫内膜癌患者对PD1抗体治疗具有超预期（维持14个月）反应，该患者同时具有高突变复核。（PMID: 27159395）'
        },
        {
            'disease': '脑瘤、结肠癌等多种肿瘤与POLE/POLD1热点突变',
            'title': '特定POLE/POLD1热点突变与高突变负荷相关，是肿瘤的驱动因子（2017《CELL》）',
            'text': '该研究通过对将近10万例肿瘤样本测序数据进行分析发现，POLE、POLD1特定热点突变与高突变负荷相关，肿瘤的突变负荷情况可以作为POLE、POLD1基因驱动突变和乘客突变的区分指标。（PMID: 27159395）'
        },
        {
            'disease': '前列腺癌与CDK12基因纯合失活',
            'title': 'CDK12双等位基因失活和缺失的前列腺癌患者基因组不稳定、局部串联重复增加、基因融合、新抗原负荷和T细胞浸润增加，能够从免疫检查点治疗中获益（2018《CELL》）',
            'text': 'CDK12双等位基因失活和缺失的前列腺癌患者基因组不稳定、局部串联重复增加、基因融合、新抗原负荷和T细胞浸润增加，能够从免疫检查点治疗中获益。在11例CDK12突变患者中，4例患者进行了PD1抗体单药治疗，其中2例患者具有超乎寻常的的PSA反应（MSS患者一般对PD1抗体治疗不敏感）（PMID: 29906450）'
        },
        {
            'disease': '非小细胞肺癌与TP53合并KRAS突变',
            'title': '多项研究发现TP53合并KRAS突变非小细胞肺癌患者能够从免疫检查点治疗中获益（2018《CELL》）',
            'text': '多线研究发现， KRAS合并TP53突变的非小细胞肺癌患者中，PD-L1 的表达显著提高，T 细胞的浸润性和肿瘤免疫敏感性增强，能够从PD1治疗中获益（[PMID:28039262; PMID:29572005; PMID:29484144）'
        },
        {
            'disease': '非小细胞肺癌与TP53合并ATM突变',
            'title': 'TP53合并ATM突变与更高的TMB和经ICIs治疗后更好的OS和PFS相关（2019《JAMA Network Open》）',
            'text': '5个队列共计5781例NSCLC患者中发现TP53合并ATM突变与更高的TMB和经ICIs治疗后更好的OS和PFS相关,其中具有ICIs治疗患者有两个队列，共计1203例，具体生存数据如下：①、MSKCC ICIs治疗队列：TP53/ATM共突、TP53单独突变、ATM单独突变患者和无突变患者总生存期OS分别为未达到、14月、40月和22月，p=0.001；②、POPLAR和OAK队列：TP53/ATM共突、TP53单独突变、ATM单独突变患者和无突变患者中位PFS分别为10.4月、1.6月、3.5月和2.8月，p=0.01;中位OS分别为22.1月、8.3月.15.8月和15.3月，p=0.002（[PMID: 31539077）'
        },
        {
            'disease': '肾癌与PBRM1基因纯合失活',
            'title': 'PBRM1突变肾癌患者PD1抗体临床获益率更高（54.2% vs 24%）（2018《Science》）',
            'text': '在35例肾细胞癌中发现，SWI/SNF染色质重塑复合物相关基因PBRM1基因失活与PD1抗体单药治疗获益密切相关（p=0.012），同时进一步在一个65例的经PD1抗体单药或者PD1联合CTLA4治疗的肾细胞癌队列中得到验证（p=0.0071）。总体而言，PBRM1失活（双等位基因失活或者完全缺失）患者免疫检查点抑制剂治疗获益率为54.17%，而PBRM1野生型患者或疑虑为24%。（PMID: 29301960）'
        },
        {
            'disease': '肾癌与PBRM1基因失活变异',
            'title': 'PBRM1突变肾癌患者中PBRM1作为免疫检查点治疗反应标志物的临床验证及其局限性（2019《JAMA Oncology》；2018《Nature medicine》）',
            'text': '在一个证明既往接受过抗血管生成治疗后抗PD1治疗相比依维莫司显著改善总生存的三期临床实验的肾细胞癌队列中对其中382例（总队列共803例）患者进行基因分析发现，PBRM1突变与PD1治疗更高的临床获益（34.6% vs 19.7% p=0.04）、PFS增加（HR为0.67，P=0.03）和OS增加（HR=0.67，P=0.03）相关。然而值得注意的是，既往研究发现，PBRM1失活状态与抗血管生成疗效相关且未经抗血管生成治疗的肾细胞癌患者PBRM1失活状态与免疫检查点疗效无关（PMID: 31486842；PMID：29867230）'
        },
        {
            'disease': '非小细胞肺癌、类恶性横纹肌样瘤胸部肿瘤、高钙血型小细胞卵巢癌与SMARCA4纯合失活',
            'title': 'SMARCA4失活驱动的多种肿瘤PD1治疗有效的案例报道（2018《JNCI》；2019《Thoracic cancer》；2019《Annal of oncology》）',
            'text': '由SMARCA4失活的单基因疾病（低TMB）高钙血型小细胞卵巢癌，4例患者PD1抗体治疗有效（1例持续部分反应6个月；3例维持无疾病状态1.5年或者更长）。在11例样本中，绝大多数（8例）PDL1表达且具有强烈的T细胞浸润。1例SMARCA4完全失活（免疫组化阴性）、TMB相对较高（全外显子测序共找到396个突变，大约11个/Mb）的非小细胞肺癌部分反应，持续疾病控制时间超过14月。1例SMARCA4失活、PDL1阴性的胸部肿瘤经PD1抗体治疗11个月后，获得相对于基线高达-72%的PR（PMID:29365144；PMID:30972962; PMID:31114851）'
        },
        {
            'disease': '非小细胞肺癌与ARID1A基因失活变异',
            'title': 'ARID1A基因失活与NSCLC PDL1联合CTLA4治疗中位OS延长相关（2019 WCLC abstract；2018《Nature medicine》）',
            'text': '在一项三期临床试验MYSTIC研究（抗PDL1治疗durvalumab vs 抗PDL1联合CTLA4tremelimumab vs 铂类为基础的化疗）中，三组患者分别为374例、372例和372例，ARID1A突变患者在PDL1联合CTLA4治疗组中与中位OS延长相关（23.2月 vs 9.8月），然而在PDL1单药组和化疗组并未观察到类似现象（PDL1单药组为8.6月 vs 13.7月，化疗组为10.6月 vs 12.4月）。既往临床前研究发现，ARID1A失活导致ARID1A无法结合到MMR蛋白MSH2，增加突变频率，并且在ARID1A失活的卵巢癌小鼠模型中发现，PDL1抑制导致肿瘤负荷降低，以及带来相比于野生型小鼠更长的生存。（2019 WCLC abtract OA04.07；PMID：29736026）'
        },
        {
            'disease': '黑色素瘤与SERPINB3/4基因突变',
            'title': 'SERPINB3/4基因突变与黑色素瘤CTLA4和PD1抗体治疗疗效密切相关（2016《Nature Genetics》；2017《CELL》）',
            'text': '在俩个独立的黑色素瘤队列（174例）中发现，SERPINB3/4基因突变与黑色素瘤CTLA4抗体治疗疗效密切相关，多因素分析显示这两个基因突变与总生存密切相关且独立于突变负荷（队列1，HR为0.34，p=0.047；队列2，HR=0.32，p=0.01）。值得注意的是，TCGA未经免疫治疗的黑色素瘤队列中，SERPINB3/4基因突变与预后无关。另在一项针对未经CTLA4治疗，同时行PD1治疗的33例黑色素瘤患者研究发现，虽然SERPINB3/B4突变与治疗反应未能达到统计学显著性，但是6例突变患者中有5例患者达到疾病控制（CR/PR或者疾病稳定）。（PMID：27668655；PMID：29033130）'
        },
        {
            'disease': '皮肤癌、肺癌等多种肿瘤与TET1基因突变',
            'title': 'TET1基因突变与皮肤癌、肺癌等多种肿瘤免疫检查点治疗疗效密切相关（2019《Journal for ImmunoTherapy of Cancer》）',
            'text': '在21个与DNA甲基化密切相关的关键基因中，TET1突变在免疫检查点治疗反应组中显著富集。在发现组中（519例），TET1突变患者和野生型患者在客观缓解率（ORR，60.9% vs 22.8%，p＜0.001）、持续临床获益（DCB，71.4% vs 31.6%，p＜0.001）和无疾病进展生存期（PFS，HR=0.46，p=0.008）等各方面具有显著差异。在验证组中（1395例），相比于TET1野生型，TET1突变型患者具有显著的总生存获益（HR=0.47，p=0.019），而且与TMB、MSI和TET1突变的预后影响均完全独立（PMID：31623662）'
        }
    ])
    return para, tip, tr1, level


def write_chapter_naiyao(data, ploidy):
    # 匹配规则：
    # 1、EGFR、ALK、STK11、CTNNB1均为常规驱动基因阳性加星过来；
    # 2、PTEN、IFNGR1、IFNGR2、IRF1、B2M、JAK1、JAK2、APLNR满足以下条件之一才判断为阳性：
    #   ①，不考虑加星，拷贝数为0，纯合缺失且肿瘤细胞比例大于80%以上时；
    #   ②、“单核苷酸变异+小插入缺失”加星， 肿瘤细胞比例>80%、lcn_em = 0
    # 3. PIAS4、SOCS1：拷贝数变异页出现该基因且“变异状态”列结果为“AMP”时为阳性facets_call：变异状态
    # 证据规则：所有证据均显示为C类证据

    genes_red = []
    genes1 = 'EGFR、ALK、STK11、CTNNB1'.split('、')
    genes2 = 'PTEN、IFNGR1、IFNGR2、IRF1、B2M、JAK1、JAK2、APLNR'.split('、')
    tr1 = '免疫治疗耐药驱动基因无变异'
    tr2 = 'PD1等免疫检查点抑制剂治疗可能耐药风险较低'

    gene_names = [
        {'db': 'variant_stars', 'gene': ['EGFR'], 'text': '激活突变'},
        {'db': 'sv_stars', 'gene': ['ALK'], 'text': '融合'},
        {'db': 'variant_stars', 'gene': ['STK11'], 'text': '失活变异'},
        {'db': 'variant_stars', 'gene': ['CTNNB1'], 'text': '激活突变'},
        {'db': 'variant_list', 'gene': ['PTEN'], 'text': '纯合失活变异'},
        {'db': 'variant_list', 'gene': ['IFNGR1', 'IFNGR2'], 'text': '纯合失活变异'},
        {'db': 'variant_list', 'gene': ['IRF1'], 'text': '纯合失活变异'},
        {'db': 'variant_list', 'gene': ['B2M'], 'text': '纯合失活变异'},
        {'db': 'variant_list', 'gene': ['JAK1', 'JAK2'], 'text': '纯合失活变异'},
        {'db': 'variant_list', 'gene': ['APLNR'], 'text': '纯合失活变异'},
        {'db': 'cnvs', 'gene': ['PIAS4'], 'text': '扩增'},
        {'db': 'cnvs', 'gene': ['SOCS1'], 'text': '扩增'},
    ]
    genes = {}
    level = ''
    var_items = []
    cnv_items = []
    sv_items = []

    table_items = []
    for d_gene in gene_names:
        gene_names = d_gene.get('gene')
        db = d_gene.get('db')
        items = data.get(db) or []
        text = d_gene.get('text')
        arr1 = []
        arr2 = []
        n = d_gene.get('n') or 0
        for g in gene_names:
            items_matched = filter(lambda x: x.get('gene') == g or (x.get('gene1') and x.get('gene1').split('(')[0] == g), items)
            for item_matched in items_matched:
                ccf_expected_copies_em = item_matched.get('ccf_expected_copies_em') or item_matched.get('clone_proportion') # 肿瘤细胞比例
                tcn_em = item_matched.get('tcn_em')  # 拷贝数
                lcn_em = item_matched.get('lcn_em')  # 低拷贝数
                add_star = item_matched.get('add_star')
                is_match3 = (tcn_em == 0 and ccf_expected_copies_em > 0.8) or (add_star > 0 and lcn_em == 0 and ccf_expected_copies_em > 0.8)
                if g in genes1:
                    genes[g] = item_matched  # 阳性
                if g in genes2 and is_match3:
                    genes[g] = item_matched  # 阳性
                if g in ['PIAS4', 'SOCS1']:
                    # PIAS4、SOCS1：拷贝数变异页出现该基因且“变异状态”列结果为“AMP”时为阳性
                    facets_call = item_matched.get('facets_call')  # facets_call：变异状态
                    if facets_call == 'AMP':
                        genes[g] = item_matched
            if genes.get(g):
                arr1.append(g[-1])
            arr2.append(g[-1])

        action_name1 = '%s%s' % (gene_names[0][:-1], '/'.join(arr1))
        action_name2 = '%s%s' % (gene_names[0][:-1], '/'.join(arr2))
        if len(arr1) > n:
            text00 = '%s基因发生%s' % (action_name1, text)
            items200 = {'text': text00, 'color': red}
            genes_red.append(text00)
            for g2 in gene_names:
                g_item = genes.get(g2)
                if g_item:
                    if 'cnv' in db:
                        cnv_items.append(g_item)
                    elif 'sv' in db:
                        sv_items.append(g_item)
                    elif 'variant' in db:
                        var_items.append(g_item)
        else:
            items200 = {'text': '%s基因未发生%s' % (action_name2, text), 'color': gray}
        table_items.append(items200)

    tip = tr1
    if len(genes_red) > 0:
        tr1 = '免疫治疗耐药驱动相关%s' % concat_str(genes_red)
        tip = '免疫治疗耐药驱动相关%s%s' % (genes_red[0], '' if len(genes_red) == 1 else '等')
        level = 'C'
        tr2 = 'PD1等免疫检查点抑制剂治疗可能具有耐药风险(%s)' % level
    # level = 'C'
    para = write_immun_table([tr1, tr2], level, dark if level else '')
    para += p.write(p.set(line=1))
    col = 3
    para += write_mingan([table_items[i*col: (i+1) * col] for i in range(4)], col)
    para += write_detail_table(var_items, cnv_items, sv_items, ploidy)
    para += write_explain_new({'title': '结果说明',
                               'text': '免疫治疗耐药可以由多种因素引起，以上基因通过不同机制导致免疫治疗耐药。EGFR、ALK基因与TMB、PDL1表达较低有一定关系，CTNNB1基因则是通过影响枝状细胞招募进抗PD1治疗的耐药。B2M基因纯合失活突变，主要通过损害抗原提呈机制使免疫治疗耐药。JAK1、JAK2、IFNGR1、IFNGR2、IRF1、APLNR、PIAS3和SOCS等基因的纯合失活突变，则是通过损害效应T细胞杀伤肿瘤细胞的信号通路（γ干扰素通路）导致免疫治疗耐药。PTEN基因表达缺失或者纯合失活突变，则可能是通过影响T细胞浸润使免疫治疗耐药。'})
    para += write_evidence_old([
        {
            'disease': '非小细胞肺癌与EGFR、ALK变异',
            'title': 'NCCN等指南推荐免疫治疗用于EGFR、ALK阴性患者，现阶段证据不支持EGFR突变患者进行单药免疫治疗，多项早期临床试验显示EGFR TKIs联合免疫治疗效果不一，毒副作用大',
            'text': '目前的证据显示，EGFR突变患者对PD1/PDL1免疫检查点单药治疗反应不佳。一项针对比较nivolumab、pembrolizumab、atezolizumab和化疗药多西他赛二线治疗三项研究的Meta分析显示，EGFR突变患者使用免疫治疗不能带来OS的获益[18]。同样，Keynote001研究结果显示，pembrolizumab治疗PD-L1表达≥50%NSCLC中，EGFR野生型NSCLC患者的中位OS为15.7个月，ORR为40%，但在突变型患者中，中位OS仅为6.5个月，ORR仅为20%，EGFR突变型NSCLC使用免疫治疗的疗效明显劣于EGFR野生型患者，因此目前NCCN指南并不推荐EGFR突变NSCLC患者接受免疫治疗。目前有CheckMate012、NCT02013219、NCT0208812、KeyNote021、TATTON、CAURAL等多项早期临床试验报道了EGFR TKIs联合免疫治疗的结果，结果如下表罗列。由于临床试验规模均较小，无法得出明确结论，但是大致可以得到以下有待证实的推论：1、EGFR TKIs联合免疫治疗无法提高ORR，甚至可能会降低ORR，KeyNote021研究厄洛替尼联合帕博利珠单抗的有效率仅为41.7%，远低于其他临床试验厄洛替尼单药的70-80%，CAURAL研究也可以得到类似的结果；2、以NCT02013219研究和TATTON研究为例，未经EGFR TKIs治疗的患者，EGFR TKIs联合免疫治疗毒副作用发生比例大，其中吉非替尼和奥希替尼引起毒副作用的比例可能比厄洛替尼高；3、以KeyNote021厄洛替尼联合帕博利珠单抗为例，ORR降低但是PFS提高，CAURAL 也得到类似的结果，EGFR TKIs联合免疫治疗可能会延长患者PFS，延缓EGFR TKIs耐药的出现。（PMID：27765535；https://doi.org/10.1093/annonc/mdw594.005；Journal of Thoracic Oncology (2016) 11 (supplement 4): S57-S166. S1556-0864(16)X0004-4；PMID：30529597；https://doi.org/10.1016/S1556-0864(16)30246-5；PMID: 30763730）',
            'para': write_table_naiyao()
        },
        {
            'disease': '非小细胞肺癌与STK11基因失活',
            'title': 'STK11是独立于TMB和PDL1表达的非小细胞肺癌PD1抗体治疗耐药预测因子（2018《Cancer Discovery》）',
            'text': '在队列1（SU2C）中，KRAS合并STK11突变（KL）组、KRAS合并TP53（KP）组和KRAS单独突变（K-only）组PD1治疗客观缓解率分别为7.4% vs 35.7% vs 28.6%，p＜0.001。在队列2（Checkmate-057）中，三组则分别为0% vs 57.1% vs 18.2%，p=0.047。在肺腺癌中，STK11变异是在TMB较高或者高的亚组中，与PDL1阴性显著相关的标志物，进一步研究发现，STK11变异（突变或者表达缺失）对PD1治疗的影响在PDL1阳性的NSCLC一样可以观察到，在一组66例PDL1阳性患者的验证队列中，STK11突变（不管KRAS基因状态）与STK11完整的患者相比有效率显著降低（ORR，0% vs 34.5%， p=0.026）。STK11基因变异的耐药机制可能与趋化因子/细胞因子环境改变、效应T细胞代谢限制和抗原性损害等有关（PMID：29773717）'
        },
        {
            'disease': '肝癌与CTNNB1基因激活',
            'title': 'β-catenin活化提升免疫逃逸，导致肝细胞癌中抗PD1治疗耐药（2019《Cancer Discovery》）',
            'text': '动物模型证明，β-catenin (CTNNB1)通过影响枝状细胞招募进而导致肝细胞癌动物模型对抗PD1治疗耐药，进一步的临床观察发现，15例肝细胞癌患者进行抗PD1治疗，6名（40%）对治疗产生响应，3例CTNNB1突变的患者中，1例响应，2例无响应。（PMID：31186238）'
        },
        {
            'disease': '黑色素瘤与JAK1、JAK2和B2M的纯合失活',
            'title': 'JAK1、JAK2和B2M的纯合失活突变与PD1抗体治疗继发耐药有关（2016《NEJM》）',
            'text': '针对4名PD1抗体治疗原始有效，后续发生继发性耐药患者原发灶和复发病灶进行测序。患者1发生了一个JAK1 Q503*的纯合终止突变（55个复发病灶新发突变中出现的3个纯合突变）；患者2发生了一个纯合JAK2 F547的剪切突变（76个复发病灶新发突变中出现的唯一一个纯合突变），后续的RNA测序确认为功能失活突变。随后的细胞功能实验确认，JAK1/2失活突变通过γ干扰素通路导致免疫治疗耐药。患者3中发现了B2M 1号外显子的一个纯合移框突变（24个复发病灶新发突变中出现的唯一一个纯合突变），免疫组化发现相对于基线肿瘤，复发病灶中，MHC 1类重链缺乏膜外定位。患者4没有找到明确定义的基因变异。（PMID：27433843）'
        },
        {
            'disease': '黑色素瘤、结直肠癌与JAK1和JAK2的纯合失活突变',
            'title': 'JAK1、JAK2的纯合失活突变与PD1抗体治疗原发耐药相关（2017《Cancer Discovery》）',
            'text': '23名黑色素瘤患者中的1位，16位错配修复缺陷肠癌中的1位，分别出现JAK1（P429S，位于SH2结构域，VAF为0.71，很可能是纯合突变）和JAK2（W690*终止突变，VAF为0.94，伴随该基因区域正常基因的杂合缺失，为明确纯合突变）失活突变，虽然均具有高突变负荷，但是对PD1抗体治疗原发耐药。后续的细胞学实验证明，JAK1/2失活导致γ干扰素通路介导的PDL1表达增加的能力受到损害。（PMID：27903500）'
        },
        {
            'disease': '非小细胞肺癌与JAK2和B2M的纯合失活突变',
            'title': '单中心PD1治疗经验确认JAK2突变与耐药相关，但是B2M突变与预期结果不符合（2018《JCO》）',
            'text': '240例具有完整临床数据的PD1抗体治疗患者，经过二代测序分析，发现1例JAK2纯合突变导致原发耐药，但是1例B2M失活突变、高TMB的患者，PD1抗体治疗疗效评估为PR。（PMID：29337640）'
        },
        {
            'disease': '平滑肌肉瘤与PTEN的纯合失活突变',
            'title': '双等位基因PTEN缺失通过上调VEGFA和STAT3表达量导致PD1治疗耐药（2017《Immunity》）',
            'text': '在一例未经治疗的转移性平滑肌肉瘤患者，经PD1抗体单药治疗，经历两年的肿瘤完全缓解。针对原发灶和单发治疗抵抗转移灶的基因组多组学整合分析（外显子组和转录组），在16个继发突变中，PTEN双等位基因缺失（点突变合并杂合缺失）是唯一一个与致癌信号通路相关的突变，进一步的转录组表达量分析验证了之前的研究，PTEN缺失通过上调VEGFA和STAT3表达量导致PD1治疗耐药。进一步在TCGA数据库中241例未经治疗的肉瘤中分析发现，PTEN相关区域缺失和PTEN致癌突变共同出现的患者，STAT3表达量显著上调，而单独出现PTEN相关区域缺失或PTEN致癌突变的患者，则未能观察到相关现象。（PMID：29337640）'
        },
        {
            'disease': '黑色素瘤与PTEN的表达缺失',
            'title': 'PTEN表达缺失通过增加免疫抑制细胞因子表达量，降低肿瘤中T细胞浸润导致T细胞介导的免疫治疗耐药（2016《Cancer Discovery》）',
            'text': '对一组39名转移性黑色素瘤患者进行PD1抗体治疗，PTEN相比正常PTEN缺失（免疫组化，10%以下的肿瘤细胞表达定义为缺失）的患者，肿瘤缩小比例显著增加（P=0.029）。后续的细胞学实验和动物学实验证明，PTEN表达缺失通过增加免疫抑制细胞因子表达量，降低肿瘤中T细胞浸润导致T细胞介导的免疫治疗耐药（PMID：26645196）'
        },
        {
            'disease': '黑色素瘤、肺癌、膀胱癌等多种肿瘤与IFNγ通路基因缺陷',
            'title': 'IFNγ通路基因缺陷与（2016《Cancer Discovery》）',
            'text': 'IFNγ是宿主免疫反应的关键细胞因子，其通路基因状态与免疫检查点治疗疗效密切相关。在一个CTLA4治疗的黑色素瘤队列中发现，IFNγ通路基因缺陷（IFNGR1、IFNGR2、JAK2、IRF1基因缺失和IFNγ通路抑制基因SOCS1、PIAS4基因扩增）在耐药组中显著富集，且IFNγ通路基因缺陷组患者总生存时间显著长于野生型患者（p=0.0018）。另一项CRISPR筛查研究则发现IFNγ通路相关基因APLNR失活与免疫治疗耐药相关。一项包含黑色素瘤、肺癌、膀胱癌、头颈肿瘤等多种肿瘤共计249例经免疫检查点治疗的患者一样发现IFNγ通路基因缺陷中耐药组患者中显著富集（19/123 vs 3/70 p=0.019）（PMID：26645196）'
        }
    ])
    return para, tip, tr1, level


def write_chapter_chaojinzhan(data, ploidy):
    # 匹配规则：
    # 1、CDKN2A、CDKN2B、MDM2、MDM4、EGFR、11q13均为常规驱动基因阳性加星过来；
    # 2、DNMT3A为任意突变即可，但是对突变比例有限制：
    #   肿瘤细胞比例≥50%，肿瘤细胞比例不可获得时，突变丰度vaf≥0.1
    # 证据规则：
    # MDM2、MDM4、DNMT3A这三个基因的阳性，标注为 “PD1等免疫治疗抗体治疗可能具有超进展风险（D级）”
    # 其他都是  “PD1等免疫治疗抗体治疗可能具有超进展风险（C级）”
    variant_stars = data.get('variant_stars')
    cnv_stars = data.get('cnv_stars')
    genes_red = []
    genes1 = 'CDKN2A、CDKN2B、MDM2、MDM4、EGFR'.split('、')
    genes_11q13 = 'CCND1、FGF3、FGF4、FGF19'.split('、')
    DNMT3A = 'DNMT3A'
    genes = {}
    for star in variant_stars:
        gene = star.get('gene')
        # gene = 'PDL1'
        ccf_expected_copies_em = star.get('ccf_expected_copies_em') or star.get('clone_proportion') # 肿瘤细胞比例
        dna_vaf = star.get('dna_vaf')  # 突变丰度
        is_match2 = (ccf_expected_copies_em is None and dna_vaf >= 0.1) or (ccf_expected_copies_em >= 0.5)
        if gene == DNMT3A and is_match2:
            star['tip'] = '突变'
            genes[gene] = star  # 阳性
    for star in cnv_stars:
        gene = star.get('gene')
        if gene in (genes1 + genes_11q13):
            star['tip'] = '扩增'
            genes[gene] = star # 阳性

    level = ''
    var_items = []
    cnv_items = []
    sv_items = []

    def get_naiyao(gene_names, text, n=0):
        arr1 = []
        arr2 = []
        for g in gene_names:
            g_item = genes.get(g)
            if g_item:
                g_tip = g_item.get('tip') or ''
                if ('扩增' in text or '缺失' in text) and '扩增' in g_tip :
                    arr1.append(g[-1])
                elif '融合' in text and '融合' in g_tip:
                    arr1.append(g[-1])
                elif g_item.get('add_star') > 0:
                    arr1.append(g[-1])
            arr2.append(g[-1])
        action_name1 = '%s%s' % (gene_names[0][:-1], '/'.join(arr1))
        action_name2 = '%s%s' % (gene_names[0][:-1], '/'.join(arr2))
        if gene_names == genes_11q13:
            action_name1 = '11q13(CCND1、FGF3、FGF4、FGF19)'
            action_name2 = action_name1
        if len(arr1) > n:
            text00 = '%s基因发生%s' % (action_name1, text)
            items200 = {'text': text00, 'color': red}
            genes_red.append(text00)
            for g2 in gene_names:
                g_item = genes.get(g2)
                if g_item:
                    tip = g_item.get('tip') or ''
                    if '扩增' in text or '缺失' in text:
                        cnv_items.append(g_item)
                    elif '融合' in text:
                        sv_items.append(g_item)
                    elif tip:
                        var_items.append(g_item)
            # if '扩增' in text:
            #     cnv_items.append()
        else:
            items200 = {'text': '%s基因未发生%s' % (action_name2, text), 'color': gray}
        return items200
    items_11q13 = get_naiyao(genes_11q13, '扩增', 3)
    items2 = [
        get_naiyao(['CDKN2A', 'CDKN2B'], '缺失'),
        get_naiyao(['MDM2'], '扩增'),
        get_naiyao(['MDM4'], '扩增'),
        get_naiyao([DNMT3A], '突变'),
        get_naiyao(['EGFR'], '扩增'),
        items_11q13,
    ]
    tr1, tr2 = '免疫治疗超进展相关基因无变异', 'PD1等免疫检查点抑制剂可能无超进展风险'
    tip = tr1
    if len(genes_red) > 0:
        tr1 = '免疫治疗超进展相关%s' % concat_str(genes_red)
        tip = '免疫治疗超进展相关%s%s' % (genes_red[0].split('(')[0], '' if len(genes_red) == 1 else '等事件')
        level = 'C'
        if items2[1] or items2[2] or items2[3]:
            level = 'D'
        tr2 = 'PD1等免疫治疗抗体治疗可能具有超进展风险(%s)' % level
    # level = 'C'
    para = write_immun_table([tr1, tr2], level, dark if level else '') + p.write()
    col = 3
    para += write_mingan([items2[i*col: (i+1) * col] for i in range(2)], col)
    para += write_detail_table(var_items, cnv_items, sv_items, ploidy)
    para += write_explain_new({'title': '结果说明',
                               'text': '免疫治疗耐药可以由多种因素引起，以上基因通过不同机制导致免疫治疗耐药。EGFR、ALK基因与TMB、PDL1表达较低有一定关系，CTNNB1基因则是通过影响枝状细胞招募进抗PD1治疗的耐药。B2M基因纯合失活突变，主要通过损害抗原提呈机制使免疫治疗耐药。JAK1、JAK2、IFNGR1、IFNGR2、IRF1、APLNR、PIAS3和SOCS等基因的纯合失活突变，则是通过损害效应T细胞杀伤肿瘤细胞的信号通路（γ干扰素通路）导致免疫治疗耐药。PTEN基因表达缺失或者纯合失活突变，则可能是通过影响T细胞浸润使免疫治疗耐药。'})
    para += write_evidence_old([
        {
            'disease': '膀胱癌、乳腺癌、子宫内膜间质肉瘤等多种肿瘤与MDM2/4、EGFR等',
            'title': 'MDM2/MDM4明确与免疫治疗超进展相关，EGFR变异有较高可能性与超进展相关，DNMT3A有可能与超进展相关（2017《Clin Cancer Res》）',
            'text': '文献中超进展定义：1、用药后出现明显进展，治疗失败时间（TTF）＜2个月；2、与治疗前影像学相比肿瘤负荷增大50%；3、＞2倍的肿瘤进展速度。6位MDM2/MDM4患者中，所有人的TTF时间均小于2个月，其中4名患者为严格定义的超进展患者，出现肿瘤明显增大（55%-258%）和显著的进展加速（2.3倍、7.1倍、7.2倍和42.3倍）。10名EGFR变异的患者中，8名患者（单独EGFR扩增 2名、合并EGFR扩增、突变4名、单独EGFR突变2名）TTF（治疗至失败时间）小于两个月，其中两名患者（单独EGFR突变1名，EGFR扩增、突变合并1名）出现严格定义的超进展（36倍和42倍于2个月治疗前肿瘤负荷进展速度，分别增大53.6%和125%）。4名DNMT3A变异（突变或扩增）患者中，3名患者TTF小于2个月。（PMID：28351930）'
        },
        {
            'disease': '肺癌、食管癌和肾癌与MDM2/4、EGFR和11q13基因扩增',
            'title': '4名超进展患者出现中MDM2/4扩增、EGFR扩增和11q13扩增事件（2017 ESMO abstrat）',
            'text': '文献中超进展定义：1、接受PD-1抗体治疗后第一次复查CT，就出现了疾病进展；2、肿瘤大小增大了50%；3、肿瘤生长速度增快了2倍以上的患者。66%（2/3）的MDM2/MDM4扩增患者，50%（1/2）的EGFR扩增患者和43%（3/7）的11q13扩增（CCND1、FGF33/4/9同时存在）出现超进展。（ESMO abstract：Singavi A K,et al. [J]. Annals of Oncology, 2017, 28(suppl_5).）'
        },
        {
            'disease': '非小细胞肺癌与MDM2/4基因扩增',
            'title': 'MDM2/4基因扩增不一定与超进展相关（2018《JCO》）',
            'text': '240名具备完整资料的免疫检查点抑制剂治疗患者中，8名患者出现DMD2/DMD4扩增，但是中位无疾病进展生存期与总体数据与其他患者并没有明显差异。（PMID：29337640）'
        },
        {
            'disease': '非小细胞肺癌与MDM2基因扩增、CDKN2A/B缺失',
            'title': '5例NSCLC超进展患者中1例为MDM2扩增，4例为CDKN2A/B缺失，非超进展患者无相关基因变异（2019 ASCO abstrat）',
            'text': '在20例患者中，其中5例患者出现了超进展，研究者采用NGS、IHC、FISH检测这些患者的基因。5例出现超进展的患者NGS 分析显示, 1 例HPD患者 MDM2 扩增, 4 例患者CDKN2A/B缺失。另外，非超进展患者中IHC分析没有检测到MDM2基因或蛋白的扩增，NGS 分析也没有发现 MDM2 和/或CDKN2A基因改变。5例NSCLC超进展患者中，1例MDM2扩增，4例患者CDKN2A/B缺失，其他非超进展患者无相关变异（J Clin Oncol 37, 2019 (suppl; abstr e2)'
        },
        {
            'disease': '非小细胞肺癌与MDM2/4基因扩增',
            'title': 'MDM2/4基因扩增与超进展无关（2019《Clin Cancer Res》）',
            'text': '187例经ICI治疗的NSCLC患者中发现39例（25.7%）超进展患者。超进展组11例患者，非超进展组17例患者共获得30例FFPE组织，通过FISH检测MDM2/4发现，超进展组发现3例患者扩增（2 MDM2、1 MDM4），非超进展组发现6例扩增（4例MDM2、1例MMD4和1例MDM2合并MDM4），MDM2/4扩增与超进展无关。（PMID：30206165）'
        }
    ])
    return para, tip, tr1, level


def write_chapter_hla(overview, diagnosis):
    hla1 = [' ']
    for k in overview.keys():
        if k.startswith('hla_'):
            hla1.append(overview[k])
    # print 'hla', data
    if len(hla1) == 0:
        return '', '', '', ''
    # HLA分型结果中，A、B、C三个等位基因均为杂合状态（合并）具有免疫治疗疗效较好的HLA-B44超型，提示PD1等免疫检查点抑制剂可能有效
    # HLA分型结果中，具有免疫治疗较差的HLA-B66超型，提示PD1等免疫检查点抑制剂可能效果不显著
    # HLA分型结果中，具有免疫治疗较差的HLA-B15:01，提示PD1等免疫检查点抑制剂可能效果不显著
    # 可能有效
    #   HLA分型结果中发现A、B、C三个等位基因均为杂合状态且具有免疫治疗敏感超型HLA-B44
    # 可能耐药（纯合或者出现耐药超型且不出现敏感超型）
    #   HLA分型结果中发现等位基因纯合现象
    #   HLA分型结果中发现等位基因纯合现象、免疫治疗耐药超型HLA-B66、免疫治疗耐药分型HLA-B15:01
    #   HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药超型HLA-B66
    #   HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药分型HLA-B15:01
    #   HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药超型HLA-B66、免疫治疗耐药分型HLA-B15:01
    # 可能无效（其他所有情况：如单纯杂合、如杂合且出现耐药超型且出现敏感超型、如杂合同时出现）
    # hla1 = 'HLA-A32:01 | HLA-A24:02 | HLA-B44:03 | HLA-B39:01 | HLA-C07:02 | HLA-C04:01'.split(' | ')
    hla1.sort()
    item = []
    naiyaos = []
    mingan = False
    for d in hla1:
        if d.strip().startswith('HLA'):
            text = d.split('-')[1].replace('*', '')
            if text.startswith('B66'):
                naiyaos.append('免疫耐药超型HLA-B66')
            if text.startswith('B15:01'):
                naiyaos.append('免疫治疗耐药分型HLA-B15:01')
            if text.startswith('B44'):
                # 具有免疫治疗敏感超型HLA-B44
                mingan = True
            item.append(text)
    if len(item) < 6:
        print 'please check overview: hla.., you may lose something.'
        return '', '', '', ''
    b1 = item[2]
    b2 = item[3]
    is_zahe = item[0] != item[1] and b1 != b2 and item[4] != item[5]
    level = ''
    tip2s = ['A、B、C三个等位基因%s' % ('均为杂合状态' if is_zahe else '发现等位基因纯合现象')] + naiyaos
    tip2 = '、'.join(tip2s)
    youxiao = False
    fill = ''
    color = ''
    if is_zahe and mingan and ('B15:01' not in [b1, b2]):
        # HLA分型结果中发现A、B、C三个等位基因均为杂合状态
        # 且
        # 有免疫治疗敏感超型HLA-B44
        # 且
        # 不出现耐药分型B15:01
        tip1 = 'PD1等免疫检查点抑制剂可能有效'
        level = 'C'
        if diagnosis in ['非小细胞肺癌', '黑色素瘤']:
            level = 'C-同癌种证据'
        tip1 += '(%s)' % level
        tip2 = 'HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗敏感超型HLA-B44'
        tip2s.append('免疫治疗敏感超型HLA-B44')
        youxiao = True
        fill = level_tips_wz[2].get('color')
        color = white
    elif is_zahe is False or (len(naiyaos) > 0 and is_zahe and mingan is False) :
        # 可能耐药（纯合或者出现耐药超型、分型且不出现敏感超型）
        # HLA分型结果中发现等位基因纯合现象
        # HLA分型结果中发现等位基因纯合现象、免疫治疗耐药超型HLA-B66、免疫治疗耐药分型HLA-B15:01
        # HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药超型HLA-B66
        # HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药分型HLA-B15:01
        # HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药超型HLA-B66、免疫治疗耐药分型HLA-B15:01
        tip1 = 'PD1等免疫检查点抑制剂治疗可能具有耐药风险'
        fill = gray
    else:
        tip1 = 'PD1等免疫检查点抑制剂可能效果不显著'
        fill = ''

    texts = []
    for j in range(3):
        h1 = item[j * 2]
        h2 = item[j * 2+1]
        texts.append({'text': 'HLA-%s HLA-%s' % (h1, h2), 'w': w_sum/3})
    postfix = '' if len(tip2s) == 1 else '等'
    postfix1 = '' if len(tip2s) < 2 else '事件'
    # tip0 = tip2 if youxiao else ('HLA分型结果中发现%s%s%s' % (tip2s[0] if len(tip2s) < 2 else tip2s[1] , postfix, postfix1))
    tip0 = ('HLA分型结果中发现%s%s%s' % (tip2s[0] if len(tip2s) < 2 else tip2s[1] , postfix, postfix1))
    tip01 = 'HLA分型结果中发现%s%s' % ('、'.join(tip2s), postfix1)
    trs2 = write_tr1(tip2, '')
    trs2 += write_tr2(tip1, fill, color)
    para = table_weizhi(trs2) + p.write(p.set(line=4))
    trs3 = write_tr_weizhi(texts)
    para += table_weizhi(trs3)
    para += write_explain_new({'title': '结果说明', 'text': 'HLA分型与免疫治疗疗效高度相关。HLA(human lymphocyte antigen ，人类淋巴细胞抗原)，是编码人类的主要组织相容性复合体（MHC）的基因。HLA是免疫系统区分自身和异体物质的基础。HLA主要包括HLA Ⅰ类分子和Ⅱ分子。HLAⅠ类分子又进一步细化分成A、B、C三个基因。特定的超型，如HLA-B44，与免疫检查点抑制剂治疗疗效好相关；HLA-B66（包括HLA-B*15：01），与免疫检查点抑制剂治疗疗效差相关。HLA Ⅰ类三个基因均纯合，免疫检查点抑制剂治疗反应更好。HLA杂合缺失的基因相关的新抗原可能在个性化治疗疫苗或者特异性细胞治疗中无效。'})
    para += write_evidence4(2)
    return para, tip0, tip01, level


def write_chapter_signature(signature_etiology):
    tr1, tr2 = '', []
    s_dict = {}
    signature_etiology = signature_etiology[-30:]
    # signature_etiology = ["0.508231606547237", "0", "0", "0", "0", "0.0611274931509934", "0", "0", "0.190740860285723", "0", "0", "0", "0", "0", "0.129833061544803", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    for s_id, item in enumerate(signature_etiology):
        text = reset_sig(s_id+1)
        if text != '未知':
            arr = s_dict.get(text) or []
            arr.append(float(item))
            if text not in tr2:
                tr2.append(text)
            s_dict[text] = arr
            # print item, text
    pd1 = []
    prap = []
    tips = []

    for k in s_dict.keys():
        f = sum(s_dict[k])
        if f > 0.5:
            if k in ['APOBEC', u'吸烟', 'POLE', u'错配修复缺陷dMMR']:
                pd1.append(k)
            if k in [u'同源重组修复缺陷HRD']:
                prap.append(k)
        if f > 0:
            tips.append('%s(%s)' % (k, float2percent(f, 1)))
    tips.sort(key=lambda x: x.split('(')[-1], reverse=True)
    tr1 = '通过突变特征分析，该肿瘤'
    if len(tips) > 0:
        tr1 += '可能由%s等原因导致' % ('、'.join(tips))
    tr2 = '无相关治疗提示'
    level = ''
    tip = tr1
    if len(pd1) > 0:
        tr1 = '%s占据主导因素' % ('、'.join(pd1))
        tr2 = '提示PD1等免疫检查点抑制剂治疗可能有效'
        level = 'C'
        tip += ', %s, %s' % (tr1, tr2)
    if len(prap) > 0:
        tr1 = '同源重组修复缺陷HRD占据主导因素'
        tr2 = '提示奥拉帕尼等PARP抑制剂可能有效'
        level = 'C'
        tip += ''
    tip += ', %s' % tr2
    if level:
        tr2 += '(%s)' % level
    data = [tr1, tr2]
    para = write_immun_table(data, level)
    para += p.write()
    para += p.write(p.set(spacing=[2, 12]), r_aiyi.picture(cy=8, rId='signature_dict', posOffset=[0, 0.1], align=['center', '']))
    para += p.write(p.set(spacing=[2, 0]), r_aiyi.picture(7.5, rId='signature', posOffset=[0, 0.6]))
    para += write_explain({"title": '结果说明：', 'text': '体细胞突变存在于人体的所有细胞中并且贯穿整个生命。它们是多种突变过程的结果，包括DNA复制机制内在的轻微错误，外源或内源诱变剂暴露，DNA酶促修饰和DNA修复缺陷。不同的突变过程产生独特的突变类型组合，称为“突变特征”。在过去的几年中，大规模的分析研究揭示了许多人类癌症类型的突变特征。目前这组突变特征是基于对40种不同类型的人类癌症中的10,952个外显子组和1,048个全基因组的分析得到的。使用六个取代亚型显示每个标记的概况：C> A，C> G，C> T，T> A，T> C和T> G，进而向前先后各延伸一个碱基，每个碱基有4种可能，所以，总共就有96个三核苷酸的突变类型。现在已经明确的，总共有30种明确注释的“突变特征”，每种特征都有对应的发生机制，如吸烟、错配修复缺陷、同源重组修复缺陷等。'}, ind=[23, 0])
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % 6)))
    return para, tip, level


def write_chapter_yichuan():
    texts = '''共济失调性毛细血管扩张症	自身免疫性淋巴增生综合征	巨舌巨人综合征	Birt-Hogg-Dubé综合征
    Bloom综合征	Carney综合征	Cowden综合征	Diamond-Wiedemann贫血症
    家族性腺瘤性息肉病	家族性胃肠道间质瘤	Fanconi贫血	遗传性乳腺癌-卵巢癌综合征
    遗传性弥漫型胃癌	遗传性平滑肌瘤病肾癌	遗传性多发性骨软骨瘤	遗传性乳头状肾细胞癌
    遗传性前列腺癌	Howell-Evans综合征	甲状旁腺机能亢进-颌骨肿瘤综合征	幼年性息肉病综合征
    Li-Fraumeni综合征	Lynch综合征	皮肤恶性黑色素瘤	多发性内分泌腺瘤病1型
    多发性内分泌腺瘤病2型	MUTYH相关性息肉病	家族性神经母细胞瘤	神经纤维瘤病1型
    神经纤维瘤病2型	痣样基底细胞癌综合症	Nijmegen断裂综合征	遗传性副神经节瘤-嗜铬细胞瘤综合征
    Peutz-Jeghers综合征	PTEN错构瘤综合征	遗传性视网膜母细胞瘤	Rothmund-Thomson综合征
    结节性硬化症	Turcot综合征	von Hippel-Lindau综合征	Werner综合征（成人早衰症）
    家族性肾母细胞瘤	着色性干皮病'''
    items = texts.split('\n')
    tr1 = '在42种遗传性肿瘤综合征相关的162个基因中，未发现与遗传性肿瘤相关的明确致病突变位点'
    tr2 = '遗传性肿瘤相关基因变异可能在该肿瘤的发生发展中扮演次要角色'
    data = [tr1, tr2]
    para = write_immun_table(data)
    para += p.write()
    para += write_46(items, col=4)
    run = r_aiyi.text(' 红色 ', color=red, size=9, space=True)
    run += r_aiyi.text('，表示该遗传性肿瘤综合征相关基因具有明确致病突变位点', size=9)
    para += p.write(p.set(spacing=[0.5, 0.5]), run)
    return para, tr1, tr1, ''


def cmp_var(x, y):
    keys = ['add_star', 'cosmic_var_sum', 'dna_vaf']
    for k in keys:
        v = cmp(y.get(k), x.get(k))
        if v != 0:
            return v
    return 0


def write_chapter51(title, data):
    para = ''

    # para += h4_aiyi('体细胞突变')
    stars = data.get('variant_list')
    stars = sorted(stars, cmp=cmp_var)
    stars = stars[:200]
    para += write_table_var(stars, title)
    return para


def write_table_var(stars, title=''):
    stars = sorted(stars, cmp=cmp_var)
    titles = ['基因', '核苷酸变化', '氨基酸变化', '外显子', '变异类型', '突变丰度', '覆盖度',  'Cosmic计数']
    ws = [1000, 1700, 1700, 1000, 1400, 1200, 1000, 1000]
    trs = ''
    if title:
        trs += write_table_title(title, len(ws))
    trs += write_thead51(titles, pPr=p_set_tr_center, ws=ws)
    if len(stars) == 0:
        trs += write_tr51(['无'] * len(titles), ws, 0, 1)
    for k in range(len(stars)):
        star = stars[k]
        gene = star['gene']
        nucleotide_change = star.get('nucleotide_change')  # 变异c.变化 核苷酸变化
        amino_acid_change = star.get('amino_acid_change')  # 变异P.变化 氨基酸变化
        exon_number = 'Exon%s' % star.get('exon_number')  # 外显子位置
        effect = effect2cn(star.get('effect'))  # 变异类型
        dna_vaf = float2percent(star.get('dna_vaf')) # 突变丰度
        t_depth = '%sx' % star.get('t_depth') # 突变丰度
        cosmic_var_sum = star.get('cosmic_var_sum')  # Cosmic计数
        item = [
            gene, nucleotide_change, amino_acid_change, exon_number, effect, dna_vaf, t_depth, cosmic_var_sum
        ]
        trs += write_tr51(item, ws, row=k, count=len(stars))
    return table_weizhi(trs)


def write_table_cnv(items, ploidy, title=''):
    titles = ['基因', '总拷贝数', '低拷贝数', '区域大小', 'WGD状态', '基因组倍性', '变异状态']
    ws = [w_sum / len(titles)] * len(titles)
    trs = ''
    if title:
        trs += write_table_title(title, len(ws))
    trs += write_thead51(titles, ws=ws)
    if len(items) == 0:
        trs += write_tr51(['无'] * len(titles), ws, 0, 1)
    for k in range(len(items)):
        star = items[k]
        item = [
            star.get('gene'),
            star.get('tcn_em'),
            star.get('lcn_em'),
            '%sM' % star.get('region_size'),
            star.get('wgd'),
            ploidy,
            star.get('facets_call'),
            ]
        trs += write_tr51(item, ws, row=k, count=len(items))
    return table_weizhi(trs)


def write_chapter_cnvs(title, data):
    cnvs = data.get('cnvs')
    stars = data.get('cnv_stars')
    ploidy = data.get('ploidy')
    para = ''
    # para += h4_aiyi('（1）重点基因拷贝数变异结果汇总')
    para += write_genes_cnv(stars, title)
    run = r_aiyi.text(' 红色 ', color=white, fill=red, size=9, space=True)
    run += r_aiyi.text('，表示该基因扩增；', size=9)
    run += r_aiyi.text(' 深蓝色 ', color=white, fill=dark_blue, size=9, space=True)
    run += r_aiyi.text('，表示该基因纯合缺失；', size=9)
    run += r_aiyi.text(' 淡蓝色 ', color=white, fill=blue, size=9, space=True)
    run += r_aiyi.text('，表示该基因杂合缺失，', size=9)
    run += r_aiyi.text('扩增缺失状态未达阈值用灰色表示', size=9)
    para += p.write(p.set(spacing=[0.5, 0.5]), run)

    extra = []
    for gene in ['ERBB2', 'MET']:
        arr1 = filter(lambda x: x.get('gene') == gene, stars)
        if len(arr1) == 0:
            extra += filter(lambda x: x.get('gene') == gene, cnvs)
    # para += h4_aiyi('（2）拷贝数变异相关基因详细信息汇总')
    para += write_table_cnv(stars + extra, ploidy, title='拷贝数变异相关基因详细信息汇总')
    para += p.write(
        r_aiyi.text('注：肿瘤纯度低于30%时，二代测序拷贝数变异检测准确性会发生比较明显下降。', '小五')
    )
    return para


def write_chapter53(data):
    tr53 = write_table_title('肿瘤重要信号通路变异信息汇总')
    para = table_weizhi(tr53)
    para += p.write(
        p.set(spacing=[0.5, 1]),
        r_aiyi.text('评估肿瘤重点信号通路的状态是从全局对癌症进行理解的重要方式。肿瘤相关驱动基因一般都处在肿瘤的重点信号通路上。该样本相关的肿瘤驱动基因变异和非驱动基因变异究竟累及哪些信号通路，信号通路之间各个基因的关系如何，针对相关信号通路的治疗方式以及各个信号通路上下游的信号通路的分布，都能够协助医生和患者理解肿瘤所处状态。', 10, weight=1))
    for i in range(1, gene_list53.nrows):
        title = gene_list53.cell_value(i, 0)
        stars = (data.get('cnv_stars') + data.get('variant_stars'))if '融合' not in title else data.get('sv_stars')
        if i == 1:
            title = 'PI3K/AKT/mTOR信号通路'
        if i == 2:
            title = '受体酪氨酸激酶/生长因子信号通路'
        if i == 3:
            title = '细胞凋亡信号通路'
        if i == 4:
            title = '细胞周期调控信号通路'
        if i == 5:
            title = '代谢通路'
        if i == 6:
            title = 'WNT/ß-catenin信号通路'
        if i == 7:
            title = 'Hedgeho信号通路'
        if i == 8:
            title = 'TGFβ信号通路'
        if i == 9:
            title = 'JAK/STAT信号通路'
        if i == 10:
            title = '激酶融合信号通路'
        ch = {'title': title, 'para': gene_list53.cell_value(i, 1)}
        genes = []
        for j in range(3, gene_list53.ncols):
            v = gene_list53.cell_value(i, j)
            if v.strip() != '':
                genes.append(v)
        ch['genes'] = genes

        para += write_chapter5311(ch, i, stars)
    return para


def write_references():
    texts = '''1.	PMID: 21828076 A comprehensive functional analysis of PTEN mutations: implications in tumor- and autism-related syndromes.
2.	PMID: 10866302 Functional evaluation of PTEN missense mutations using in vitro phosphoinositide phosphatase assay.
3.	PMID: 11051241 Functional evaluation of p53 and PTEN gene mutations in gliomas.
4.	PMID: 29533785 Systematic Functional Annotation of Somatic Mutations in Cancer.
5.	PMID: 22949682 Oncogenic mutations mimic and enhance dynamic events in the natural activation of phosphoinositide 3-kinase p110α (PIK3CA).
6.	PMID:23246288 Germline PIK3CA and AKT1 mutations in Cowden and Cowden-like syndromes.
7.	PMID: 23455880 KRAS allel-specific activity of sunitinib in an isogenic disease model of colorectal cancer.
8.	PMID: 26037647 Biochemical and Structural Analysis of Common Cancer-Associated KRAS Mutations.
9.	PMID: 22662154 Genotype-dependent efficacy of a dual PI3K/mTOR inhibitor, NVP-BEZ235, and an mTOR inhibitor, RAD001, in endometrial carcinomas.
10.	PMID: 23471917 An inducible knockout mouse to model the cell-autonomous role of PTEN in initiating endometrial, prostate and thyroid neoplasias.
11.	PMID: 25692619 Therapeutic approach guided by genetic alteration: use of MTOR inhibitor in renal medullary carcinoma with loss of PTEN expression.
12.	PMID: 25902899 Phase I combination of pazopanib and everolimus in PIK3CA mutation positive/PTEN loss patients with advanced solid tumors refractory to standard therapy.
13.	PMID: 24366516 Sirolimus treatment of severe PTEN hamartoma tumor syndrome: case report and in vitro studies.
14.	2018 ASCO Abstract e24283 Pan-cancer genomic features of PIK3CA/PTEN and clinical response to everolimus in Chinese population.
15.	PMID: 28183140 Correlation between PIK3CA mutations in cell-free DNA and everolimus efficacy in HR+, HER2+ advanced breast cancer: results from BOLERO-2.
16.	PMID: 28330462 Prospective phase II trial of everolimus in PIK3CA amplification/mutation and/or PTEN loss patients with advanced solid tumors refractory to standard therapy.
17.	PMID: 27589687 Phase I dose-escalation study of the mTOR inhibitor sirolimus and the HDAC inhibitor vorinostat in patients with advanced malignancy.
18.	PMID: 24166148 Molecular Determinants of Outcome With Mammalian Target of Rapamycin Inhibition in Endometrial Cancer.
19.	PMID: 27016228 Tumor mutational analysis of GOG248, a phase II study of temsirolimus or temsirolimus and alternating megestrol acetate and tamoxifen for advanced endometrial cancer (EC): An NRG Oncology/Gynecologic Oncology Group study.
20.	PMID: 23407561 Phase II study of docetaxel in combination with everolimus for second- or third-linetherapy of advanced non-small-cell lung cancer.
21.	PMID: 25969130 Phase II trial of everolimus in patients with refractory metastatic adenocarcinoma of the esophagus, gastroesophageal junction and stomach: possible role for predictive biomarkers.
22.	PMID: 18184959 Sirolimus for angiomyolipoma in tuberous sclerosis complex or lymphangioleiomyomatosis.
23.	PMID: 27206639 A phase I study of mTOR inhibitor everolimus in association with cisplatin and radiotherapy for the treatment of locally advanced cervix cancer: PHOENIX I.
24.	PMID: 21788564 Phase II study of temsirolimus in women with recurrent or metastatic endometrial cancer: a trial of the NCIC Clinical Trials Group.
25.	PMID: 26294908 Beneficial Effects of the mTOR Inhibitor Everolimus in Patients with Advanced Medullary Thyroid Carcinoma: Subgroup Results of a Phase II Trial.
26.	PMID: 21232120 Two-dose-level confirmatory study of the pharmacokinetics and tolerability of everolimus in Chinese patients with advanced solid tumors.
27.	NCT02688881 Study to Evaluate the Safety and Efficacy of Sirolimus, in Subject With Refractory Solid Tumors.
28.	NCT01430572 Pazopanib and Everolimus in PI3KCA Mutation Positive/PTEN Loss Patients.
29.	PMID: 21325073 Antitumor efficacy of PKI-587, a highly potent dual PI3K/mTOR kinase inhibitor.
30.	PMID: 25652454 First-in-Human Study of PF-05212384 (PKI-587), a Small-Molecule, Intravenous, Dual Inhibitor of PI3K and mTOR in Patients with Advanced Cancer.
31.	PMID: 27103175 A randomized phase II non-comparative study of PF-04691502 and gedatolisib (PF-05212384) in patients with recurrent endometrial cancer.
32.	NCT03065062 Study of the CDK4/6 Inhibitor Palbociclib (PD-0332991) in Combination With the PI3K/mTOR Inhibitor Gedatolisib (PF-05212384) for Patients With Advanced Squamous Cell Lung, Pancreatic, Head & Neck and Other Solid Tumors.
33.	PMID: 23287563 Targeting Activated Akt with GDC-0068, a Novel Selective Akt Inhibitor That Is Efficacious in Multiple Tumor Models.
34.	2018 ASCO Abstract 1008 2018 ASCO Abstract 1008 Overall survival (OS) update of the double-blind placebo (PBO)-controlled randomized phase 2 LOTUS trial of first-line ipatasertib (IPAT) + paclitaxel (PAC) for locally advanced/metastatic triple-negative breast cancer (mTNBC).
35.	NCT02162719 A Study Assessing the Safety and Efficacy of Adding Ipatasertib to Paclitaxel Treatment in Participants With Breast Cancer That Has Spread Beyond the Initial Site, and the Cancer Does Not Have Certain Hormonal Receptors.
36.	2018 ASCO Abstract CT041 Primary results from FAIRLANE (NCT02301988), a double-blind placebo (PBO)-controlled randomized phase II trial of neoadjuvant ipatasertib (IPAT) + paclitaxel (PAC) for early triple-negative breast cancer (eTNBC).
37.	NCT03673787 A Trial of Ipatasertib in Combination With Atezolizumab
38.	PMID: 24608574 Characterization of the novel and specific PI3Kα inhibitor NVP-BYL719 and development of the patient stratification strategy for clinical trials.
39.	PMID: 31091374 Alpelisib for PIK3CA-Mutated, Hormone Receptor-Positive Advanced Breast Cancer.
40.	PMID: 29401002 Phosphatidylinositol 3-Kinase a–Selective Inhibition With Alpelisib (BYL719) in PIK3CA-Altered Solid Tumors: Results From the First-in-Human Study.
41.	NCT01219699 A Study of BYL719 in Adult Patients With Advanced Solid Malignancies, Whose Tumors Have an Alteration of the PIK3CA Gene.
42.	PMID: 20453058 Predictive biomarkers of sensitivity to the phosphatidylinositol 3' kinase inhibitor GDC-0941 in breast cancer preclinical models.
43.	PMID: 18725974 Breast tumor cells with PI3K mutation or HER2 amplification are selectively addicted to Akt signaling.
44.	PMID: 20664172 Deregulation of the PI3K and KRAS signaling pathways in human cancer cells determines their response to everolimus.
45.	PMID: 22271473 PI3K/AKT/mTOR inhibitors in patients with breast and gynecologic malignancies harboring PIK3CA mutations.
46.	2016 AACR Abstract 2273 Targeting the PI3K/AKT/mTOR pathway for the treatment of metaplastic breast cancer: Does location of PIK3CA mutation or histology affect response.
47.	2018 ASCO Abstract 1040 Phase Ib study of gedatolisib in combination with palbociclib and endocrine therapy (ET) in women with estrogen receptor (ER) positive (+) metastatic breast cancer (MBC) (B2151009).
48.	PMID: 25167228 KRAS mutational subtype and copy number predict in vitro response of human pancreatic cancer cell lines to MEK inhibition.
49.	2014 ASCO Abstract 9051 A phase 1b dose-escalation study of BYL719 plus binimetinib (MEK162) in patients with selected advanced solid tumors.
50.	PMID: 29108355 A phase I clinical trial of binimetinib in combination with FOLFOX in patients with advanced metastatic colorectal cancer who failed prior standard therapy.
51.	PMID: 28152546 A phase 1 dose-escalation and expansion study of binimetinib (MEK162), a potent and selective oral MEK1/2 inhibitor.
52.	NCT01363232 Safety, Pharmacokinetics and Pharmacodynamics of BKM120 Plus MEK162 in Selected Advanced Solid Tumor Patients.
53.	PMID: 19401449 PI3K pathway activation mediates resistance to MEK inhibitors in KRAS mutant cancers.
54.	PMID: 21451123 A MEK inhibitor abrogates myeloproliferative disease in Kras mutant mice.
55.	PMID: 24576621 Combination PI3K/MEK inhibition promotes tumor apoptosis and regression in PIK3CA wild-type, KRAS mutant colorectal cancer.
56.	PMID: 20215549 Phase I pharmacokinetic and pharmacodynamic study of the oral MAPK/ERK kinase inhibitor PD-0325901 in patients with advanced cancers.
57.	2017 AACR Abstract CT046 Phase I dose escalation study of the CDK4/6 inhibitor palbociclib in combination with the MEK inhibitor PD-0325901 in patients with RAS mutant solid tumors.
58.	NCT02022982 PALBOCICLIB + PD-0325901 for NSCLC & Solid Tumors.
59.	NCT02039336 Dacomitinib Plus PD-0325901 in Advanced KRAS Mutant Malignancies (M13DAP).
60.	NCT02510001 MErCuRIC1: MEK and MET Inhibition in Colorectal Cancer.
61.	PMID: 24170544 Modeling RAS phenotype in colorectal cancer uncovers novel molecular traits of RAS dependency and improves prediction of response to targeted agents in patients.
62.	PMID: 25322874 Phase II study of selumetinib (AZD6244, ARRY-142886) plus irinotecan as second-line therapy in patients with K-RAS mutated colorectal cancer.
63.	PMID: 27231576 A long-term surviving patient with recurrent low-grade serous ovarian carcinoma treated with the MEK1/2 inhibitor, selumetinib.
64.	NCT02188264 Selumetinib and Cyclosporine in Treating Patients With Advanced Solid Tumors or Advanced or Metastatic Colorectal Cancer.
65.	NCT01586624 A Phase I Trial of Vandetanib (ZD6474) and Selumetinib (AZD6244)for Solid Tumours Including Non Small Cell Lung Cancer (VanSel-1).
66.	PMID: 18332469 Dose- and schedule-dependent inhibition of the mammalian target of rapamycin pathway with everolimus: a phase I tumor pharmacodynamic study in patients with advanced solid tumors.
67.	PMID: 16494995 The TP53 mutation, R337H, is associated with Li-Fraumeni and Li-Fraumeni-like syndromes in Brazilian families.
68.	PMID: 16861262 Inactive full-length p53 mutants lacking dominant wild-type p53 inhibition highlight loss of heterozygosity as an important aspect of p53 status in human cancers.
69.	PMID: 21343334 Dominant-negative features of mutant TP53 in germline carriers have limited impact on cancer outcomes.
70.	PMID: 22319594 Benzo[a]pyrene, aflatoxine B₁ and acetaldehyde mutational patterns in TP53 gene using a functional assay: relevance to human cancer aetiology.
71.	PMID:29470806 Screening of over 1000 Indian patients with breast and/or ovarian cancer with a multi-gene panel: prevalence of BRCA1/2 and non-BRCA mutations.
72.	PMID: 12661006 Fusion of FIG to the receptor tyrosine kinase ROS in a glioblastoma with an interstitial del(6)(q21q21).
73.	PMID: 18083107 Global survey of phosphotyrosine signaling identifies oncogenic kinases in lung cancer.
74.	PMID: 21253578 Survey of tyrosine kinase signaling reveals ROS kinase fusions in human cholangiocarcinoma.
75.	PMID: 23174882 Role of early B-cell factor 1 (EBF1) in Hodgkin lymphoma.
76.	PMID: 21606506 Ebf1 or Pax5 haploinsufficiency synergizes with STAT5 activation to initiate acute lymphoblastic leukemia.
77.	PMID: 27993330 Standards and Guidelines for the Interpretation and Reporting of Sequence Variants in Cancer: A Joint Consensus Recommendation of the Association for Molecular Pathology, American Society of Clinical Oncology, and College of American Pathologists.
78.	PMID: 24737648 The Bim deletion polymorphism clinical profile and its relation with tyrosine kinase inhibitor resistance in Chinese patients with non-small cell lung cancer.
79.	PMID: 26510020 DNA-Repair Defects and Olaparib in Metastatic Prostate Cancer.
80.	NCT02952534 A Study of Rucaparib in Patients With Metastatic Castration-resistant Prostate Cancer and Homologous Recombination Gene Deficiency (TRITON2).
81.	2015 ASCO Abstract 5508 Results of ARIEL2: A Phase 2 trial to prospectively identify ovarian cancer patients likely to respond to rucaparib using tumor genetic analysis.
82.	2015 EMSO-ECC Abstract 435 Candidate biomarkers of PARP inhibitor sensitivity in ovarian cancer beyond the BRCA genes.
83.	PMID:28588062 Secondary Somatic Mutations Restoring RAD51C and RAD51D Associated with Acquired Resistance to the PARP Inhibitor Rucaparib in High-Grade Ovarian Carcinoma.
84.	NCT03344965 Olaparib In Metastatic Breast Cancer.
85.	2019 ASCO Abstract 3006 Talazoparib beyond BRCA: A phase II trial of talazoparib monotherapy in BRCA1 and BRCA2 wild-type patients with advanced HER2-negative breast cancer or other solid tumors with a mutation in homologous recombination (HR) pathway genes.
86.	NCT02401347 Phase II Talazoparib in BRCA1 +BRCA2 Wild-Type &Triple-Neg /HER2-Negative Breast Cancer /SolidTumors
87.	ESMO 2019 TRITON2 Updated Analyses Preliminary Results from the TRITON2 Study of Rucaparib in Patients with DNA Damage Repair-deficient mCRPC: Updated Analyses.
88.	NCT03967938 Efficacy of Olaparib in Advanced Cancers Occurring in Patients With Germline Mutations or Somatic Tumor Mutations in Homologous Recombination Genes.
89.	NCT03742895 Efficacy and Safety of Olaparib (MK-7339) in Participants With Previously Treated, Homologous Recombination Repair Mutation (HRRm) or Homologous Recombination Deficiency (HRD) Positive Advanced Cancer (MK-7339-002 / LYNK-002).
90.	ESMO 2019: GALAHAD A Phase 2 Study of Niraparib in Patients with mCRPC and Biallelic DNA-Repair Gene Defects, A Pre-Specified Interim Analysis.
91.	NCT02854436 An Efficacy and Safety Study of Niraparib in Men With Metastatic Castration-Resistant Prostate Cancer and DNA-Repair Anomalies.
92.	NCT04171700 A Study to Evaluate Rucaparib in Patients With Solid Tumors and With Deleterious Mutations in HRR Genes (LODESTAR).
93.	PMID: 24736070 Clinical significance of BIM deletion polymorphism in non-small-cell lung cancer with epidermal growth factor receptor mutation.
94.	2016 ASCO Abstract 9017 Total mutation burden (TMB) in lung cancer (LC) and relationship with response to PD-1/PD-L1 targeted therapies.
95.	PMID: 25765070 Cancer immunology.Mutational landscape determines sensitivity to PD-1 blockade in non-small cell lung cancer.
96.	PMID: 26028255 PD-1 Blockade in Tumors with Mismatch-Repair Deficiency.
97.	PMID: 27159395 Immune activation and response to pembrolizumab in POLE-mutant endometrial cancer.
98.	PMID: 27486176 Regression of Chemotherapy-Resistant Polymerase ε (POLE) Ultra-Mutated and MSH6 Hyper-Mutated Endometrial Tumors with Nivolumab.
99.	PMID: 27001570 Immune Checkpoint Inhibition for Hypermutant Glioblastoma Multiforme Resulting From Germline Biallelic Mismatch Repair Deficiency.
100.	PMID: 27671167 Targeted Next Generation Sequencing Identifies Markers of Response to PD-1 Blockade.
101.	PMID: 26952546 Atezolizumab in patients with locally advanced and metastatic urothelial carcinoma who have progressed following treatment with platinum-based chemotherapy: a single-arm, multicentre, phase 2 trial.
102.	2017 ASCO abstract e14508 Comprehensive genomic profiling to identify tumor mutational burden (TMB) as an independent predictor of response to immunotherapy in diverse cancers.
103.	PMID: 28972084 Hypermutated Circulating Tumor DNA: Correlation with Response to Checkpoint Inhibitor-Based Immunotherapy.
104.	Onclive 2017 FDA Grants Pembrolizumab Priority Review in Second-Line Bladder Cancer.
105.	2017 ASCO abstract 3071 Pembrolizumab therapy for microsatellite instability high (MSI-H) colorectal cancer (CRC) and non-CRC.
106.	PMID: 28795418 CD274 (PDL1) and JAK2 genomic amplifications in pulmonary squamous-cell and adenocarcinoma patients.
107.	2016 ASCO Abstract 3031 Occurrence of PDL1/2 copy number gains detected by FISH in adeno and squamous cell carcinomas of the lung and association with PDL1 overexpression in adenocarcinomas.
108.	PMID: 29902298 Prevalence of PDL1 Amplification and Preliminary Response to Immune Checkpoint Blockade in Solid Tumors.
109.	PMID: 25482239 PD-1 blockade with nivolumab in relapsed or refractory Hodgkin's lymphoma.
110.	PMID: 27942391 Metastatic basal cell carcinoma with amplification of PD-L1: exceptional response to anti-PD1 therapy.
111.	NCT02593786 A Study of Safety, Tolerability and Pharmacokinetics of Nivolumab in Chinese Subjects With Previously Treated Advanced or Recurrent Solid Tumors.
112.	NCT02864316 Phase 2 Study of Nivolumab in Solid Tumors Induced by Prior Radiation Exposure.
113.	PMID: 28329682 The SWI/SNF Protein PBRM1 Restrains VHL-Loss-Driven Clear Cell Renal Cell Carcinoma.
114.	PMID: 29301960 Genomic correlates of response to immune checkpoint therapies in clear cell renal cell carcinoma.
115.	PMID: 29301958 A major chromatin regulator determines resistance of tumor cells to T cell-mediated killing.
116.	PMID: 29270615 Clinical and Molecular Characteristics Associated With Survival Among Patients Treated With Checkpoint Inhibitors for Advanced Non-Small Cell Lung Carcinoma: A Systematic Review and Meta-analysis.
117.	2017 AACR Abstract CCR-16-2554 Potential Predictive Value of TP53 and KRAS Mutation Status for Response to PD-1 Blockade Immunotherapy in Lung Adenocarcinoma.
118.	PMID: 29773717 STK11/LKB1 Mutations and PD-1 Inhibitor Resistance in KRAS-Mutant Lung Adenocarcinoma.
119.	Adam Lauko et al.2019 Abstract THER-09 Impact of KRAS mutation status on the efficacy of immunotherapy in lung cancer brain metastases.
120.	PMID: 28525386 Prognostic value of KRAS mutation in advanced non-small-cell lung cancer treated with immune checkpoint inhibitors: A meta-analysis and review.
121.	2019 ASCO 9077 Abstract DNA damage response gene alterations are associated with high tumor mutational burden and clinical benefit from programmed death 1 axis inhibition in non-small cell lung cancer.
122.	PMID: 29983880 Ipilimumab plus nivolumab and DNA-repair defects in AR-V7-expressing metastatic prostate cancer.
123.	2019 ASCO Abstract 142 Initial results from a phase II study of nivolumab (NIVO) plus ipilimumab (IPI) for the treatment of metastatic castration-resistant prostate cancer (mCRPC; CheckMate 650).
124.	PMID: 30171052 Comutations in DNA Damage Response Pathways Serve as Potential Biomarkers for Immune Checkpoint Blockade.
125.	PMID: 29337640 Molecular Determinants of Response to Anti-Programmed Cell Death (PD)-1 and Anti-Programmed Death-Ligand 1 (PD-L1) Blockade in Patients With Non-Small-Cell Lung Cancer Profiled With Targeted Next-Generation Sequencing.
126.	2019 ASCO Abstract 9082 Impact of KRAS allele subtypes and concurrent genomic alterations on clinical outcomes to programmed death 1 axis blockade in non-small cell lung cancer.
127.	2018 IASLC Abstract MA19.09 Concurrent Mutations in STK11 and KEAP1 is Associated with Resistance to PD-(L)1 Blockade in Patients with NSCLC Despite High TMB.
128.	2019 ASCO Abstract 4036 Association of frequent amplification of chromosome 11q13 in esophageal squamous cell cancer with clinical benefit to immune check point blockade.
129.	2017 ESMO Abstract 1140PD Predictive biomarkers for Hyper-progression (HP) in response to Immune Checkpoint Inhibitors (ICI) – Analysis of Somatic Alterations (SAs).
130.	PMID: 29056344 Comprehensive Analysis of Hypermutation in Human Cancer.
131.	NCT03150706 Avelumab for MSI-H or POLE Mutated Metastatic Colorectal Cancer
132.	NCT03461952 Nivolumab Ipilimumab in Patients With hyperMutated Cancers Detected in Blood (NIMBLe)
133.	PMID: 28188185 Response to PD-1 Blockade in Microsatellite Stable Metastatic Colorectal Cancer Harboring a POLE Mutation.
134.	NCT03491345 K-Basket, Avelumab, Biomarker-driven, Advanced Solid Tumor.
135.	PMID: 26645196 Loss of PTEN Promotes Resistance to T Cell-Mediated Immunotherapy.
136.	PMID: 28228279 Loss of PTEN Is Associated with Resistance to Anti-PD-1 Checkpoint Blockade Therapy in Metastatic Uterine Leiomyosarcoma.
137.	PMID: 28167612 JAK Mutations as Escape Mechanisms to Anti-PD-1 Therapy.
138.	PMID: 27433843 Mutations Associated with Acquired Resistance to PD-1 Blockade in Melanoma.
139.	PMID: 27903500 Primary Resistance to PD-1 Blockade Mediated by JAK1/2 Mutations.
140.	PMID: 22137796 Combined genetic inactivation of β2-Microglobulin and CD58 reveals frequent escape from immune recognition in diffuse large B cell lymphoma.
141.	PMID: 29070816 Resistance to checkpoint blockade therapy through inactivation of antigen presentation.
142.	PMID: 27225694 EGFR Mutations and ALK Rearrangements Are Associated with Low Response Rates to PD-1 Pathway Blockade in Non-Small Cell Lung Cancer: A Retrospective Analysis.
143.	PMID: 26069186 Co-occurring genomic alterations define major subsets of KRAS-mutant lung adenocarcinoma with distinct biology, immune profiles, and therapeutic vulnerabilities.
144.	PMID: 26833127 STK11/LKB1 Deficiency Promotes Neutrophil Recruitment and Proinflammatory Cytokine Production to Suppress T-cell Activity in the Lung Tumor Microenvironment.
145.	PMID: 1614537 Amplification of a gene encoding a p53-associated protein in human sarcomas.
146.	PMID: 16905769 Hdmx modulates the outcome of p53 activation in human tumor cells.
147.	PMID: 27827313 Hyperprogressive Disease Is a New Pattern of Progression in Cancer Patients Treated by Anti-PD-1/PD-L1.
148.	PMID: 28351930 Hyperprogressors after Immunotherapy: Analysis of Genomic Alterations Associated with Accelerated Growth Rate.
149.	PMID: 26858935 Clinical Overview of MDM2/X-Targeted Therapies.
150.	PMID: 16354690 Tissue-specific differences of p53 inhibition by Mdm2 and Mdm4.
151.	PMID: 10555141 DNA methyltransferases Dnmt3a and Dnmt3b are essential for de novo methylation and mammalian development.
152.	PMID: 29414941 Structural basis for DNMT3A-mediated de novo DNA methylation.
153.	PMID: 28976787 Negative predictive biomarkers of checkpoint inhibitors in hyper-progressive tumors.
154.	PMID: 29217585 Patient HLA class I genotype influences cancer response to checkpoint blockade immunotherapy.'''
    para = ''
    para += p.write(
        p.set(spacing=[0, 0.5], line=12),
        r_aiyi.text(' 参考文献', '小四', 1, wingdings=True, color='3EA6C2', space=True)
    )
    for index, text in enumerate(texts.split('\n')):
        ind = 1
        if index < 9:
            ind = 1
        elif index < 99:
            ind = 1.5
        else:
            ind = 2
        para += p.write(
            p.set(line=18, ind=['hanging', ind, 0]),
            r_aiyi.text(text, 10)
        )

    para += set_page()
    return para

# Part5 . 3 通路涉及重点基因变异情况
def write_chapter5311(ch, index, stars):
    p_set = p.set(spacing=[0.2, 0.2])
    para = ''
    para_title = p.write(p.set(line=12, jc='center'),
                         r_aiyi.text(ch['title'], '五号', 1))
    # para += con1
    para_ev = write_explains(ch['para'], p_set)
    para_pic = p.write(p.set(),
                       r_aiyi.picture(cx=14, rId='image%d' % (index + 17), align=['center', '']))
    trs = ''
    trs += tr.write(tc.write(para_title), tc.set(w_sum, fill=green_lighter, color=gray))
    trs += tr.write(tc.write(para_ev), tc.set(w_sum, color=gray))
    trs += tr.write(tc.write(para_pic), tc.set(w_sum, color=gray))
    para += table_weizhi(trs)
    n = 10
    para += p.write(p.set(line=6))
    # para2 = p.write(p.set(line=18, jc='center'),
    #                 r_aiyi.text(ch['title'] + '重点基因变异情况', '五号', color=white))
    # trs2 = tr.write(tc.write(para2), tc.set(w_sum, fill='A6A6A6', gridSpan=n, color=gray))
    trs2 = ''
    trs2 += write_genes((ch['genes']), n, w_sum, 'right', stars, title=ch['title'])
    para += table_weizhi(trs2)
    para += p.write()
    para += p.write(p.set(sect_pr=set_page()))
    return para


def write_db_info(setting2, setting3):
    para = h4_aiyi('肿瘤解读数据库相关说明', **setting2)
    infos = [
        {'rId': 'CIVic', 'cx': 4.23, 'cy': 1.8, 'off_y': 0.22,
         'para': [
             {'text': 'CIVic是一个基于开放用户提供内容，领域专家进行审核的精准医疗知识社区。领域专家在社区中起着至关重要的作用。领域专家通常是科学家或医生，具有高级学位（PHD或MD级），并展示了与癌症精确医学知识相关的专长（发表记录）。该社区的知识库将变异分成五类：A级，已验证，已批准或者已形成共识；B级，临床证据，来源于临床试验证据或者其他患者来源证据支持；C级：案例研究，来源于临床的案例报道；D级：临床前证据，体内或体外生物学支持证据；E级：非直接证据。'}
         ]},
        {'rId': 'Oncokb', 'cx': 3, 'cy': 1,
         'para': [
             {'text': ' OncoKB是一个肿瘤精准医学数据库，包含特定的癌症基因变异效应和治疗提示的信息。这是由Memorial Sloan Kettering癌症中心（MSK）的MarieJosée和Henry R. Kravis分子肿瘤学中心的知识系统小组与Quest Diagnostics合作开发和维护的。由MSK的临床人员、研究人员和教学人员共同组成的协作网络进行专家手工注释，OncoKB包含有关477种癌症基因特定变异的详细信息。这些信息具有各种来源，如FDA，NCCN或ASCO等指南，和ClinicalTrials.gov和科学文献等。对于每一种变异，该数据库均会专家手工注释生物学效应、患病率、预后信息和治疗影响。治疗信息使用自行开发的证据级别系统进行分类。该证据级别共分为四类：FDA批准、专家共识、强有力临床证据和强有力生物学证据四种，其分类与ASCO、AMP和CAP共同发布的指南一一对应。'}
         ]},
        {'rId': 'CGI', 'cx': 5.74, 'cy': 1.11,
         # 'para': 'CGI(癌症基因组解释器)被设计用于识别驱动肿瘤发展，可能可治疗的变异。',
         'para': [
             {
                 'text': 'CGI(癌症基因组解释器)被设计用于识别驱动肿瘤发展，可能可治疗的变异。CGI依赖于多个数据源和计算机算法，依照不同的证据级别对变异进行分类。这是一个由巴塞罗那生物医学基因组实验室维护开发的一个癌症基因组注释工具。该注释工具相关的数据库大致将变异分为以下五类：临床指南、晚期临床试验、早期临床试验、临床案例报道和临床前数据这五类。由于人类知识积累有限，大部分基因变异是否为致癌变异均是未知的。该注释工具的核心特色是一个针对未知是否致癌的变异进行致癌性预测的工具，oncodriverMUT。该工具结合了大规模肿瘤基因组数据（来自28个癌种的6792个样本）和大规模正常人基因组数据（60706个未经选择的正常人样本）中突变的分布，并结合突变功能预测的多种规则，对未知变异的致癌性进行预测。未知突变经预测，分类为预测为驱动突变级别1、预测为驱动突变级别2和预测为乘客突变。',
             },
             {
                 'text': '通过对1077已知致癌变异、2819个癌症易感变异、241个癌症基因上已知为良性的PAM（影响蛋白功能突变）和1006个癌症基因上经常出现在一般人群中的PAM的验证，发现该算法的准确性为0.91。',
             },
             {
                 'pic': {'rId': '1.3.4.1', 'cx': 14.1, 'cy': 6, 'off_y': 0}
             },
             {
                 'pic': {'rId': '1.3.4.2', 'cx': 13.76, 'cy': 6}
             },
         ]},
    ]
    for i in range(len(infos)):
        info = infos[i]
        rId = info['rId']
        text = rId if 'text' not in info else info['text']
        off_y = 0.48 if 'off_y' not in info else info['off_y']
        off_y -= 0.1
        para += h4_aiyi('%s. %s数据库证据呈现' % (chr(i+97), text), runs=r_aiyi.picture(cy=0.8, rId=info['rId'], posOffset=[4.5, 0]), **setting3)
        for p_text in info['para']:
            if 'text' in p_text:
                para += p.write(p.set(), r_aiyi.text(p_text['text'], '小五'))
            if 'pic' in p_text:
                pic = p_text['pic']
                para += write_pic_center(pic['cy'], pic['rId'])
                # para += p.write(p.set(spacing=[9, 0]), r_aiyi.picture(cy=pic['cy'], rId=pic['rId'], posOffset=[0, 5.59], align=['center', 'bottom']))
    return para


def cmp_drug(x, y):
    for k in ['aiyi_level', 'evidence_direction']:
        v = cmp(x.get(k), y.get(k))
        # Resistant (Support) Responsive (Support)
        if v != 0:
            return v
    return 0


def write_table_title(title, gridSpan=0, sub_title=''):
    tcs = ''
    run = r_aiyi.text(title, 11, color=white, weight=1)
    if sub_title:
        run += r_aiyi.text(sub_title, '小五', color=white)
    para = p.write(p.set(line=18, jc='center'), run)
    tcs += tc.write(para, tc.set(w_sum, tcBorders=[], gridSpan=gridSpan, fill=RGB_to_Hex('62,175,150')))
    return tr.write(tcs)


def write_patient_info(data):
    sample_detail = data.get('sample_detail')
    para = ''
    trs = ''
    trs += write_table_title('受检者信息和样本信息', gridSpan=8)
    w = 1200
    items = [
        [
            {'text': '姓名:', 'w': w},
            {'text': sample_detail.get('patient_name'), 'w': w},
            {'text': '性别:', 'w': w},
            {'text': sex2str(sample_detail.get('sex')), 'w': w},
            {'text': '年龄:', 'w': w},
            {'text': sample_detail.get('age'), 'w': w},
            {'text': '医院:', 'w': w},
            {'text': sample_detail.get('inspection_department'), 'w': 1800},
        ],
        [
            {'text': '病理诊断:', 'w': w},
            {'text': '%s' % (sample_detail.get('comment') or sample_detail.get('diagnosis')), 'w': w * 3, 'gridSpan': 3},
            {'text': '既往靶向/免疫用药方案:', 'w': w * 2, 'gridSpan': 2},
            {'text': '', 'w': 3000, 'gridSpan': 2},
        ],
        [
            {'text': '样本编号:', 'w': w},
            {'text': sample_detail.get('sample_id'), 'w': w * 2, 'gridSpan': 2},
            {'text': '组织来源:', 'w': w},
            {'text': sample_detail.get('tissue'), 'w': w * 2, 'gridSpan': 2},
            {'text': '样本类型:', 'w': w},
            {'text': sample_detail.get('sample_type'), 'w': 1800}
        ],
        [
            {'text': '取样日期:', 'w': w},
            {'text': '', 'w': w * 2, 'gridSpan': 2},
            {'text': '送检日期:', 'w': w},
            {'text': '', 'w': w * 2, 'gridSpan': 2},
            {'text': '报告日期:', 'w': w},
            {'text': data.get('report_time'), 'w': 1800}
        ]
    ]
    for item in items:
        trs += write_tr_weizhi(item)
    para += table_weizhi(trs)
    para += p.write(
        p.set(spacing=[0.3, 1.5]),
        r_aiyi.text('附注：以上受检者信息和样本信息均为患者送检时提供的信息，本检测不对这些内容进行判读或解读。', '小五')
    )
    return para


# part0 靶向治疗提示
def write_target_tip(data):
    target_tips = data.get('target_tips')
    cnv_stars = data.get('cnv_stars')
    yesheng = data.get('yesheng')
    # plo =
    ploidy = data.get('ploidy')
    items, show_extra, extra_item = target_tips
    ws = [1200, 2800, w_sum - 1200 - 2800]
    trs = ''
    trs += write_table_title('靶向治疗提示', len(ws))
    trs += write_thead_weizhi(ws, cnv_stars, ploidy)
    if len(yesheng) == 2:
        items.insert(0, {
            'col1': '、'.join(yesheng), 'col2': '野生型', 'yesheng': True, 'action1': '野生型',
            'known_db': [
                {'evidence_direction': 'Responsive (Support)', 'aiyi_level': 'A', 'drugs': '西妥昔单抗'},
                {'evidence_direction': 'Responsive (Support)', 'aiyi_level': 'A', 'drugs': '帕尼单抗'}
            ]
        })
    if len(target_tips) == 0:
        trs += write_tr51(['无'] * len(ws), ws, 0, 1)
    for k in range(len(items)):
        fill = ''
        bdColor = gray
        item1 = items[k]
        # if k == 0:
        #     for kk in item1.keys():
        #         print kk, item1[kk]
        tcs = ''

        tcs += tc.write(
            p.write(p_set_tr_center,
                    r_aiyi.text(item1.get('gene') or item1.get('gene1') or item1.get('col1'), '小五', italic=True, weight=1)),
            tc.set(ws[0], fill=fill, color=bdColor)
        )
        ccf_expected_copies_em = item1.get('ccf_expected_copies_em') or item1.get('clone_proportion') # 肿瘤细胞比例
        if ccf_expected_copies_em is None:
            ccf_expected_copies_em = item1.get('dna_vaf') or item1.get('vaf')
        ccf = float2percent(ccf_expected_copies_em)
        # 没有p.用c.
        amino_acid_change = item1.get('amino_acid_change') # 变异P.变化
        nucleotide_change = item1.get('nucleotide_change') # 变异C.变化
        amino_acid_change = amino_acid_change or nucleotide_change
        tcn_em = item1.get('tcn_em')  # 拷贝数
        try :
            tcn_em = int(tcn_em)
        except:
            tcn_em = tcn_em
        action_name = None
        action1 = ''
        tip = ''
        lcn_text = ''
        if amino_acid_change:
            amino = amino_acid_change.split('p.')[-1]
            tumor_suppressor_gene = item1.get('tumor_suppressor_gene')
            lcn_em = item1.get('lcn_em')
            action_name = 'Exon %s %s' % (item1.get('exon_number'), amino)
            action1 = ' %s' % amino
            if tumor_suppressor_gene == 1 and str(lcn_em) == '0':
                lcn_text = '合并野生型Allele缺失'
                # action_name += '合并野生型Allele缺失'
                # action1 += '合并野生型Allele缺失'
            tip = '突变'
        elif item1.get('gene1'):
            action1 = '融合'
            action_name = '融合'
            tip = '融合'
        elif tcn_em > 0:
            action_name = '%s倍扩增' % tcn_em
            tip = '扩增'
            action1 = '扩增'
        elif tcn_em == 0:
            action_name = '纯合缺失'
            action1 = '纯合缺失'
            tip = '纯合缺失'
        item1['tip'] = tip
        item1['action'] = ''
        item1['action_name'] = action_name
        if 'action1' not in item1:
            item1['action1'] = action1 + lcn_text
        # 【amino_acid_change】变异P.变化，
        # 【tcn_em】拷贝数，
        col2 = item1.get('col2') or '%s（%s）' % (action_name, ccf) + lcn_text
        tcs += tc.write(
            p.write(p_set_tr_center, r_aiyi.text(col2, '小五')),
            tc.set(ws[1], fill=fill, color=bdColor)
        )
        known_db = item1.get('known_db') or []
        para = ''
        run = ''
        evidence_directions = ['Responsive (Support)', 'Resistant (Support)']
        # '耐药Resistant (Support)', '敏感Responsive (Support)'
        known_db = filter(lambda x: x.get('evidence_direction') in evidence_directions, known_db)
        known_db.sort(cmp=cmp_var)
        for evidence_direction in evidence_directions:
            ds1 = filter(lambda x: x.get('evidence_direction') in evidence_direction, known_db)
            for tip_item in level_tips_wz:
                level = tip_item.get('text')
                ds = filter(lambda x: x.get('aiyi_level') == level, ds1)
                for d_item in ds:
                    d = d_item.get('drugs')
                    color = ''
                    # '耐药Resistant (Support)', '敏感Responsive (Support)'
                    if evidence_direction == 'Resistant (Support)':
                        fill1 = gray
                        color = ''
                        d += '(耐药)'
                    else:
                        fill1 = tip_item.get('color')

                    run1 = r_aiyi.text(' ' + d, '小五', fill=fill1, color=color, space=True)
                    run1 += r_aiyi.text(level, vertAlign='top', fill=fill1, color=color)
                    run1 += r_aiyi.text(' ', fill=fill1, space=True)
                    run1 += r_aiyi.text('  ', space=True)

                    run += run1
        if run:
            para += p.write(p_set_tr, run)
        if para == '':
            para = p.write(p_set_tr)
        tcs += tc.write(para, tc.set(ws[2], fill=fill, color=bdColor))
        trs += tr.write(tcs)
    if len(yesheng) == 2:
        del items[0]
    return table_weizhi(trs)


# part0 免疫治疗提示
def write_immun_tip_weizhi(immun_tip):
    trs = write_table_title('免疫治疗提示', 2, '（PD1等免疫检查点抑制剂治疗）')
    # trs = ''
    trs += write_tr_weizhi([
        {'text': '检测指标', 'w': 2000, 'tcFill': green_lighter, 'jc': 'center'},
        {'text': '检测结果', 'w': w_sum-2000, 'tcFill': green_lighter, 'jc': 'center'},
    ])
    for immun_item in immun_tip:
        level = immun_item.get('level')
        fill = get_level_color(level)
        text = immun_item.get('result') or immun_item.get('text')
        if level:
            text += '(%s级)' % level
            if '耐药' in text or '超进展' in text:
                fill = gray
        elif 'HLA' in text and '耐药' in text and '纯合' in text:
            fill = gray
        trs += write_tr_weizhi([
            {'text': immun_item.get('index'), 'weight': 1, 'w': 2000, 'tcFill': fill, 'jc': 'center'},
            {'text': text, 'weight': 0, 'w': w_sum-2000, 'tcFill': fill, 'jc': 'center'},
        ])
    return table_weizhi(trs) + p.write()


def write_immun_table(data, level='', color=''):
    level1 = filter(lambda x: level.startswith(x['text']), level_tips_wz)
    fill2 = ''
    if len(level1) > 0:
        fill2 = level1[0].get('color')
    if color:
        fill2 = color
    trs2 = write_tr1(data[0], '')
    trs2 += write_tr2(data[1], fill2 or '', bdColor=fill2 or gray)
    return table.write(trs2, bdColor=fill2 or gray, tblBorders=['top', 'bottom'], line=12)


def write_evidence_old(evidences):
    para = ''
    para += p.write(p.set(spacing=[1.5, 0], ind=[0.5, 0]), r_aiyi.text('相关循证医学证据：', '五号', weight=1, wingdings=True))
    for i in range(len(evidences)):
        text = evidences[i]
        p_set0 = p.set(spacing=[1, 0.5], shade=gray, ind=['hanging', 0.5], line=17, rule='exact')
        p_set = p.set(spacing=[0, 0.2], shade=gray, ind=['hanging', 0.5], line=17, rule='exact')
        para += p.write(p_set0, r_yahei.text(' ' + text.get('disease'), 10.5, weight=1, space=True))
        para += p.write(p_set, r_yahei.text(' %s' % text.get('title'), 9, space=True, weight=1))
        para += p.write(p_set, r_yahei.text(' %s' % text.get('text'), 9, space=True))
        if 'para' in text:
            para += text['para']
    return para


def write_evidence_new(evidences):
    para = ''
    para += p.write(p.set(spacing=[0.5, 0.2]), r_aiyi.text('相关循证医学证据：', '五号', weight=1, wingdings=True))
    for i in range(len(evidences)):
        item = evidences[i]
        p_set = p.set(spacing=[0.2, 0.2])
        # para += p.write(p_set0, r_aiyi.text(' ' + item.get('disease'), 10.5, weight=1, space=True))
        para2 = p.write(p_set, r_aiyi.text('%s' % item.get('title'), '小五', space=True, weight=1))
        para2 += p.write(p_set, r_aiyi.text('%s' % item.get('text'), '小五', space=True))
        trs = ''
        trs += tr.write(write_tc_weizhi({
            'text': item.get('disease'), 'pPr': p_set, 'tcFill': RGB_to_Hex('233,233,233'),
            'weight': 1, 'size': 10
        }), tr.set(trHeight=int(0.8*567)))
        trs += tr.write(
            tc.write(para2),
            # tr.set()
        )
        para += table_weizhi(trs, tblBorders=['top', 'bottom'], line=15 if i < len(evidences)- 1 else 1)
        para += item.get('para') or ''
    return para


def write_evidence4(index):
    para = p.write(p.set(spacing=[0.5, 1], ind=[0, 0]), r_aiyi.text('相关循证医学证据：', '五号', weight=1, wingdings=True))
    evidence_path = '4.%d.evidence.txt' % index
    evidence = []
    evidence = base_file.read(evidence_path, dict_name='').split('\n')
    for i in range(len(evidence)):
        text = evidence[i]
        weight = 0
        if len(text) < 171:
            weight = 1
        after = 0
        if i % 4 == 0:
            after = 0.2
        if i % 4 == 2:
            after = 1
        if after > 0:
            para += p.write(p.set(spacing=[0, after], shade=gray, line=17, rule='exact', ind=[0, 0]), r_aiyi.text(text, 9.5, weight=weight))
    return para


def write_evidence_tc(d, t_item):
    key = t_item.get('key')
    text = d.get(key)
    pPr = p.set(jc='left', spacing=[0.5, 0.5])
    return tc.write(
        p.write(pPr, r_aiyi.text(text, 9)),
        tc.set(t_item.get('w'), tcBorders=['top', 'bottom', 'left', 'right'], color=gray, gridSpan=t_item.get('gridSpan') or 0)
    )


def write_evidence1(gene, data, **kwargs):
    data = filter(lambda x: x.get('evidence_statement'), data or [])
    if len(data) == 0:
        return ''
    trs = ''
    pPr = p.set(jc='left', spacing=[0.5, 0.5])
    w = w_sum/4
    titles = [
        {'title': '生物标志物', 'key': 'col1', 'w': w},
        {'title': '药物', 'key': 'col2', 'w': w * 1.5},
        {'title': '证据类型', 'key': 'col3', 'w': w * 1.5},
        {'title': '证据描述', 'key': 'col4', 'w': w},
    ]
    size = 9
    tcs_th1 = ''
    borders1 = ['top', 'bottom', 'left', 'right']
    for (t_index, t) in enumerate(titles[:-1]):
        run = r_aiyi.text(t.get('title'), size)
        tcs_th1 += tc.write(p.write(pPr, run), tc.set(t.get('w'), tcBorders=borders1, fill=gray, color=gray))
    tr_h1 = tr.write(tcs_th1)
    tc_h2 = tc.write(
        p.write(pPr, r_aiyi.text('证据描述', size)),
        tc.set(w, tcBorders=borders1, fill=gray, color=gray)
    )
    para_ev = ''
    for d in data:
        d['col1'] = '%s %s' % (gene, d.get('alteration_in_house'))
        d['col2'] = '%s ( %s )' % (d.get('drugs'), d.get('known_db_level'))
        d['col3'] = '%s;%s' % (d.get('disease'), d.get('evidence_direction'))
        d['col4'] = '%s (PMID: %s )' % (d.get('evidence_statement'), d.get('reference'))
        trs = tr_h1
        tcs = ''
        for (t_index, t_item) in enumerate(titles[:-1]):
            tcs += write_evidence_tc(d, t_item)
        trs += tr.write(tcs)
        tcs2 = tc_h2
        t_item2 = titles[-1]
        t_item2['w'] = w * 3
        t_item2['gridSpan'] = 2
        tcs2 += write_evidence_tc(d, t_item2)
        trs += tr.write(tcs2)
        para_ev += table_weizhi(trs, line=15)
    return para_ev


def write_explain_new(i):
    # run = r_aiyi.text(i['title'], weight=1) + r_aiyi.text(i['text'], size=9)
    # return p.write(p_set, run)
    para = ''
    para += p.write(p.set(spacing=[0.5, 0.2]), r_aiyi.text(' %s' % i['title'], 10.5, weight=1, wingdings=True, space=True))
    para += p.write(r_aiyi.text(i['text'], '小五'))
    return para


def write_explain(i, ind=[0, 0], p_set=None):
    run = r_aiyi.text(i['title'], weight=1) + r_aiyi.text(i['text'], size=9)
    if p_set is None:
        p_set = p.set(ind=ind, line=16, rule='exact')
    return p.write(p_set, run)
    # para = ''
    # para += p.write(p_set, r.text(i['title'], weight=1))
    # para += p.write(p_set, r.text(i['text'], 9))
    # return para


def write_mingan(items, ncol):
    nrow = len(items)
    ws = [w_sum/ncol] * ncol
    trs2 = ''
    for row in range(nrow):
        genes = items[row]
        tcs = ''
        fill = ''
        for col in range(ncol):
            text = ''
            color = '000000'
            fill1 = ''
            if col < len(genes):
                item = genes[col]
                text = item.get('text')
                fill1 = item.get('fill') or item.get('color') or ''
            if fill1 not in ['', gray]:
                color = white
            else:
                fill1 = ''
            para = p.write(p.set(jc='center'), r_aiyi.text(text, color=color, size=9, fill=fill1))
            tcs += tc.write(para, tc.set(w=ws[col], fill=fill, color=gray))
        trs2 += tr.write(tcs, tr.set(trHeight=int(0.9) * 567))
    return table_weizhi(trs2)


def write_43(genes, ncol):
    col = len(genes)
    ws = [w_sum/ncol] * ncol
    # ws = [1800, 1800, 1800, 1800, 2400] if 'ws' not in kwargs else kwargs['ws']
    fill, weight, jc = gray, 0, 'center'
    pPr = p.set(jc=jc, line=12, rule='auto')
    tcs = ''
    for j in range(col):
        item = genes[j]
        fill = item.get('fill') or item.get('color')
        color = '000000'
        if fill != gray:
            color = white
        if fill == gray:
            fill = ''
        para = p.write(pPr, r_aiyi.text(item['text'], color=color, size=9))
        tcs += tc.write(para, tc.set(w=ws[j], fill=fill, tcBorders=borders, color=white))
    trs2 = tr.write(tcs, tr.set(trHeight=800))
    return table_weizhi(trs2)


def write_46(items, **kwargs):
    ws = []
    if 'col' in kwargs and 'ws' not in kwargs:
        col = kwargs['col']
        ws = [w_sum / col] * col
    if 'ws' in kwargs and 'col' not in kwargs:
        ws = kwargs['ws']
        col = len(ws)
    fill, weight, jc = gray, 0, 'center'
    pPr = p.set(jc=jc, spacing=[0.5, 0.5])
    trs2 = ''
    for row, item in enumerate(items):
        tcs = ''
        rows = item.split('\t')
        rows += [''] * (4-len(rows))
        for j in range(len(rows)):
            item = {'fill': gray, 'text': rows[j]}
            fill = ''
            color = '000000'
            para = p.write(pPr, r_aiyi.text(item['text'], color=color, size='小五'))
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, color=gray, tcBorders=['top', 'bottom', 'left', 'right']))
        if len(tcs) > 0:
            trs2 += tr.write(tcs, tr.set(trHeight=800))
    return table_weizhi(trs2)


def write_genes(gene_list, col, width, table_jc='center', stars=[], title=''):
    trs2 = ''
    fill, weight, jc = gray, 0, 'center'
    pPr = p.set(jc=jc, line=12, rule='auto')
    row = int(math.ceil(float(len(gene_list)) / col))
    if row == 1:
        col = len(gene_list)
    para2 = p.write(p.set(line=18, jc='center'),
                    r_aiyi.text(title + '重点基因变异情况', '五号', color=white))
    ws = [width / col] * col
    trs2 = tr.write(tc.write(para2, tc.set(width, fill='A6A6A6', gridSpan=col, color=gray)))
    for i in range(row):
        tcs = ''
        for j in range(col):
            gene_index = col * i + j
            tip = ''
            if gene_index < len(gene_list):
                item = gene_list[gene_index]
                fill, tip, var_item = get_var_color(item, stars)
            else:
                fill = gray
                item = ''
            color, text, var_text = '000000', item, ''
            if fill not in ['', gray]:
                color = white
                var_text = p.write(pPr, r_aiyi.text(tip, color=color, size=9))
            else:
                fill = ''
            para = p.write(pPr, r_aiyi.text(text, color=color, size=9)) + var_text
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, color=gray))
        if tcs:
            trs2 += tr.write(tcs, tr.set(trHeight=660))
    return trs2


def get_var_color(gene, vars):
    for item in vars:
        if gene == item.get('gene') or (item.get('gene1') and item.get('gene1').split('(')):
            add_star = item.get('add_star')
            tip = item.get('tip')
            if add_star > 0:
                return red, tip, item
    return '', '', None


def get_level_color(level):
    if level:
        for l_item in level_tips_wz:
            if level.startswith(l_item.get('text')):
                return l_item.get('color')
    return ''


def write_genes_cnv(cnv_stars, title):
    col = 8
    trs2 = write_table_title(title, col)
    gene_list = cnv_genes
    ws = [w_sum / col] * col
    # fill, weight, jc = gray, 0, 'center'
    # pPr = p.set(jc='center', line=12, rule='auto')
    row = int(math.ceil(float(len(gene_list)) / col))
    for i in range(row):
        tcs = ''
        fill = ''
        for j in range(col):
            gene_index = col * i + j
            tip = ''
            if gene_index < len(gene_list):
                item = gene_list[gene_index]
                fill1, tip = get_var_new(item, cnv_stars)
            else:
                item = ''
                fill1 = ''
            # fill = gray
            color, text, var_text = '000000', item, ''
            if fill1 not in ['', gray]:
                color = white
            else:
                fill1 = ''
            para = p.write(p.set(line=12*1.3, jc='center'), r_aiyi.text(text, color=color, size=9, fill=fill1))
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, tcBorders=[]))
        if tcs:
            trs2 += tr.write(tcs)
    return table_weizhi(trs2)


def write_thead_weizhi(ws, cnv_stars, ploidy):
    pPr = p_set_tr if len(cnv_stars) > 0 else p.set(line=24)
    tcs = ''
    size = 9.5
    titles = [
        {'run': r_aiyi.text('基因', size)},
        {'run': r_aiyi.text('检测结果(突变肿瘤细胞比例)', size)},
        {'run': r_aiyi.text('可能获益的治疗方式', size)},
    ]
    for i in range(len(titles)):
        t = titles[i]
        run = t.get('run')
        if i < 2:
            pPr = p_set_tr_center if len(cnv_stars) > 0 else p.set(line=24, jc='center')
        para = p.write(pPr, run)
        if i == 1 and len(cnv_stars) > 0:
            para += p.write(pPr, r_aiyi.text('(基因组倍性%s)' % (ploidy), 9))
        tcs += tc.write(para, tc.set(w=ws[i], color=green_lighter, fill=green_lighter))
    return tr.write(tcs)


def write_thead51(titles, **kwargs):
    ws = [1800, 1600, 1600, 1600, 1800]
    pPr = p.set(jc='center', spacing=[0.5, 0.5])
    if 'pPr' in kwargs:
        pPr = kwargs['pPr']
    if 'ws' in kwargs:
        ws = kwargs['ws']
    tcFill = kwargs.get('tcFill') or ''
    gridSpan = kwargs.get('gridSpan') or 0
    tcs = ''
    size = kwargs.get('size') or 10
    weight = kwargs.get('weight') or 0
    inline = kwargs.get('inline') or ['top', 'bottom']
    for i in range(len(titles)):
        t = titles[i]
        run = r_aiyi.text(t, size=size, weight=weight)
        borders = ['top', 'bottom']
        color = gray
        if i > 0:
            borders = inline
            if 'inline' in kwargs:
                color = white
        tcs += tc.write(p.write(pPr, run), tc.set(w=ws[i], fill=tcFill, tcBorders=borders, color=color, gridSpan=gridSpan))
    return tr.write(tcs)


def write_tr51(item, ws, row=0, count=0):
    tcs = ''
    size = 9
    fill = ''
    for i in range(len(item)):
        texts = item[i]
        para = ''
        if isinstance(texts, str) or isinstance(texts, unicode):
            arr = texts.split('\n')
        elif isinstance(texts, list):
            arr = texts
        else:
            arr = [str(texts)]
        for t in arr:
            run = r_aiyi.text(t, size=size)
            para += p.write(p_set_tr_center, run)
        tcs += tc.write(para, tc.set(w=ws[i], fill=fill, tcBorders=['bottom'], color=gray))
        # tcs += tc.write(para, tc.set(w=ws[i], fill=fill, color=bdColor, tcBorders=['bottom']))
    return tr.write(tcs)


def write_tr1(text, fill='', wingdings=True, jc='center', weight=0, size=9, before=0.2, tcBorders=['top', 'bottom'], color=gray):
    pPr = p.set(jc=jc, spacing=[before, 0.2])
    para = ''
    text = text or ''
    for t in text.split('\n'):
        run = r_aiyi.text(
            ' ' + t,
            size=size,
            color='' if fill in [gray, '', bg_blue] else white,
            wingdings=wingdings, space=True, weight=weight
        )
        para += p.write(pPr, run)
    tcs2 = tc.write(para, tc.set(w=w_sum, fill=fill, tcBorders=tcBorders, color=color))
    return tr.write(tcs2)


def write_tr2(data, fill=gray, bdColor=gray):
    return write_tr1(data, fill, False, weight=1, size=10, color=fill or gray)


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
    pPr = item.get('pPr') or p.set(jc=jc, spacing=[0.3, 0.3])
    size = item.get('size') or '小五'
    weight = item.get('weight') or 0
    wingdings = item.get('wingdings') or False
    italic = item.get('italic') or False
    para = ''
    tcFill = item.get('tcFill') or ''
    tcColor = item.get('tcColor') or gray
    level = item.get('level')
    w = item.get('w') or w_sum
    underline = item.get('underline') or ''
    if level:
        tcFill = get_level_color(level)
    tcBorders = ['top', 'bottom']
    if 'tcBorders' in item:
        tcBorders = item.get('tcBorders')
    gridSpan = item.get('gridSpan') or 0
    lineSize = item.get('lineSize') or 8
    color = item.get('color') or 'auto'
    vMerge = item.get('vMerge') or ''
    text = str(text)
    for t in text.split('\n'):
        if wingdings is True:
            t = ' ' + t
        run = r_aiyi.text(t, size=size, weight=weight, italic=italic, wingdings=wingdings, space=True, color=color, underline=underline)
        para += p.write(pPr, run)
    return tc.write(para, tc.set(w=w, fill=tcFill, tcBorders=tcBorders, gridSpan=gridSpan, color=tcColor, lineSize=lineSize, vMerge=vMerge))


def write_pages(t, sample_id):
    title = get_page_titles()
    relationship = Relationship()
    pkg_parts, relationshipss = '', ''
    title += ['']
    for i in range(len(title)):
        h_index = 'header%d' % (i + 1)
        if i == len(title) - 1:
            paras1, rel = '', ''
        else:
            paras_cover = p.write(
                p.set(spacing=[1, 0]), r_aiyi.text(title[i], '五号', color=RGB_to_Hex('62,175,150'), space=True)
            )
            tcs = ''
            tcs += tc.write(paras_cover, tc.set(w=12*567, tcBorders=[]))
            tcs += tc.write(p.write(), tc.set(w=6*567, tcBorders=[]))
            paras1 = table.write(tr.write(tcs, tr.set(trHeight=1.25*567)), tblBorders=[], jc='left')
            # rel = relationship.write_rel('logo_weizhi', target_name='media/logo_weizhi.png')
            rel = ''
        pkg_parts += relationship.about_page(h_index, paras1, page_type='header', rels=rel)
        relationshipss += relationship.write_rel(h_index, 'header')

    # 页头-cover
    header_id_cover = 'headercover'
    relationshipss += relationship.write_rel(header_id_cover, 'header')
    pkg_parts += relationship.about_page(header_id_cover, p.write(), page_type='header')

    # 页脚-cover
    page_type = 'footer'
    footer_id_cover = 'cover'
    size = 9
    paras_cover = ''
    # paras += p.write(p.set(jc='right'), sdt.write())
    paras_cover += p.write(p.set(jc='right'), r_aiyi.text('仅用于科研，请勿用于临床诊断。', size))
    relationshipss += relationship.write_rel(footer_id_cover, page_type)
    pkg_parts += relationship.about_page(footer_id_cover, paras_cover, page_type=page_type)
    # 页脚
    page_type = 'footer'
    footer_id = 'report_time'
    texts = [
        {'text': '样本编号:', 'w': 2 * 567, 'size': size},
        {'text': sample_id, 'w': 7 * 567, 'size': size},
        {'text': '报告日期:', 'w': 2 * 567, 'size': size},
        {'text': t, 'w': 7 * 567, 'size': size},
    ]
    tcs = ''
    for t in texts:
        tcs += write_tc_weizhi(t)
    paras = table_weizhi(tr.write(tcs))
    # paras += p.write(p.set(jc='right'), sdt.write())
    relationshipss += relationship.write_rel(footer_id, page_type)
    pkg_parts += relationship.about_page(footer_id, paras, page_type=page_type)
    # return footer, relationships
    return pkg_parts, relationshipss


def write_kangyuan(neoantigens):
    para = ''
    ws = [1600, 1600, 2600, 2600, 1600]
    trs = write_thead51(['基因', '多肽', '亲和力（突变/正常）', '突变点（克隆组成）', 'HLA分子'], ws=ws)
    # neoantigen = get_neoantigen()[:15]
    # neoantigen = neoantigens.sort(key=lambda x: x['MutRank'])[:15]
    neoantigen = neoantigens[:15]
    if len(neoantigen) == 0:
        trs += write_tr51(['无'] * len(ws), ws, 0, 1)
    for n, item in enumerate(neoantigen):
        # q = get_quantum_cellurity(chr, start)
        q = float2percent(item.get('cellularity')) or ''
        if q:
            q = '(%s)' % q
        item = [item['gene'], item['mut_peptide'], '/'.join([item['mut_aff'], item['ref_aff']]), item['mut'] +q, item['hla']]
        trs += write_tr51(item, ws, n, len(neoantigen))
    para += table_weizhi(trs)
    para += p.write(r_aiyi.text('注：仅显示部分重要新抗原信息', size=8.5))
    para += write_explain_new({'title': '结果说明',
                               'text': '新抗原是指因肿瘤基因突变所导致的能够被该患者免疫系统HLA分子所识别，有潜力能够激活患者免疫系统的新生抗原，这是一组异常多肽片段。新抗原预测信息能够作为癌症个性化治疗疫苗或者特异性细胞治疗最核心的信息。新抗原预测一般 通过外显子组测序得到该患者所有的编码区域基因突变，进一步通过外显子组或者转录组获得该患者的HLA分型，根据基因突变信息和HLA分子信息，预测各个突变位点与该患者HLA分子结合的亲和力，并进一步通过转录组测序筛选其中表达的新抗原。本次未行转录组检测，会明显降低新抗原预测的准确性。'})
    # para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    return para


def write_table_naiyao():
    text = '''研究	干预手段	EGFR突变人群	疗效	毒副作用AEs
    CheckMate012\t厄洛替尼+纳武利尤单抗	21例（20例经E治疗，1例Naive）\tORR 19%<br>24周PFS率51%\t3级毒性发生率为19%，2例终止治疗，未发生4级-5级毒性
    NCT02013219\t厄洛替尼+atezolizumab	20例naive	ORR 75%<br>mPFS 11.3月	39%患者有3-4级AEs，主要为发热和ALT升高，未见肺炎和间质性肺病
    NCT0208812\t吉非替尼+durvalumab\t9例naïve（A组）<br>10例经28d G治疗（B组）\tORR 77.8% (A)<br>ORR 80% (B)\t导致治疗终止的3-4级AEs发生在B组共4例
    KeyNote021\t吉非替尼+帕博利珠单抗\t12例naïve（A）<br>7例naïve（B）	ORR 41.7% SD 41.7% <br>mPFS 19.5月（A）<br>ORR 14.3%<br>57.1%未评估<br>mPFS 1.4月（B）	33.3%（4例）发生3级以上AEs，其中3例导致治疗终止<br>85.7%（6例）发生3级以上AEs，其中5例导致治疗终止
    TATTON\t奥希替尼+durvalumab\t23例经EGFRTKIs治疗(A)<br>11例Naïve（B）\tORR 57.1% T790M阳性67%，阴性21%<br>ORR 80%（B）\tA组：26%发生间质性肺病<br>B组：64%发生间质性肺病
    CAURAL\t奥希替尼+durvalumab（对照组为奥希替尼单药）\t12例经治且T790M阳性\tORR 64%（低于对照组的80%）<br>PFS未达到（对照组为19.3月）<br>12月生存率为86%（对照组为100%）\t8%发生3级以上AEs，间质性肺病发生1例且推测由奥希替尼引起'''
    text = text.strip('\n').split('\n')
    trs = ''
    ws = [1600, 1800, 2000, 2000, 2600]
    for index, t in enumerate(text):
        ts = t.strip().split('\t')
        tcs = ''
        fill = ''
        # for t1 in ts:
        weight = 1 if index == 0 else 0
        for col, t1 in enumerate(ts[:5]):
            para = ''
            for t2 in t1.split('<br>'):
                para += p.write(p_set_tr, r_aiyi.text(t2, 9, weight=weight))
            if para == '':
                para = p.write()
            tcs += tc.write(
                para,
                tc.set(ws[col], fill=fill, tcBorders=[])
            )
        trs += tr.write(tcs)
    return table_weizhi(trs)


def write_detail_table(var_items, cnv_items, sv_items, ploidy):
    para = ''
    if len(var_items) >0:
        para += h4_aiyi('体细胞突变相关基因详细信息')
        para += write_table_var(var_items)
    if len(cnv_items) > 0:
        para += h4_aiyi('扩增相关基因详细信息')
        para += write_table_cnv(cnv_items, ploidy)
    return para


def h2_aiyi(cat):
    return h4_aiyi(cat=cat, spacing=[1, 0.5], weight=1, size=11, outline=2)


def h3_aiyi(text, size=12, spacing=[0.5, 0.2]):
    return h4_aiyi(' %s' % text, wingdings=True, spacing=spacing, ind=['hanging', 0.5], outline=3, size=size, line=12)


def h4_aiyi(text='',
            size=12,
            spacing=[1, 0.5], weight=1, ind=[0, 0], line=15, runs='', bm_name='', cat=None, color='', jc='left',
            wingdings=False, outline=4,
            rule='exact'
            ):
    space = False
    if cat is not None:
        bm_name = cat['bm']
        text = cat['title']
    if wingdings:
        space = True
        text = ' %s' % text
    run = r_aiyi.text(text, size=size, weight=weight, color=color, wingdings=wingdings, space=space) + runs
    return p.write(p.set(spacing=spacing, line=line, rule=rule, outline=outline, ind=ind, jc=jc), run, bm_name)


def table_weizhi(trs2, tblBorders=['bottom'], line=1, jc='center', bdColor=gray):
    para = table.write(trs2, tblBorders=tblBorders,  bdColor=bdColor, jc=jc)
    if line > 0:
        para += p.write(p.set(line=line, rule='exact'))
    return para


def float2percent(p, n=2):
    try:
        p = float(p)
    except:
        return p
    return '%s%%' % (round(p*100, n))


#报告相关数据
def get_catalog():
    catalogue = [
        [u"一、靶向治疗提示", 0, 1, 10],
        [u"一、靶向治疗提示", 2, 1, 23],
        [u"该驱动变异关键突变循证医学证据", 2, 1, 23],
        [u"靶向治疗解读说明", 2, 1, 23],
        [u"二、免疫治疗提示", 0, 1, 10],
        [u"二、免疫治疗提示", 2, 1, 23],
        [u"MSI微卫星不稳定检测结果", 2, 1, 23],
        [u"TMB肿瘤突变负荷检测结果", 2, 2, 23],
        [u"DDR基因（DNA损伤修复反应基因）检测结果", 2, 6, 23],
        [u"免疫治疗敏感驱动突变检测结果", 2, 6, 23],
        [u"免疫治疗耐药驱动突变检测结果", 2, 2, 23],
        [u"免疫治疗超进展相关基因检测结果", 2, 3, 23],
        [u"HLA分型检测结果", 2, 3, 23],
        [u"肿瘤新抗原检测结果", 2, 3, 23],
        [u"免疫治疗解读说明", 2, 3, 23],
        [u"三、化学治疗提示", 0, 3, 10],
        [u"三、化学治疗提示", 2, 4, 23],
        [u"各化疗药循证医学证据", 2, 5, 23],
        [u"四、肿瘤遗传性检测结果", 0, 5, 10],
        [u"肿瘤突变模式检测结果", 2, 8, 23],
        [u"肿瘤遗传性检测结果", 2, 8, 23],
        [u"五、基因突变检测结果汇总", 0, 5, 10],
        [u"体细胞突变", 2, 6, 23],
        [u"重点基因拷贝数检测结果", 2, 6, 23],
        [u"肿瘤重要信号通路变异信息汇总", 2, 7, 23],
        [u"检测方法", 2, 7, 23]
    ]
    items = []
    for index, cat in enumerate(catalogue):
        item = {"title": cat[0], 'left': cat[1], 'page': cat[2], 'style': cat[3], 'bm': bm_index0 + index}
        items.append(item)
    return items


def get_page_titles():
    title_cn, title_en = u' ', ' '
    title = '%s%s%s' % (title_cn, ' ' * 64,  title_en)
    title1 = '%s%s%s' % (title_cn, ' ' * (64+11),  title_en)
    titles = [title, title1]
    cats = get_catalog()
    for i in [0, 4, 15, 18, 21]:
        n = 64 + 14
        if test_chinese(cats[i]['title']) == 11:
            n -= 8
        titles.append('%s%s%s' % (cats[i]['title'], ' ' * n,  title_en))
    titles.append('附录')
    return titles


def get_imgs_weizhi(path, is_refresh=False, others=[]):
    if is_refresh:
        img_info = get_imgs(img_dir)
        img_info += get_imgs(path)
        img_info += get_imgs(weizhi_dir)
        img_info2 = []
        for info in img_info:
            is_exists = len(filter(lambda x: x['rId'] == info['rId'], img_info2))
            if is_exists == 0:
                img_info2.append(info)
        img_info2 += others

        my_file.write(img_info_path, img_info2)
    else:
        img_info2 = my_file.read(img_info_path)
    return img_info2


def get_var_new(gene, items1):
    items = filter(lambda x: x['gene'] == gene, items1)
    # 纯合缺失 TCN=0
    # 杂合缺失 TCN=1
    # 红色，表示该基因扩增；深蓝色，表示该基因纯合缺失；淡蓝色，表示该基因杂合缺失，扩增缺失状态未达阈值用灰色表示
    for item in items:
        if gene == item.get('gene'):
            tcn_em = item.get('tcn_em')
            lcn_em = item.get('lcn_em')
            try:
                tcn_em = int(tcn_em)
            except:
                tcn_em = tcn_em
            try:
                lcn_em =int(lcn_em)
            except:
                lcn_em = lcn_em
            if tcn_em > 0:
                return red, '扩增'
            if tcn_em == 0:
                return dark_blue, '纯合缺失'
            if tcn_em > 0 and tcn_em <= 3 and lcn_em == 0:
                return blue, '杂合缺失'
    return '', ''


def get_line(rId):
    img = get_img(img_info_path, rId)
    if img is not None:
        zoom = 17.7 / img['w']
        return int(zoom * img['h']) + 1
    return 0


def compare_level3(list1, list2):
    # 当相反证据量数量一致时，根据证据级别确定（证据级别的等级 1A＞1B＞2A＞2B＞3）
    eqs = ['1A', '1B', '2A', '2B', '3']
    for i in range(len(eqs)):
        eq = eqs[i]
        aa = filter(lambda x: x['level'] == eq, list1)
        for j in range(0, i+1):
            eq1 = eqs[j]
            bb = filter(lambda x: x['level'] == eq1, list2)
            if j < i and len(bb) > 0:
                return 2
            if len(aa) * len(bb) > 0:
                return 3
            if len(aa) > 0:
                return 1
            if len(bb) > 0:
                return 2
    return 3


def filter_rs_list(old_item):
    items = old_item['genes']
    rs_list = old_item['rs_list']
    for rs_item in rs_list:
        rs_list1 = []
        for item in items:
            if item['gene'] == rs_item['gene'] and item['rs'] == rs_item['rs'] and item['level'] == rs_item['level'] and item['category'] == rs_item['category']:
                rs_list1.append(item)
        rs_item['rs_list'] = rs_list1
    return rs_list


def concat_str(arr):
    if len(arr) == 1:
        return arr[0]
    tip1 = '、'.join(arr[:-1])
    if len(arr) > 1:
        return '合并'.join([tip1, arr[-1]])
    return tip1


def reset_sig(s_id):
    signature_cns = signature_cn.split('\n')
    for s_index, s in enumerate(signature_cns):
        if s.strip() == str(s_id):
            if s_index < len(signature_cns) - 1:
                text = signature_cns[s_index + 1].strip()
                return text
    return ''


def crop_img(input_url, output_url):
    if os.path.exists(input_url) is False:
        msg = 'file not exsits, %s' % input_url
        print msg
        return msg
    if os.path.exists(os.path.dirname(output_url)) is False:
        msg = 'folder not exists, %s' % os.path.dirname(output_url)
        print msg
        return msg
    img = Image.open(input_url)
    sp = img.size
    w, h = sp[0], sp[1]
    region = (0, h/3, w, h/3 * 2)
    if 'pie' in input_url:
        region = (w/3 - 60, 320, w / 3 * 2 + 200, h-320)
    if os.path.exists(output_url):
        os.remove(output_url)
    #裁切图片
    cropImg = img.crop(region)
    #保存裁切后的图片
    cropImg.save(output_url)
    return 'success'


def effect2cn(effect):
    if effect == 'Missense_Mutation':
        return '错义突变'
    if effect == 'Splice_Site':
        return '剪切位点突变'
    if effect == 'In_Frame_Ins':
        return '框内插入'
    if effect == 'In_Frame_Del':
        return '框内缺失'
    if effect == 'Frame_Shift_Ins':
        return '移码插入'
    if effect == 'Frame_Shift_Del':
        return '移码缺失'
    if effect == 'Splice_Region':
        return '剪切区域突变'
    if effect == 'Nonsense_Mutation':
        return '终止突变'
    return effect


def RGB_to_Hex(tmp, prefix='#'):
    rgb = tmp.split(',')#将RGB格式划分开来
    strs = '#'
    for i in rgb:
        num = int(i)#将str转int
        #将R、G、B分别转化为16进制拼接转换并大写
        strs += str(hex(num))[-2:].replace('x','0').upper()
    return '%s%s' % (prefix, strs)