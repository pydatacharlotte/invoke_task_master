from python:3.8

RUN pip install invoke

COPY tasks.py .

ENTRYPOINT ["python", "-c", "print('Running gunicorn to serve the api.')"]

