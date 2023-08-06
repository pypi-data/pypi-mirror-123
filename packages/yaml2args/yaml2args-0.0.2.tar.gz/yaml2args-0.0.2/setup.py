import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yaml2args",
    version="0.0.2",
    author="LOOKCC",
    author_email="wang1397665447@gmail.com",
    description="A simple pkg to update your yaml configs to args",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LOOKCC/Yaml2args",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
