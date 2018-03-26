FROM python:3.3

MAINTAINER walter.arruda.alves@gmail.com
# -- Install Pipenv:
#RUN set -ex && pip install pipenv --upgrade
RUN set -ex && pip install git+git://github.com/pypa/pipenv.git@8378a1b104f2d817790a05da370bef0a1b00f452

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app


COPY Pipfile Pipfile
#COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install  --system

COPY . /app

EXPOSE 9000

CMD ["python", "app.py"]
