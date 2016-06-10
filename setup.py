from setuptools import setup, find_packages

setup(
    name='fispy',
    version='0.1',
    description='To explore various personal financial scenarios',
    packages=find_packages(exclude=['*test']),
    scripts=[],
    author_email='benlaken@icloud.com',
    author='Benjamin Laken',
    url='https://github.com/benlaken/fispy',
    download_url="https://github.com/benlaken/fispy/tarball/0.1",
    license='by-nc-sa',
    install_requires=['bokeh', 'pandas'],
    keywords=['finance', 'personal', 'independence'],
    zip_safe=False,
)
