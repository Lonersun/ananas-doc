# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(name='ananas-doc',
      version='1.2.3',
      description=u"docs tools",
      long_description="",
      classifiers=[],
      keywords='docs tools',
      author="Lonerusn",
      author_email="yang.guo.sun@gmail.com",
      url='https://github.com/Lonersun/ananas-doc',
      license='Apache License 2.0',
      platforms='any',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=[
          'sphinx>=1.6.3',
          'sphinx-rtd-theme>=0.2.4',
          'm2r>=0.1.12',
          'ruamel.yaml==0.12.5',
      ],
      entry_points={
          'console_scripts': [
              'ananas-mkdoc = ananasdoc:main',
          ],
          'gui_scripts': [
              'ananas-mkdoc = ananasdoc:main',
          ]
      },
)

