from setuptools import setup, find_packages

setup(
    name='vm-analyzer',
    packages=find_packages(),
    version='0.1.0',
    entry_points={
        'console_scripts': [
            'vm-analyzer-agent=agent.main:main'
        ]
    }
)
