# -*- coding: utf-8 -*-
# @Time    : 2022/2/24 14:16
# @Author  : wangxin
# @File    : conftest.py.py
# @Software: PyCharm
import pytest
from py._xmlgen import html

'''
pytest里面默认读取conftest.py里面的配置
conftest.py配置需要注意以下点：
    conftest.py配置脚本名称是固定的，不能改名称
    conftest.py与运行的用例要在同一个pakage下，并且有__init__.py文件
    不需要import导入 conftest.py，pytest用例会自动查找
'''


def pytest_html_report_title(report):
    report.title = "自动化回归测试"


'''Environment 修改
    pytest-metadata提供Environment section,
    通过pytest_configure访问 '''


def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = "标书检查"
    # config._metadata['接口地址'] = 'https://www.baidu.com/'
    # 删除Java_Home
    # config._metadata.pop("JAVA_HOME")


'''Additional summary information  
    附加摘要信息'''


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("作者: 王鑫")])
    # prefix.extend([html.p("负责人: 王鑫")])


'''在报表对象上创建'额外'列表，从而向HTML报告添加详细信息'''


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        # always add url to report
        # extra.append(pytest_html.extras.text('http://www.baidu.com/'))
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        report.description = str(item.function.__doc__)
        report.extra = extra
        report.path = extra

def pytest_html_results_table_header(cells):
#     cells.insert(2, html.th("路径"))
#     # cells.insert(1, html.th("Time", class_="sortable time", col="time"))
#     # cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
#     cells.insert(2, html.td(next(report.description)))
#     # cells.insert(1, html.td(datetime.utcnow(), class_="col-time"))
#     # cells.insert(1, html.td(datetime.utcnow(), class_="col-time"))
    cells.pop()
