"""组装jmx"""
import html
import json
import os
import shutil
from urllib.parse import urlparse

import jinja2


def to_str(value):
    if isinstance(value, str):
        return value
    if value is True:
        return 'true'
    if value is False:
        return 'false'
    if value is None:
        return ''
    if isinstance(value, (dict, list, tuple)):
        return html.escape(json.dumps(value))  # todo check
    # todo url_encode


def build_jmx(obj: models.TestPlan) -> str:
    data = build_test_plan(obj)
    test_plan_dir = os.path.join(WORKSPACE, f'testplan_{obj.id}')
    jmx_file = os.path.join(test_plan_dir, f'testplan_{obj.id}.jmx')
    dat_dir = os.path.join(test_plan_dir, 'dat')
    report_jtl_dir = os.path.join(test_plan_dir, 'report_jtl')
    report_html_dir = os.path.join(test_plan_dir, 'report_html')

    # 创建目录
    for dir in [test_plan_dir, dat_dir, report_jtl_dir, report_html_dir]:
        if not os.path.isdir(dir):
            print('不存在', dir)
            os.makedirs(dir)

    # [os.mkdir(dir) for dir in [test_plan_dir, dat_dir, report_jtl_dir, report_html_dir] if not os.path.isdir(dir)]

    # 读取模板
    with open(TPL_FILE, encoding='utf-8') as f:
        tpl = f.read()

    # 生成jmx
    jmx = jinja2.Template(tpl).render(data)
    with open(jmx_file, 'w', encoding='utf-8') as f:
        f.write(jmx)

    # 复制csv文件
    copy_all_data_files(obj, test_plan_dir)

    return test_plan_dir


if __name__ == '__main__':
    t = models.TestPlan.objects.get(id=1)
    build_jmx(t)
