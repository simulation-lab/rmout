from setuptools import find_packages, setup


setup(
    name='rmout',
    version='0.3.0',

    author='kino',
    author_email='simulation.space.labs@gmail.com',
    url='https://github.com/simulation-lab/rmout',

    description='rmout is a tool for throwing unnecessary files in a directory into the trash.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    python_requires='~=3.8',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'click~=7.1',
        'send2trash~=1.5',
    ],

    entry_points={
        'console_scripts': [
            'rmout=rmout.core:run'
        ]
    },

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],

)
