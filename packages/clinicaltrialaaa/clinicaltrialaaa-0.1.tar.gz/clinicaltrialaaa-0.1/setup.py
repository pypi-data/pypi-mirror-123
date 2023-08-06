from distutils.core import setup
from setuptools import find_packages

setup(name='clinicaltrialaaa',  # 包名
      version='0.1',  # 版本號
      description='A small example package',
      long_description='clinical trial information retriver',
      author='slindev',
      author_email='slin.devel@gmail.com',
      url='https://github.com/suylin/clinicaltrial',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],)
