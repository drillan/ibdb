from setuptools import setup, find_packages


setup(
    name="ibdb",
    version="0.0.0a2",
    description="IB-insync to Database",
    author="driller",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=["ib-insync", "sqlalchemy"],
    python_requires='>=3.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
)