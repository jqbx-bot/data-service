FROM amazon/aws-lambda-python:3.8

RUN echo ${LAMBDA_TASK_ROOT}

COPY Pipfile.lock .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pipenv lock --requirements > requirements.txt
RUN cat requirements.txt
RUN pip install -r requirements.txt
COPY src/ ${LAMBDA_TASK_ROOT}

CMD ['src.main.lambda_handler']