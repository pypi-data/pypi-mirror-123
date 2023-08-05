import os
import setuptools
import bddjango


dirname = 'bddjango'
version = bddjango.version()


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name=dirname,
    version=version,
    author="bode135",
    author_email='2248270222@qq.com',   # 作者邮箱
    description="常用的django开发工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitee.com/bode135/bdtools/tree/master/bddjango',   # 主页链接
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas', 'openpyxl', 'xlrd'],      # 依赖模块
    include_package_data=True,
)
