from setuptools import setup, find_packages

setup(
    name='subzerod',
    version='1.0',
    python_requires='>=3.6',
    install_requires=['aiohttp'],
    packages=find_packages()+['.'],
    include_package_data=True,
    entry_points='''
       [console_scripts]
       subzerod=subzerod.cli:cli_run
    ''',
    url='https://github.com/sanderfoobar/subzerod',
    license='BSD-3.0',
    description='Subdomain enumeration tool',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        "License :: OSI Approved :: WTFPL-Clause",
        'Operating System :: POSIX :: Linux',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Topic :: Security',
    ],
    keywords='subdomain pentesting pentest security'
)
