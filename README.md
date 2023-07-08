# ukg-mira
MIRA - Multifunctional Intelligent Robotic Assistant
Mira is a versatile virtual assistant, integrating with Outlook and simplifying task scheduling and meeting organization.

MIRA is born as part of 48hrs hackathon held at our company on 11th - 13th July, 2023. Contributors: harsh.pundir@ukg.com harshul.gupta@ukg.com bismeet.chawla@ukg.com saiswathi.tella@ukg.com and irfan.sheik@ukg.com

## Implemenation Design

![Basic-Mira](https://github.com/irfan-ukg/ukg-mira/assets/117180317/6f961011-bd5f-4d80-afcf-ab5fc70039d5)

## Getting Started with Development

### Prerequisites

1. Python 3.6 or higher
2. For Mac OS
>  brew install flac
The above library is required to read audio files of multiple formats including ".wav"

To install the required libraries, run:

```bash
pip install -r requirements.txt
```

### Known Bugs - Mitigation
While using `pyttsx3` for the text to speech translation. We will see an error "AttributeError: 'super' object has no attribute 'init'".

this turns out to be a little tricky. and this is a workaround! hope works for you.

Under the hood, this module pyttsx3 uses PyObjC as a bridge between Python and Objective-C.

Step 1: Check that pyobjc is installed(pip show pyobjc), if not install as pip install pyobjc.
Step 2: open this file /usr/local/lib/python3.11/site-packages/pyttsx3/drivers/nsss.py and change the following:

#self = super(NSSpeechDriver, self).init() comment this line , and add the following
self = objc.super(NSSpeechDriver, self).init()

[Source for the bug mitigation](https://stackoverflow.com/questions/76434535/attributeerror-super-object-has-no-attribute-init)

### Setting up API keys

You need to obtain API keys for the following services:

1. OpenAI
2. Microsoft Graph

TBD: Setting up the keys in the respective env variables

### Run

Run the program using the following command:

```bash
python main.py
```

### Useful Commands

> conda remove -n mira-ukg --all
> conda create --name=mira-ukg python=3.10