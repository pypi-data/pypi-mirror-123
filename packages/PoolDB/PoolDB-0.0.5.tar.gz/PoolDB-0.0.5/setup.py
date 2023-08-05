
# @Time    : 2020/8/24 20:24
# @Author  : alita
# File     : setup.py

import setuptools

with open("./PoolDB/readme.md", "r", encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="PoolDB",
  version="0.0.5",
  author="alita",
  author_email="1906321518@qq.com",
  description="Pool DB package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/AlitaIcon/PoolDB",
  packages=setuptools.find_packages(include=['PoolDB']),
  license='MIT',
  include_package_data=True,
  install_requires=[
      'SQLAlchemy>=1.3.19',
      'gevent>=21.1.2',
      'loguru>=0.5.3',
      'gevent>=21.8.0',
      'pandas>=1.1.5'
  ],
  python_requires='>=3.6',
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  project_urls={
    'Documentation': 'https://github.com/AlitaIcon/PoolDB',
  },
)

# 执行 python setup.py sdist
# 执行 python setup.py upload