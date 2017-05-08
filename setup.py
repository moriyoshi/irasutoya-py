from setuptools import setup, find_packages


from irasutoya import __version__

setup(
    name='irasutoya',
    version=__version__,
    author='Moriyoshi Koizumi',
    author_email='mozo@mozo.jp',
    description='Scrapes over www.irasutoya.com and fetchs information about illustrations provided there',
    long_description=open('README.rst').read(),
    keywords='scraping irasutoya illustration',
    url='https://github.com/moriyoshi/irasutoya-python',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
    packages=find_packages(),
    zip_safe=False,
    package_data={
        '': ['*.rst', '*.txt', '*.html'],
        },
    install_requires=[
        'urllib3',
        'lxml',
        'six',
        ],
    tests_require=[
        'mock',
        ],
    extras_require={
        'tox': ['tox'],
        },
    entry_points={
        'console_scripts': [
            'irasutoya = irasutoya.tools:main',
            ],
        },
    test_suite='irasutoya.tests'
    )
