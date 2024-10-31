Here is a summarized version of the steps taken to set up the BetterSpeaker environment using conda and pip:

## Activate the Conda Environment:

sh
Copy code
```
conda activate betterspeak
```
Attempted to use conda to install from requirements, but the usage was incorrect.
sh
Copy code
```
conda install -r requirements
```

## Install pip using Conda:

Copy code
```
conda install pip
```
This results in the installation of various dependencies including pip, python, setuptools, and other system packages.
User consented to the installation of 36.5 MB of packages.
## Install Packages from requirements.txt File Using pip:

sh
Copy code
```
pip install -r requirements.txt
```
Installation begins for packages listed in the requirements.txt file, such as streamlit.
