from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='spl_parser',
    version='0.1',
    description='SPL Parser',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Lukáš Kotlaba',
    author_email='lukas.kotlaba@gmail.com',
    keywords='splunk,spl,sytax,highlighting',
    license='GNU GPLv3',
    url='https://github.com/kotlaluk/spl-parser',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Editors',
        'Topic :: Utilities'
        ],
    install_requires=['aiohttp', 'lark-parser', 'click'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'spl_parser = spl_parser.cli:cli',
        ],
    },
    package_data={'spl_parser': ['templates/*.json', 'grammars/*.lark']},
    zip_safe=False,
)
