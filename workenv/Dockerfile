FROM debian:stable

RUN \
    apt-get update && \
    apt-get install -y python3 python3-pip git tmux nano vim sudo

# Create user
RUN useradd -ms /bin/bash lab
RUN echo "lab ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER lab
WORKDIR /home/lab

# Python requirements
COPY ./requirements.txt ./requirements.txt
RUN \
    pip3 install -r requirements.txt

RUN mkdir -p /home/lab/workdir

ENTRYPOINT ["/bin/bash"]
