FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ansible \
    openssh-client \
    python3 \
    python3-pip

RUN ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""

RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

CMD ["sh", "-c", "cp /root/.ssh/id_rsa.pub /keys/master.pub; tail -f /dev/null"]
