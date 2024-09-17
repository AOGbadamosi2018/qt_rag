
<!--- BADGES: START --->
![Python-Badge](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Streamlit-Badge](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Docker-Badge](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
<!--- BADGES: END --->

# Financial App QA assitant

A Retrieval-Augmented Generation (RAG) application designed to assist in answering user queries about Quickteller(a financial app). This project integrates AI-based techniques to assist in issue resolution.


## Features  

- Answers commonly asked questions based on FAQ documents.

- Utilizes RAG architecture with **_ElasticSearch_** (for Vector Search).

- Added support to use Open Source models locally using **_Ollama_** and online using **_OpenAI_**.

- Monitoring support to view dashboards via Postgres integration.

  

## Table of Contents

  

- [Description](#description)

- [Features](#features)

- [Installation](#installation)

- [Usage](#usage)

- [Configuration](#configuration)

- [Contributing](#contributing)


  

## Description

  

### What is Quickteller?


Quickteller is a versatile online payment platform designed to simplify financial transactions for individuals and businesses. It allows users to perform a wide range of activities, such as:

Airtime Recharge: Easily top up your mobile phone.
Funds Transfer: Send money to other accounts.
Bill Payments: Pay for utilities, cable TV, internet subscriptions, and more.
Purchases: Buy flight tickets, pay for events, and shop online.

The platform is managed by Interswitch Nigeria Limited and is accessible via mobile apps, web browsers, and ATMs. It’s known for its user-friendly interface and extensive network of over 8,000 billers


### Business Problem

The company just released a new version of the app,improving several features and radically changing the UI. Both new and returning users have a lot of questions, this has led to customer support personnel being overwhelmed. 

In addition, some of the old users are having issues logging back into their accounts while a lot of the new users have questions about the apps features. 

This application was created to answer user queries based on two faq documents.

1. [The general company FAQ](https://www.interswitchgroup.com/faq/faq.html)
2. [The new app's FAQ](https://rebirth.quickteller.com/portal/faq/personal/)
  

### Prerequisites

- Docker

- Docker Compose

- Python 3.9+

  

## Installation

  

To set up this project locally, follow these steps:

  

1. Clone the repository:

```
git clone https://github.com/A0Gbadamosi2024/financial_app_qabot.git

cd project_isw/app
```


2. Set up a virtual environment (recommended):

```

python -m venv venv

source venv/bin/activate

```

- On windows
```
source venv\Scripts\activate
```


3. Install the required dependencies for the virtual environment(sentence transformers may require significant space):

```

pip install -r requirements.txt

```

  

#### Set Up Docker Compose

- Follow this [link](./setup-docs/docker-compose-installation-guide.md) to install `docker-compose`

  

## Usage


#### 0. Create a new ".env" file inside the "app" folder and copy the following details into it. - remember to add your open-ai-key

```
# PostgreSQL Configuration
POSTGRES_HOST=postgres
POSTGRES_DB=course_assistant
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
 
# Elasticsearch Configuration
# PostgreSQL Configuration
POSTGRES_HOST=postgres
POSTGRES_DB=course_assistant
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
 
# Elasticsearch Configuration
ELASTIC_URL_LOCAL=http://localhost:9200
ELASTIC_URL=http://elasticsearch:9200
ELASTIC_PORT=9200
 
# Ollama Configuration
OLLAMA_PORT=11434
 
# Streamlit Configuration
STREAMLIT_PORT=8501
 
# Other Configuration
MODEL_NAME=all-mpnet-base-v2
INDEX_NAME=course-questions
OPENAI_API_KEY = 'add_your_key'
```

  

#### 1. Start the docker-compose

- Make sure that you've access to run **`docker-compose`**

- Open a terminal and run the following

##### On Linux/Mac:

```

docker-compose up --build

```

  

##### On Windows:

Ensure Docker Desktop is installed. Open a terminal and run:

```

docker-compose up --build

```


* Don't close the terminal

#### 2. Confirm that the containers are running

  

-  ##### Via Docker Desktop

  

If you're using `Docker Desktop`, open it and make sure all the below containers are up and running.

  

1. grafana

2. postgres

3. elastic-search

4. Ollama

  

-  ##### Via Command line (lists all the docker containers)
Open another terminal and execute the below command.

```

docker ps -a

```

 - Copy the Ollama docker container id then run

'''
docker exec it <ollama_container> pull phi3
'''


## Ingesting the base 

#### (Optional) Manual Ingestion of data
> *Note:* 1. Remember to change the json file paths to the actual path the "isw_rebirth_faq_document.json" file is located.
> *Note:* 2. Run the prep.py file only after the docker containers are up and active.

 Run the following command in a terminal with your virtual environment activated and the location where the "prep.py" file is located.

- Below command will start creating the embeddings and pushing the vectors to elasticsearch.
```
python3 prep.py
```
or 

```
python prep.py

```

### Pull the LLM model through Ollama(may not be necessary since it is already done from the DockerFile)

- Exec into Ollama docker container to pull the required model.
> *Note:* As part of this project, I have used `phi3`. We try to pull the same using Ollama.

```
docker exec -it <Ollama-Container-ID> bash
```
```
ollama pull phi3
```


  
### Accessing the app

Once you're sure the setup is done. Visit the streamlit app on the exposed port specified in the docker compose file:

- On your favorite browser visit http://localhost:8501.
- - On your favorite browser visit http://localhost:3000. For the graphana app

- Upon visiting the page, you should see below screen.

![App UI screen](add link to app UI screen setup here)

  

### Accessing Grafana Monitoring Dashboard

> *Note*: Seen issue while accessing Grafana dashboard on Chrome. Please try different browsers if you get `Unauthorzied` error.

- On your favorite browser visit http://localhost:3000

- Upon visiting the page, if you're asked to enter credentials, it's defaulted to below ones:

```

username: admin

password: admin

```

Give a new password also as `admin`

- Once you successfully authenticate, you'll be taken to homescreen like this:


  

- On the left panel, click on `Dashboards` -> `My custom Grapana page`

- Your monitoring dashboard should look like this

>  *Note*: At first, there will be no data. As you begin using the app, all the monitoring dashboards will start to update.


  
  

## Contributing

  

Contributions to this project are welcome! Please follow these steps:

  

1. Fork the repository

2. Create a new branch: `git checkout -b feature-branch-name`

3. Make your changes and commit them: `git commit -m 'Add some feature'`

4. Push to the branch: `git push origin feature-branch-name`

5. Submit a pull request
