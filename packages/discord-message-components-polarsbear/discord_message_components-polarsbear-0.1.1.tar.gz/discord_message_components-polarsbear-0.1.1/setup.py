ver = "0.1.1"
import setuptools, os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discord_message_components-polarsbear",
    version=ver,
    author="Lars Von Wangenheim",
    author_email="larzitovw@gmail.com",
    description="A python library that adds message component support to discord bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PolarsBear/Discord-Message-Components",
    project_urls={
        "Bug Tracker": "https://github.com/PolarsBear/Discord-Message-Components/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["discord"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)