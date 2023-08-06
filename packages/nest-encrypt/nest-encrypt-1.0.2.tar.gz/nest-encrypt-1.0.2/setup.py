import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nest-encrypt",
    version="1.0.2",
    author="fuqiang",
    author_email="imock@sina.com",
    description="nest common encrypt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['rsa==4.7.2', 'pycryptodome==3.10.1'],
    python_requires='>=3'
)