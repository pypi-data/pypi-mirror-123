#coding=utf-8
from distutils.core import setup

setup(
    name='zwkPython', # 对外我们模块的名字
    version='1.0', # 版本号
    description='a test for create my own module', #描述
    author='zwk', # 作者
    author_email='376848969@qq.com', py_modules=['zwkPython.test'] # 要发布的模块
)