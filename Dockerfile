FROM python:3.6.5-alpine
MAINTAINER whitefirer

RUN apk add --no-cache alpine-sdk autoconf automake libtool
RUN apk add --update graphviz ttf-ubuntu-font-family
COPY ./ /src/
WORKDIR /src
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
ENV MODULE_ID="hb"
ENV PORT="9102"
EXPOSE 9102

ENTRYPOINT ["gunicorn", "--config", "gunicorn.ini", "run:app"]