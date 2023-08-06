from setuptools import setup, find_packages

setup(
    name="cdftpy",
    version="0.0.4",
    author='Marat Valiev and Gennady Chuev',
    author_email='marat.valiev@gmail.com',
    description='Classical density functional theory code',
    packages=find_packages(exclude=('tests*',)),
    package_data={
        "":["data/*"]
    },
    install_requires=[
            'scipy>=1.6.1',
            'numpy>=1.20.1',
            'matplotlib>=3.3.4',
            'click',
            'prompt_toolkit'
    ],
    entry_points={
        'console_scripts': [
            'cdft = cdft1d.cli:cdft',
            'rism1d = cdftpy.cdft1d.cli:rism1d_run_input',
            'rsdft1d = cdftpy.cdft1d.cli:rsdft1d_run_input'
        ]
    }
)
