# -*- coding: utf-8 -*-
# Author:df_coding
# Time:2021/10/12 10:58
# -*- coding: UTF-8 -*-

import setuptools
import os

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
    name='cookielab',
    version='0.0.1',
    keywords='spider, cookie',
    description='An Util for python packaging.',
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
