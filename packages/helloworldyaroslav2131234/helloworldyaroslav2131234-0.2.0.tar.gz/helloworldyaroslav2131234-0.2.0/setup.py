import setuptools

setuptools.setup(
    name='helloworldyaroslav2131234',
    version='0.2.0',
    description='A hello world Python package',
    author='Yaroslav Yaroslav',
    package_dir={"": "source"},
    packages=setuptools.find_packages(where="source"),
    install_requires=['numpy<1.20.0']
)
