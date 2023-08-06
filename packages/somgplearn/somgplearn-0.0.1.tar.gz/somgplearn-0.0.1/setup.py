
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='somgplearn',
  version='0.0.1',
  description='simpy+gplearn',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Alzain',
  author_email='taryarwinhtet@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  ackages=find_packages(include=['somgplearn']),
  install_requires=[        
        'PyYAML',
        'pandas==0.23.3',
        'numpy>=1.14.5',
        'matplotlib>=2.2.0',
        'jupyter',
        'sklearn','scikit-learn','joblib'] 
)