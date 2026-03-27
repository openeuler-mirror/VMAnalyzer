from setuptools import setup, find_packages
import os

# Read README for long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vm-analyzer',
    packages=find_packages(),
    version='0.1.0',
    description='A lightweight virtualization performance monitoring analysis tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='China Mobile (SuZhou) Software Technology Co.,Ltd.',
    license='Mulan PSL v2',
    url='https://gitee.com/openeuler/VMAnalyzer',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (Mulan PSL v2)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    install_requires=[
        'redis',
        'mock',
        'python3-libvirt'
    ],
    entry_points={
        'console_scripts': [
            'vm-analyzer-agent=agent.main:main'
        ]
    }
)
