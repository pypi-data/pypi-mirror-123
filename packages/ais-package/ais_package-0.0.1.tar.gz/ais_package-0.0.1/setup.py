from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ais_package',
  version='0.0.1',
  description='Test package!',
  long_description='',
  url='',  
  author='Ed Valdez',
  author_email='efvaldez.consultant@adb.org',
  license='MIT', 
  classifiers=classifiers,
  keywords='AIS', 
  packages=find_packages(),
  install_requires=[''] 
)