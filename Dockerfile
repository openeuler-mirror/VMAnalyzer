FROM openeuler-24.03-lts:latest

RUN yum install -y python3 python3-pip python3-libvirt gcc python3-devel libvirt-devel
WORKDIR /app
COPY . /app
RUN pip3 install -e .
ENTRYPOINT ["vm-analyzer-agent"]
CMD []
