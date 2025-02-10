FROM python:3.12
# here i pick python:3.xx instead of our base on ACR
# becuase the base on ACR is amd64
# then arm machines will have issues
ENV PYTHONUNBUFFERED 1
# to prevent run as root
ARG DOCKER_HOME="/opt/motiong"
ARG DOCKER_CODE="/opt/motiong/code"
ARG DOCKER_GROUP="motiong"
ARG DOCKER_USER="motiong"
ARG DOCKER_UID=5000

ENV ZSH="/opt/motiong/.oh-my-zsh"

WORKDIR ${DOCKER_CODE}

RUN groupadd -g ${DOCKER_UID} ${DOCKER_GROUP} \
    && useradd -r -u ${DOCKER_UID} -g ${DOCKER_GROUP} -d ${DOCKER_HOME} ${DOCKER_USER} \
    && chown -R ${DOCKER_USER}:${DOCKER_GROUP} ${DOCKER_HOME}

RUN apt-get update && \
    apt-get install -y libgl1 && \
    apt-get install -y curl && \
    apt-get install -y git && \
    apt-get install -y postgresql-client && \
    apt-get install -y openssh-client && \
    pip install --upgrade pip && \
    pip install poetry==1.8.3 && \
    poetry config virtualenvs.create false

# Install zsh, omz, plugins
RUN apt-get install -y zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Install yq (for yaml and json)
RUN wget https://github.com/mikefarah/yq/releases/download/v4.40.7/yq_linux_amd64 -O /usr/bin/yq && \
    chmod +x /usr/bin/yq

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# will add examples to install our own python modules
# maybe not via git+ssh, well we will decide later if we have any
RUN mkdir ${DOCKER_HOME}/.ssh && \
    chown -R ${DOCKER_USER} ${DOCKER_HOME}/.ssh && \
    ssh-keyscan github.com >> ${DOCKER_HOME}/.ssh/known_hosts

# Configure git
RUN git config --global --add safe.directory /opt/motiong/code
RUN git config --global user.email "zhengzhe@outlook.com"
RUN git config --global user.name "Zheng Zhe Reggie"

ENV PATH "$PATH:/opt/motiong/.local/bin"
ENV PYTHONPATH=.

USER ${DOCKER_USER}
ENTRYPOINT [ "/bin/sh", "-c" ]