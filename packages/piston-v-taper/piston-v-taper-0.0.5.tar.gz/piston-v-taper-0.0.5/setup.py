import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piston-v-taper",
    version="0.0.5",
    author="Benjamin Alheit",
    author_email="alhben001@myuct.ac.za",
    description="A trained machine learning model for predicting the force due to contact between a deformable end cap and a taper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenAlheit/piston-vs-taper",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
