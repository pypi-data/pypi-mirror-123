from setuptools import setup

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="text_scrambler",
    version="0.1.4",
    packages=[
        "text_scrambler",
    ],
    url="https://text-scrambler.readthedocs.io",
    license="MIT",
    author="GLNB",
    author_email="glnb.dev@gmail.com",
    description="text_scrambler, a tool to scramble texts",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=install_requires,
    project_urls={
        "Documentation": "https://text-scrambler.readthedocs.io",
        "Source": "https://github.com/GuillaumeLNB/text-scrambler",
    },
    include_package_data=True,
    package_data={"text_scrambler": ["txt_files/confusablesSummary.txt"]},
)
