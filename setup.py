from setuptools import setup, find_packages
import os

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8') as f:
        return f.read()

def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name="conciliacion-bancaria",
    version="0.1.0",
    author="Lionel Alan Choque",
    author_email="lionelchoque@gmail.com",
    description="Herramienta de conciliación bancaria",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/LionelChoque/Conciliacion-excel",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'conciliacion=conciliacion.conciliacion:run_cli',
        ],
    },
    include_package_data=True,
)