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
orange = 'F14623'
colors = ['2C3792', '3871C1', '50ADE5', '37AB9C', '27963C', '40B93C', '80CC28']
borders = ['top', 'right', 'bottom', 'left']
title_cn, title_en = u'多组学临床检测报告', 'AIomics1'

# 初始化
aiyi_dir = os.path.join(static_dir, 'aiyi')
base_dir = os.path.join(aiyi_dir, 'base_data')
chemotherapy_dir = os.path.join(aiyi_dir, 'chemotherapy')
img_dir = os.path.join(aiyi_dir, 'images')
my_file = File()
base_file = File(base_dir)
print os.path.exists(chemotherapy_dir)
gene_list12 = base_file.read('1.2gene_list.json')
gene_list53 = base_file.read('5.3gene_list.xlsx', sheet_name='Sheet2')
company = base_file.read('5.company.txt', sheet_name='Sheet2')
gene_MoA = base_file.read('gene_MoA.tsv')
signature_cn = base_file.read('signature_cn.txt')
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
sect_pr_catalog = set_page('A4', footer='rIdFooter1')
# sect_pr_catalog = set_page('A4', footer='rIdFooter1', header='rIdHeader1')
sect_pr_content = set_page('A4', footer='rIdReport_time', pgNumType_s=1, header='rIdHeader2')
con1 = p.write(p.set(rule='exact', line=12, sect_pr=set_page(type='continuous', cols=1)))
con2 = p.write(p.set(rule='exact', line=12, sect_pr=set_page(type='continuous', cols=2, space=40)))
page_br = p.write(set_page(page_margin=page_margin))
sect_pr1 = set_page('A4', page_margin=page_margin, footer='rIdFooter2', header='rIdHeader2', type='continuous', cols=1)
# sect_pr2 = set_page('A4', page_margin=page_margin, footer='rIdReport_time', header='rIdHeader2', pgNumType_s=1)
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
blue_d = '71BAE3'
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
level_tips = [
    {'text': 'A', 'tip': 'FDA/NCCN推荐药物', 'color': '#00B050', 'x': 1.4},
    {'text': 'B', 'tip': '专家共识药物', 'color': '#00B0F0', 'x': 4.2},
    {'text': 'C', 'tip': '临床证据药物', 'color': '#32B1D1', 'x': 6.15},
    {'text': 'D', 'tip': '临床前证据药物', 'color': '#71BAE3', 'x': 8.15}
]


def get_report_core(data):
    overview = data.get('overview') or {}
    other_pic = []
    for pic_k in ['signature_pic', 'tmb_pic']:
        pic_path = overview.get(pic_k)
        if pic_path and os.path.exists(pic_path):
            pic_info = get_img_info(pic_path)
            other_pic.append(pic_info)
    img_info = get_imgs_aiyi(img_dir, is_refresh=True, others=other_pic)
    body = write_body(title_cn, title_en, data)
    pages = write_pages(data.get('report_time'))
    pkgs1 = write_pkg_parts(img_info, body, other=pages)
    return pkgs1


def write_body(title_cn, title_en, data):
    diagnose = data.get('diagnosis')
    variant_list = data.get('variant_list')
    overview = data.get('overview')
    stars0 = data.get('stars0')
    stars = data.get('stars')

    sample_detail = data.get('sample_detail')
    sequencing_type = sample_detail.get('sequencing_type') or ''
    #关于hrd
    hrd_hisens_loh = overview.get('hrd_hisens_loh')
    hrd_hisens_tai = overview.get('hrd_hisens_tai')
    hrd_hisens_lst = overview.get('hrd_hisens_lst')
    hrd = hrd_hisens_loh + hrd_hisens_lst + hrd_hisens_tai
    paras_hr, items_hr = write_hrd(sequencing_type, data, [0.5, 0])
    # print len(variant_list), report_detail.keys()
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
            data['paras_hr'] = paras_hr
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
    chem_items, trs3 = get_data3(data.get('rs_geno'), diagnose)

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
        {'tip1': tip_ddr1, 'text': tip_ddr, 'level': level_ddr, 'w': (w_sum-300) / 2},
        {'tip1': tip_mingan1, 'text': tip_mingan, 'level': level_mingan, 'w': (w_sum-300) / 2},
        {'tip1': tip_naiyao1, 'text': tip_naiyao, 'level': level_naiyao, 'w': (w_sum-300) / 2},
        {'tip1': tip_chaojinzhan1, 'text': tip_chaojinzhan, 'level': level_chaojinzhan, 'w': (w_sum-300) / 2},
        {'tip1': tip_hla1, 'text': tip_hla, 'level': level_hla, 'w': w_sum}
    ]
    data['chem_tip'] = [
        '可能有效且毒副作用低的药物：%s' % ('无' if len(trs3[1][1]) == 0 else ', '.join(trs3[1][1])),
        ]
    data['recent_study'] = [{'text': tip_yichuan, 'level': ''}, {'text': tip_signature, 'level': level_signature}]
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
    body += write_chapter3(5, trs3, chem_items)
    body += write_chapter4(6, data)
    body += write_chapter5(7, data)
    # body = write_read_guide()
    return body


def write_cover(data):
    cx = 3.76
    run_logo1 = r_aiyi.picture(cx, rId='cover1', posOffset=[0, -1.37])
    run_logo2 = r_aiyi.picture(cx, rId='cover1', posOffset=[13.5, 22.2])
    para = ''
    sample_detail = data.get('sample_detail')
    report_time = data.get('report_time')
    para += p.write(p.set(jc='center', spacing=[5, 0]), r_aiyi.text('肿瘤个体化诊疗基因检测', '小初', weight=1))
    para += p.write(p.set(jc='center', spacing=[0.5, 4]), r_aiyi.text('Precision Oncology & Personalized Treatment', '小三', weight=1))
    texts = [
        {'label': '项目名称', 'value': u'实体瘤580基因检测'},
        {'label': '患者姓名', 'key': 'patient_name'},
        {'label': '样本编号', 'key': 'sample_id'},
        {'label': '送检医院', 'key': 'inspection_department'},
        {'label': '收样日期'},
        {'label': '报告日期', 'value': report_time},
    ]
    size = '四号'
    p_set = p.set(line=24, ind=[8, 0])
    for t_item in texts:
        label = t_item.get('label')
        key = t_item.get('key')
        value = t_item.get('value') or sample_detail.get(key) or ''
        n = 34
        len_cn = test_chinese(value)
        kongge = n - len(value) - len_cn
        left = 11
        right = kongge - left
        run = r_aiyi.text('%s：' % label, size, 1)
        run += r_aiyi.text('%s%s%s' % (' ' * left, value, ' ' * right), size, 1, space=True, underline='single')
        para += p.write(p_set, run)
    para += p.write(p.set(sect_pr=set_page('A4')))
    return para


def write_catalog():
    # 目   录
    para = p.write(
        p.set(spacing=[0, 0], jc='center', outline=3, line=24, rule='auto'),
        r_aiyi.text("目录", size=18, color=white) +
        r_aiyi.picture(12, rId='content', relativeFrom=['page', 'page'], align=['center', 'center'])
    )
    para += p.write(p.set(sect_pr=sect_pr_catalog))
    return para


def write_chapter0(title_cn, data):
    para = ''
    sample_detail = data.get('sample_detail') or {}
    para += write_patient_info(data)
    title = u'靶向治疗提示'
    para += h4_aiyi(title, spacing=[0.5, 0.5])
    sequencing_type = sample_detail.get('sequencing_type') or ''
    para += write_target_tip(data)
    para += write_immun_tip(data.get('immun_tip'))
    technology = '检测技术：基于Illumina novaseq平台，检测外显子组联合35个融合基因，肿瘤组织500×、外周血100×'
    if 'panel' in sequencing_type.lower():
        technology = '本检测基于第二代测序技术，本次检测使用IDT 39M全外显子探针联合35个融合基因内含子区域，以及其他50个基因在实体肿瘤中高发突变的热点区域。测序深度如下：肿瘤组织1000×，ctDNA 10000×，胚系对照100×。'
    tips = [
        {'title': '化学治疗提示', 'text': data['chem_tip'], 'rId': blue_d},
        {'title': '最新研究进展治疗提示', 'sub_title': '（完整信息见附录）', 'text': data['recent_study'], 'rId': bg_blue},
        {'rId': bg_blue, 'title': '检测方法', 'text': technology + '\n相关局限性说明：由于肿瘤异质性等原因，本检测报告仅对本样本负责，患者诊疗决策需在临床医生指导下进行'},
    ]
    for tip in tips:
        para += h4_aiyi(tip['title'], spacing=[1, 0.5])
        tips = tip['text']
        if isinstance(tip['text'], list) is False:
            tips = tips.split('\n')
        for t in tips:
            rId = tip.get('rId')
            if isinstance(t, dict):
                text = t.get('text')
                rId = t.get('rId') or bg_blue
                level = t.get('level')
                if level:
                    arr = filter(lambda x: x.get('level') == level, level_tips)
                    if len(arr):
                        rId = arr[0].get('color').lstrip('#')
            else:
                text = t
            if len(text) > 0:
                rId = '#' + rId
                setting = {'stroke-color': rId, 'fill-color': rId, 'radius': 0.1}
                para += p.write(
                    p.set(line=10, rule='exact', spacing=[0, 0.5], ind=['hanging', 1.3]),
                    # r_aiyi.picture(cy=0.3, rId=rId, posOffset=[0, 0.15])
                    r_aiyi.radius(0.3, 0.3, **setting)
                    + r_aiyi.text('   ' + text, 9.5, space=True)
                )
    para += p.write(p.set(sect_pr=sect_pr_content))
    para += write_read_guide()
    return para


def write_chapter1(data):
    cats = get_catalog()[0: 4]
    para = ''
    para += h4_aiyi(cat=cats[1], spacing=[0, 1])

    para1 = ''
    para1 += h4_aiyi(cat=cats[2])
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
        if action2 and action2 not in action:
            action.append(action2)
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
        ind = [0.5, 0]
        if item.get('hrd'):
            action_name = 'HRD%s' % item.get('col2')
            para_hrd = data.get('paras_hr')
        elif item.get('hr'):
            action_name = item.get('hr')
            para_hrd = data.get('paras_hr')
        para1 += p.write(
            p.set(shade=bg_blue, line=24),
            r_aiyi.text('  变异事件%s:  ' % (i + 1), space=True) +
            r_aiyi.text(action_name, color=white, fill=red, space=True)
        )
        # para1 += p.write(
        #     p.set(shade=red, line=24),
        #     r_aiyi.text('  变异事件%s：%s(%s%s)' % (i + 1, gene, action1, cc)
        #                 , color=white, space=True)
        # )
        para_index = 1

        pPr = p.set(line=15, ind=ind, spacing=[0, 1])
        para_eve = ''
        oncogenicity_variant_summary = item.get('oncogenicity_variant_summary')
        if oncogenicity_variant_summary:
            para_eve += p.write(pPr, r_aiyi.text(oncogenicity_variant_summary, 9))
        aiyi_db = item.get('known_db')
        para_eve += write_evidence1(gene, aiyi_db)
        if para_eve:
            para1 += h4_aiyi('（1）该驱动变异关键循证医学证据') + para_eve
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
            para_gene += p.write(p.set(line=15, ind=[1, 0], spacing=[0, 0.5]), r_aiyi.text('%s %s基因' % (gene, '、'.join(xingzhi)), 9, 1))
        summary = item.get('summary_cn')
        if summary:
            para_gene += p.write(p.set(line=15, ind=[1, 0], spacing=[0, 0]), r_aiyi.text(summary, 9))
        cn_intro = item.get('cn_intro')
        if cn_intro:
            para_gene += p.write(p.set(line=15, ind=[1, 0], spacing=[0, 1.5]), r_aiyi.text(cn_intro, 9))
        if para_gene:
            para1 += h4_aiyi('（%d）该基因临床治疗说明' % (para_index), ind=ind)
            para1 += para_gene
        # else:
        #     para1 += p.write()
        para1 += para_hrd
    para1 += p.write(p.set(sect_pr=set_page(page_margin=page_margin4, header='rIdHeader3')))
    para1 += write_chapter13(cats[3])
    # tip = tip
    tip = '本次检测共找到%d个驱动基因的变异事件' % len(genes.keys())
    if len(action) > 0:
        tip += '：'
    if len(action) < 2:
        tip += '%s' % ''.join(action)
    else:
        tip += '、'.join(action[:-1]) + '和' + action[-1]
    tip += '。'
    paras = para
    paras += p.write(p.set(line=19.2, rule='exact'), r_aiyi.text(tip))
    paras += write_common_diagnosis(data)
    paras += p.write(p.set(line=18, rule='exact'), r_aiyi.text('注：驱动变异是靶向治疗提示的基础和前提条件，此处仅呈现通过数据库、文献等各方面数据和规则判断为驱动突变的肿瘤变异事件。', '小五'))
    paras += para1

    return paras


def write_chapter2(index, data):
    n, start, bm0 = 11, 5, 453150350
    cats = get_catalog()[start-1: start + n]
    para = ''
    immun_tip = data.get('immun_tip') or []
    text = '、'.join([x.get('tip1') or x.get('text') for x in immun_tip])

    para += h4_aiyi(cat=cats[1], spacing=[0, 1])
    para += p.write(p.set(line=19.2, rule='exact'), r_aiyi.text('本次检测显示该患者%s。' % text, '五号'))
    para += p.write(
        p.set(spacing=[0, 1]),
        r_aiyi.text('注：与靶向治疗一个驱动基因变异推荐一种或者多种药物形成显著差异，免疫治疗目前是多个生物标志物同时指导免疫检查点抗体治疗（包括PD1和CTLA4抗体）。免疫治疗需要综合多维度标志物进行综合决策。本检测报告从两个维度将纷繁复杂的各类型免疫治疗标志物进行分类：一、证据方向维度，将相关标志物分成敏感类和耐药类（含超进展）标志物。由于在所有未经筛选的肿瘤中，免疫检查点治疗的有效率大概仅有20%左右，所以一般未出现敏感类标志物时，提示免疫治疗可能无效。同时，多数耐药标志物均是无视敏感类标志物的存在与否均会导致免疫治疗耐药。然而不同证据的采信程度究竟有多高，需要进一步评估权衡；二、证据级别维度：根据ASCO、AMP和CAP共同发布的规则进行证据级别划分。A级：1、针对某一特定癌症，经过FDA批准的；2，针对某一特定癌种，专业指南推荐的；B级：基于高水平研究，相关领域专家意见一致；C级：1、同一分子标志物，FDA批准用于其他癌症；2、作为临床试验纳入标准；3、多项小型研究形成的一些共识；D级：临床前研究或者少量案例报道，结果不确定。其中A级和B级推荐药物相关变异为强烈临床意义的一类变异，C级和D级推荐药物相关变异为潜在临床意义的二类变异。', '小五')
    )
    msi_info = data.get('msi_info')
    tmb_info = data.get('tmb_info')
    msi_sort_paired_total = msi_info.get('total')
    msi_sort_paired_somatic = msi_info.get('somatic')
    msi_score = msi_info.get('score')

    chs = [
        {
            'title': h4_aiyi(cat=cats[2], spacing=[0, 1]), 'note_before': 0,
            'img_id': 'msi_score',
            'data': msi_info,
            'note': '注：肿瘤组织-正常样本配对分析的模式',
            'before': 8,
            'cy': 4.19,
            'w': 3600,
            'infos': [
                {'title': '结果说明：', 'text':
                    'MSI是指与正常组织相比，在肿瘤中某一微卫星由于重复单位的插入或缺失而造成的微卫星长度的任何改变，出现新的微卫星等位基因现象。' +
                    '其发生机制主要包括DNA多聚酶的滑动导致重复序列中1个或多个碱基的错配和微卫星重组导致碱基对的缺失或插入。' +
                    '该结果采用经FDA批准的MSIsensor算法获得。本次检测采用肿瘤组织-正常样本配对分析的模式，' +
                    '共分析了%s个微卫星位点，' % msi_sort_paired_total +
                    '其中%s个微卫星位点为具有显著差异的体细胞变异点，' % msi_sort_paired_somatic +
                    '比例为%s%%，' % msi_score +
                    '即MSIsensor评分为%s。' % msi_score +
                    '研究表明，MSIsensor评分免疫治疗疗效正相关，也与错义突变和插入缺失突变总量显著正相关（PMID:31048490）。'},
                {'title': '检测意义：', 'text': '目前FDA批准Pembrolizumab用于dMMR/MSI-H型的转移性实体瘤，Nivolumab用于dMMR/MSI-H的转移性结直肠癌。Science发表了NCT01876511的临床研究结果显示，Pembrolizumab用于治疗MSI-H的晚期肿瘤患者，MSI-H型肿瘤患者ORR高达54%。MSI-H在结直肠癌、胃癌、子宫内膜癌中较多，其他多种癌种都有一定量的分布。MSI是MMR（错配修复系统）的一个反映标志，MMR是人体细胞DNA修复的一种方式之一，MMR缺陷导致DNA出错的概率大规模提升，进而导致该类型肿瘤细胞具有非常高的突变量，而高的突变负荷进一步导致肿瘤细胞高概率采用PD1等通路的免疫逃逸机制。因此，PD1抗体对MSI-H/dMMR肿瘤更可能有效。'},
            ] },
        {
            'title': h4_aiyi(cat=cats[3]), 'before': 0, 'note_before': 13,
            'img_id': 'tmb',
            'cy': 7,
            'note': tmb_info.get('tmb_tip'),
            'data': tmb_info,
            'w': 3200,
            'infos': [
                {'title': '结果说明', 'text': '该结果通过肿瘤外显子组检测得到。全外显子组包含人体所有大约两万多个基因，大约有38M左右的编码区域。TMB肿瘤突变负荷指平均每M（兆）区域，肿瘤细胞发生的非同义突变的个数。（证据级别说明：常规以10个突变/Mb标准时非小细胞肺癌证据级别为B级，结直肠癌和胰腺癌由于免疫治疗有效率低，常规阈值为20，其他所有癌种均为C级；当TMB大于20，高于绝大多数情况阈值时，非小细胞肺癌更新为A级，其他癌种（结直肠癌和胰腺癌除外）更新为B级。'},
                {'title': '检测意义：', 'text': 'TMB在多项临床研究中均被证明能够有效区分PD1抗体、CTLA4抗体等免疫检查位点抗体治疗是否有效的人群。综合型研究表明，在不同肿瘤中，不同患者的PD1抗体治疗有效性的差异55%可以由TMB的差异解释。TMB是不同肿瘤间体细胞突变量的评估。一般情况下，TMB越高，该肿瘤可能会拥有更多的肿瘤新生抗原，该肿瘤也越有可能在经过免疫检查位点抗体解除肿瘤免疫逃逸之后，被患者自身的免疫系统所识别，相关治疗在该患者身上也就越可能有效。'},
            ]
        }
    ]
    for ch in chs:
        para += write_chapter21(ch)
    para += h4_aiyi(cat=cats[4]) + data.get('para_ddr')
    para += h4_aiyi(cat=cats[5]) + data.get('para_mingan')
    para += h4_aiyi(cat=cats[6]) + data.get('para_naiyao')
    para += h4_aiyi(cat=cats[7]) + data.get('para_chaojinzhan')
    para += h4_aiyi(cat=cats[8]) + data.get('para_hla')
    para += h4_aiyi(cat=cats[9]) + write_kangyuan(data.get('neoantigens'))
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    para += h4_aiyi(cat=cats[10])
    para += h4_aiyi('1、免疫治疗与肿瘤免疫')
    para_set = p.set(line=18, rule='exact')
    para += p.write(para_set, r_aiyi.text('自2012年，约翰霍普金斯大学PD1抗体临床试验结果发表在《新英格兰医学杂志》之后，免疫治疗真正进入临床医生和产业界的视野，并迅速取代靶向治疗成为肿瘤治疗最新最主流的治疗研究方向。CTLA4、PD1抗体以惊人的产业化速度和疗效，迅速在多个癌种中获批，并在肺癌中成为一线治疗药物。PDL1表达、微卫星不稳定迅速成为有效协助患者药物筛选的分子标志物，肿瘤突变负荷TMB、新抗原负荷、肿瘤CD8+T淋巴细胞浸润状态等在各种数据中证明具有筛选有效患者的能力，然而，新型免疫治疗手段以超越基础研究的速度在发展，免疫治疗人群筛选和联合治疗时机选择远远没有到达完美，新的标志物层出不求', '小五'))
    para += p.write(para_set, r_aiyi.text('肿瘤免疫治疗是通过协助免疫系统发挥被抑制或者缺失的免疫能力，进而实现肿瘤治疗的手段。更好的理解肿瘤免疫过程，能够协助我们对各种新型肿瘤免疫治疗手段和新型标志物形成更好的全局性理解，以便我们更好的采取与化疗、放疗、靶向治疗的联合治疗手段，优化免疫治疗时机和方式的选择。肿瘤免疫周期理论是由Mellman等人提出来的肿瘤免疫过程框架，目前已经成为肿瘤免疫学研究和临床应用的思维框架。', '小五'))
    para += h4_aiyi('2、肿瘤免疫周期理论')
    para += p.write(r_aiyi.picture(cy=10, rId='2.4.2', align=['center', ''], posOffset=[0, 0.5]))
    para += p.write(para_set) * 16
    para += p.write(para_set, r_aiyi.text('肿瘤免疫治疗是通过协助免疫系统发挥被抑制或者缺失的免疫能力，进而实现肿瘤治疗的手段。更好的理解肿瘤免疫过程，能够协助我们对各种新型肿瘤免疫治疗手段和新型标志物形成更好的全局性理解，以便我们更好的采取与化疗、放疗、靶向治疗的联合治疗手段，优化免疫治疗时机和方式的选择。肿瘤免疫周期理论是由Mellman等人提出来的肿瘤免疫过程框架，目前已经成为肿瘤免疫学研究和临床应用的思维框架。', '小五'))
    para += h4_aiyi('（1）肿瘤细胞死亡并释放肿瘤特异抗原', size='五号')
    para += p.write(para_set, r_aiyi.text('从某种意义上说，肿瘤是由基因突变积累形成的疾病，同时，肿瘤基因突变也是肿瘤免疫过程发生的主要驱动因素。各种原因形成的肿瘤基因突变，部分情况下会让肿瘤细胞表达出与未突变基因不一样的蛋白质，其中部分突变蛋白的肽段会被身体的免疫系统识别为“外源”抗原，即所谓的“新抗原”。当肿瘤因为各种原因死亡后，含有新抗原的蛋白就会从肿瘤细胞中释放出来，进而驱动肿瘤免疫反应。所以，部分情况下，放疗、化疗、靶向治疗等治疗手段会跟免疫检查位点抗体治疗形成协同增强作用，也是因为该原因引起。最新部分研究甚至发现，不管PDL1表达状态，PD通路抗体联合化疗的疗效远高于单独化疗。微卫星高不稳定、肿瘤突变负荷高的肿瘤患者，一般情况下免疫检查位点抗体具有更好的疗效，也均是因为一般情况下，更高的突变负荷，意味着更多的新抗原可能性。', '小五'))
    para += h4_aiyi('（2）抗原提呈细胞摄取并处理肿瘤新抗原', size='五号')
    para += p.write(para_set, r_aiyi.text('抗原提呈细胞摄取含有新抗原的突变蛋白，并将水解为可以结合到MHC（主要组织相容性复合物，又称为HLA人类白细胞抗原）的肽段。抗原提呈细胞需要有包括促炎症细胞因子和肿瘤细胞死亡释放的信号因子在内的多种免疫原性信号才能够有效启动，因此，不同免疫状态下的肿瘤，新抗原的提呈效率是不一样的。不同人的MHC具有异质性，所以，不同患者哪些新抗原能够被提呈是不一样的。目前通过生物信息手段，新抗原能够以一定的准确性被预测出来。目前有研究通过预测的新抗原进行个性化治疗疫苗设计，促进抗原提呈过程，并取得了相当惊人的效果。', '小五'))
    para += h4_aiyi('（3）抗原提呈细胞进入淋巴结激活T细胞', size='五号')
    para += p.write(para_set, r_aiyi.text('（抗原提呈细胞被新抗原激活后，进入淋巴结激活初始T细胞。初始T细胞在共刺激分子的协同作用下诱导T细胞增殖并分化成为激活免疫杀伤的效应T细胞和抑制免疫杀伤的调节性T细胞，并通过两者比例的精确控制达成免疫反应性质确定和平衡。重组白细胞介素2（IL-2）即通过该环节调节肿瘤免疫反应。', '小五'))
    para += h4_aiyi('（4）激活的T细胞离开淋巴结进入循环系统', size='五号')
    para += p.write(para_set, r_aiyi.text('激活的T细胞基于细胞黏附分子组分变化的原因，脱离淋巴结进入循环系统。', '小五'))
    para += h4_aiyi('（5）T细胞穿过血管壁浸润到肿瘤微环境', size='五号')
    para += p.write(para_set, r_aiyi.text('肿瘤细胞死亡等原因引起的局部免疫反应会让周围组织跟炎症反应一样释放细胞因子和趋化因子，结合该部位血管内皮细胞由于炎症反应表达量增加的附着蛋白，让循环系统中的T细胞通过与血管内皮细胞锚定后进入肿瘤微环境中。初步研究结果表明，抗血管生成治疗与免疫治疗能够起到非常好的协同作用，部分临床试验中甚至提高将近一倍的治疗效果。', '小五'))
    para += h4_aiyi('（6）T细胞通过特异性受体识别肿瘤细胞', size='五号')
    para += p.write(para_set, r_aiyi.text('肿瘤细胞和一般体细胞一样，在核糖体进行蛋白质翻译的过程中，会有一定比例的缺陷蛋白并会被水解成肽段，其中能够被MHC结合的潜在抗原会被提呈到细胞膜表面。T细胞通过特异性受体（TCR）识别肿瘤细胞表面的新抗原。有研究表明，部分肿瘤中，肿瘤细胞MHC缺失对于免疫逃逸的发生贡献重要意义。目前CAR-T和TCR-T是重点研究方向，并在部分肿瘤中发挥惊人的治疗效果。CAR-T治疗又称人工合成嵌合抗原受体T细胞治疗，直接取代T细胞识别肿瘤细胞的方式，而TCR-T则是通过筛选分离针对肿瘤特定抗原的TCR，将原来未能识别肿瘤细胞的T细胞改造成能够识别肿瘤细胞的T细胞。', '小五'))
    para += h4_aiyi('（7）肿瘤细胞被T细胞识别并溶解消灭', size='五号')
    para += p.write(para_set, r_aiyi.text('当效应T细胞识别出肿瘤细胞表面的特异性抗原后，胞浆内储存的效应分子将朝目标方向释放，在不影响周围正常细胞的情况下溶解肿瘤细胞。CD8+T细胞是最重要的执行细胞杀伤的效应T细胞，所以，一般情况下，其肿瘤微环境浸润情况与免疫治疗疗效正相关。同时，PD1和CTLA-4是T细胞表面的抑制性受体，肿瘤细胞通过相应配体的表达，抑制T细胞的免疫杀伤作用。', '小五'))
    para += h4_aiyi('3.肿瘤免疫表型理论')
    para += p.write(r_aiyi.picture(cy=10, rId='2.4.3.1', align=['center', ''], posOffset=[0, 0.5]))
    para += p.write(para_set) * 16
    para += p.write(para_set, r_aiyi.text('肿瘤免疫表型理论是由Mellman在肿瘤免疫周期的基础上，进一步根据最新的研究成果，细化发展出来的一套肿瘤免疫分型体系。该分型体系根据相应的生物学机制，将肿瘤分成免疫沙漠型（棕色）、免疫豁免型（蓝色）和炎症型（红色）三种，并进一步根据宿主基因、微生物组、环境因素、治疗药物和癌症共五个维度，将影响免疫原性的多种研究进展整合成如下图所示，与免疫治疗疗效和免疫原性相关的癌症-免疫设定点。', '小五'))
    para += p.write(r_aiyi.picture(6, rId='2.4.3.2', posOffset=[2, 0.3]))
    # para += p.write(para_set) * 4
    para += p.write(p.set(ind=[24.5, 0], line=18, spacing=[0, 0]), r_aiyi.text('癌症免疫设定点是指产生有效癌症免疫原性所需克服的阈值，为指导免疫治疗临床应用和研究提供一个系统性框架。该设定点可以理解为理解为刺激因子、抑制因子和TCR结合信号（T细胞抗原受体与新抗原、癌症相关抗原等癌症抗原的亲和力）的平衡。癌症免疫治疗主要是针对肿瘤部位，通过增加的刺激因子、减少抑制因子或者增加TCR结合信号这三种方式进行的。', '小五'))
    para += h4_aiyi('4、免疫检查位点抗体疗联合传统治疗研究进展')
    para += p.write(para_set, r_aiyi.text('免疫检查位点抗体单药治疗虽然在临床治疗中显示出广泛的抗癌效果，不同癌种的总体有效率基本在20%左右，即使通过多种标志物进行预测可一定程度上减少无效人群，但其获益人群一样有限。从肿瘤免疫过程上看，将免疫阻隔型和免疫沙漠型的“冷”肿瘤，转变成免疫炎症型的“热”肿瘤，扩大免疫检查位点抗体的获益人群，可以通过联合治疗的方式进行。对PDL1、MSI、TMB等各类型标志物预测检查位点抗体单药治疗效获益可能性较低的患者，最好进行检查位点抗体与其他治疗方式的联合治疗。多项研究发现放疗、化疗和靶向治疗等传统治疗联合免疫检查位点抗体治疗能够获得惊人的效果，中位生存期、无疾病进展生存期和有效率等疗效指标翻倍的情况。同时，值得注意的是，联合治疗会成倍甚至多倍的提高毒副反应。基于对肿瘤免疫过程理解的加深，特异性针对特定肿瘤免疫过程的免疫治疗是联合治疗的更优选择。', '小五'))
    para += h4_aiyi('5、新型免疫治疗手段研究进展')
    para += p.write(para_set, r_aiyi.text('免疫治疗是癌症治疗有史以来最激动人心的治疗领域，甚至有的医生认为，癌症免疫治疗让人类真正真正看到了癌症被治愈的希望。随着PD1抗体在各癌种中的攻城略地，新型的免疫治疗手段也展现出未来的王者之相。', '小五'))
    para += h4_aiyi('（1）个性化癌症治疗疫苗', size='五号')
    para += p.write(para_set, r_aiyi.text('癌症疫苗，这种通过主动免疫去扩大肿瘤特异性T细胞反应的治疗方式，一直被认为是癌症免疫治疗的有效手段。尽管大家能够清晰看到癌症疫苗的合理性，但是，过去在临床方面的尝试都是不成功的。不同患者之间的肿瘤抗原具有强烈的多样性，因此，个性化癌症疫苗的发展是必要的。随着二代测序和生物信息工具的逐步完善，癌症疫苗的核心环节，新抗原预测逐渐成熟，该技术在最近的研究中取得突破性的进展，且由于安全性较好，是最值得跟进参与的新型癌症免疫治疗手段之一。', '小五'))
    para += p.write(r_aiyi.picture(cy=11, rId='2.4.5.1', align=['center', ''], posOffset=[0, 0.2]))
    para += p.write(para_set) * 17
    para += h4_aiyi('（2）免疫检查位点抑制剂相关抗体', size='五号')
    para += p.write(para_set, r_aiyi.text('肿瘤免疫检查位点不仅仅PD1和CTLA-4，还有至少几十种免疫检查位点。目前该领域，IDO抑制剂、LAG3抑制剂在早期临床试验中显示出相当好的疗效，与PD1联合用药的情况下，部分结果甚至成倍提升有效率，其中IDO抑制剂，已经进入三期临床临床试验（注：IDO抑制剂Epacadostat与Keytruda联用的关键三期临床试验ECHO-301失败）。', '小五'))
    para += h4_aiyi('（3）CAR-T和TCR-T治疗', size='五号')
    para += p.write(para_set, r_aiyi.text('CAR-T和TCR-T都属于细胞治疗的范畴，主要通过对患者自身的T细胞进行工程化改造，让其能够发挥肿瘤细胞的杀灭功能。CAR-T，又称嵌合抗原受体T细胞治疗，是通过人工合成的受体使患者自身的T细胞能够进行肿瘤细胞识别，进而发挥肿瘤细胞杀伤效果。由于CAR-T细胞在实体瘤中的浸润能力相对较差，目前临床主要应用于血液肿瘤中。随着技术进展，如通过提升CAR-T中对增强T细胞浸润能力相关基因的表达，未来应该也能够在实体瘤治疗中发挥重要作用。TCR-T，又称T细胞识别受体（TCR）工程化改造T细胞治疗，是通过将对特定抗原亲和力强的TCR移植到患者自身的T细胞上使患者自身的T细胞发挥肿瘤细胞杀伤效果。其中特异性TCR-T，是指针对患者特异的新抗原进行设计的TCR-T治疗方式，是未来最有价值的癌症治疗手段，相比通过个性化疫苗诱导形成肿瘤杀伤T细胞，从原理上来说，特异性TCR-T治疗属于更靠后的免疫周期中的环节，可能具有更好的治疗效果。', '小五'))
    para += h4_aiyi('（4）溶瘤病毒', size='五号')
    para += p.write(para_set, r_aiyi.text('溶瘤病毒是一群倾向于感染和杀伤肿瘤细胞的病毒。溶瘤病毒治疗是指将本身对身体伤害较低的溶瘤病毒经工程化改造减毒处理和治疗效果提升后，感染肿瘤患者的治疗方式。这种治疗思路和方法，是多年前发现和临床实践过的方法，且2005年中国CFDA批准了一种溶瘤腺病毒。但是，单药治疗效果有限，并未引起广泛关注。随着PD1抗体治疗的普及，临床研究发现，溶瘤病毒联合PD1治疗能够大幅度提高PD1抗体治疗的有效率，2015年，溶瘤病毒治疗T-Vec批准用于黑色素瘤。溶瘤病毒在提高PDL1表达、逆转肿瘤相关免疫抑制等多个层面，均能够与PD1抗体治疗形成非常好的协同效果。', '小五'))
    para += p.write(r_aiyi.picture(cy=10, rId='2.4.5.2', align=['center', ''], posOffset=[0, 0.3]))
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    return para


def write_chapter3(index, trs, chem_items):
    n, start = 2, 10+6
    cats = get_catalog()[start-1: start + n]
    c2 = ''
    for i in range(len(chem_items)):
        item = chem_items[i]
        cell = item['cell']
        row, col = cell[0], cell[1]
        c2 += h4_aiyi('%d.%s%s' % (i+1, item['category'], item['drug']))
        data = [item['tr1'], '%s%s，%s' % (item['category'], trs[0][col], trs[row][0])]
        c2 += write_immun_table(data)
        c2 += p.write()
        text = 'PharmGKB'
        c2 += h4_aiyi('（%d）                   %s药物基因组数据库（基因多态性相关证据）' % (0 + 1, text), runs=r_aiyi.picture(cy=0.6, rId=text, posOffset=[1.3, 0.53]))
        c2 += p.write()
        rs_list0 = item['genes']
        c2 += write_gene_list3(rs_list0)
        c2 += p.write()
        for rs_item0 in rs_list0:
            c2 += write_genotype(rs_item0, [1400, w_sum-1400])
    para = ''
    para += h4_aiyi(cat=cats[1], spacing=[0, 1])
    para += write_chemotherapy(trs, [w_sum/4] * 4)
    para += p.write()
    para += write_explain({'title': '结果说明：', 'text': '该疗效预测汇总仅根据以下证据进行汇总。疗效预测证据主要来自CIVic数据库，并根据专家人工对相关证据进行梳理取舍。毒副作用证据及部分由基因多态性提供的疗效证据则来自于药物基因组数据库PharmGKB。采取该数据库二级以上的证据，并结合部分三级证据（不具备二级以上证据的情况下）。由于化学治疗的疗效影响因素较多，各个生物标志物的预测能力有限，且多个证据之间缺乏合理的证据平衡方式。目前初步采取多个证据之间目前采取均权投票的方式，即默认多个生物标志物的预测能力完全一致，仅根据各个证据的量进行评估,当相反证据量一致时，将证据级别纳入考量。'})
    para += h4_aiyi(cat=cats[2])
    para += c2
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index, page_margin=[4, 1.5, 2.54, 1.5, 1.5, 1.75])))
    return para


def write_chapter4(index, data):
    cats = get_catalog()[18: 22]
    para = ''
    # print cats[1].get('title'), '==='
    para += h4_aiyi(cat=cats[1], spacing=[0, 1]) + data['para_signature']
    para += h4_aiyi(cat=cats[2]) + data['para_yichuan']
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    return para


def write_chapter5(index, data):
    s, n = 21, 6
    cats = get_catalog()[s: s+n]
    para = ''
    para += h4_aiyi(cat=cats[1], spacing=[0, 1])
    para += write_chapter51(data)
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    para += h4_aiyi(cat=cats[2])
    para += write_chapter_cnvs(data)
    svs = data.get('svs')
    svs = filter(lambda x: filter_sv(x), svs)
    para += h4_aiyi(cat=cats[3])
    para += write_table_svs(svs)
    para += p.write(p.set(sect_pr=set_page('A4', header='rIdHeader%d' % index)))
    # para += p.write(p.set(sect_pr=set_page()))
    para += h4_aiyi(cat=cats[4], spacing=[0, 0.5]) + write_chapter53(data)
    para += h4_aiyi(cat=cats[5], spacing=[0, 1])
    overview = data.get('overview')
    sample_purity = overview.get('purity')
    normal_base_aligned = overview.get('normal_base_aligned')  # 外周血数据量
    tumor_base_aligned = overview.get('tumor_base_aligned')  # 肿瘤数据量
    if normal_base_aligned:
        normal_base_aligned = int((float(normal_base_aligned) / 1024.0/1024/1024) * 100) / 100.0
    if tumor_base_aligned:
        tumor_base_aligned = int((float(tumor_base_aligned) / 1024.0/1024/1024) * 100) / 100.0
    summary = '本检测报告共涉及两个样本，肿瘤组织样本和外周血。'
    summary += '本次检测使用IDT 39M全外显子探针联合35个融合基因内含子区域，'
    summary += '目标测序数据量为肿瘤组织样本50G，'
    summary += '外周血样本10G，'
    summary += '实际可用cleandata数据量为肿瘤组织%sG，外周血样本%sG。' % (tumor_base_aligned, normal_base_aligned)
    summary += '经分析，肿瘤组织的预测肿瘤细胞纯度为%s，' % float2percent(overview.get('purity'))
    summary += '经初步分析共获得体细胞SNV %s个，' % overview.get('snv_no')
    summary += '体细胞Indel %s个。' % overview.get('indel_no')
    line = get_line('protocol')
    para += p.write(p.set(spacing=[0, 1.5], line=19.2, rule='exact'), r_aiyi.text(summary, '小五'))
    p_set1 = p.set(spacing=[0, 1.5], line=19.2, rule='exact')
    para += p.write(
        p_set1,
        r_aiyi.text('感谢您选择北京皑医科技有限公司（皑医）提供的癌症多组学临床检测。皑医是由中国从业十年的第一批癌症精准医疗资深专家、医科院北京协和医学院的医学专家和中科院计算所的技术专家共同发起成立的一家癌症多组学数据临床解读公司。皑医致力于协助中国顶级肿瘤医生，以患者获益为中心，重新定义癌症，延长患者有质量生存时间。', '小五')
    )
    para += p.write(
        p_set1,
        r_aiyi.text('AIomics1癌症多组学临床检测，现阶段主要包括全外显子组、转录组和微生物组这三个标准化的组学检测。皑医将获得的高达70G以上的数据进行标准化的深度解读。首先，通过根据ASCO（美国临床肿瘤协会）、AMP（美国分子病理学协会）和CAP（美国病理学家联合学会）的国际指南进行变异解读相关生物信息流程质量控制；其次，在NCCN指南基础上，深度整合CGI、CIVic、OncoKB等多个解读数据库，并结合专家知识进行确认；最后，为了让患者更快的接触了解跟自己组学特征相关的研究进展专门性设计了 “最新研究进展” 模块。这是基于癌症真实世界研究和精准医疗高度发展，癌症循证医学证据以爆炸性的方式在扩大的现状所作的创新性设计。', '小五')
    )
    para += p.write(
        p_set1,
        r_aiyi.text('AIomics1癌症多组学临床检测标准化检测环节，由皑医委托北京贝瑞和康生物技术有限公司（贝瑞）进行检测。贝瑞拥有CFDA批准的第三方检验所资质（医疗机构执业许可证，诊疗科目：临床细胞分子遗传学专业），具备完善的实验质控流程。相关资质和质控流程是数据获取可靠性的核心保证。结合贝瑞的标准化检测和皑医的个性化化深度解读，AIomics1癌症多组学临床检测能够为您提供国际标准质量控制、紧扣癌症最新研究进展的系统性精准诊疗提示。', '小五')
    )
    para += p.write(r_aiyi.picture(8, rId='protocol', posOffset=[0, 2]))
    para += p.write(p.set(ind=[38.5, 0], spacing=[3, 0]), r_aiyi.text('北京皑医科技有限公司'))
    para += p.write(p.set(ind=[38.5, 0], spacing=[1, 0]), r_aiyi.text('盖章：'))
    para += p.write(p.set(ind=[38.5, 0], spacing=[1, 0]), r_aiyi.text(data['report_time']))
    para += p.write(p.set(sect_pr=set_page(header='rIdHeader8', footer='rIdFooter1')))
    return para


def write_backcover():
    para = p.write(r_aiyi.picture(2.4, rId='logo', posOffset=[0, 10], align=['center', ''], relativeFrom=['page', 'page']))
    para += p.write(p.set(spacing=[20, 10], jc='center'), r_aiyi.text('重新定义癌症', 26, color=blue))
    para += p.write(p.set(line=19.2, rule='exact'), r_aiyi.text('皑医是由中国从业十年的第一批癌症精准医疗资深专家、医科院北京协和医学院的医学专家和中科院计算所的技术专家共同发起成立的一家癌症多组学数据临床解读公司。皑医致力于协助中国顶级肿瘤医生，以患者获益为中心，重新定义癌症，延长患者有质量生存时间。'))
    imgs = [
        [
            {'id': 'logo', 'posOffset': 0.11, 'text': '北京皑医科技有限公司     '},
            {'id': 'location', 'posOffset': 5.17, 'text': '北京市中关村科技园区大兴生物医药基地绿地启航3号楼1003'},
        ],
        [
            {'id': 'website', 'posOffset': 0, 'text': 'https://aiyi.link          '},
            {'id': 'phone', 'posOffset': 5.17, 'text': '010-86399801'}
        ]
    ]
    for i in range(len(imgs)):
        infos = imgs[i]
        run = ''
        y = 0.2
        before = 0.5
        if i == 1:
            y = 0.26
            before = 0.3
        for info in infos:
            run += r_aiyi.picture(cy=0.6, rId=info['id'], posOffset=[info['posOffset'], y])
            run += r_aiyi.text(info['text'], 9, space=True)
        para += p.write(p.set(spacing=[before, 0]), run)
    para += set_page(header='rIdHeader8', footer='rIdFooter1')
    return para


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
        for t_n, t in enumerate(level_tips):
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
        return ''
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
    paras += p.write(p.set(spacing=[1, 0.5]), r_heiti.text('%s常见癌种驱动基因检测结果说明' % diagnosis))
    col = 6
    items2 = []
    for i in range(0, len(d_items), col):
        items2.append(d_items[i: i+col])
    paras += write_mingan(items2, col)
    return paras


def write_hrd(sequencing_type, data, ind):
    paras = ''
    p_set = p.set(line=15, ind=[1, 0], spacing=[0, 1.5])
    index = 1
    variant_stars = data.get('variant_stars')
    paras_hr, items_hr = write_genes_hr(variant_stars)
    text = '在临床试验中，NOVA研究中发现，在铂类敏感的复发高级别卵巢癌中，HRD评分高的患者，PARP抑制剂niraparib治疗组相比安慰剂组，PFS为12.9m vs 3.8m（PMID：27717299）。然而，HRD评分并非总能预测PARP抑制剂治疗效果，今年ASCO上报道的GeparOLA研究发现，HRD评分高、BRCA1/2突变的早期乳腺癌患者中，奥拉帕尼组与化疗组（卡铂联合紫杉醇）疗效类似，（pCR率55.1% vs 48.6%（2019 ASCO abstract 506）。'
    if 'panel' not in sequencing_type.lower():
        paras += h4_aiyi('（1）HRD评分说明', ind=ind)
        index += 1
        paras += p.write(p_set, r_aiyi.text('奥拉帕尼等PARP抑制剂主要通过协同致死的方式对肿瘤细胞起到杀伤作用，同源重组修复缺陷HRD是PARP抑制剂发挥作用的生物学基础。由于HRD涉及到多个基因的突变、甲基化等多种状态，目前无法直接检测，HRD评分通过检测肿瘤基因组的三个特征杂合性缺失（LOH）、端粒等位基因不平衡（TAI），和大规模的状态转换（LST）作为HRD的标志物。HRD评分为LOH、TAI和LST三个评分的总和，既往回顾性研究将HRD评分＞42作为HRD状态的阈值。（注：本检测采用WES数据评估HRD评分，与通过SNP芯片或者专门设计的捕获芯片检测的结果有少量差异。', 9))
        text += 'HR通路相关基因变异与肿瘤的HRD状态密切相关。'
    else:
        tip = ''
    paras += h4_aiyi('（%s）HR通路基因检测结果' % index, ind=ind)
    paras += paras_hr
    paras += h4_aiyi('（%s）检测意义' % (index +1), ind=ind)
    paras += p.write(p_set, r_aiyi.text(text))
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


def write_explains(content):
    para = ''
    for text in content.split('\n'):
        texts = text.split('：')
        if len(texts) > 1:
            para += write_explain({'title': '%s：' % texts[0], 'text': '：'.join(texts[1:])})
        else:
            para += p.write(p.set(line=14, rule='exact'), r_aiyi.text(text))
    return para


def write_chapter13(cat):
    para = h4_aiyi(cat=cat)
    p_set = p.set(line=18, rule='exact')
    para += h4_aiyi('1.靶向治疗与驱动基因')
    para += p.write(p_set, r_aiyi.text('靶向治疗药物是针对特定的肿瘤发生发展相关特定基因设计的药物。传统化疗主要针对快速分裂的细胞，既杀伤肿瘤细胞、又杀伤正常细胞，毒副作用大，而靶向治疗更精准的针对肿瘤特定特征或者肿瘤微环境，所以毒副作用相对较低。', '小五'))
    para += p.write(p_set, r_aiyi.text('实际临床应用中，靶向药初步可以分成针对肿瘤抗血管生成及多靶点相关的靶向药和针对肿瘤细胞特定基因变异的靶向药。抗血管生成及多靶点相关的靶向药现阶段大多没有特定的基因变异可以预测其疗效。针对肿瘤细胞特定基因变异的靶向药，一般情况下仅对该类突变患者有效。此类特定基因，包含在肿瘤驱动基因范畴中。', '小五'))
    para += h4_aiyi('2.驱动基因及突变形式说明')
    para += h4_aiyi('（1）驱动基因说明', spacing=[1, 0.5])
    para += p.write(p_set, r_aiyi.text('在肿瘤发生发展中扮演重要角色，能够“驱动”癌症疾病进程的基因称为驱动基因。乘客基因则是指对肿瘤发生发展重要性不高的基因，但是，重要性目前只是一个相对概念而不是绝对概念，所以，虽目前有多种方式进行驱动基因的鉴定，但是并没有统一的完整标准。驱动基因又分成发生激活突变后具有促进癌症发生发展的原癌基因和功能正常情况下抑制癌症发生的抑癌基因。驱动基因上的基因变异，可以是驱动突变，也可以是乘客突变。驱动突变可以是原癌基因的激活突变，也可以是抑癌基因的失活突变。一般情况下，肿瘤靶向治疗针对驱动基因中的原癌基因激活突变进行抑制，如EGFR Tkis抑制EGFR突变，或者针对抑癌基因的失活突变进行相关信号通路的协同致死，如PARP抑制剂治疗BRCA1、2基因变异肿瘤。', '小五'))
    para += h4_aiyi('（2）原癌基因和激活突变')
    para += p.write(p_set, r_aiyi.text('原癌基因指正常功能情况下，在细胞信号传导等多个层面扮演重要角色，但是发生激活突变后会促进癌症发生发展的基因。激活突变一般情况下发生在原癌基因经常发生突变的热点位置上，如下图的PIK3CA和IDH1基因，且突变以错义突变为主。', '小五'))
    para += h4_aiyi('（3）抑癌基因和失活突变', spacing=[1, 0])
    para += p.write(p.set(line=18, rule='exact', spacing=[0, 12]),
                    r_aiyi.text('抑癌基因指正常功能下，扮演着DNA修复等抑制癌症发生发展过程的基因。抑癌基因发生失活突变会导致身体抑制癌症的功能降低。抑癌突变一般情况下热点突变较少，可发生在基因近乎任何区域，如下图的RB1和VHL基因，且会出现更多的截断突变。', '小五')
                    +r_aiyi.picture(10, rId='1.3.3', align=['center', ''], posOffset=[0, 3])
                    )
    # para += p.write(p.set(jc='center', spacing=[0, 12]), run=r_aiyi.picture(13.34, rId='1.3.3', align=['center', '']))
    # para += p.write(p.set(sect_pr=set_page()))
    para += h4_aiyi('3.肿瘤数据解读证据级别说明')
    para += p.write(p_set, r_aiyi.text('通过二代测序技术，特别是本报告采用的组学检测技术，每个肿瘤患者会找到几十个、几百个甚至于几千个肿瘤基因变异。不同基因变异具有不同的临床指导意义。美国临床肿瘤协会（ASCO）、美国病理学家联合学会会（CAP）和分子病理协会（AMP）共同发布了相关的标准和指南。该指南首先把变异根据临床意义等级分成四类：等级Ⅰ，强临床意义的变异；等级Ⅱ，潜在临床意义的变异；等级Ⅲ，不清楚临床意义的变异；等级Ⅳ，良性和可能良性的变异。其中，又根据变异的证据级别，等级Ⅰ和等级Ⅱ的变异进一步细化分成Level A、B、C、D四个级别。', '小五'))
    para += p.write(p_set, r_aiyi.text('Level A：1、针对某一特定癌症，经过FDA批准的；2，针对某一特定癌种，专业指南推荐的；', '小五'))
    para += p.write(p_set, r_aiyi.text('Level B：基于高水平研究，相关领域专家意见一致；', '小五'))
    para += p.write(p_set, r_aiyi.text('Level C：1、同一分子标志物，FDA批准用于其他癌症；2、作为临床试验纳入标准', '小五'))
    para += p.write(p_set, r_aiyi.text('Level D：临床前研究，结果不确定', '小五'))
    para += write_db_info()
    para += p.write(p.set(sect_pr=set_page(header='rIdHeader3')))
    return para


def write_chapter21(ch):
    para = ''
    para += ch['title']
    info = ch.get('data')
    text = info.get('text')
    effect = info.get('effect')
    level = info.get('level')
    para += write_immun_table([text, effect], level)
    para += p.write(
        p.set(jc='center', spacing=[ch['before'], 0]),
        run=r_aiyi.picture(cy=ch['cy'], rId=ch['img_id'], posOffset=[0, 0.5], align=['center', ''])
    )
    para += p.write(p.set(jc='center', spacing=[ch['note_before'], 0]), r_aiyi.text(ch['note'], size=8.5))
    for i in ch['infos']:
        para += write_explain(i)
    return para


def write_chapter_ddr(variants, diagnosis):
    ddr = write_genes_ddr(variants, diagnosis)
    para = write_immun_table([ddr['tr1'], ddr['tr2']], ddr['level'])
    para += p.write()
    para += ddr['para']
    para += write_explain({'title': '结果说明：', 'text': 'DDR基因突变患者更可能从免疫检查位点抗体治疗中获益。细胞内正常的代谢活动与环境因素均会引起DNA损伤，初步估算，每个正常细胞每天产生1000-1000000处分子损伤。肿瘤细胞由于基因组等异常，大部分情况下DNA损伤的速率远高于正常细胞。DNA损伤反应基因主要包括错配修复、同源重组修复等DNA修复相关基因（DDR基因），也包括细胞周期检查点、染色质重塑等其他基因，据一篇专家手工注释研究表明，DDR基因大约有450个。DNA损伤反应跟免疫系统之间具有非同寻常的关系，如召集免疫细胞聚集，对T细胞杀伤更敏感等。以上是根据目前最新研究，将已有证据证明相关基因突变与免疫检查位点疗效直接相关的DDR基因子集。该基因列表可能会随着DDR基因的研究进展逐步扩大。'})
    para += write_evidence_new([
        {
            'disease': '泌尿上皮癌',
            'title': 'DDR基因明确致病突变泌尿上皮癌患者PD1抗体治疗反应率为80%，意义未明突变患者有效率为54%（2018《JCO》）',
            'text': '60例泌尿上皮癌患者入组相关抗PD治疗前瞻性临床实验。DDR基因（共34个基因）突变患者28例（47%），其中明确致病突变患者15例（25%）。出现任意DDR基因突变的患者与更高的治疗反应率相关(67.9% v 18.8%; P<0.001)。 其中明确致病突变患者治疗反应率为80%，意义不明突变患者有效率为54%，显著高于DDR基因野生型患者（19%，P<0.001）(PMID：29489427)'
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
    ws = [w_sum/10] * 10
    pPr = p.set(line=12, rule='auto', jc='center')
    reds = []
    oranges = []
    var_items = []
    for k in range(len(genes)):
        gene = genes[k]
        gene_list = gene['genes']
        gene_list += [''] * (col-len(gene_list))
        tcs = ''
        fill = '' if k % 2 == 0 else bg_blue
        if 'title' in gene:
            para = p.write(pPr, r_aiyi.text(gene['title'], size=9))
            tcs += tc.write(para, tc.set(w=ws[k], fill=fill, color=white, tcBorders=[]))
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
                elif fill1 == orange:
                    oranges.append(gene)
            para = p.write(pPr, r_aiyi.text(text, color=color, size=9, fill=fill1)) + var_text
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, color=white, tcBorders=[]))
        trs2 += tr.write(tcs, tr.set(trHeight=620))
    tr1 = 'DDR基因无变异'
    tr2 = 'PD1等免疫检查位点抗体等免疫治疗可能不显著'
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
        tr2 = 'PD1等免疫检查位点抗体等免疫治疗可能有效'
        level = 'C'
        if diagnosis in ['泌尿上皮癌', '非小细胞肺癌', '前列腺癌']:
            level = 'C-同癌种证据'
        tr2 += '(%s)' % level
    paras = table_aiyi(trs2)
    run = r_aiyi.text(' 红色 ', color=white, fill=red, size=9, space=True)
    run += r_aiyi.text('，表示明确致病突变位点；', size=9)
    run += r_aiyi.text(' 橙红色 ', color=white, fill=orange, size=9, space=True)
    run += r_aiyi.text('，表示未明意义突变位点', size=9)
    paras += p.write(p.set(spacing=[0.5, 0.5]), run)
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
        fill = '' if k % 2 == 1 else bg_blue
        for j in range(len(gene_list)):
            gene = gene_list[j]
            fill1, tip, var_item = get_var_color(gene, variant_stars)
            color, text, var_text = '000000', gene, ''
            if fill1 not in ['', gray]:
                color = white
                if fill1 == red:
                    var_items.append(var_item)
            para = p.write(p_set_tr, r_aiyi.text(text, color=color, size=9, fill=fill1)) + var_text
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, tcBorders=[]))
        trs2 += tr.write(tcs)
    paras = table_aiyi(trs2)
    run = r_aiyi.text(' 红色 ', color=white, fill=red, size=9, space=True)
    run += r_aiyi.text('，表示明确致病突变位点', size=9)
    paras += p.write(p.set(spacing=[0.5, 0.5], ind=[1, 0]), run)
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
                        return orange, item
                if ccf_expected_copies_em >= 0.5:
                    return orange, item
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
    tr2 = 'PD1等免疫检查位点抗体可能效果不显著'
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
                    var_items.append(star)
                    items03.append(gene)
        if gene in ['TP53', 'ATM']:
            if gene not in items04:
                if is_match3:
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
        items203 = {'text': 'TP53合并KRAS突变未发生', 'color': gray}
    else:
        text03 = '%s突变发生' % ('合并'.join(items03))
        items203 = {'text': text03, 'color': red}
        if diagnose == '非小细胞肺癌':
            level = 'C-同癌种证据'
        genes_red.append(text03)
    if len(items04) < 2:
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
    items2 = [[items200, items201, items202, items203, items204], items21 + [items213, items214]]
    tip = tr1
    if len(genes_red) > 0:
        tr1 = '发现免疫治疗敏感相关%s' % concat_str(genes_red)
        tip = '发现免疫治疗敏感相关%s%s' % (genes_red[0], '' if len(genes_red) == 1 else '等事件')
        if level == '':
            level = 'C'
        tr2 = 'PD1等免疫检查位点抗体等免疫治疗可能有效(%s)' % level
    data = [tr1, tr2]
    para = write_immun_table(data, level)
    para += p.write()
    para += write_mingan(items2, 5)
    para += write_detail_table(var_items, cnv_items, [], ploidy)
    para += write_explain({
        'title': '结果说明：',
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
                '进而能够被免疫检查点抗体重新激活。'
                'TET1是一个DNA去甲基化酶，是在21个与DNA甲基化密切相关的关键基因中突变频率最高的基因，'
                '且TET1突变在免疫检查点治疗反应组中显著富集。'
    })
    para += write_evidence_new([
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
            'text': '在35例肾细胞癌中发现，SWI/SNF染色质重塑复合物相关基因PBRM1基因失活与PD1抗体单药治疗获益密切相关（p=0.012），同时进一步在一个65例的经PD1抗体单药或者PD1联合CTLA4治疗的肾细胞癌队列中得到验证（p=0.0071）。总体而言，PBRM1失活（双等位基因失活或者完全缺失）患者免疫检查点抗体治疗获益率为54.17%，而PBRM1野生型患者或疑虑为24%。（PMID: 29301960）'
        },
        {
            'disease': '肾癌与PBRM1基因失活变异',
            'title': 'PBRM1突变肾癌患者中PBRM1作为免疫检查点治疗反应标志物的临床验证及其局限性（2019《JAMA Oncology》；2018《Nature medicine》）',
            'text': '在一个证明既往接受过抗血管生成治疗后抗PD1治疗相比依维莫司显著改善总生存的三期临床实验的肾细胞癌队列中对其中382例（总队列共803例）患者进行基因分析发现，PBRM1突变与PD1治疗更高的临床获益（34.6% vs 19.7% p=0.04）、PFS增加（HR为0.67，P=0.03）和OS增加（HR=0.67，P=0.03）相关。然而值得注意的是，既往研究发现，PBRM1失活状态与抗血管生成疗效相关且未经抗血管生成治疗的肾细胞癌患者PBRM1失活状态与免疫检查点疗效无关（PMID: 29301960；PMID：29867230）'
        },
        {
            'disease': '非小细胞肺癌、类恶性横纹肌样瘤胸部肿瘤、高钙血型小细胞卵巢癌与SMARCA4纯合失活',
            'title': 'SMARCA4失活驱动的多种肿瘤PD1治疗有效的案例报道（2018《JNCI》；2019《Thoracic cancer》；2019《Annal of oncology》）',
            'text': '由SMARCA4失活的单基因疾病（低TMB）高钙血型小细胞卵巢癌，4例患者PD1抗体治疗有效（1例持续部分反应6个月；3例维持无疾病状态1.5年或者更长）。在11例样本中，绝大多数（8例）PDL1表达且具有强烈的T细胞浸润。1例SMARCA4完全失活（免疫组化阴性）、TMB相对较高（全外显子测序共找到396个突变，大约11个/Mb）的非小细胞肺癌部分反应，持续疾病控制时间超过14月。1例SMARCA4失活、PDL1阴性的胸部肿瘤经PD1抗体治疗11个月后，获得相对于基线高达-72%的PR（PMID: 29301960；PMID：29867230）'
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
    tr2 = 'PD1等免疫检查点抗体治疗可能耐药风险较低'

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
        tr2 = 'PD1等免疫检查点抗体治疗可能具有耐药风险(%s)' % level
    para = write_immun_table([tr1, tr2], level, dark if level else '')
    para += p.write(p.set(line=1))
    para += write_mingan([table_items[:6], table_items[6:]], 6)
    para += write_detail_table(var_items, cnv_items, sv_items, ploidy)
    para += p.write()
    para += write_explain({'title': '结果说明：',
                           'text': '免疫治疗耐药可以由多种因素引起，以上基因通过不同机制导致免疫治疗耐药。EGFR、ALK基因与TMB、PDL1表达较低有一定关系，CTNNB1基因则是通过影响枝状细胞招募进抗PD1治疗的耐药。B2M基因纯合失活突变，主要通过损害抗原提呈机制使免疫治疗耐药。JAK1、JAK2、IFNGR1、IFNGR2、IRF1、APLNR、PIAS3和SOCS等基因的纯合失活突变，则是通过损害效应T细胞杀伤肿瘤细胞的信号通路（γ干扰素通路）导致免疫治疗耐药。PTEN基因表达缺失或者纯合失活突变，则可能是通过影响T细胞浸润使免疫治疗耐药。'})
    para += write_evidence_new([
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
    tr1, tr2 = '免疫治疗超进展相关基因无变异', 'PD1等免疫检查位点抗体可能无超进展风险'
    tip = tr1
    if len(genes_red) > 0:
        tr1 = '免疫治疗超进展相关%s' % concat_str(genes_red)
        tip = '免疫治疗超进展相关%s%s' % (genes_red[0].split('(')[0], '' if len(genes_red) == 1 else '等事件')
        level = 'C'
        if items2[1] or items2[2] or items2[3]:
            level = 'D'
        tr2 = 'PD1等免疫治疗抗体治疗可能具有超进展风险(%s)' % level
    para = write_immun_table([tr1, tr2], level, dark if level else '')
    para += p.write(p.set(line=1))
    para += write_mingan([items2], 6)
    para += p.write(p.set(line=1))
    para += write_detail_table(var_items, cnv_items, sv_items, ploidy)
    para += p.write()
    para += write_explain({'title': '结果说明：',
                           'text': '免疫治疗耐药可以由多种因素引起，以上基因通过不同机制导致免疫治疗耐药。EGFR、ALK基因与TMB、PDL1表达较低有一定关系，CTNNB1基因则是通过影响枝状细胞招募进抗PD1治疗的耐药。B2M基因纯合失活突变，主要通过损害抗原提呈机制使免疫治疗耐药。JAK1、JAK2、IFNGR1、IFNGR2、IRF1、APLNR、PIAS3和SOCS等基因的纯合失活突变，则是通过损害效应T细胞杀伤肿瘤细胞的信号通路（γ干扰素通路）导致免疫治疗耐药。PTEN基因表达缺失或者纯合失活突变，则可能是通过影响T细胞浸润使免疫治疗耐药。'})
    para += write_evidence_new([
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
            'text': '240名具备完整资料的免疫检查点抗体治疗患者中，8名患者出现DMD2/DMD4扩增，但是中位无疾病进展生存期与总体数据与其他患者并没有明显差异。（PMID：29337640）'
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
    # HLA分型结果中，A、B、C三个等位基因均为杂合状态（合并）具有免疫治疗疗效较好的HLA-B44超型，提示PD1等免疫检查位点抗体可能有效
    # HLA分型结果中，具有免疫治疗较差的HLA-B66超型，提示PD1等免疫检查位点抗体可能效果不显著
    # HLA分型结果中，具有免疫治疗较差的HLA-B15:01，提示PD1等免疫检查位点抗体可能效果不显著
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
        tip1 = 'PD1等免疫检查位点抗体可能有效'
        level = 'C'
        if diagnosis in ['非小细胞肺癌', '黑色素瘤']:
            level = 'C-同癌种证据'
        tip1 += '(%s)' % level
        tip2 = 'HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗敏感超型HLA-B44'
        tip2s.append('免疫治疗敏感超型HLA-B44')
        youxiao = True
        fill = level_tips[2].get('color')
        color = white
    elif is_zahe is False or (len(naiyaos) > 0 and is_zahe and mingan is False) :
        # 可能耐药（纯合或者出现耐药超型、分型且不出现敏感超型）
        # HLA分型结果中发现等位基因纯合现象
        # HLA分型结果中发现等位基因纯合现象、免疫治疗耐药超型HLA-B66、免疫治疗耐药分型HLA-B15:01
        # HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药超型HLA-B66
        # HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药分型HLA-B15:01
        # HLA分型结果中发现A、B、C三个等位基因均为杂合状态、免疫治疗耐药超型HLA-B66、免疫治疗耐药分型HLA-B15:01
        tip1 = 'PD1等免疫检查点抗体治疗可能具有耐药风险'
        fill = gray
    else:
        tip1 = 'PD1等免疫检查位点抗体可能效果不显著'
        fill = ''

    texts = []
    for j in range(3):
        h1 = item[j * 2]
        h2 = item[j * 2+1]
        texts.append('HLA-%s HLA-%s' % (h1, h2))
    postfix = '' if len(tip2s) == 1 else '等'
    postfix1 = '' if len(tip2s) < 2 else '事件'
    # tip0 = tip2 if youxiao else ('HLA分型结果中发现%s%s%s' % (tip2s[0] if len(tip2s) < 2 else tip2s[1] , postfix, postfix1))
    tip0 = ('HLA分型结果中发现%s%s%s' % (tip2s[0] if len(tip2s) < 2 else tip2s[1] , postfix, postfix1))
    tip01 = 'HLA分型结果中发现%s%s' % ('、'.join(tip2s), postfix1)
    trs2 = write_tr1('            '.join(texts) + '\n' + tip2, bg_blue)
    trs2 += write_tr2(tip1, fill, color)
    para = table_aiyi(trs2)
    para += p.write()
    para += write_explain({'title': '结果说明：', 'text': 'HLA分型与免疫治疗疗效高度相关。HLA(human lymphocyte antigen ，人类淋巴细胞抗原)，是编码人类的主要组织相容性复合体（MHC）的基因。HLA是免疫系统区分自身和异体物质的基础。HLA主要包括HLA Ⅰ类分子和Ⅱ分子。HLAⅠ类分子又进一步细化分成A、B、C三个基因。特定的超型，如HLA-B44，与免疫检查点抗体治疗疗效好相关；HLA-B66（包括HLA-B*15：01），与免疫检查点抗体治疗疗效差相关。HLA Ⅰ类三个基因均杂合，免疫检查点抗体治疗反应更好。HLA杂合缺失的基因相关的新抗原可能在个性化治疗疫苗或者特异性细胞治疗中无效。'})
    para += write_evidence4(2)
    return para, tip0, tip01, level


def write_chapter_signature(signature_etiology):
    tr1, tr2 = '', []
    s_dict = {}
    signature_etiology = signature_etiology[-30:]
    for s_id, item in enumerate(signature_etiology):
        text = reset_sig(s_id+1)
        if text != '未知':
            arr = s_dict.get(text) or []
            arr.append(float(item))
            if text not in tr2:
                tr2.append(text)
            s_dict[text] = arr
    pd1 = []
    prap = []
    tips = []
    for k in s_dict.keys():
        f = sum(s_dict[k])
        if f > 0.5:
            if k in ['APOBEC', '吸烟', 'POLE', '错配修复缺陷dMMR']:
                pd1.append(k)
            if k in ['同源重组修复缺陷HRD']:
                prap.append(k)
        elif f > 0:
            tips.append('%s(%s)' % (k, float2percent(f, 1)))
    tr1 = '通过突变特征分析，该肿瘤'
    if len(tips) > 0:
        tr1 += '可能由%s等原因导致' % ('、'.join(tips))
    tr2 = '无相关治疗提示'
    level = ''
    tip = tr1
    if len(pd1) > 0:
        tr1 = '%s占据主导因素' % ('、'.join(pd1))
        tr2 = '提示PD1等免疫检查点抗体治疗可能有效'
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
    texts = '''共济失调性毛细血管扩张症	自身免疫性淋巴增生综合征	巨舌巨人综合征	Birt-Hogg-Dubé综合征	Bloom综合征
    Carney综合征	Cowden综合征	Diamond-Wiedemann贫血症	家族性腺瘤性息肉病	家族性胃肠道间质瘤
    Fanconi贫血	遗传性乳腺癌-卵巢癌综合征	遗传性弥漫型胃癌	遗传性平滑肌瘤病肾癌	遗传性多发性骨软骨瘤
    遗传性乳头状肾细胞癌	遗传性前列腺癌	Howell-Evans综合征	甲状旁腺机能亢进-颌骨肿瘤综合征	幼年性息肉病综合征
    Li-Fraumeni综合征	Lynch综合征	皮肤恶性黑色素瘤	多发性内分泌腺瘤病1型	多发性内分泌腺瘤病2型
    MUTYH相关性息肉病	家族性神经母细胞瘤	神经纤维瘤病1型	神经纤维瘤病2型	痣样基底细胞癌综合症
    Nijmegen断裂综合征	遗传性副神经节瘤-嗜铬细胞瘤综合征	Peutz-Jeghers综合征	PTEN错构瘤综合征	遗传性视网膜母细胞瘤
    Rothmund-Thomson综合征	结节性硬化症	Turcot综合征	von Hippel-Lindau综合征	Werner综合征（成人早衰症）
    家族性肾母细胞瘤	着色性干皮病'''
    items = texts.split('\n')
    tr1 = '在42种遗传性肿瘤综合征相关的162个基因中，未发现与遗传性肿瘤相关的明确致病突变位点'
    tr2 = '遗传性肿瘤相关基因变异可能在该肿瘤的发生发展中扮演次要角色'
    data = [tr1, tr2]
    para = write_immun_table(data)
    para += p.write()
    para += write_46(items, col=5)
    para += p.write()
    run = r_aiyi.text(' 红色 ', color=white, fill=red, size=9, space=True)
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


def write_chapter51(data):
    para = ''
    para += h4_aiyi('（1）体细胞突变汇总')
    ws = [1000, 1700, 1700, 1000, 1400, 1200, 1000, 1000]
    titles = ['基因', '核苷酸变化', '氨基酸变化', '外显子', '变异类型', '突变丰度', '覆盖度',  'Cosmic计数']
    stars = data.get('variant_list')
    stars = sorted(stars, cmp=cmp_var)
    stars = stars[:200]
    para += write_table_var(stars)
    para += p.write()
    para += h4_aiyi('（2）遗传性肿瘤、HRD、DDR相关基因胚系突变汇总')
    para += p.write('呈现基因list上出现的所有突变，把明确治病给突变排在前面，并作标记')
    return para


def write_table_var(stars):
    stars = sorted(stars, cmp=cmp_var)
    titles = ['基因', '核苷酸变化', '氨基酸变化', '外显子', '变异类型', '突变丰度', '覆盖度',  'Cosmic计数']
    ws = [1000, 1700, 1700, 1000, 1400, 1200, 1000, 1000]
    trs = write_thead51(titles, pPr=p_set_tr, ws=ws)
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
    return table_aiyi(trs)


def write_table_svs(stars):
    para = ''
    ws = [1000, 1400, 1400, 1400, 1400, 1200, 1200, 1000]
    titles = ['基因1', '位置1', '基因2', '位置2', '融合', 'cosmic', '突变丰度', '支持reads']
    trs = write_thead51(titles, ws=ws)
    if len(stars) == 0:
        trs += write_tr51(['无'] * len(titles), ws, 0, 1)
    for k in range(len(stars)):
        star = stars[k]
        item = [
            star.get('gene1'),
            star.get('site1'),
            star.get('gene2'),
            star.get('site2'),
            star.get('fusion'),
            star.get('cosmic_fusion_counts'),
            float2percent(star.get('vaf')),
            star.get('reads_support'),
        ]
        trs += write_tr51(item, ws, row=k, count=len(stars))
    para += table_aiyi(trs)
    return para


def write_table_cnv(items, ploidy):
    titles = ['基因', '总拷贝数', '低拷贝数', '区域大小', 'WGD状态', '基因组倍性', '变异状态']
    ws = [w_sum / len(titles)] * len(titles)
    trs = write_thead51(titles, ws=ws)

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
    return table_aiyi(trs)


def write_chapter_cnvs(data):
    cnvs = data.get('cnvs')
    stars = data.get('cnv_stars')
    ploidy = data.get('ploidy')
    para = ''
    para += h4_aiyi('（1）重点基因拷贝数变异结果汇总')
    para += write_genes_cnv(stars)
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
    para += h4_aiyi('（2）拷贝数变异相关基因详细信息汇总')
    para += write_table_cnv(stars + extra, ploidy)
    para += p.write(
        r_aiyi.text('注：肿瘤纯度低于30%时，二代测序拷贝数变异检测准确性会发生比较明显下降。', '小五')
    )
    return para


def write_chapter53(data):
    para = p.write(p.set(line=16, rule='exact'), r_aiyi.text('评估肿瘤重点信号通路的状态是从全局对癌症进行理解的重要方式。肿瘤相关驱动基因一般都处在肿瘤的重点信号通路上。该样本相关的肿瘤驱动基因变异和非驱动基因变异究竟累及哪些信号通路，信号通路之间各个基因的关系如何，针对相关信号通路的治疗方式以及各个信号通路上下游的信号通路的分布，都能够协助医生和患者理解肿瘤所处状态。'))
    para += p.write()
    for i in range(gene_list53.nrows):
        title = gene_list53.cell_value(i, 0)
        stars = (data.get('cnv_stars') + data.get('variant_stars'))if '融合' not in title else data.get('sv_stars')
        ch = {'title': '%d.%s' % (i + 1, title), 'para': gene_list53.cell_value(i, 1)}
        genes = []
        for j in range(3, gene_list53.ncols):
            v = gene_list53.cell_value(i, j)
            if v.strip() != '':
                genes.append(v)
        ch['genes'] = genes
        para += write_chapter5311(ch, i, stars)
    return para


# Part5 . 3 通路涉及重点基因变异情况
def write_chapter5311(ch, index, stars):
    p_set = p.set(line=14, rule='exact')
    para = p.write(p_set, r_aiyi.text(ch['title'], '小四', 1))
    # para += con1
    para += p.write()
    # print ch['title'], '5.3.%d.1' % (index + 1)
    # title = '' if 'img_id' not in ch else '（1）'
    # para += p.write(p_set, r_aiyi.text('%s通路涉及重点基因变异情况：' % title, weight=1))
    para += p.write(p.set(spacing=[0, 13.5]), r_aiyi.picture(cx=7.8, rId='5.3.%d.1' % (index + 1), align=['center', ''], posOffset=[0, 0.6]))
    n = 10
    para += write_genes((ch['genes']), n, w_sum, 'right', stars)
    para += p.write()
    para += write_explains(ch['para'])
    para += p.write(p.set(sect_pr=set_page()))
    return para


def write_db_info():
    para = h4_aiyi('4.肿瘤解读数据库相关说明')
    infos = [
        {'rId': 'CIVic', 'cx': 4.23, 'cy': 1.8, 'off_y': 0,
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
                 'pic': {'rId': '1.3.4.1', 'cx': 14.1, 'cy': 8.57, 'off_y': 0}
             },
             {'text': ''},
             {'text': ''},
             {'text': ''},
             {'text': ''},
             {'text': ''},
             {
                 'text': '通过对1077已知致癌变异、2819个癌症易感变异、241个癌症基因上已知为良性的PAM（影响蛋白功能突变）和1006个癌症基因上经常出现在一般人群中的PAM的验证，发现该算法的准确性为0.91。',
                 'pic': {'rId': '1.3.4.2', 'cx': 13.76, 'cy': 7.54}
             },
         ]},
    ]
    for i in range(len(infos)):
        info = infos[i]
        rId = info['rId']
        text = rId if 'text' not in info else info['text']
        off_y = 0.48 if 'off_y' not in info else info['off_y']
        off_y -= 0.1
        para += h4_aiyi('（%d）                   %s数据库证据呈现' % (i + 1, text), runs=r_aiyi.picture(cy=1, rId=info['rId'], posOffset=[1.3, off_y]))
        for p_text in info['para']:
            para += p.write(p.set(rule='exact', line=18), r_aiyi.text(p_text['text'], '小五'))
            if 'pic' in p_text:
                pic = p_text['pic']
                para += p.write(p.set(spacing=[9, 0]), r_aiyi.picture(cy=pic['cy'], rId=pic['rId'], posOffset=[0, 5.59], align=['center', 'bottom']))
    return para


def write_patient_info(data):
    overview = data.get('overview') or {}
    purity = float2percent(overview.get('purity'), 0)
    sample_detail = data.get('sample_detail')
    para = ''
    trs = ''
    ws = [2300, 2300, 3100, 2500]
    pPr = p.set(jc='left', spacing=[0.5, 0.5], line=16, rule='exact')
    ps = [
        '姓名: %s' % sample_detail['patient_name'],
        '性别: %s' % sex2str(sample_detail['sex']),
        '年龄: %s' % sample_detail['age'],
        '患者ID: %s' % sample_detail['sample_id'],
        '医院: %s' % sample_detail.get('inspection_department'),
        '病理诊断: %s' % sample_detail.get('diagnosis'),
        '组织类型: %s(肿瘤细胞纯度%s)+白细胞' % (sample_detail.get('sample_type'), purity),
        '组织来源: %s' % sample_detail.get('tissue')
    ]
    n = len(ps) / 2
    for k in range(2):
        tr2 = ps[k * n: (k+1) * n]
        tcs2 = ''
        size = 10
        line_type = 'thickThinSmallGap' if k == 0 else 'single'
        tcBorders = ['top'] if k == 0 else ['bottom']
        lineSize = 24 if k == 0 else 8
        for i in range(len(tr2)):
            ts = tr2[i].split(':')
            run = r_aiyi.text(ts[0].strip() + ': ', size=size, weight=0)
            run += r_kaiti.text(ts[1].strip(), size=size, weight=1)
            tcs2 += tc.write(p.write(pPr, run), tc.set(w=ws[i], color=blue, tcBorders=tcBorders, line_type=line_type, lineSize=lineSize))
        trs += tr.write(tcs2)
    para += table.write(trs, insideColor=white, tblBorders=[])
    return para


def cmp_drug(x, y):
    for k in ['aiyi_level', 'evidence_direction']:
        v = cmp(x.get(k), y.get(k))
        # Resistant (Support) Responsive (Support)
        if v != 0:
            return v
    return 0


# part0 靶向治疗提示
def write_target_tip(data):
    target_tips = data.get('target_tips')
    cnv_stars = data.get('cnv_stars')
    # plo =
    ploidy = data.get('ploidy')
    items, show_extra, extra_item = target_tips
    ws = [1200, 2400, w_sum - 1200 - 2400]
    trs = write_thead_target(ws, cnv_stars, ploidy)
    if len(target_tips) == 0:
        trs += write_tr51(['无'] * len(ws), ws, 0, 1)
    for k in range(len(items)):
        fill = '' if k % 2 == 0 else bg_blue
        bdColor = blue if k == len(items) - 1 else white
        item1 = items[k]
        # if k == 0:
        #     for kk in item1.keys():
        #         print kk, item1[kk]
        tcs = ''

        tcs += tc.write(
            p.write(p_set_tr, r_aiyi.text(item1.get('gene') or item1.get('gene1') or item1.get('col1'), '小五')),
            tc.set(ws[0], fill=fill, color=bdColor, tcBorders=['bottom'])
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
            p.write(p_set_tr, r_aiyi.text(col2, '小五')),
            tc.set(ws[1], fill=fill, color=bdColor, tcBorders=['bottom'])
        )
        known_db = item1.get('known_db') or []
        para = ''
        run = ''
        d_len = 0
        evidence_directions = ['Responsive (Support)', 'Resistant (Support)']
        # '耐药Resistant (Support)', '敏感Responsive (Support)'
        known_db = filter(lambda x: x.get('evidence_direction') in evidence_directions, known_db)
        known_db.sort(cmp=cmp_var)
        for evidence_direction in evidence_directions:
            ds1 = filter(lambda x: x.get('evidence_direction') in evidence_direction, known_db)
            for tip_item in level_tips:
                level = tip_item.get('text')
                ds = filter(lambda x: x.get('aiyi_level') == level, ds1)
                for d_item in ds:
                    d = d_item.get('drugs')
                    evidence_direction = d_item.get('evidence_direction')
                    color = white
                    # '耐药Resistant (Support)', '敏感Responsive (Support)'
                    if evidence_direction == 'Resistant (Support)':
                        fill1 = gray
                        color = ''
                    else:
                        fill1 = tip_item.get('color')

                    run1 = r_aiyi.text(' ' + d, '小五', fill=fill1, color=color, space=True)
                    run1 += r_aiyi.text(level, vertAlign='top', fill=fill1, color=color)
                    run1 += r_aiyi.text(' ', fill=fill1, space=True)
                    run1 += r_aiyi.text('  ', space=True)

                    run += run1
                # if d_len > 60:
                #     para += p.write(p.set(line=16), run)
                #     d_len = 0
                #     run = ''
                # d_len += len(d)
                # if left - 0.2 > (7200/567.0):
                #     left = 0
                #     para += p.write(p.set(line=16), run)
                #     run = ''
        if run:
            para += p.write(p_set_tr, run)
        if para == '':
            para = p.write(p_set_tr)
        tcs += tc.write(para, tc.set(ws[2], fill=fill, color=bdColor, tcBorders=['bottom']))
        trs += tr.write(tcs)
    return table_aiyi(trs)


# part0 免疫治疗提示
def write_immun_tip(immun_tip):
    para = ''
    run = r_heiti.text('免疫治疗提示', '小四', 1)
    run += r_aiyi.text('(               分别指指南、专家共识、临床证据和临床前证据阳性,提示PD1等免疫检查点抗体治疗,可能有效.    提示可能无效.    提示可能耐药)', '小六')
    tips = [
        {'text': 'A'},
        {'text': 'B'},
        {'text': 'C'},
        {'text': 'D'}
    ]
    for t_index, tip in enumerate(tips):
        run += r_aiyi.picture(0.38, rId=tip.get('text'), posOffset=[2.71 + t_index * 0.42, 0.38], wrap='undertext')
    run += r_aiyi.picture(0.38, rId='white_block', posOffset=[14.1, 0.4], wrap='undertext')
    run += r_aiyi.picture(0.38, rId='gray_block', posOffset=[16, 0.4], wrap='undertext')
    para += p.write(p.set(spacing=[0.5, 0.5], line=15, rule='exact', outline=4), run)
    gap = {'text': ' ', 'bdColor': white, 'fill': white, 'w': 300}
    items1 = [
        [
            immun_tip[0],
            gap,
            immun_tip[1]
        ],
        [
            immun_tip[2],
            gap,
            immun_tip[3]
        ],
        [
            immun_tip[4],
            gap,
            immun_tip[5]
        ],
        [
            immun_tip[6]
        ]
    ]
    for i_index, items in enumerate(items1):
        trs = ''
        tcs = ''
        for item in items:
            text = item.get('text')
            color = item.get('color') or 'auto'
            level = item.get('level') or ''
            level1 = filter(lambda x: level.startswith(x['text']), level_tips)
            fill = item.get('fill') or ''
            if len(level1) > 0:
                fill = level1[0].get('color')
                if '超进展' in text or '耐药' in text:
                    fill = gray
            if fill not in ['', gray]:
                color = white
            run1 = r_aiyi.text(text.split('(')[0], '小五', color=color)
            if level:
                run1 += r_aiyi.text(level[0], vertAlign='top', color=color)
            p1 = p.write(p.set(line=12, rule='auto'), run1)

            tcs += tc.write(
                p1,
                tc.set(
                    item.get('w'),
                    lineSize=24,
                    tcBorders=borders,
                    fill=fill,
                    color=fill or gray
                )
            )
        trs += tr.write(tcs)
        para += table.write(trs, tblBorders=[])
        if i_index < (len(items1) -1):
            para += p.write(p.set(line=8, rule='exact'))
    return para


def write_immun_table(data, level='', color=''):
    level1 = filter(lambda x: level.startswith(x['text']), level_tips)
    fill2 = ''
    if len(level1) > 0:
        fill2 = level1[0].get('color')
    if color:
        fill2 = color
    trs2 = write_tr1(data[0], bg_blue if fill2 =='' else '')
    trs2 += write_tr2(data[1], fill2, bdColor=fill2)
    return table.write(trs2, bdColor=fill2 or blue, tblBorders=['top', 'bottom'])


def write_evidence_new(evidences):
    para = ''
    para += p.write(p.set(spacing=[1.5, 0], ind=[0.5, 0]), r_aiyi.text('相关循证医学证据：', 12, weight=1))
    for i in range(len(evidences)):
        text = evidences[i]
        p_set0 = p.set(spacing=[1, 0.5], shade=bg_blue, ind=['hanging', 0.5], line=17, rule='exact')
        p_set = p.set(spacing=[0, 0.2], shade=bg_blue, ind=['hanging', 0.5], line=17, rule='exact')
        para += p.write(p_set0, r_aiyi.text(' ' + text.get('disease'), 10.5, weight=1, space=True))
        para += p.write(p_set, r_aiyi.text(' %s' % text.get('title'), 9, space=True, weight=1))
        para += p.write(p_set, r_aiyi.text(' %s' % text.get('text'), 9, space=True))
        if 'para' in text:
            para += text['para']
    return para


def write_evidence4(index):
    para = p.write(p.set(spacing=[0.5, 1], ind=[0.5, 0]), r_aiyi.text('相关循证医学证据：', weight=1))
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
            para += p.write(p.set(spacing=[0, after], shade=bg_blue, line=16, rule='exact', ind=[0.5, 0]), r_aiyi.text(text, 9.5, weight=weight))
    return para


def write_evidence_tc(d, t_item):
    key = t_item.get('key')
    text = d.get(key)
    pPr = p.set(jc='left', spacing=[0.5, 0.5])
    return tc.write(
        p.write(pPr, r_aiyi.text(text, 9)),
        tc.set(t_item.get('w'), tcBorders=[], gridSpan=t_item.get('gridSpan') or 0)
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
    for (t_index, t) in enumerate(titles[:-1]):
        run = r_aiyi.text(t.get('title'), size)
        borders1 = [] if t_index == 0 else ['left']
        tcs_th1 += tc.write(p.write(pPr, run), tc.set(t.get('w'), tcBorders=['top'], fill=bg_blue, color=blue))
    tr_h1 = tr.write(tcs_th1)
    tc_h2 = tc.write(
        p.write(pPr, r_aiyi.text('证据描述', size)),
        tc.set(w, tcBorders=['bottom'], fill=bg_blue, color=blue)
    )
    for d in data:
        d['col1'] = '%s %s' % (gene, d.get('alteration_in_house'))
        d['col2'] = '%s ( %s )' % (d.get('drugs'), d.get('known_db_level'))
        d['col3'] = '%s;%s' % (d.get('disease'), d.get('evidence_direction'))
        d['col4'] = '%s (PMID: %s )' % (d.get('evidence_statement'), d.get('reference'))
        trs += tr_h1
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
    if trs:
        return table_aiyi(trs)
    return ''


def write_explain(i, ind=[0, 0]):
    run = r_aiyi.text(i['title'], weight=1) + r_aiyi.text(i['text'], size=9)
    p_set = p.set(ind=ind, line=16, rule='exact')
    return p.write(p_set, run)
    # para = ''
    # para += p.write(p_set, r.text(i['title'], weight=1))
    # para += p.write(p_set, r.text(i['text'], 9))
    # return para


def write_chemotherapy(trs, ws):
    trs2 = ''
    for k in range(len(trs)):
        size = 10
        items = trs[k]
        tcs = ''
        for j in range(len(items)):
            item = items[j]
            if isinstance(item, list):
                item = ';'.join(uniq_list(item))
                if item == '':
                    item = '无'
            fill, weight, jc, color = 'auto', 0, 'left', bg_blue
            if k == 0 or j == 0:
                fill, weight, jc, color = bg_blue, 1, 'center', white
            pPr = p.set(jc=jc, spacing=[0.5, 0.5])
            run = r_aiyi.text(item, size=size, weight=weight)
            tcs += tc.write(p.write(pPr, run), tc.set(w=ws[k], fill=fill, tcBorders=[]))
        trs2 += tr.write(tcs)
    return table_aiyi(trs2)


def write_gene_list3(genes, width=w_sum):
    trs2 = ''
    fill, weight, jc = bg_blue, 0, 'center'
    pPr = p.set(jc=jc, line=12, rule='auto', spacing=[0.5, 0.5])
    col = 5
    if len(genes) < col:
        col = len(genes)
    ws = [width / col] * col
    row = int(math.ceil(float(len(genes)) / col))
    for k in range(row):
        tcs = ''
        size = 9
        for j in range(col):
            this_index = k * col + j
            if this_index < len(genes):
                item = genes[this_index]
                gene = item['gene']
                para = p.write(pPr, r_aiyi.text('%s(%s) %s(%s)' % (gene, item['level'], item['rs'], item['genotype']), size))
                para += p.write(pPr, r_aiyi.text(item['summary'], size))
                tcs += tc.write(para, tc.set(w=ws[k], fill=fill, color=white, tcBorders=borders))
        trs2 += tr.write(tcs)
    return table_aiyi(trs2)


def write_genotype(gt, ws):
    size = 9
    tcs = ''
    fill, weight, jc = 'auto', 0, 'left'
    gridSpan = 2
    text = '%s %s (%s)' % (gt['gene'], gt['rs'], '证据级别%s' % gt['level'])
    trs2 = tr.write(tc.write(
        p.write(p.set(jc='center', spacing=[0.5, 0.5]), r_aiyi.text(text, size=size, weight=1)),
        tc.set(w=sum(ws), fill=bg_blue, color=white, tcBorders=borders, gridSpan=gridSpan)))
    for k in range(2):
        key = 'introduction'
        fill = 'auto'
        jc = 'left'
        if k == 0:
            fill, jc, key = bg_blue, 'center', 'genotype'
        pPr = p.set(jc=jc, spacing=[0.5, 0.5])
        run = r_aiyi.text(gt[key], size=size, weight=weight)
        tcs += tc.write(p.write(pPr, run), tc.set(w=ws[k], fill=fill, color=bg_blue, tcBorders=borders))
    trs2 += tr.write(tcs)
    return table_aiyi(trs2) + p.write()


def write_mingan(items, ncol):
    nrow = len(items)
    ws = [w_sum/ncol] * ncol
    trs2 = ''
    for row in range(nrow):
        genes = items[row]
        tcs = ''
        fill = '' if row % 2 == 1 else bg_blue
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
            para = p.write(p_set_tr, r_aiyi.text(text, color=color, size=9, fill=fill1))
            tcs += tc.write(para, tc.set(w=ws[row], fill=fill, tcBorders=[]))
        trs2 += tr.write(tcs)
    return table_aiyi(trs2)


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
    return table_aiyi(trs2)


def write_46(items, **kwargs):
    ws = []
    if 'col' in kwargs and 'ws' not in kwargs:
        col = kwargs['col']
        ws = [w_sum / col] * col
    if 'ws' in kwargs and 'col' not in kwargs:
        ws = kwargs['ws']
        col = len(ws)
    fill, weight, jc = gray, 0, 'center'
    pPr = p.set(jc=jc, line=12, rule='auto')
    trs2 = ''
    for row, item in enumerate(items):
        tcs = ''
        rows = item.split('\t')
        rows += [''] * (5-len(rows))
        for j in range(len(rows)):
            item = {'fill': bg_blue, 'text': rows[j]}
            fill = '' if row % 2 == 1 else bg_blue
            color = '000000'
            para = p.write(pPr, r_aiyi.text(item['text'], color=color, size=9))
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, tcBorders=[]))
        if len(tcs) > 0:
            trs2 += tr.write(tcs, tr.set(trHeight=800))
    return table_aiyi(trs2)


def write_genes(gene_list, col, width, table_jc='center', stars=[]):
    trs2 = ''
    fill, weight, jc = gray, 0, 'center'
    pPr = p.set(jc=jc, line=12, rule='auto')
    row = int(math.ceil(float(len(gene_list)) / col))
    if row == 1:
        col = len(gene_list)
    ws = [width / col] * col
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
                fill = '' if i % 2 == 1 else bg_blue
            para = p.write(pPr, r_aiyi.text(text, color=color, size=9)) + var_text
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, tcBorders=[]))
        if tcs:
            trs2 += tr.write(tcs, tr.set(trHeight=660))
    return table_aiyi(trs2)


def get_var_color(gene, vars):
    for item in vars:
        if gene == item.get('gene') or (item.get('gene1') and item.get('gene1').split('(')):
            add_star = item.get('add_star')
            tip = item.get('tip')
            if add_star > 0:
                return red, tip, item
    return '', '', None


def write_genes_cnv(cnv_stars):
    col = 8
    trs2 = ''
    gene_list = cnv_genes
    ws = [w_sum / col] * col
    # fill, weight, jc = gray, 0, 'center'
    # pPr = p.set(jc='center', line=12, rule='auto')
    row = int(math.ceil(float(len(gene_list)) / col))
    for i in range(row):
        tcs = ''
        fill = '' if i % 2 == 0 else bg_blue
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
            para = p.write(p.set(line=12*1.3), r_aiyi.text(text, color=color, size=9, fill=fill1))
            tcs += tc.write(para, tc.set(w=ws[j], fill=fill, tcBorders=[]))
        if tcs:
            trs2 += tr.write(tcs)
    return table_aiyi(trs2)


def write_thead_target(ws, cnv_stars, ploidy):

    pPr = p_set_tr if len(cnv_stars) > 0 else p.set(line=24)
    offy = 0.06 if len(cnv_stars) > 0 else 0.35
    tcs = ''
    size = 9.5
    titles = [
        {'run': r_aiyi.text('基因', size)},
        {'run': r_aiyi.text('变异(肿瘤细胞比例)', size)}
    ]
    for i in range(len(titles)):
        t = titles[i]
        run = t.get('run')
        para = p.write(pPr, run)
        if i == 1 and len(cnv_stars) > 0:
            para += p.write(pPr, r_aiyi.text('(基因组倍性%s)' % (ploidy), 9))
        tcs += tc.write(para, tc.set(w=ws[i], color=blue, fill=bg_blue))
    run3 = ''
    run3 += r_aiyi.text('药物推荐', size)
    for tip in level_tips:
        run3 += r_aiyi.picture(0.41, 0.5, tip.get('text'), posOffset=[tip.get('x'), offy], wrap='behinddoc')
        run3 += r_aiyi.text('     %s' % (tip.get('tip')), 6.5, space=True)
    tcs += tc.write(p.write(pPr, run3), tc.set(w=ws[-1], color=blue, fill=bg_blue))
    return tr.write(tcs)


def write_thead51(titles, **kwargs):
    ws = [1800, 1600, 1600, 1600, 1800]
    pPr = p.set(jc='left', spacing=[0.5, 0.5])
    if 'pPr' in kwargs:
        pPr = kwargs['pPr']
    if 'ws' in kwargs:
        ws = kwargs['ws']
    tcs = ''
    size = 10
    for i in range(len(titles)):
        t = titles[i]
        run = r_aiyi.text(t, size=size, weight=0)
        tcs += tc.write(p.write(pPr, run), tc.set(w=ws[i], fill=bg_blue, tcBorders=[]))
    return tr.write(tcs)


def write_tr51(item, ws, row=0, count=0):
    tcs = ''
    size = 9
    fill = '' if row % 2 == 0 else bg_blue
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
            para += p.write(p_set_tr, run)
        tcs += tc.write(para, tc.set(w=ws[i], fill=fill, tcBorders=[]))
        # tcs += tc.write(para, tc.set(w=ws[i], fill=fill, color=bdColor, tcBorders=['bottom']))
    return tr.write(tcs)


def write_tr1(text, fill='', wingdings=True):
    pPr = p.set(jc='left', spacing=[0.5, 0.5])
    para = ''
    for t in text.split('\n'):
        run = r_aiyi.text(' ' + t, size=9, color='' if fill in [gray, '', bg_blue] else white, wingdings=wingdings, space=True)
        para += p.write(pPr, run)
    tcs2 = tc.write(para, tc.set(w=w_sum, fill=fill, tcBorders=[]))
    return tr.write(tcs2)


def write_tr2(data, fill=gray, bdColor=gray):
    return write_tr1(data, fill, False)


def write_pages(t):
    title = get_page_titles()
    relationship = Relationship()
    pkg_parts, relationshipss = '', ''
    title += ['']
    for i in range(len(title)):
        h_index = 'header%d' % (i + 1)
        if i == len(title) - 1:
            paras1, rel = '', ''
        else:
            paras = p.write(p.set(spacing=[1, 0]), r_aiyi.text(title[i], 9, color='00ADEF', space=True) + r_aiyi.picture(cy=1.25, rId='logo', posOffset=[0, -1.2], zoom=0.35))
            paras1 = table.write(tr.write(tc.write(paras, tc.set(w=10000, tcBorders=[]))), ws=[10000], tblBorders=['bottom'], bdColor='DDDDDD', border_size=18)
            rel = relationship.write_rel('logo', target_name='media/logo.png')
        pkg_parts += relationship.about_page(h_index, paras1, page_type='header', rels=rel)
        relationshipss += relationship.write_rel(h_index, 'header')

    # 页脚
    page_type = 'footer'
    footer_id = 'report_time'
    size = 9
    paras = ''
    paras += p.write(p.set(jc='right'), sdt.write())
    paras += p.write(p.set(jc='right'), r_aiyi.text( '检测报告时间: %s' % t, size))
    relationships = relationship.write_rel(footer_id, page_type)
    footer = relationship.about_page(footer_id, paras, page_type=page_type)
    # return footer, relationships
    return pkg_parts + footer, relationshipss + relationships


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
    para += table_aiyi(trs)
    para += p.write(r_aiyi.text('注：仅显示部分重要新抗原信息', size=8.5))
    para += write_explain({'title': '结果说明：',
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
        fill = '' if index % 2 == 1 else bg_blue
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
    return table_aiyi(trs)


def write_detail_table(var_items, cnv_items, sv_items, ploidy):
    para = ''
    if len(var_items) >0:
        para += h4_aiyi('体细胞突变相关基因详细信息')
        para += write_table_var(var_items)
    if len(cnv_items) > 0:
        para += h4_aiyi('扩增相关基因详细信息')
        para += write_table_cnv(cnv_items, ploidy)
    if len(sv_items) > 0:
        para += h4_aiyi('融合相关基因详细信息')
        para += write_table_svs(sv_items)
    return para


def h4_aiyi(text='', size=12, spacing=[1, 0.5], weight=1, ind=[0, 0], line=15, runs='', bm_name='', cat=None, color='', jc='left'):
    if cat is not None:
        bm_name = cat['bm']
        text = cat['title']
    if bm_name != '':
        print text
    run = r_heiti.text(text, size=size, weight=weight, color=color) + runs
    return p.write(p.set(spacing=spacing, line=line, rule='exact', outline=4, ind=ind, jc=jc), run, bm_name)


def table_aiyi(trs2):
    return table.write(trs2, tblBorders=['top', 'bottom'], insideColor=white, bdColor=blue)


def float2percent(p, n=2):
    try:
        p = float(p)
    except:
        print p
        return p
    return '%s%%' % (round(p*100, n))


#报告相关数据
def get_catalog():
    catalogue = [
        [u"一、靶向治疗提示", 0, 1, 10],
        [u"（一）、驱动突变靶向治疗提示汇总", 2, 1, 23],
        [u"（二）、各驱动突变循证医学证据", 2, 1, 23],
        [u"（三）、靶向治疗解读说明", 2, 1, 23],
        [u"二、免疫治疗提示", 0, 1, 10],
        [u"（一）、免疫治疗提示汇总", 2, 1, 23],
        [u"（二）、MSI微卫星不稳定检测结果", 2, 1, 23],
        [u"（三）、TMB肿瘤突变负荷检测结果", 2, 2, 23],
        [u"（四）、DDR基因DNA损伤修复反应基因突变检测结果", 2, 6, 23],
        [u"（五）、免疫治疗敏感驱动突变检测结果", 2, 6, 23],
        [u"（六）、免疫治疗耐药驱动突变检测结果", 2, 2, 23],
        [u"（七）、免疫治疗超进展相关基因检测结果", 2, 3, 23],
        [u"（八）、HLA分型检测结果", 2, 3, 23],
        [u"（九）、肿瘤新抗原检测结果", 2, 3, 23],
        [u"（十）、免疫治疗解读说明", 2, 3, 23],
        [u"三、化学治疗提示", 0, 3, 10],
        [u"（一）、化学治疗提示汇总", 2, 4, 23],
        [u"（二）、各化疗药循证医学证据", 2, 5, 23],
        [u"四、最新研究进展治疗提示", 0, 5, 10],
        [u"（一）、肿瘤突变模式检测结果", 2, 8, 23],
        [u"（二）、肿瘤遗传性检测结果", 2, 8, 23],
        [u"五、检测信息汇总", 0, 5, 10],
        [u"（一）、基因突变检测结果汇总", 2, 6, 23],
        [u"（二）、重点基因拷贝数检测结果汇总", 2, 6, 23],
        [u"（三）、融合基因检测结果汇总", 2, 7, 23],
        [u"（四）、肿瘤重要信号通路变异信息汇总", 2, 7, 23],
        [u"（五）、检测方法", 2, 7, 23]
    ]
    items = []
    for index, cat in enumerate(catalogue):
        item = {"title": cat[0], 'left': cat[1], 'page': cat[2], 'style': cat[3], 'bm': bm_index0 + index}
        items.append(item)
    return items


def get_page_titles():
    title_cn, title_en = u'多组学临床检测报告', 'AIomics1'
    title = '%s附录目录%s%s' % (title_cn, ' ' * 64,  title_en)
    title1 = '%s%s%s' % (title_cn, ' ' * (64+11),  title_en)
    titles = [title, title1]
    cats = get_catalog()
    for i in [0, 4, 15, 18, 21]:
        n = 64 + 14
        if test_chinese(cats[i]['title']) == 11:
            n -= 8
        titles.append('%s%s%s' % (cats[i]['title'], ' ' * n,  title_en))
    return titles


def get_imgs_aiyi(path, is_refresh=False, others=[]):
    if is_refresh:
        img_info = get_imgs(img_dir)
        img_info += get_imgs(path)
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


def get_data3(rs_geno, diagnose):
    new_items = []
    trs = [
        ['', '疗效可能好', '疗效可能差', '疗效未知'],
        ['毒副作用低', [], [], []],
        ['毒副作用高', [], [], []],
        ['毒副作用未知', [], [], []]
    ]
    drugs = get_variant_knowledges(rs_geno, diagnose)
    for item in drugs:
        new_item = {}
        category = item['category']
        new_item['category'] = category
        new_item['drug'] = item['drug']
        new_item['genes'] = item['genes']
        new_item = get_data31(new_item)
        cell = new_item['cell']
        cell_value = '%s%s' % (item['category'], new_item['drug'])
        row, col = cell[0], cell[1]
        if row * col > 0:
            trs[row][col].append(cell_value)
        new_items.append(new_item)
    return new_items, trs


def get_data31(item):
    venoms = [[], [], [], []]
    curative_effects = [[], [], [], []]
    liaoxiao = 0
    duxing = 0
    for item1 in item['genes']:
        summary = item1['summary'].split('、')
        venom = summary[0]  # 毒副作用
        curative_effect = '疗效未知'
        if len(summary) > 1:
            curative_effect = summary[1]
        else:
            if summary[0].startswith(u'疗效'):
                curative_effect = summary[0]
                venom = '毒副作用未知'
        if '好' in curative_effect:
            curative_effects[1].append(item1)
        elif '差' in curative_effect:
            curative_effects[2].append(item1)
        # else:
        #     curative_effects[3].append(item1)
        if '疗效' in item1['summary']:
            liaoxiao += 1
        if '毒' in item1['summary']:
            duxing += 1
        if '低' in venom:
            venoms[1].append(item1)
        elif '高' in venom:
            venoms[2].append(item1)
        # else:
        #     venoms[3].append(item1)

    venoms_num = [len(x) for x in venoms]
    curative_effects_num = [len(x) for x in curative_effects]
    good = len(curative_effects[1])
    bad = len(curative_effects[2])
    low = len(venoms[1])
    high = len(venoms[2])
    row, col = venoms_num.index(max(venoms_num)), curative_effects_num.index(max(curative_effects_num))

    # 判断逻辑问题：
    # 根据证据的数量确定推荐的方向，这种情况下，证据的权重一致；
    # 当相反证据量数量一致时，根据证据级别确定（证据级别的等级 1A＞1B＞2A＞2B＞3）
    if good == bad:
        col = compare_level3(curative_effects[1], curative_effects[2])
    if low == high > 0:
        row = compare_level3(venoms[1], venoms[2])
    item['cell'] = row, col
    item['venoms'] = venoms
    item['curative_effects'] = curative_effects
    tr1 = '疗效预测方面共纳入%d个证据，其中%d个预测疗效好，%d个预测疗效差；' % (liaoxiao, good, bad)
    tr1 += '毒副作用预测共纳入%d个证据，其中%d个预测毒副作用低，%d个预测毒副作用高' % (duxing, low, high)
    item['tr1'] = tr1
    return item


def get_variant_knowledges(rs_geno, diagnose):
    variant_knowledge_names = []
    variant_knowledge_index = 2 #默认为肉瘤
    for indexx, v in enumerate(os.listdir(unicode(chemotherapy_dir, 'utf-8'))):
        if diagnose in v:
            variant_knowledge_index = indexx
        variant_knowledge_names.append(u'%s: %s' % (indexx, v.split('.')[0].encode('utf-8')))

    var_know_name = variant_knowledge_names[variant_knowledge_index]
    variant_knowledge_name = var_know_name.split(':')[1].strip()
    # 静态的数据：
    variant_knowledge = my_file.read('%s/%s.xlsx' % (chemotherapy_dir, variant_knowledge_name), sheet_name='Sheet1')
    categories = []
    for i in range(variant_knowledge.nrows):
        j = 1
        cell_value = variant_knowledge.cell_value(i, j)
        if cell_value.startswith('rs') is False and i > 0:
            drug = '' if cell_value != '铂类药物' else '(顺铂、卡铂、奥沙利铂)'
            category = {'category': cell_value, 'drug': drug, 'genes': []}
            for k in range(i + 1, variant_knowledge.nrows):
                row_value = variant_knowledge.row_values(k)
                cell_value1 = row_value[j]
                if not cell_value1.startswith('rs'):
                    break
                gene = variant_knowledge.cell_value(k, j-1)
                if gene == '':
                    print variant_knowledge_name
                #     gene = variant_knowledge.cell_value(k-1, j-1)
                item = {
                    'gene': gene,
                    'rs': cell_value1,
                    'genotype': row_value[j+1],
                    'summary': row_value[j+2],
                    'introduction': row_value[j+3],
                    'level': row_value[j+4],
                    'category': category,
                }
                for x in rs_geno:
                    if x[0] == item['rs']:
                        if x[1] == item['genotype'] and item not in category['genes']:
                            category['genes'].append(item)
            if len(category['genes']) > 0:
                categories.append(category)
    return categories


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