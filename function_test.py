# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 17:06
# @Author  : wangxin
# @File    : function_test.py
# @Software: PyCharm
import os
import re

from core.cust_tasks.bid_func.bid_all_data_composition import check_tender_catalogue
from core.cust_tasks.commitment.contrast_commit import contrast_commit_result
from core.cust_tasks.credit.contrast_credit import contrast_credit_result
from core.cust_tasks.deposit.contrast_deposit import contrast_deposit_result
# from core.cust_tasks.duration.contrast_duration import contrast_duration_bid_tender
from core.cust_tasks.finance.compare_money_func import compare_money_res
from core.cust_tasks.letter_of_tender.letter_of_tender import contrast_letter_of_tender
from core.cust_tasks.output.tender_person import person_result
from core.cust_tasks.performance.contrast import contrast_performance
from core.cust_tasks.performance.tender_performance_info import get_total_performance
from core.cust_tasks.person.contrast_person import for_play, contrast_person_for_play
from core.cust_tasks.price.tender_price_same import get_tender_data, get_period_price_of_tender, con_tender_price
from core.cust_tasks.qualification.compare_qualificaton_res_fun import contrast_qualification_result_new
from core.cust_tasks.signature.new_tender_invalidity_info import new_contrast_and_output_result
from core.cust_tasks.signature.tender_invalidity_info import contrast_and_output_result
from core.cust_tasks.tender_func.bidder_name_info import person_summary, get_bidder_info, \
    check_person_name
from core.db import cached_file
from core.regular_expression_rule.bid_data_analysis import bid_performance_analysis
from core.script.from_bid_get_table import from_bid_get_table, all_bid_table
from core.utils.get_document_title_range_index import get_title_info, page_type_extrapolate
import pandas as pd


def result_to_copy(res_list):
    out_dict = {
        '证书 - 存在验证': ['投标文件中响应了', '投标文件中未提供'],
        '证书 - 等级验证': ['证书等级', '等级'],
        '证书 - 专业验证': ['专业'],
        '证书 - 有效期验证': ['有效期'],
        '业绩 - 存在验证': [],
        '业绩 - 类型验证': [],
        '业绩 - 金额验证': [],
        '业绩 - 数量验证': [],
        '业绩 - 年份验证': [],
        '业绩 - 证明材料类型验证': [],
        '业绩 - 装修装饰建筑面积验证': [],
        '社保证明 - 存在验证': ['社保'],
        '劳动合同 - 存在验证': ['劳动合同'],
        '不得兼任承诺书 - 存在验证': [],
        '职位人数要求 - 验证': [r'\d+人'],
    }
    # try:
    flatten_list = []
    for one_people_dict in res_list:
        role_name = one_people_dict['name']
        singular_type = one_people_dict['singular_type']
        for one_small_dict in singular_type:
            singular_detail = one_small_dict['singular_detail']
            for one_dict in singular_detail:
                cat = one_dict['cat']
                status = one_dict['status']
                page_number = [str(i) for i in one_dict['page_number']]
                rep = one_dict['rep']
                person_name = one_dict['person_name']
                res = one_dict['res']
                check_key = '未覆盖的检查点-查看out_dict'
                if '业绩' in cat:
                    continue
                for ch_key, rule_list in out_dict.items():
                    if rule_list and re.findall('|'.join(rule_list), res):
                        check_key = ch_key.replace(' ', '')
                        break
                final_one_dict = {
                    'role_name': role_name,
                    'skit': '',
                    'cat': cat,
                    'check_key': check_key,
                    'status': status,
                    'page_number': '页码为'+','.join(page_number),
                    'res': res,
                    'rep': rep,
                    'person_name': person_name,
                }
                flatten_list.append(final_one_dict)
    # print(flatten_list)
    pd.DataFrame(flatten_list).to_excel(r'C:\Users\shy\Desktop\复制结果.xlsx', index=False,)
    # except:
    # print('本地输出投标人员结果，失败')
    # pass


if __name__ == '__main__':
    b_path = r"\\Tlserver\标书文件\work\标书文件\02-昆明标书\06-昆明-市政类标书\33\云南雄辉建筑工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"\\Tlserver\标书文件\work\标书文件\02-昆明标书\06-昆明-市政类标书\33\云南雄辉建筑工程有限公司_TBJ\项目管理机构评审.pdf"


    # b = cached_file(b)
    # t = cached_file(t)
    # 跑已经在文件夹里有的缓存


    # title_info = get_title_info(b_path)
    # first_table = from_bid_get_table(b_path, 1)
    # second_table = from_bid_get_table(b_path, 2)
    # all_table = all_bid_table(b_path)



    # 梁兴敏 - 企业信息检查
    # print('人员信息交叉检查')

    # print(check_person_name(t_path, p1))
    #
    # # 梁兴敏 - 目录完整性检查
    # print('目录完整性检查')
    # catalogue_result = check_tender_catalogue(b_path, t_path, title_info, first_table, second_table, all_table, p1)
    # print(catalogue_result)
    #
    # # 韩-总工期检查
    # sum_work_time = contrast_duration_bid_tender(t_path, b_path)
    # print(sum_work_time)
    # # 佳玉- 投标有效期检查
    # valid_time = new_contrast_and_output_result(b_path, t_path, title_info, all_table, None, p1)
    # print(valid_time)
    # # 米- 保证金
    # ten_money = contrast_deposit_result(b_path, t_path, title_info, first_table, second_table, all_table, p2, person_summary_res)
    # print(ten_money)
    #
    # financial = compare_money_res(t_path, b_path, title_info, first_table, second_table, all_table, p2, person_summary_res)
    # print(financial)
    #
    # commit_result = contrast_commit_result(b_path, t_path, title_info, first_table, second_table, all_table, p1, person_summary_res)
    # print(commit_result)

    # print(get_tender_data(t))
    # print(get_period_price_of_tender(t))
    # print(con_tender_price(t_path, p1))

    # # 黄琦妍
    # print('资质')
    # print(contrast_qualification_result_new(t_path, b_path, title_info, first_table, second_table, all_table, p2,
    #                                         person_summary_res))
    # print('业绩')
    # print('招标')
    # print(bid_performance_analysis(b_path, title_info, first_table, second_table, all_table))
    # print('-----------------------------------------------------\n')
    # print('投标文件')
    # print(get_total_performance(t_path, p1, person_summary_res))
    # # print('-----------------------------------------------------\n')
    # print('招投标对比')
    # a = contrast_performance(b_path, t_path, title_info, first_table, second_table, all_table, p1, person_summary_res)
    # print(a)
    # print('--------------------------------------')
    # # 信用
    # cre_result = contrast_credit_result(b_path, t_path, title_info, first_table, second_table, all_table, p2)
    # print(cre_result)

    # # 魏琦
    # print('投标函对比')
    # res = contrast_letter_of_tender(b_path, t_path, title_info, first_table, second_table, all_table, p2, person_summary_res)
    # print(res)

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\云南杰恺建筑工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\云南杰恺建筑工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\云南水工程（集团）股份有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\云南水工程（集团）股份有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\赣州博达公路有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\赣州博达公路有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\赣州荣辉建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\赣州荣辉建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\江西丽景建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\江西丽景建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\昆明市市政工程(集团)有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\58\昆明市市政工程(集团)有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中建三局第一建设工程有限责任公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中建三局第一建设工程有限责任公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁十六局集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁十六局集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁四局集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁四局集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁五局集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁五局集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁一局集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\59\中铁一局集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\60\云南创宇景航实业有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\60\云南创宇景航实业有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\60\云南昊滇建设工程集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\60\云南昊滇建设工程集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\60\云南信丰建筑工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\60\云南信丰建筑工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\61\云南勾股建筑工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\61\云南勾股建筑工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\61\云南中正建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\61\云南中正建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\61\中鸿国际建工集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\61\中鸿国际建工集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\62\中铁八局集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\62\中铁八局集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\62\中铁十二局集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\62\中铁十二局集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\62\中铁十六局集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\62\中铁十六局集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\63\江西中云建设有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\63\江西中云建设有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\63\昆明市自来水设备制造安装有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\63\昆明市自来水设备制造安装有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\63\云南先启建筑工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\63\云南先启建筑工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\64\云南宇恒铁路工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\64\云南宇恒铁路工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\64\云南正瞿铁路工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\64\云南正瞿铁路工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\64\中铁八局集团第六工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\64\中铁八局集团第六工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\湖南建科园林有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\湖南建科园林有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南碧美市政环境工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南碧美市政环境工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南红洲园林工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南红洲园林工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南永烨环境建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南永烨环境建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南正浩建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\65\云南正浩建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\66\贵州仟亿筑城建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\66\贵州仟亿筑城建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\66\昆明市自来水建筑安装工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\66\昆明市自来水建筑安装工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\66\昆明市自来水设备制造安装有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\66\昆明市自来水设备制造安装有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\昆明建投建设工程集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\昆明建投建设工程集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\四川鑫圆建设集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\四川鑫圆建设集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\云南金沙江建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\云南金沙江建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\重庆市宏贵建设有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\67\重庆市宏贵建设有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南官房建筑集团股份有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南官房建筑集团股份有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南建投第二建设有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南建投第二建设有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南景顺建设工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南景顺建设工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南源邦建筑工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\68\云南源邦建筑工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\69\广东电白建设集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\69\广东电白建设集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\69\广东裕达建设集团有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\69\广东裕达建设集团有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\69\中建宏图建设发展有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\69\中建宏图建设发展有限公司_TBJ\项目管理机构评审.pdf"

    b_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\70\中国电建集团湖北工程有限公司_TBJ\ZBWJ.pdf"
    t_path = r"C:\Users\shy\Desktop\标书文件\昆明标书\70\中国电建集团湖北工程有限公司_TBJ\项目管理机构评审.pdf"

    b_path = cached_file(b_path, project=os.path.dirname(b_path))
    t_path = cached_file(t_path, project=os.path.dirname(t_path))
    p1, p2 = page_type_extrapolate(t_path, 2)
    person_summary_res = person_summary(t_path, p1)
    res = contrast_person_for_play(b_path, t_path, person_summary_res=person_summary_res)
    print(res)
    result_to_copy(res)
