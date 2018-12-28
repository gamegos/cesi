FROM python:3.7

ENV INSTALL_PATH /opt/cesi
ENV CESI_CONFIG_PATH /etc/cesi.conf.toml

WORKDIR $INSTALL_PATH
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY defaults/cesi.conf.toml $CESI_CONFIG_PATH

COPY . .

WORKDIR $INSTALL_PATH/cesi

EXPOSE 5000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "--log-level", "info", "--reload", "wsgi:app" ]
