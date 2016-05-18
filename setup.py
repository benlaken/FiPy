from setuptools import setup, find_packages

setup(
    name='fispy',
    version='0.1',
    description='To explore various personal financial scenarios',
    packages=find_packages(exclude=['*test']),
    scripts=[],
    author='Benjamin Laken',
    url='https://github.com/benlaken/fispy',
    license='by-nc-sa',
    install_requires=['bokeh', 'pandas']
)
