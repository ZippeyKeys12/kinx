from json import load

from setuptools import setup, find_packages

with open("package.json", "r") as f:
    info = load(f)

with open("README.md", "r") as f:
    readme = f.read()


setup(
    name=info["name"],
    version=info["version"],
    description=info["description"],
    long_description=readme,
    long_description_content_type="text/markdown",
    url=info["homepage"],
    license=info["license"],
    author=info["author"]["name"],
    author_email=info["author"]["email"],
    platforms="any",
    python_requires=">=3.6.0",
    setup_requires=["pipenv"],
    packages=find_packages(),
    install_requires=["cython", "mistune", "python-frontmatter", "jinja2", "pyyaml"],
    test_requires=["pytest"],
    include_package_data=True,
    package_data={"templates": "*.md"},
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
