# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(name='ananas-doc',
      version=1.0,
      description=u"docs tools",
      long_description="",
      classifiers=[],
      keywords='',
      author="Lonerusn",
      url='https://github.com/Lonersun/ananas-doc',
      license='Apache License 2.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'sphinx>=1.6.3',
          'sphinx-rtd-theme>=0.2.4',
          'm2r>=0.1.12',
          'pyaml>=3.12',
      ],
      dependency_links=[

      ],
      extras_require={

      },
)

