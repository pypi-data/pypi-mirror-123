from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    packages = find_packages(),
    name = 'mingwtomsys',
    version='0.0.2',
    author="Stanislav Doronin",
    author_email="mugisbrows@gmail.com",
    url='https://github.com/mugiseyebrows/mingw-to-msys',
    description='PKGBUILD converter for msys2',
    long_description = long_description,
    install_requires = [],
    entry_points={
        'console_scripts': [
            'mingw-to-msys=mingwtomsys:main',
        ]
    },
    license_files = ('LICENSE',),
)