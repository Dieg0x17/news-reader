### Build and install packages
FROM python:3.9 as python

FROM python as python-build-stage

RUN apt-get -y update \
  && apt-get install --no-install-recommends -y \
  gettext \
  build-essential \
  postgresql-client \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /src/
WORKDIR /src
RUN pip install -r requirements.txt


FROM python as python-run-stage

RUN apt-get -y update \
  && apt-get install --no-install-recommends -y \
  gettext \
  postgresql-client \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


RUN groupadd -r newsreader && useradd -r -g newsreader newsreader

RUN mkdir -p /app /app/media /app/static && chown -R newsreader:newsreader /app/

COPY --from=python-build-stage /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=python-build-stage /usr/local/bin/ /usr/local/bin/

COPY /src/production /start
#COPY /src/develop /start
#COPY /src/tests /start

RUN chmod +x /start

WORKDIR /src/news

EXPOSE 8000
ENV PYTHONUNBUFFERED 1

#CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "news.asgi.gunicorn_worker.UvicornWorker", "news.asgi:application"]
CMD ["/start"]
