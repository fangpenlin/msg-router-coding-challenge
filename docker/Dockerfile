FROM phusion/baseimage:0.9.15
MAINTAINER Victor Lin <bornstub@gmail.com>

# install dependencies
RUN apt-get -qq update && \
    apt-get install -y \
        python \
        python-dev \
        python-pip \
        libpq-dev \
        libffi-dev \
        libpcre3-dev \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN easy_install -U setuptools
RUN pip install -U pip

# extra python packages
RUN pip install uwsgi newrelic ipython ipdb raven

# add uwsgi service
RUN mkdir /etc/service/uwsgi
ADD uwsgi.sh /etc/service/uwsgi/run
RUN chmod +x /etc/service/uwsgi/run

# install packages
ADD msg_router.tar /srv/msg_router/
RUN pip install -e /srv/msg_router/

ADD version.txt /srv/msg_router/msg_router/version.txt
ADD git_revision.txt /srv/msg_router/msg_router/git_revision.txt

VOLUME ["/var/log"]
EXPOSE 80
ENTRYPOINT ["/sbin/my_init"]
