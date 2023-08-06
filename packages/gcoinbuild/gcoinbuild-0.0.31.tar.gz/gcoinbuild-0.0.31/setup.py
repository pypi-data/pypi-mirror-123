import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gcoinbuild",
    version="0.0.31",
    author="Yek",
    author_email="gwojtysiak34@gmail.com",
    description="Official GCoin Library",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)