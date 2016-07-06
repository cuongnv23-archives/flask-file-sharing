FROM python:2.7-alpine
MAINTAINER "https://github.com/learningpython08"
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /opt/app
WORKDIR /opt/app
RUN find . \( -name __pycache__ -o -name '*.pyc' \) -delete
RUN tox
EXPOSE 8080
CMD ["python", "run.py"]
