# ukg-mira
MIRA - Multifunctional Intelligent Robotic Assistant
Mira is a versatile virtual assistant, integrating with Outlook and simplifying task scheduling and meeting organization.

MIRA is born as part of 48hrs hackathon held at our company on 11th - 13th July, 2023. Contributors: harsh.pundir@ukg.com harshul.gupta@ukg.com bismeet.chawla@ukg.com saiswathi.tella@ukg.com and irfan.sheik@ukg.com

[Demo Video](https://kronos.sharepoint.com/:v:/r/sites/48Hours/Project%20Video%20Submission/July%202023/MIRA-Demo-Submission.mp4?csf=1&web=1&e=A0FoyX)

## Introduction

### What we did?

Enhanced the meeting or shift scheduling experience for the Ukrewers, UKG Customers and their employees by leveraging the power of LLMs and providing the below features:

MIRA leverages AI allowing users to use natural language _(via text or audio)_ to express their scheduling needs in any order and also allows the users to go out of domain and ask things like how is the weather today in Delhi, get answer and come back to the scheduling need.

MIRA solution design is a combination of embeddings, prompt engineering and LLMs to achieve efficient natural languge scheduling query processing. It is implemented using the "microsoft teams apps", "langchain" and "streamlit" frameworks and employs a multi-layer approach for processing. MIRA is integrated with UKG Flex APIs and Microsoft Outlook Calendar APIs.


Basic features:

* Allow the user to ask queries in natural language through text or audio


Advanced features:

* Integration with Microsoft Outlook APIs - Natural way of viewing/scheduling the meetings in the Microsfot Outlook Calender
* Integration with Workforce Dimensions using UKG Flext - Natural way of viewing/scheduling the shfits, opting for an open shift etc.,

### Why we did it?

Meeting or shift scheduling using existing tools is extremely painful for reasons. These tools often lack user-friendly interfaces, making it challenging to navigate and input information efficiently. They lack flexibility to accommodate complex scheduling requirements or handle unexpected changes. Moreover, manual entry and coordination lead to human errors, resulting in confusion and scheduling conflicts. Additionally, limited collaboration features make it difficult for teams to coordinate and communicate effectively. The overall inefficiency of these tools hinders productivity and can lead to missed appointments, increased workload, and decreased team morale.
This just adds a lot more burden on the Frontline workers.
But using the current generation AI, we see there is an immense opportunity to solve some of these problems.

### How we did it?

#### Solution Development - Thinking Framework

![Solution-Development (3)](https://github.com/irfan-ukg/ukg-mira/assets/117180317/6e113250-bf7c-41e9-852b-ad5a46d2ad25)


#### Leveraging Co-Pilot
<img width="1512" alt="Screenshot 2023-07-13 at 7 47 48 PM" src="https://github.com/irfan-ukg/ukg-mira/assets/117180317/a1e99809-7bae-4ab0-bd72-ccb9549da619">


#### Leveraging Chat GPT

<img width="1497" alt="Screenshot 2023-07-13 at 7 50 19 PM" src="https://github.com/irfan-ukg/ukg-mira/assets/117180317/23afcd37-7131-430e-b08c-cc8814815fe1">


#### Pushing the limits

<img width="1512" alt="Screenshot 2023-07-13 at 12 25 06 AM" src="https://github.com/irfan-ukg/ukg-mira/assets/117180317/06b18eed-91dd-416e-ae50-cfa53ee1753b">



## Implemenation Design

![Basic-Mira (1)](https://github.com/irfan-ukg/ukg-mira/assets/117180317/28f15fb5-79c0-4df2-93d7-2c2941657408)



## Future Integration
![FutureMira](https://github.com/irfan-ukg/ukg-mira/assets/117180317/14002b0b-8922-4526-a51f-1d86a84ffa69)


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


### Authentication For Flex API
Flex APIs do not support application to application authentication, so currenlty users need to login once into the MIRA with their UKG Dimensions credintials. In future a federated login point will be implemented to use the same authentication for both Microsoft Teams and Flex APIs
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

