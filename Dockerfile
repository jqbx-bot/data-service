FROM amazon/aws-lambda-python:3.8

MAINTAINER Aaron Mamparo

COPY Pipfile.lock .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt -t .
COPY src src

RUN ls -l .

CMD ['src.main.lambda_handler']