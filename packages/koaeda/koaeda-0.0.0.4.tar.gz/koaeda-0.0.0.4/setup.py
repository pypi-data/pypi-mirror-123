import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="koaeda",
    version="0.0.0.4",
    license="MIT",
    author="decyma",
    author_email="soos3121@gmail.com",
    description="Using Korean Language A Easier Data Augmentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kangsukmin/KoAEDA",
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
