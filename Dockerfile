FROM centos:centos8
RUN yum install -y python2 skopeo && ln -s /usr/bin/python2.7 /usr/bin/python \
    && yum clean all && mkdir /app
WORKDIR /app
ADD syncer.py /app/syncer.py
ADD README.md /app/README.md
ENTRYPOINT ["/bin/sh"]
