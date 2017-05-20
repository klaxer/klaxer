# Klaxer - A webhook alert proxy

*Klaxon, Klax-off*

## Requirements

Python 3.6 only. Try to minimize deps on external daemons/processes.

## Docker Environment

Build the docker image:
`docker build -t klaxer .`

Run the container:
`docker run -v $(pwd):/klaxer --name klaxer_instance -i -t klaxer`

Run some python:
`python -c "import klaxer.api"`
