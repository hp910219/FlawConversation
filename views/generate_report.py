# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2019/8/1 0001
__author__ = 'huohuo'
import json
import math
import os
import shutil

from jy_word.File import File
from jy_word.Word import Run, HyperLink, Paragraph, Set_page, Table, Tc, Tr
from jy_word.Word import write_pkg_parts, get_img_info
from jy_word.web_tool import test_chinese, format_time, sex2str, zip_dir, del_file

from config import read_conf
my_file = File()

r_tcm = Run(family='微软雅黑')
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
page_margin = [2.4, 0.67, 0.49, 1.23, 2, 0]
gray = 'EEEEEE'


def get_dignosis():
    data = my_file.read('diagnosis.json')
    if data is None:
        return data
    return data.get('data')


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
        paras = p.write(p.set(pStyle='a3', pBdr=p.set_pBdr()), r_tcm.text(text))
        paras += p.write(p.set(pStyle='a3', pBdr=p.set_pBdr()), r_tcm.picture(17.3, 0.66, 'line', text_wrapping='inline'))
        rels = relationship.write_rel('line', target_name='media/line.png')
    return {
        'rId': 'rId%s' % rId.capitalize(),
        'pkg': relationship.about_page(rId, paras, page_type=page_type, rels=rels),
        'rel': relationship.write_rel(rId, page_type)
    }


def write_title(title):
    return p.write(para_setting(jc='center', line=12, rule='auto', spacing=[0, 1]), r_tcm.text(title, 14, 1))


def write_cover_line(title, before=0.2, text=''):
    runs = r_tcm.text(title, 14, 0)
    runs += r_tcm.tab()
    runs += r_tcm.text('：', 14, 0)
    text = text or ''
    runs += r_tcm.text('       %s%s' % (text, ' ' * (16-len(text)-test_chinese(text))), 14, 0, underline='single', space=True)
    return p.write(para_setting(spacing=[before, 0], ind=[10, 0], tabs=['left', ' ', 4500]), runs)


run_border = r_tcm.text('□', 19)


def write_gray_tr(item):
    ws = item.get('ws')
    texts = item.get('text') or [''] * len(ws)
    fill = item.get('fill') or 'white'
    weight = 1
    size = item.get('size') or 11
    if 'weight' in item:
        weight = item.get('weight')
    jc = item.get('jc') or 'center'
    tcs = ''
    for i in range(len(texts)):
        text = str(texts[i]).split('□')
        run = [r_tcm.text(t, size, weight) for t in text]
        para = p.write(para_setting(line=18, rule='exact', jc=jc), run_border.join(run))
        tcs += tc.write(para, tc.set(ws[i], tcBorders=['top', 'bottom', 'left', 'right'], fill=fill, gridSpan=ws[i]/1200))
    return tr.write(tcs)


def write_cover(data):
    data = data or {}
    paras = ''
    title = u'国家重点专项——基于“道术结合”思路与多元融合方法的名老中医经验传承创新研究'
    paras += p.write(para_setting(jc='center'), r_tcm.text(title, 13.5, weight=0))
    paras += p.write(para_setting(jc='center', spacing=[5, 2.5]), r_tcm.text('名老中医经验病例系列研究', 28, 1))
    paras += p.write(para_setting(jc='center', line=12, rule='auto'), r_tcm.text('病例报告表', 22, 1))
    paras += p.write(para_setting(jc='center', line=18, rule='auto'), r_tcm.text('版本号：VERSION 2.0_20190607', 12, 1))
    paras += p.write(para_setting(jc='center', spacing=[3, 1], line=12, rule='auto'), r_tcm.text('研究中心', 16, 1))
    researchers = [
        '北京中医药大学',
        '首都医科大学',
        '成都中医药大学',
        '山东中医药大学第二附属医院',
        '上海中医药大学',
        '广东省中医院',
        '重庆市中医院',
        '江西中医药大学',
        '吉林省中医药学会',
    ]
    cols = 2
    ws = [4500] * cols
    rows = int(math.ceil(len(researchers)/float(cols)))
    trs = ''
    for i in range(rows):
        tcs = ''
        for j in range(cols):
            index = i + rows * j
            ps = p.write(para_setting(line=18, rule='auto'), r_tcm.text('', 12))
            r_sign = Run(family_en='宋体', familyTheme='')
            if index < len(researchers):
                text = '%02d %s' % (index + 1, researchers[index])
                rs = r_sign.text('□ ', 12, weight=0, space=True)
                ps = p.write(para_setting(line=18, rule='auto'), rs + r_tcm.text(text, 12))
            tcs += tc.write(ps, tc.set(ws[j]))
        trs += tr.write(tcs)
    paras += table.write(trs, ws, insideColor='black')
    paras += write_cover_line('所属名老中医室站', 2.5, u'名医工作室')
    paras += write_cover_line('患者姓名缩写', text=data.get('patient_name') or '')
    paras += write_cover_line('病历号', text=data.get('case_no') or '')
    paras += write_cover_line('研究者姓名(正楷)', text=data.get('contacts') or '')
    paras += p.write(para_setting(jc='center', spacing=[2, 1], line=12, rule='auto'), r_tcm.text('牵头单位：北京中医药大学', 14, weight=1))
    # paras += p.write(para_setting(spacing=[20, 0], ind=[18, 0]), r_tcm.text('姓名： %s' % data.get('health_record').get('name'), 12))
    # paras += p.write(para_setting(ind=[18, 0]), r_tcm.text('编号： %s' % data.get('sample_id'), 12))
    return paras


def write_oration():
    paras = ''
    paras += p.write(para_setting(line=12, rule='auto', jc='center'), r_tcm.text('填写说明', 22, 1))
    paras += p.write(para_setting(line=12, rule='auto', jc='center', spacing=[0, 1]), r_tcm.text('（在正式填表前，请认真阅读下列填表说明）', 12))
    p_set = para_setting(line=18, rule='auto', ind=['hanging', 1.1, 1])
    paras += p.write(p_set, r_tcm.text('1.	此病例报告表须由专人接受培训后填写，并尽可能由同一人完成；封面、结束页的医生签名由负责该份病例的研究人员填写。', 12))
    run = r_tcm.text('2.	表中凡有“', 12)
    run += r_tcm.text('□', 19)
    run += r_tcm.text('”的项目，请在符合的条目上划“', 12)

    run += r_tcm.fldChar('begin')
    run += r_tcm.text(r' eq \o\ac(')
    run += r_tcm.text('□', 19)
    run += r_tcm.text(',√)', 14)
    run += r_tcm.fldChar('end')

    run += r_tcm.text('”；需填写分值等内容的项目，请按要求填写清楚，不得空项。', 12)
    paras += p.write(p_set, run)
    paras += p.write(p_set, r_tcm.text('3.	填写病例报告表一律使用钢笔或签字笔，填写数据务必准确、清晰，数据禁止擦除或涂抹，如有错误发生，可在错误处上方书写正确值，将错误值划上“—”， 修改者签名并加注日期，必要时说明理由。举例：  99.6  90.6  王二19.07.10。', 12))
    paras += p.write(p_set, r_tcm.text('4.	患者姓名一律以拼音缩写，填写大写字母，四格填满。两字姓名者填写两字拼音前两字母；三字姓名者填写三字首字母及第三字第二字母；四字姓名者，填写每字拼音的第一个字母。举例：', 12))
    tcs = ''

    names = [
        {'cn': '张红', 'en': 'ZHHO'},
        {'cn': '李淑明', 'en': 'LSMI'},
        {'cn': '欧阳小惠', 'en': 'OYXH'},
    ]
    ws = [1100] + [400] * 4
    for i, name in enumerate(names):
        cn = name.get('cn')
        en = name.get('en')
        w = ws[i]
        tcs += tc.write(p.write(para_setting(line=12, rule='auto', jc='right'), r_tcm.text(cn)), tc.set(ws[0], tcBorders=[]))
        for ene in en:
            tcs += tc.write(p.write(para_setting(line=12, rule='auto'), r_tcm.text(ene)), tc.set(400, tcBorders=['top', 'bottom', 'left', 'right']))

    paras += table.write(tr.write(tcs), ws * len(names), tblBorders=[], tblp=True, tblpY=0.3)
    paras += p.write() * 3
    paras += p.write(p_set, r_tcm.text('5.	检查项目如有则必须填写，未查填写“ND”；数据不详/未知的，请填写“UK”；选项不适用时请填写“NA”。', 12))
    paras += p.write(p_set, r_tcm.text('6.	病例报告表的每页均须填写病例号、患者姓名缩写，医师必须签署姓名和日期。', 12))
    paras += p.write(p_set, r_tcm.text('7.	病历记录页供填写CRF 中备选项目无法说明的特殊情况。', 12))
    return paras


def write_process():
    paras = ''
    paras += write_title('研究实施流程')
    trs = ''
    w = 1200
    items = [
        {'ws': [w*3, w * 3, w * 2], 'text': ['阶段', '诊次', '随访'], 'fill': gray, 'weight': 1},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['访视', '首诊', '二诊', '三诊', '随访1', '随访2'], 'fill': gray, 'weight': 1},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['诊断、纳入和排除诊', '√'] + [''] * 4, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['基本信息、病史', '√'] + [''] * 4, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['签署知情同意书', '√'] + [''] * 4, 'weight': 0},
        {'ws': [w * 8], 'text': ['名老中医辨证诊疗措施'], 'fill': gray},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['四诊信息'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['中医证候诊断'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['处方信息'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['名老中医/弟子点评录音'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 8], 'text': ['图像采集'], 'fill': gray},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['舌象照片采集'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['实验室检查信息'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['院外合并治疗情况'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 8], 'text': ['疗效评价'], 'fill': gray},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['MYMOP'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['SF-36'] + ['√'] * 5, 'weight': 0},
        {'ws': [w * 3] + [w] * 3 + [w] * 2, 'text': ['SAS/SDS'] + ['选填'] * 5, 'weight': 0},
        {'ws': [w * 8], 'text': ['疗效评价'], 'fill': gray},
        {'ws': [w * 3, w*5], 'text': ['不良事件记录', '随时记录'], 'weight': 0},
        {'ws': [w * 8], 'text': ['病例记录页'], 'fill': gray},
        {'ws': [w * 8], 'text': ['粘贴页'], 'fill': gray},
        {'ws': [w * 8], 'text': ['该病诊断相关资料粘贴处'], 'weight': 0},
        {'ws': [w * 8], 'text': ['相关处方粘贴处'], 'weight': 0},
        {'ws': [w * 8], 'text': ['相关检查资料粘贴处'], 'weight': 0},
        {'ws': [w * 8], 'text': ['审核情况'], 'fill': gray},
        {'ws': [w * 8], 'text': ['研究者审核及声明'], 'weight': 0},
        {'ws': [w * 8], 'text': ['室站及课题组监察审核声明'], 'weight': 0},
        {'ws': [w * 8], 'text': ['备注：MYMOP ：自评医疗成效问卷；SF-36：生活质量量表；SAS：焦虑自评量表；SDS：抑郁自评量表。'], 'weight': 0, 'jc': 'left'},
    ]
    for item in items:
        trs += write_gray_tr(item)
    paras += table.write(trs, [w] * 8, insideColor='black')
    return paras


def write_standard(sample_detail):
    paras = ''
    paras += p.write(para_setting(line=12, rule='auto', spacing=[0, 1]), r_tcm.text('入组日期：20190801', 14, 1))
    trs = ''
    w = 1200
    ws = [w*6, w, w]
    sample_detail = sample_detail or {}
    items = [
        {'ws': ws, 'text': ['纳入标准（任何一项选“否” 即不能纳入本研究）', '是', '否'], 'fill': gray},
        {'ws': ws, 'text': ['1.	符合西医%s诊断；\n请提供诊断证据并粘贴于“该病诊断相关资料粘贴处”' % sample_detail.get('diagnosis'), '□', '□'], 'weight': 0, 'jc': 'left'},
        {'ws': ws, 'text': ['2.	符合中医%s诊断；' % sample_detail.get('sample_type'), '□', '□'], 'weight': 0, 'jc': 'left'},
        {'ws': ws, 'text': ['3.	签署知情同意书；', '□', '□'], 'weight': 0, 'jc': 'left'},
        {'ws': ws, 'text': ['4.	保证参加三次诊疗及随访。', '□', '□'], 'weight': 0, 'jc': 'left'},
        {'ws': [w * 8], 'text': ['注：如果以上任何一项答案为“否”，此患者不能纳入本研究。'], 'weight': 0, 'jc': 'left'},
        {'ws': ws, 'text': ['排除标准（任何一项选“是” 即不能纳入本研究）', '否', '否'], 'fill': gray},
        {'ws': ws, 'text': ['1.	正在参加其他临床试验者；', '□', '□'], 'weight': 0, 'jc': 'left'},
        {'ws': ws, 'text': ['2.	其他                 ', '□', '□'], 'weight': 0, 'jc': 'left'},
        {'ws': [w * 8], 'text': ['注：如果以上任何一项答案为“是”，此患者不能纳入本研究。'], 'weight': 0, 'jc': 'left'},
    ]
    for item in items:
        trs += write_gray_tr(item)
    paras += table.write(trs, [w] * 8, insideColor='black')
    return paras


def write_common(patient_detail, history_info):
    paras = ''
    paras += write_title('一般资料及主要病史')
    trs = ''
    w = 1200
    w1 = [w * 2] + [w * 5]
    items = [
        {'ws': [w*7], 'text': ['人口学资料'], 'fill': gray, 'weight': 1},
        {'ws': w1, 'text': ['性别', sex2str(patient_detail.get('sex'))]},
        {'ws': w1, 'text': ['出生日期', patient_detail.get('birth') or '']},
        {'ws': w1, 'text': ['民族', patient_detail.get('nation') or '未知']},
        {'ws': w1, 'text': ['婚否', patient_detail.get('relationship') or '未知']},
        {'ws': w1, 'text': ['教育程度', patient_detail.get('education') or '未知']},
        {'ws': w1, 'text': ['职业', patient_detail.get('native') or '未知']},
        {'ws': w1, 'text': ['身高体重', '身高     cm     体重    kg']}
    ]
    for item in items:
        if 'weight' not in item:
            item['weight'] = 0
        item['jc'] = 'left'
        trs += write_gray_tr(item)
    paras += table.write(trs, [w] * 7, insideColor='black')
    items3 = []
    if history_info is not None:
        items3 = history_info.get('items_info') or []
    paras += p.write(para_setting(spacing=[0, 2]))
    trs2 = write_gray_tr({'ws': [w*7], 'text': ['基本病史'], 'fill': gray, 'weight': 1, 'jc': 'left'})
    for item33 in items3:
        value = item33.get('value')
        if value is None:
            value = '无'
        else:
            try:
                value = json.loads(value)
            except:
                value = value
        if isinstance(value, list):
            value = '  '.join(value)
        if item33.get('tag') == 'monthpicker':
            value = value.split('T')[0]
        item_tr = {'ws': w1, 'text': [item33.get('item_name'), value], 'weight': 0, 'jc': 'left'}
        trs2 += write_gray_tr(item_tr) 
    paras += table.write(trs2, [w] * 7, insideColor='black')
    return paras


times = [
    {},
    {'cn': '首诊'},
    {'cn': '次诊'},
    {'cn': '三诊'},
    {'cn': '四诊'}
]


def write_dignosis(diagnosis):
    # [u'index_no', u'template', u'treatment_time', u'sample_no', u'template_info', u'insert_time', u'diagnosis_no']
    paras = ''
    index_no = diagnosis.get('index_no')
    time_info = {'cn': '%s诊' % index_no} if index_no >= len(times) else times[index_no]
    cn = time_info.get('cn')
    paras += write_title('中医信息采集（%s）' % cn )
    template_info = diagnosis.get('template_info')
    treatment_time = diagnosis.get('treatment_time')
    run = r_tcm.text('%s日期：' % cn, 12, 1) + r_tcm.text(format_time(treatment_time, '%Y年%m月%d日'), 12)
    paras += p.write(para_setting(line=12, rule='auto'), run)
    imgs, files = [], []
    for template_i in template_info[1:]:
        for block in template_i:
            # [u'block_id', u'items', u'labelCol', u'input_items', u'entry_name', u'text']
            items = block.get('items_info')
            block_name = block.get('block_name')
            display_control = block.get('display_control') or {}
            block.update(display_control)
            if len(items) > 0:
                paras += write_title(block_name)
                for item in items:
                    display_control1 = block.get('display_control') or {}
                    item.update(display_control1)
                    item2 = write_item(item)
                    paras += item2.get('para')
                    imgs += item2.get('imgs')
                    files += item2.get('files')
                paras += para_sect(page_margin=[2.4, 1.67, 0.49, 1.67, 2, 0])
    return {
        'para': paras,
        'imgs': imgs,
        'files': files
    }


def write_item(item):
    display_control = item.get('display_control') or {}
    tag = display_control.get('tag')
    value = item.get('value')
    ind = item.get('ind') or [0, 0]
    imgs = []
    files = []
    item_name = item.get('item_name')
    paras = ''
    h1 = item.get('h1')
    if h1:
        paras += p.h4(h1)
    header = item.get('header')
    if header:
        paras += p.h5(header)
    if value is not None:
        try:
            value = json.loads(value)
        except:
            value = value
        if value is True:
            value = '是'
        if value is False:
            value = '否'
    else:
        value = 'NA'
    run0 = ''
    if item_name:
        run0 += r_tcm.text('%s: ' % item_name, 11.5, space=True, weight=1)
    if tag in ['textarea',  'upload']:
        paras += p.write(para_setting(line=12, rule='auto', ind=ind), run0)
        if isinstance(value, list):
            value = '见附件'
        else:
            values = value.strip('\n').split('\n')
            if value.endswith('.png') or value.endswith('.jpg'):
                info = get_img_info(value)
                r_pic = r_tcm.picture(cy=8, rId=info.get('rId'), img_info=info)
                paras += p.write(para_setting(line=24, spacing=[0, 12]), r_pic)
                if info not in imgs:
                    imgs.append(info)
            elif tag == 'upload':
                if value and value not in ['NA']:
                    files.append(value)
            else:
                for v in values:
                    paras += p.write(para_setting(line=12, rule='auto', ind=ind), r_tcm.text(v, 10))
            return {
                'para': paras,
                'imgs': imgs,
                'files': files
            }

    if isinstance(value, list):
        item_items = item.get('items') or []
        if item.get('is_list'):
            data = item.get('data') or []
            for d_index, d in enumerate(data):
                item2 = write_item({
                    'ind': [2, 0],
                    'item_name': d,
                    'value': value[d_index]
                })
                paras += item2.get('para')
                imgs += item2.get('imgs')
                files += item2.get('files')
        for item_index, item_item in enumerate(item_items):
            # print type(value[item_index])
            item_item['ind'] = [2, 0]
            item_item['item_name'] = item_item.get('label')
            item_item['value'] = value[item_index]
            item2 = write_item(item_item)
            paras += item2.get('para')
            imgs += item2.get('imgs')
            files += item2.get('files')
        return {
            'para': paras,
            'imgs': imgs,
            'files': files
        }

    run = run0 + r_tcm.text(value, 10)
    # if item.get('is_list'):
    #     print item_name, value
    #     for d in item.get('data'):
    #         print d

    # print tag, item.keys()
    return {
        'para': paras + p.write(para_setting(line=12, rule='auto', ind=ind), run),
        'imgs': imgs,
        'files': files
    }


def down_common(data, sort_func):
    # my_file.write(file_name.split('.')[0] + '.json', data)
    # print file_name
    # img_info_path = os.path.join(static_dir, 'json/img_info_%s.json' % ('_'.join(data['img_dirs'])))
    # # if env.startswith('Development'):
    # if os.path.exists(img_info_path):
    #     os.remove(img_info_path)
    # imgs = get_img_info(data['img_dirs'], img_info_path)
    # pic.img_info_path = img_info_path
    # data['img_info'] = img_info_path
    # data['pic'] = pic
    report_data = sort_func(data)
    body = write_body(report_data)
    imgs = report_data.get('imgs') or []
    files = report_data.get('files') or []
    file_name = report_data.get('file_name')
    zip_name = report_data.get('zip_name')
    imgs2 = []
    for img in imgs:
        if img not in imgs2:
            imgs2.append(img)
    pkg = write_pkg_parts(imgs2, body, other=report_data.get('other_page'))
    status = False
    while status != 5:
        status = my_file.download(pkg, file_name)
    return files, zip_name


def write_body(data):
    para = ''
    for key in data['para_keys']:
        para += data[key]
    return '<w:body>%s</w:body>' % para


def sort_jingan_data(data):
    # img_info_path = data['img_info']
    # r_tcm.img_info_path = img_info_path
    pkgs = ''
    rels = ''
    chapters = ''
    diagnosis = data.get('diagnosis')
    patient_detail = data.get('patient_detail')
    sample_detail = data.get('sample_detail')
    diagnosis0 = None if len(diagnosis) == 0 else diagnosis[0]
    history_info = None
    if diagnosis0:
        template_infos = diagnosis0.get('template_info')
        template_info0 = None if len(template_infos) == 0 else template_infos[0]
        if template_info0:
            if template_info0 is not None:
                for tem in template_info0:
                    if tem.get('block_name') == '病史信息':
                        history_info = tem
    imgs, files = [], []
    for diag in diagnosis:
        sort_diag = write_dignosis(diag)
        chapters += sort_diag.get('para')
        imgs += sort_diag.get('imgs')
        files += sort_diag.get('files')
    p_sect = para_sect(page_margin=[2.4, 1.67, 0.49, 1.67, 2, 0])

    patient_name = None
    if patient_detail:
        patient_name = patient_detail.get('patient_name')

    action_name = u'%s_CRF报告' % (patient_name)
    conf = read_conf()
    if isinstance(conf, str):
        return conf
    file_dir = conf.get('file_dir') or '/tmp'
    report_dir = os.path.join(file_dir, 'report')
    if os.path.exists(report_dir) is False:
        os.makedirs(report_dir)
    file_name = os.path.join(report_dir, u'%s.doc' % action_name)
    zip_name = os.path.join(report_dir, u'%s.zip' % action_name)
    files.append(file_name)
    return {
        'other_page': (pkgs, rels),
        'cover': write_cover(patient_detail) + p_sect,
        'oration': write_oration() + p_sect,
        'process': write_process() + p_sect,
        'standard': write_standard(sample_detail) + p_sect,
        'chapters': chapters,
        'common': write_common(patient_detail, history_info) + p_sect,
        'files': files,
        'file_name': file_name,
        'zip_name': zip_name,
        'imgs': imgs,
        # 'contents': cont.get('paras') + sect1,
        # 'health_record': write_health_jingan(data.get('health_record')) + para_sect([2.54, 2, 0, 1.75, 2, 0], header='rIdHeader0'),
        # 'understand': write_understand() + para_sect([2.54, 2, 0, 1.75, 2, 0], header='rIdHeader1'),
        # 'overview': overview + para_sect([2.54, 2, 0, 1.75, 2, 0], header='rIdHeader2'),
        # 'core': core,
        # 'relief': write_relief_jingan(catalogs[-2]['cn'], 2, catalogs[-2]['en'], header_index=len(catalogs) - 2),
        # 'profile': write_relief_jingan(catalogs[-1]['cn'], 1, header_index=len(catalogs) - 1),
        # 'backcover': write_backcover_jy(),
        'para_keys': [
            'cover',
            'oration',
            'process',
            'standard',
            'common',
            'chapters'
            #  'contents', 'health_record',
            # 'understand', 'overview', 'core',
            # 'relief', 'profile', 'backcover'
        ]
    }


def generate_word(data):
    files, zip_name = down_common(data, sort_jingan_data)
    if os.path.exists(zip_name):
        os.remove(zip_name)
    dir_name = '.'.join(zip_name.split('.')[:-1])
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name)
    for ff in files:
        if os.path.isfile(ff):
            print type(ff), ff
            print type(dir_name), dir_name
            shutil.copy(ff, dir_name)
        else:
            del ff
    print type(zip_name)
    zip_status = zip_dir('', dir_name, zip_name)
    if zip_status == 5:
        del_file(dir_name)
        return os.path.abspath(zip_name)
    return zip_status


if __name__ == "__main__":
    # generate_word(get_dignosis() or [])
    pass
    

