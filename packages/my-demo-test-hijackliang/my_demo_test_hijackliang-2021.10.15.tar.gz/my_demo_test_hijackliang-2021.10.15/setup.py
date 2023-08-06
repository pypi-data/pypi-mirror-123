# -*- coding: UTF-8 -*-
import os
 
import setuptools
 
setuptools.setup(
    name='my_demo_test_hijackliang',
    version='2021.10.15',
    keywords='demo',
    description='A demo for python packaging.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    author='hijackliang',      # 替换为你的Pypi官网账户名
    author_email='2858744808@qq.com',  # Pypi账户名绑定的邮箱
 
    url='https://github.com/mamabi/demo',   # 这个地方为github项目地址，貌似非必须
    packages=setuptools.find_packages(),
    license='MIT'
)
