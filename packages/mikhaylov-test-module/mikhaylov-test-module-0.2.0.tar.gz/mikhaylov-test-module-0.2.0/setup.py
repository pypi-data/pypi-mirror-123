from setuptools import setup

setup(
    name='mikhaylov-test-module',
    version='0.2.0',
    description='A test module for ITMO DA course',
    url='https://github.com/Jovvik/mikhaylov-test-module',
    author='Maxim Mikhaylov',
    author_email='284542@niuitmo.ru',
    license='BSD 2-clause',
    packages=['mikhaylov_test_module'],
    install_requires=['numpy <= 1.18'],

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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
