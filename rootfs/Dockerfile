FROM registry.drycc.cc/drycc/base:bullseye as build-app

ADD web /web
WORKDIR /web

ENV NODE_VERSION="16.14.2"

RUN install-stack node $NODE_VERSION && . init-stack \
  && npm install --global yarn \
  && yarn install \
  && yarn build

FROM registry.drycc.cc/drycc/base:bullseye

ENV DRYCC_UID=1001 \
  DRYCC_GID=1001 \
  DRYCC_HOME_DIR=/workspace \
  PYTHON_VERSION="3.10.4"

RUN groupadd drycc --gid ${DRYCC_GID} \
  && useradd drycc -u ${DRYCC_UID} -g ${DRYCC_GID} -s /bin/bash -m -d ${DRYCC_HOME_DIR}

COPY requirements.txt ${DRYCC_HOME_DIR}/requirements.txt

RUN buildDeps='gcc rustc cargo libffi-dev musl-dev libldap2-dev libsasl2-dev'; \
    install-packages $buildDeps \
  && install-stack python $PYTHON_VERSION && . init-stack \
  && python3 -m venv ${DRYCC_HOME_DIR}/.venv \
  && source ${DRYCC_HOME_DIR}/.venv/bin/activate \
  && pip3 install --disable-pip-version-check --no-cache-dir -r ${DRYCC_HOME_DIR}/requirements.txt \
  && chown -R ${DRYCC_UID}:${DRYCC_GID} ${DRYCC_HOME_DIR} \
  # set env
  && echo "source ${DRYCC_HOME_DIR}/.venv/bin/activate" >> /opt/drycc/python/profile.d/python.sh \
  # cleanup
  && scanelp ${DRYCC_HOME_DIR}/.venv/lib > runtime.txt \
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

USER ${DRYCC_UID}

COPY --chown=${DRYCC_UID}:${DRYCC_GID} . ${DRYCC_HOME_DIR}
COPY --chown=${DRYCC_UID}:${DRYCC_GID} --from=build-app /web/dist ${DRYCC_HOME_DIR}/web/dist

WORKDIR ${DRYCC_HOME_DIR}
CMD ["bin/boot"]
EXPOSE 8000
