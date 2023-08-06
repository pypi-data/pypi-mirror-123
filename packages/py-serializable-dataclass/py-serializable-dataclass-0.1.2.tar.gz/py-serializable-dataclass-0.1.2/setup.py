from setuptools import setup, find_packages

setup(
    name="py-serializable-dataclass",
    version="0.1.2",
    packages=find_packages("erializable_dataclass", exclude=("tests*",)),
    package_data={"lib": ["py.typed"]},
    author="jason",
    author_email="jiahuic@twitter.com",
    description="Easily makes python object as a serializable dataclass",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/tinyHui/python-serializable-dataclass",
    project_urls={"Tracker": "https://github.com/tinyHui/python-serializable-dataclass/issues"},
    license="GNU General Public License v3.0",
    keywords="dataclasses json",
    install_requires=[],
    python_requires=">=3.7",
    extras_require={"dev": ["pytest", "pytest-cov", "mypy", "flake8", "black"]},
    include_package_data=True,
    scripts=["publish.py"],
)


