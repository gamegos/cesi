FROM python:3.7.2

LABEL maintainer="whatever@whatever.com"

# Enter version to install
ENV CESI_VERSION 2.7.1
ENV SETUP_PATH /var/opt/cesi
ENV CESI_CONFIG_PATH /etc/cesi.conf.toml

# Add cesi user/group to run gunicorn as non root
RUN groupadd -r cesi && useradd -r -s /sbin/nologin -g cesi cesi

WORKDIR ${SETUP_PATH}
RUN wget --quiet --output-document cesi.tar.gz https://github.com/gamegos/cesi/releases/download/v${CESI_VERSION}/cesi-extended.tar.gz \
    && tar -xzf cesi.tar.gz \
    && rm cesi.tar.gz \
    && chown -R cesi:cesi /var/opt/cesi

WORKDIR ${SETUP_PATH}
RUN apt-get update \
    && pip3 install -r requirements.txt \
    && pip3 install gunicorn

COPY defaults/cesi.conf.toml ${CESI_CONFIG_PATH}

WORKDIR ${SETUP_PATH}/cesi
EXPOSE 5000
USER cesi
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "--log-level", "info", "--reload", "wsgi:app" ]