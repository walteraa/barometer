FROM ubuntu

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get -y install python-pip

WORKDIR /BootTimeAgent

ADD ./agents/BootTimeAgent /BootTimeAgent

RUN pip install python-novaclient==7.1.0

ENV OS_AUTH_URL ${OS_AUTH_URL}
ENV OS_USERNAME ${OS_USERNAME}
ENV OS_PASSWORD ${OS_PASSWORD}
ENV OS_PROJECT_ID ${OS_PROJECT_ID}
ENV OS_USER_DOMAIN_NAME ${OS_USER_DOMAIN_NAME}

CMD ["python", "main.py"]
