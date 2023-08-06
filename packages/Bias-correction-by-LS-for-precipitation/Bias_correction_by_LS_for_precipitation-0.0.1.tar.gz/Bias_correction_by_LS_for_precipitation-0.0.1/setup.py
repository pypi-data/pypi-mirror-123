from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
     'Programming Language :: Python :: 3' 
]

setup(
    name='Bias_correction_by_LS_for_precipitation',
    version='0.0.1',
    description='Bias correction for precipitation using linear scaling method',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Akkarapon Chaiyana',
    author_email='akkarapon.chaiyana@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Bias correction, Linear scaling, Precipitation',
    packages=find_packages(),
    install_require=['']
)