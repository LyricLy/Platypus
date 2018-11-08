import setuptools


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name = "Platypus-discord",
    packages = setuptools.find_packages(),
    version = "0.1.0",
    description = "A toolkit for the discord.py library.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = "LyricLy",
    author_email = "gulliverhanson@gmail.com",
    url = "https://github.com/LyricLy/Platypus",
    keywords = ["discord.py", "toolkit", "discord"],
    install_requires = [x for x in requirements if "git+" not in x],
    dependency_links = [x.split("git+")[1] for x in requirements if "git+" in x],
    license = "MIT",
    classifiers = [
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities"
    ]
)
