# ukg-mira
MIRA - Multifunctional Intelligent Robotic Assistant
Mira is a versatile virtual assistant, integrating with Outlook and simplifying task scheduling and meeting organization.

MIRA is born as part of 48hrs hackathon held at our company on 11th - 13th July, 2023. Contributors: harsh.pundir@ukg.com harshul.gupta@ukg.com bismeet.chawla@ukg.com saiswathi.tella@ukg.com and irfan.sheik@ukg.com


## Introduction

### What we did?

Enhanced the meeting or shift scheduling experience for the Ukrewers, UKG Customers and their employees by leveraging the power of LLMs and providing the below features:

MIRA solution design is a combination of embeddings, prompt engineering and LLMs to achieve efficient natural languge scheduling query processing. It is implemented using the "microsoft teams apps", "langchain" and "streamlit" frameworks and employs a multi-layer approach for processing. MIRA is integrated with UKG Flex APIs and Microsoft Outlook Calendar APIs.


Basic features:

* Allow the user to ask queries in natural language through text or audio


Advanced features:

* Integration with Microsoft Outlook APIs - Natural way of viewing/scheduling the meetings in the Microsfot Outlook Calender
* Integration with Workforce Dimensions using UKG Flext - Natural way of viewing/scheduling the shfits, opting for an open shift etc.,

### Why we did it?

Meeting or shift scheduling using existing tools is extremely painful for reasons. These tools often lack user-friendly interfaces, making it challenging to navigate and input information efficiently. They lack flexibility to accommodate complex scheduling requirements or handle unexpected changes. Moreover, manual entry and coordination lead to human errors, resulting in confusion and scheduling conflicts. Additionally, limited collaboration features make it difficult for teams to coordinate and communicate effectively. The overall inefficiency of these tools hinders productivity and can lead to missed appointments, increased workload, and decreased team morale.
But using the current generation AI, we see there is an immense opportunity to solve some of these problems.

### How we did it?

#### Solution Development - Thinking Framework

![Solution-Development (3)](https://github.com/irfan-ukg/ukg-mira/assets/117180317/8bda2f75-e0fa-4c9a-929c-37cd82528b43)

#### Leveraging Co-Pilot
<img width="1512" alt="Screenshot 2023-07-13 at 7 47 48 PM" src="https://github.com/irfan-ukg/ukg-mira/assets/117180317/90040e92-5a1c-4abb-9825-53030c520b5e">

#### Leveraging Chat GPT

<img width="1497" alt="Screenshot 2023-07-13 at 7 50 19 PM" src="https://github.com/irfan-ukg/ukg-mira/assets/117180317/ff77e30f-788c-4ee0-8205-10979776d91c">

#### Pushing the limits
<img width="1512" alt="Screenshot 2023-07-13 at 12 25 06 AM" src="https://github.com/irfan-ukg/ukg-mira/assets/117180317/08036689-9eea-47f2-b927-81ea5fa5a885">



## Implemenation Design

![Basic-Mira](https://github.com/irfan-ukg/ukg-mira/assets/117180317/6f961011-bd5f-4d80-afcf-ab5fc70039d5)


![FutureMira](https://github.com/irfan-ukg/ukg-mira/assets/117180317/b429f6ee-c5ab-477a-9fa7-143387a3b074)

## Getting Started with Development

### Prerequisites

1. Python 3.6 or higher

To install the required libraries, run:

```bash
pip install -r requirements.txt
```
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
