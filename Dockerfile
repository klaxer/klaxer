FROM python:3.6
MAINTAINER Kevin Dwyer

RUN pip install flask==0.12.2 zappa==0.42.0

ENTRYPOINT ["bash"]
#CMD ["-c", "python"]
