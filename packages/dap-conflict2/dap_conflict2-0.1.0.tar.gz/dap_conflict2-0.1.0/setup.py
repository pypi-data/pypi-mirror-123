from setuptools import setup

setup(
    name='dap_conflict2',
    version='0.1.0',    
    description='A confict Python package',
    author='Ivan Naumov',
    author_email='naumovovr@mail.ru',
    packages=['dap_conflict2'],
    install_requires=['numpy<1.19.0',
                      'wheel'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

