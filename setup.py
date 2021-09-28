from setuptools import setup, find_packages

DESCRIPTION = 'Azkaban Flow Generator'
LONG_DESCRIPTION = open('README.md').read()
NAME = "azkaban-helper"
AUTHOR = "Jing Zhang"
AUTHOR_EMAIL = 'cherish244612023@gmail.com'
MAINTAINER = "Jing Zhang"
MAINTAINER_EMAIL = 'cherish244612023@gmail.com'
DOWNLOAD_URL = 'https://github.com/JingZhang-Cherish/azkaban_excel_yaml.git'
LICENSE = 'MIT Licence'
VERSION = '0.0.2'

install_reqs = ['requests~=2.25.1',
                'xlrd~=1.2.0',
                'PyYAML~=5.4.1',
                'requests-toolbelt~=0.9.1']

setup(
    name=NAME,
    version=VERSION,
    url=DOWNLOAD_URL,
    author=AUTHOR,
    packages=['src'],
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    license=LICENSE,
    include_package_data=True,
    classifiers=[
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # 开发的目标用户
        'Intended Audience :: Developers',
        'Environment :: Console',

        # 属于什么类型
        'Topic :: Software Development :: Build Tools',

        # 许可证信息
        'License :: OSI Approved :: MIT License',

        # 目标 Python 版本
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=install_reqs,
    python_requires='>=3, <=3.9',
    entry_points={
        'console_scripts': [
            'azkaban_helper = src.generator:main'
        ]
    },
    platforms=['MAC OS', 'Windows', 'Linux', 'Unix']
)
