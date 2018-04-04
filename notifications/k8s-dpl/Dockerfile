FROM python:3.6.4

MAINTAINER maysa.macedo95@gmail.com
# -- Install Pipenv:
RUN pip install git+git://github.com/pypa/pipenv.git@8378a1b104f2d817790a05da370bef0a1b00f452

# -- Install Application into container:
RUN mkdir /app

WORKDIR /app

COPY Pipfile Pipfile
#COPY Pipfile.lock Pipfile.lock

RUN pipenv install --deploy --system

COPY . /app

ENTRYPOINT python main.py
