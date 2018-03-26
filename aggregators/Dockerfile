FROM python:3.6.4

MAINTAINER walter.arruda.alves@gmail.com
# -- Install Pipenv:
#RUN set -ex && pip install pipenv --upgrade
RUN pip install git+git://github.com/pypa/pipenv.git@8378a1b104f2d817790a05da370bef0a1b00f452


# -- Install Application into container:
RUN mkdir /app

WORKDIR /app

COPY Pipfile Pipfile
#ONBUILD COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system

COPY . /app

EXPOSE 8080

ENTRYPOINT python src/aggregator.py
