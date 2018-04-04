FROM ubuntu

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get -y install python-pip

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install python-novaclient==7.1.0

CMD ["python", "main.py"]
