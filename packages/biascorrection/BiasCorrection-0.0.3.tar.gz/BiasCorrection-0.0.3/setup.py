from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
     'Programming Language :: Python :: 3' 
]

setup(
    name='BiasCorrection',
    version='0.0.3',
    description='Bias correction',
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