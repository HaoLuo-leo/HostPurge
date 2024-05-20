from setuptools import setup, find_packages

setup(
    name='hostpurge',
    version='1.0.0',
    description='Host contamination removal tool',
    author='Hao Luo',
    author_email='luohao@caas.cn',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hostpurge = hostpurge.main:main'
        ]
    },
    install_requires=[
        'kneaddata==0.12.0',
        'kraken2==2.1.2',
        'biopython'
    ],
)
