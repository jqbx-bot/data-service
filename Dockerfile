FROM amazon/aws-lambda-python:3.8

MAINTAINER Aaron Mamparo

RUN mkdir -p ${LAMBDA_TASK_ROOT}/src

COPY src/. ${LAMBDA_TASK_ROOT}/src

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt --compile -t ${LAMBDA_TASK_ROOT}

RUN ls -l ${LAMBDA_TASK_ROOT}

CMD ['src.main.lambda_handler']