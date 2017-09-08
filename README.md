# Klaxer - A webhook alert proxy

*Klaxon, Klax-off*

## Requirements

Python 3.6 only. Try to minimize deps on external daemons/processes.

## Docker Environment/Development

Build the docker image:
`docker build -t klaxer .`

Run the container:
`docker run -v $(pwd):/klaxer --name klaxer_instance -i -t klaxer`
This will start the hug server.

To get a shell in the container:
`docker exec -it klaxer_instance bash`

## Local Development

Install Klaxer and its development dependencies with:
`pip install -e .[dev]`

Run the klaxer server:
`hug -f klaxer/api.py`

Run the simulator:
`python -m klaxer.simulator`

## Registration

Klaxer uses a simple registration system to assign API keys to users for metrics and authorization.

### Getting a Key
After running an instance of the API, you can register for an API key by `POST`ing to the `/user/register` endpoint. 

```json
{
	"email": "foo@foo2.com",
	"name": "foo"
}
```

In return, you'll get an API key. **Careful!** At present, you'll only get to see this once. Klaxer staff can help recover it at present if you lose it.

**Response**
```json
{
    "id": 10,
    "api_key": "eab230d3d41b466db422ac4be3b7251c"
}
```

### Viewing Your Profile

After registering for a key, you can use this key to make requests. To see information in your profile like the amount of calls you've made. You need to make a **GET** request to the endpoint `/user/me`, setting the `x-api-key` header to your API key you received at registration.

```json
{
    "user_id": 10,
    "name": "Klaxer Fan",
    "email": "coolperson@klaxerboi.com",
    "registered": true,
    "approved": false,
    "signup_date": "2017-07-01",
    "api_key": "eab230d3d41b466db422ac4be3b7251c",
    "calls": 2,
    "messages": [
        "Welcome to Klaxer! Let staff know if you have any issues.",
        "Your account is currently unverified and may be limited until final approval."
    ]
}
```

## Defining Services

Klaxer service definition is handled via a YAML configuration file. Defining a
service determines how messages are classified, enriched, and routed by Klaxer.
Your custom configuration file should reside at `config/klaxer.yml`, and a
sample configuration file can be found at `config/klaxer.sample.yml`.

Specific rules can be defined for alert messages and titles independently. There
are four major rule categories:

 - `classification`: The criteria that determines whether an alert is
   classified as `CRITICAL`, `WARNING`, `OK`, or `UNKNOWN`. Defaults to
   `UNKNOWN`
 - `exclude`: The criteria that determines whether or not an alert is ignored
 - `enrichments`: Defines how messages and/or titles are enriched based on their
   content
 - `routes`: Defines how alerts are routed based on the message/title content

Services can be defined as follows:

```yml
# Define the name of your service at the top level
sensu:
    # An optional description can be provided
    description: "Sensu alerts"
    # Define rules for service messages
    message:
        # Defines messages containing the terms "error" or "failure" to be
        # classified as CRITICAL, and messages containing "warning" as WARNING
        classification:
            CRITICAL: ["error", "failure"]
            WARNING: ["warning"]
        # Exclude any alert where the message contains the term "keepalive"
        exclude: ["keepalive"]
        # In IF/THEN fashion, enrich a message with an @ mention IF it contains
        # the term "CheckDisk". Brackets are used to insert the original message
        enrichments:
            - IF: "CheckDisk"
              THEN: "@admin - please assist: {}"
        # In IF/THEN fashion, route any messages containing the term "build" to
        # the "devops" channel
        routes:
            - IF: "build"
              THEN: "devops"
    # Define rules for message titles (same concept as handling messages)
    title:
        classification:
            ...
        exclude:
            ...
        enrichments:
            ...
        routes:
            ...
```

