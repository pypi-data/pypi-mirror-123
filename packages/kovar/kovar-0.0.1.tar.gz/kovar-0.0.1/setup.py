from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A basic hello package'

# Setting up
setup(
    name='kovar',
    version=VERSION,
    author='@kovar',
    author_email='<jiri@kovar.cz>',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords=['python', 'personal'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)