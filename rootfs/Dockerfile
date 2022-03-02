FROM docker.io/drycc/base:bullseye  as build-app

ADD web /app
WORKDIR /app

ENV NODE_VERSION="16.14.0"

RUN install-stack node $NODE_VERSION && . init-stack \
  && npm install --global yarn \
  && yarn install \
  && yarn build

FROM docker.io/drycc/base:bullseye

RUN adduser --system \
	--shell /bin/bash \
	--disabled-password \
	--home /app \
	--group \
	drycc

ENV PYTHON_VERSION="3.10.2"
COPY requirements.txt /app/requirements.txt

RUN buildDeps='gcc rustc cargo libffi-dev musl-dev libldap2-dev libsasl2-dev'; \
    install-packages $buildDeps \
  && install-stack python $PYTHON_VERSION && . init-stack \
  && python3 -m venv /app/.venv \
  && source /app/.venv/bin/activate \
  && pip3 install --disable-pip-version-check --no-cache-dir -r /app/requirements.txt \
  # cleanup
  && scanelp /app/.venv/lib > runtime.txt \
  && apt-get purge -y --auto-remove $buildDeps \
  && install-packages $(< runtime.txt) \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf \
        /usr/share/doc \
        /usr/share/man \
        /usr/share/info \
        /usr/share/locale \
        /var/lib/apt/lists/* \
        /var/log/* \
        /var/cache/debconf/* \
        /etc/systemd \
        /lib/lsb \
        /lib/udev \
        /usr/lib/`echo $(uname -m)`-linux-gnu/gconv/IBM* \
        /usr/lib/`echo $(uname -m)`-linux-gnu/gconv/EBC* \
  && mkdir -p /usr/share/man/man{1..8}

COPY . /app
COPY --from=build-app /app/dist /app/web/dist

USER drycc
WORKDIR /app
CMD ["PATH=/app/.venv/bin:\$PATH", "/app/bin/boot"]
EXPOSE 8000
