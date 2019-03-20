FROM ubuntu:16.04
MAINTAINER Daniel Kirstenpfad <bietiekay@gmail.com>

COPY myfitnesspal /myfitnesspal/

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Update & install packages & cleanup afterwards
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install \
        wget \
        mosquitto-clients \
        python-setuptools \
        python-six \
        python-requests \
        python-libxslt1 \
        python-lxml \
        python && \
    apt-get clean autoclean && \
    apt-get autoremove && \
    rm -rf /var/lib/{apt,dpkg,cache,log}

WORKDIR "/myfitnesspal"
RUN python setup.py install

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/mfp-cron
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/mfp-cron
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
 
# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
