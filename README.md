# Klaxer - A webhook alert proxy

*Klaxon, Klax-off*

## Requirements

Python 3.6 only. Try to minimize deps on external daemons/processes.

## Docker Environment

Build the docker image:
`docker build -t klaxer .`

Run the container:
`docker run --name klaxer_instance -i -t klaxer`
