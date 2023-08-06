"""
## pypi setup
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload --skip-existing dist/*
"""
import re
import pathlib
import setuptools

project_path = pathlib.Path(__file__).parent

def find_readme():
    """find readme file

    Returns:
        result
    """
    with open(project_path / 'README.md', encoding='utf-8') as readme_file:
        result = readme_file.read()
        return result

def find_requirements():
    """find requirements.txt

    Returns:
        list libs for pip install
    """
    with open(project_path / 'requirements.txt',
              encoding='utf-8') as requirements_file:
        result = [each_line.strip()
                  for each_line in requirements_file.read().splitlines()]
        return result

def find_version():
    """find version

    Returns:
        version number in __init__.py
    """
    with open(project_path  /  '__init__.py', 'r+',
              encoding='utf-8') as version_file:
        pattern = '^__version__ = [\'\"]([^\'\"]*)[\'\"]'
        match = re.search(pattern, version_file.readline().strip())
        result = None
        if match:
            result = match.group(1)
        lines = version_file.readline()
        for line in lines:
            if line.startswith('__version__'):
                version = line.split("=")[-1].strip()
                major,minor = version.split(".")
                print(major, minor)
            return result
# This call to setup() does all the work
setuptools.setup(
    name="github_pr_label",
    version="1.0.3", #find_version(),
    description="use define labels in json file and run by executing the script in your logic",
    long_description=find_readme(),
    long_description_content_type="text/markdown",
    url="https://www.github.com/cove9988/github_pr_label",
    author="paulg",
    author_email="cove9988@gamil.com",
    license="MIT",
    keywords='github, label, pull-request labelling,',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    package_data={'':['*.json']},
    install_requires=find_requirements(),
    entry_points={
        "console_scripts": [
            "github_pr_label=github_pr_label.__main__:main",
        ]
    },
)
