import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="arithmeticericjoden94",
        version="0.0.3",
        author="Eric Oden",
        author_email="ericjoden94@gmail.com",
        description="A simple arithmetic package",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/driscollis/arithmetic",
        packages=setuptools.find_packages(),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires='>=3.6'
        )
