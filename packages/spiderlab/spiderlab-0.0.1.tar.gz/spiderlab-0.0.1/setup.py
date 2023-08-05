# -*- coding: utf-8 -*-
# Author:df_coding
# Time:2021/10/12 10:58
# -*- coding: UTF-8 -*-

import setuptools
import os
import requests


# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to': 'rst', 'from': 'markdown'},
                      files={'input_files[]': open(from_file, 'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)


md_to_rst("README.md", "README.rst")

if os.path.exists('README.rst'):
    long_description = open('README.rst', encoding="utf-8").read()
else:
    long_description = 'Add a fallback short description here'

if os.path.exists("requirements.txt"):
    with open("requirements.txt") as fr:
        install_requires = fr.read().split("\n")
else:
    install_requires = []

setuptools.setup(
    name='spiderlab',
    version='0.0.1',
    keywords='spider',
    description='An Util for python spider packaging.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author='df_coding',  # 替换为你的Pypi官网账户名
    author_email='df_coding@163.com',  # 替换为你Pypi账户名绑定的邮箱
    packages=setuptools.find_packages(),
)
