# Automated Resume Screening System (With Dataset)
A web app to help employers by analysing resumes and CVs, surfacing candidates that best match the position and filtering out those who don't.

## Description
Used recommendation engine techniques such as Collaborative , Content-Based filtering for fuzzy matching job description with multiple resumes.

## Prerequisites

# Software
* textract==1.6.3
* requests==2.22.0
* Flask==1.1.1
* gensim==3.8.0
* sklearn==0.0
* PyPDF2==1.26.0
* autocorrect==0.4.4
* nltk==3.4.5
* contractions==0.0.21
* textsearch==0.0.17
* inflect==2.1.0
* numpy==1.17.2
* pdfminer.six==20181108
* Python 3.6.0 |Anaconda 4.3.0 (64-bit)|

# Dataset

* Link1 : https://s3.ap-south-1.amazonaws.com/codebyte-bucket/Resume%26Job_Descriptions.zip
* Mirror : https://drive.google.com/open?id=17M9oDPip5JFFFNJhDCBQKy8BMqoyxajU


## Running localhost

* Run `pip install -r requirements.txt` to install dependencies
* Simply run this command from root directory.
* Login Username :admin
        Password : whitetigers2018

```
python app.py

```

## Running using Docker
* Create the docker image running: `docker build -t arss .`

* Run the container: `docker run -it -p 5000:5000 arss`

## Author

# @CodeByte
