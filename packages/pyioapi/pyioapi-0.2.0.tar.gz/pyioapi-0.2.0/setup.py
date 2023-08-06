from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='pyioapi',
    version="0.2.0",
    description=(
        'The Python library provides read,write IOAPI-like netCDF file in CMAQ'
    ),
    author='Kangjia Gong',
    author_email='kjgong@kjgong.cn',
    maintainer='Kangjia Gong',
    maintainer_email='kjgong@kjgong.cn',
    license='MIT License',
    install_requires=install_requires,
    packages=find_packages(exclude=('tests',)),
    platforms=["all"],
    url='https://github.com/Gongkangjia/pyioapi',
    entry_points={
        'xarray.backends': [
            'pyioapi=pyioapi.io:IoapiBackendEntrypoint',
            'ioapi=pyioapi.io:IoapiBackendEntrypoint',
        ]
    },
)
