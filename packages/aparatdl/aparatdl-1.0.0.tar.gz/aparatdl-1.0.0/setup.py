import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="aparatdl",
    version="1.0.0",
    author="Ali Ansari Mahyari",
    author_email="aliansari.it@gmail.com",
    description="download video from 'aparat.com' with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliansari1214/pyaparat_dl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

