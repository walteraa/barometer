FROM ubuntu

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get -y install python-pip

WORKDIR /BootTimeAgent

ADD ./agents/BootTimeAgent /BootTimeAgent

COPY ./config/examples/environment.conf /BootTimeAgent

RUN pip install python-novaclient==7.1.0

ARG BAR_CONFIG=/BootTimeAgent/environment.conf
ENV BAR_CONFIG ${BAR_CONFIG}

CMD ["python", "main.py"]
