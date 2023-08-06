# -*- encoding: utf-8 -*-
"""
@File    :   setup.py
@Time    :   2020/12/22 16:48:54
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2020, shwfed.com
@Desc    :   组件安装文件
"""

# here put the import lib
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    _domain = ''
    long_description = fh.read().replace('(docs/', '(https://gitee.com/shwfed-tsd/junglead-common-python/tree/develop/docs/')

setuptools.setup(
    name="junglead",
    version="2.2",
    author="Gary Wang",
    author_email="wangyijun@shwfed.com",
    description="Junglead common util by Python version.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://gitee.com/shwfed-tsd/junglead-common-python",
    project_urls={
        "Bug Tracker": "https://gitee.com/shwfed-tsd/junglead-common-python/issues",
    },

    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'setuptools', 'wheel'
    ],

    python_requires=">=3",
)
