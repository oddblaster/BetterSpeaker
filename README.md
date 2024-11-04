Here is a summarized version of the steps taken to set up the BetterSpeaker environment using conda and pip:

## Prerequisites:
Make sure you have Python version 3.11.7 installed. Also make sure you have the latest version of Conda installed and Visual Studio C++
cmake. Here are the link to their installations:

https://www.python.org/downloads/release/python-3117/c
https://anaconda.org/anaconda/conda

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










## Make the Nvidia API Call

Riva ASR NIM APIs provide easy access to state-of-the-art automatic speech recognition (ASR) models, capable of transcribing spoken English with exceptional accuracy. It is a XXL version of the FastConformer-CTC model. Riva ASR NIM models are built on the NVIDIA software platform, incorporating CUDA, TensorRT, and Triton to offer out-of-the-box GPU acceleration.

Install the Riva Python Client
``` bash
$ pip install -r https://raw.githubusercontent.com/nvidia-riva/python-clients/main/requirements.txt
$ pip install --force-reinstall git+https://github.com/nvidia-riva/python-clients.git
```

Download the Python client code
```bash
git clone https://github.com/nvidia-riva/python-clients.git
```

Run the python client
``` bash
$ python python-clients/scripts/asr/transcribe_file.py \
    --server grpc.nvcf.nvidia.com:443 --use-ssl \
    --metadata function-id "1598d209-5e27-4d3c-8079-4751568b1081" \
    --metadata "authorization" "Bearer $API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC" \
    --language-code en-US \
    --input-file <path_to_audio_file>
```
## Credits
Here are all the resources that helped me build this application
https://www.youtube.com/watch?v=wyWmWaXapmI