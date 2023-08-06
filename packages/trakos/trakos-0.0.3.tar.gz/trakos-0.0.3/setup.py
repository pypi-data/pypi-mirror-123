import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trakos",
    version="0.0.3",
    author="king-trakos",
    author_email="trakosiraq@gmail.com",
    description="python Package To trakos Bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhdeiiking/trakos",
    project_urls={
        "Bug Tracker": "https://github.com/mhdeiiking/trakos/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
