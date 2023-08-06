from setuptools import setup

setup(
    name='fsthist',
    version='0.1.0',
    description='Fast histogram',
    url='https://github.com/sepuhopar',
    author='Melikyan Sepuh',
    author_email='sepuhopar@gmail.com',
    license='BSD 2-clause',
    packages=['fsthist'],
    install_requires=['typing',
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
