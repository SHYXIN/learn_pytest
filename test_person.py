# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 15:09
# @Author  : wangxin
# @File    : test_person.py
# @Software: PyCharm
import os
import shelve

import pytest
from pathlib import Path

from core.cust_tasks.performance.contrast import contrast_performance
from core.cust_tasks.person.contrast_person import contrast_person_for_play
from core.db import cached_file
from core.regular_expression_rule.keyword_info import bid_file, tender_file
from core.script.from_bid_get_table import from_bid_get_table, all_bid_table
from core.utils.get_document_title_range_index import get_title_info, page_type_extrapolate
from core.cust_tasks.tender_func.bidder_name_info import person_summary

def generate_data_group(**kwargs):
    """
    找出对应根目录中有正确结果的投标和招标文件路径
    :param kwargs:
    :return:
    """
    # 根据目录
    root_path = r"\\Tlserver\标书文件\work\标书文件\02-昆明标书\06-昆明-市政类标书\30"
    bid_name = kwargs['bid_name'] if 'bid_name' in kwargs else 'ZBWJ.pdf'
    tender_name = kwargs['tender_name'] if 'tender_name' in kwargs else '项目管理机构评审.pdf'
    res_name = kwargs['res_name'] if 'res_name' in kwargs else '人员结果'

    def generate_path_group(cor_res_path):
        """根据找到对比结果，形成路径组"""
        cur_root_path = cor_res_path.parent
        bid_p = cur_root_path / bid_name
        bid_p_str = '' if not bid_p.exists() else str(bid_p)
        tender_p = cur_root_path / tender_name
        tender_p_str = '' if not tender_p.exists() else str(tender_p)
        cur_root_path_str = str(cor_res_path.parent / cor_res_path.name.split('.')[0])
        return bid_p_str, tender_p_str, cur_root_path_str

    def get_value(path_gro):
        """根据路径组，将对应的缓存文件反序列化"""
        # bid_val = cached_file(path_gro[0], project=os.path.dirname(path_gro[0]))
        # tender_val = cached_file(path_gro[1], project=os.path.dirname(path_gro[1]))
        with shelve.open(path_gro[2]) as d:
            cor_res = d.get(res_name)
        return path_gro[0], path_gro[1], cor_res

    path_obj = Path(root_path)
    correct_res_path = list(path_obj.rglob('correct_*.dat'))
    all_correct_str_list = []
    for cor_path in correct_res_path:
        path_group = generate_path_group(cor_path)
        if all(path_group):
            all_correct_str_list.append(path_group)
    all_correct_list = [get_value(g) for g in all_correct_str_list]
    # print(all_correct_list)
    return all_correct_list


def sss(**kwargs):
    ssg_group = generate_data_group(res_name='业绩结果')

    big_group = []
    for three_group in ssg_group:
        bid = three_group[0]
        title_info = get_title_info(bid_file)
        first_table = from_bid_get_table(bid_file, 1)
        second_table = from_bid_get_table(bid_file, 2)
        all_table = all_bid_table(bid_file)
        p1 = page_type_extrapolate(tender_file, 1)
        person_summary_res = person_summary(three_group[1], p1)


        new_tuple = (three_group[0], three_group[1], three_group[2], title_info, first_table, second_table, all_table, p1, person_summary_res)
        big_group.append(new_tuple)
    return big_group


res_group = generate_data_group(name='人员结果')
ids = ["招标文件：{}————投标文件：{}".format(group[0], group[1]) for group in res_group]


@pytest.mark.parametrize('bid_path, tender_path, correct_result', res_group, ids=ids)
def test_per_cer(bid_path, tender_path, correct_result):
    bid_path = cached_file(bid_path, project=os.path.dirname(bid_path))
    tender_path = cached_file(tender_path, project=os.path.dirname(tender_path))
    """测试人员证书"""
    cur_result = contrast_person_for_play(bid_path, tender_path)
    # 是否完全相等
    cor_res = cur_result == correct_result
    assert cor_res


per_res_group = generate_data_group(res_name='业绩结果')
per_ids = ["招标文件：{}————投标文件：{}".format(group[0], group[1]) for group in per_res_group]


@pytest.mark.parametrize('bid_path, tender_path, correct_result', 'title_info, first_table, second_table, all_table, p1, person_summary_res', sss, ids=per_ids)
def test_perf(bid_path, tender_path, correct_result, title_info, first_table, second_table, all_table, p1, person_summary_res):
    bid_path = cached_file(bid_path, project=os.path.dirname(bid_path))
    tender_path = cached_file(tender_path, project=os.path.dirname(tender_path))
    """测试业绩"""
    cur_result = contrast_performance(bid_file, tender_file, title_info, first_table, second_table, all_table, p1, person_summary_res)
    # 是否完全相等
    cor_res = cur_result == correct_result
    assert cor_res


if __name__ == "__main__":
    generate_data_group()
    # # pytest.main()
    # bid_file = cached_file(b_path, project=os.path.dirname(b_path))
    # tender_file = cached_file(t_path, project=os.path.dirname(t_path))
    #
    # title_info = get_title_info(bid_file)
    # first_table = from_bid_get_table(bid_file, 1)
    # second_table = from_bid_get_table(bid_file, 2)
    # all_table = all_bid_table(bid_file)
    # p1 = page_type_extrapolate(tender_file, 1)
    # person_summary_res = person_summary(tender_file, p1)
    #
    # perf_res = contrast_performance(bid_file, tender_file, title_info, first_table, second_table, all_table, p1,
    #                                 person_summary_res)
    # with shelve.open(cor_path) as data:
    #     data['业绩结果'] = perf_res
    #     # data['qiye'] = zizhi_res
