FROM node:16-alpine3.14 as build-app

ADD web /app
WORKDIR /app

RUN npm install \
  && yarn build

FROM docker.io/library/python:3.9-alpine

COPY requirements.txt /app/requirements.txt

RUN apk add --update --virtual .build-deps \
    postgresql-dev \
    gcc \
    libffi-dev \
    musl-dev \
    openldap-dev \
    openssl-dev \
    cargo \
    rust \
  && python3 -m venv /app/.venv \
  && source /app/.venv/bin/activate \
  && pip3 install --disable-pip-version-check --no-cache-dir -r /app/requirements.txt \
  && runDeps="$( \
    scanelf --needed --nobanner --format '%n#p' --recursive /app/.venv \
    | tr ',' '\n' \
    | sort -u \
    | awk 'system("[ -e /app/.venv/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
    )" \
  && apk add --update --virtual .passport-rundeps \
    $runDeps \
    ca-certificates \
    su-exec \
    bash \
    shadow \
  && apk del .build-deps

COPY . /app
COPY --from=build-app /app/dist /app/web/dist

ENTRYPOINT ["/app/bin/entrypoint"]

WORKDIR /app
CMD ["/app/bin/boot"]
EXPOSE 8000
