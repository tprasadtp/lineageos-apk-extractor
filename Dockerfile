FROM python:3.7-slim-buster

LABEL maintainer="Prasad Tengse <tprasadtp@users.noreply.github.com"

ENV TRAVIS_BUILD_NUMBER "NA"
ENV FORCE_GH_RELEASE "true"
RUN apt-get update -qq \
    && apt-get install -y -qq --no-install-recommends brotli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /lineage
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && mkdir -p /lineage/build \
    && mkdir -p /lineage/metadata \
    && rm -rf /tmp/*.txt

COPY . .

ENTRYPOINT ["/bin/bash"]
