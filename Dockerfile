FROM amazon/aws-lambda-python:3.8

MAINTAINER Aaron Mamparo

COPY Pipfile.lock .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt --compile -t ${LAMBDA_TASK_ROOT}
RUN touch ${LAMBDA_TASK_ROOT}/__init__.py
COPY src ${LAMBDA_TASK_ROOT}/src
RUN ls -l ${LAMBDA_TASK_ROOT}

CMD ['src.main.lambda_handler']