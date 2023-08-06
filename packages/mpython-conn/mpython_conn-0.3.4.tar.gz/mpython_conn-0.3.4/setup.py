from setuptools import setup,find_packages

setup(

    name='mpython_conn',
    version='0.3.4',
    keywords=('pip','mpython'),
    description="control mpython board by pc",
    long_description=''' please visit http://wiki.labplus.cn/index.php?title=Mpython_conn for tutor''',
    licence='MIT Licence',

    url='https://github.com/labplus-cn/mpython_conn',
    author='james',
    author_email="jim0575@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['pySerial']
    )
