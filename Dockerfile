FROM python:3.6-slim-stretch

LABEL maintainer Prasad Tengse <code@prasadt.com>

ENV TRAVIS_BUILD_NUMBER NA
ENV FORCE_GH_RELEASE True
RUN apt-get update -qq && apt-get install -y -qq brotli

WORKDIR /lineage
COPY . /lineage

RUN pip install -r requirements.txt && chmod +x *.py *.sh

CMD ["/bin/bash"]
