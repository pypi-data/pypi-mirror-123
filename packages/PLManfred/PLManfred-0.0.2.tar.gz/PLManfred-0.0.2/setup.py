from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='PLManfred',
  version='0.0.2',
  description='ai',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='F0X0000',
  author_email='wcalenief0x@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='manfred',
  packages=find_packages(),
  install_requires=['']
)
