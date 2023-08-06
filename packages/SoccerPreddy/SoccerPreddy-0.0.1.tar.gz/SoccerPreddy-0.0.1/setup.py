from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Other Audience',
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
    name='SoccerPreddy',
    version='0.0.1',
    description='A python package for soccer prediction',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Taiwo Gabriel',
    license='MIT',
    author_email='omomuletaiwo@gmail.com',
    url='https://github.com/Taiwo2020/SoccerPred',
    classifiers=classifiers,
    keyword=['Soccer', 'Football', 'Sport', 'Prediction'],
    install_requires=['numpy', 'pandas', 'sklearn',
                      'xgboost', 'lightgbm'],
    packages=find_packages()

)