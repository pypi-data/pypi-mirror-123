from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = "meldedaten_faker",
    version = "0.5.0",
    author = "Dominik Visca",
    author_email = "dominik.visca@hs-mainz.de",
    license = "MIT",
    description = "Generates fake citizen registration data",
    long_description = "",
    long_description_content_type = "",
    url = "",
    py_modules = ["meldedaten_faker", "app"],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires=">=3.9",
    classifierts=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points = """
        [console_scripts]
        meldedaten_faker=meldedaten_faker:cli
    """
)