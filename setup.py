from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

INSTALL_REQUIRES = [
    "aiohttp==3.*"
]

setup(
    name='subzerod',
    version='1.0',
    author='Sander',
    author_email='sander@sanderf.nl',
    python_requires='>=3.6',
    packages=['subzerod'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    entry_points='''
       [console_scripts]
       subzerod=subzerod.cli:cli_run
    ''',
    url='https://github.com/sanderfoobar/subzerod',
    license='WTFPL',
    description='Subdomain enumeration tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Operating System :: POSIX :: Linux',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Topic :: Security',
    ],
    keywords='subdomain pentesting pentest security'
)
