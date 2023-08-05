import setuptools

requirements = []
try:
    with open("./README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    with open("./requirements.txt", "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()
except Exception as e:
    raise e

setuptools.setup(
    name="api_scene",
    version="1.0.0",
    author="Mohammad Matin Parvin",
    author_email="mohammad123matin@gmail.com",
    description="unofficial API for Subscene",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mmp-8001/subscene_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
