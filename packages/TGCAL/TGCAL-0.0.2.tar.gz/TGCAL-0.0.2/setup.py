from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows ',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3'


]

setup(
    name='TGCAL',
    version='0.0.2',
    description='A basic package to perform calculations on two numbers',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Taiwo Gabriel',
    license='MIT',
    author_email='omomuletaiwo@gmail.com',
    url='https://github.com/Taiwo2020/TGCal',
    classifiers=classifiers,
    keyword=['Mathematics', 'Education', 'Calculator', 'Arithmetic'],
    install_requires=[''],
    packages=find_packages()

)