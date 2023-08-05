import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mup",
    version="0.0.0",
    author="GYAIL",
    author_email="edward.hu@microsoft.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/mup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
