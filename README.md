Here is a summarized version of the steps taken to set up the BetterSpeaker environment using conda and pip:


Make sure you have Conda, Python and Docker installed:
## Create the Conda Enviornment:
Make the environment
```bash
conda create --name BetterSpeak
```
## Activate the Conda Environment:

Initialize the conda environment:
```bash
conda init
```

Activate betterspeak conda environment:
```bash
conda activate betterspeak
```

## Install pip using Conda:

Copy code
``` bash
conda install pip
```
This results in the installation of various dependencies including pip, python, setuptools, and other system packages.

## Install Packages from requirements.txt File Using pip:

```bash
pip install -r requirements.txt
```

Installation begins for packages listed in the requirements.txt file, such as streamlit.

## Install Nvidia API Riva NIM

Riva ASR NIM APIs provide easy access to state-of-the-art automatic speech recognition (ASR) models, capable of transcribing spoken English with exceptional accuracy. It is a XXL version of the FastConformer-CTC model. Riva ASR NIM models are built on the NVIDIA software platform, incorporating CUDA, TensorRT, and Triton to offer out-of-the-box GPU acceleration.

Copy Code and get API Key
Install Riva Python Client
```bash
$ pip install -r https://raw.githubusercontent.com/nvidia-riva/python-clients/main/requirements.txt
$ pip install --force-reinstall git+https://github.com/nvidia-riva/python-clients.git
```

Download Python Client. Make sure this repo is inside the repo of BetterSpeak
```bash
$ git clone https://github.com/nvidia-riva/python-clients.git
```

## Credits:

Eye Tracking Repo: https://github.com/antoinelame/GazeTracking
Computer Vision with Streamlit: https://www.youtube.com/watch?v=wyWmWaXapmI


