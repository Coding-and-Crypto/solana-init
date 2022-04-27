import pathlib
from setuptools import setup


setup(
    name="solana_init",
    version="0.0.1",
    description="Get off the ground fast with auto-generated Solana workspaces.",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="git@github.com:Coding-and-Crypto/solana-init.git",
    author="Joseph Caulfield",
    author_email="jcaulfield135@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["solana_init"],
    include_package_data=True,
    install_requires=["pathlib", "setuptools"],
    entry_points={
        "console_scripts": [
            "solana_init=solana_init.__main__:main",
        ]
    },
)
