import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


install_requirements = """
aiohttp==3.7.4.post0
async-timeout==3.0.1
attrs==21.2.0
bleach==4.1.0
build==0.7.0
certifi==2021.5.30
chardet==4.0.0
colorama==0.4.4
cycler==0.10.0
dateparser==1.0.0
docutils==0.17.1
idna==2.10
importlib-metadata==4.8.1
joblib==1.1.0
keyring==23.2.1
kiwisolver==1.3.2
matplotlib==3.4.3
multidict==5.1.0
numpy==1.21.2
packaging==21.0
pandas==1.3.3
pep517==0.11.0
Pillow==8.3.2
pkginfo==1.7.1
Pygments==2.10.0
pyparsing==2.4.7
python-binance==1.0.12
python-dateutil==2.8.1
pytz==2021.1
pywin32-ctypes==0.2.0
readme-renderer==30.0
regex==2021.4.4
requests==2.25.1
requests-toolbelt==0.9.1
rfc3986==1.5.0
scikit-learn==1.0
scipy==1.7.1
seaborn==0.11.2
six==1.16.0
sklearn==0.0
threadpoolctl==3.0.0
tomli==1.2.1
torch==1.9.1
tqdm==4.62.3
twine==3.4.2
typing-extensions==3.10.0.0
tzlocal==2.1
ujson==4.0.2
urllib3==1.26.5
webencodings==0.5.1
websockets==9.1
wincertstore==0.2
yarl==1.6.3
zipp==3.6.0
""".split('\n')

setuptools.setup(
    name="piston-v-taper",
    version="0.1.0",
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
    include_package_data=True,
    install_requires=install_requirements,
    python_requires=">=3.6",
)
