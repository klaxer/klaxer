FROM python:3.6
MAINTAINER Kevin Dwyer

# Add Klaxer requirements to container
ADD requirements.txt /etc/klaxer/

# Install dependencies
RUN pip install -r /etc/klaxer/requirements.txt

ENV PYTHONPATH=/klaxer

ENTRYPOINT ["bash"]
#CMD ["-c", "python"]
