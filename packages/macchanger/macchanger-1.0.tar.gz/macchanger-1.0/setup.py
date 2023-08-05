from setuptools import setup, find_packages

classifier = [
    'Development Status :: Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Windows 10 :: Kali Linux',
    'License :: MIT License',
    'Programming Language :: Python3'

]

setup(
    name='macchanger',
    version='1.0',
    description='Only For Education Purpose',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='winhtut',
    author_email='winhtutonline@gmail.com',
    license='MIT',
    classifier=classifier,
    keyword='',
    packages=find_packages(),
    install_requires=['termcolor']  # external packages as dependencies
)
