from setuptools import setup

setup(
    name='comibat',
    version='0.1.4',
    py_modules=['comibat'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'comibat = comibat:cli',
        ],
    },
    author='Adil Atalay Hamamcioglu',
    author_email='38231748+recoskyler@users.noreply.github.com',
    description='A tool to add a title page to CBZ comic book archives',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/recoskyler/comibat',
    license='GNU General Public License v3.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
        'Development Status :: 4 - Beta',
    ],
)
