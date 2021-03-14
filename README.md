# schemabridge

[![Build Status](https://cloud.drone.io/api/badges/frozenfoxx/schemabridge/status.svg?ref=refs/heads/main)](https://cloud.drone.io/frozenfoxx/schemabridge)

CLI interface for [Schemaverse](https://schemaverse.com/).

Docker Hub: [https://hub.docker.com/r/frozenfoxx/schemabridge](https://hub.docker.com/r/frozenfoxx/schemabridge).

# Requirements

* python 3+
* psycopg2

# Setup

* Create an account at [Schemaverse](https://schemaverse.com/).
* `pip3 install schemabridge`
* Edit the `/etc/schemabridge/conf/schemabridge.conf` with your player information.

# Usage

* For normal use, `schemabridge` will suffice.
* If you wish to override any options in your config file use `-h` to see all overrides.

# Testing

* Create a sample config file, use the environment variables, or arguments to supply player information.
* `cd [cloned repo root]`
* `python3 -m schembridge.schemabridge`

# Docker

This tool can also be run as a Docker container. This can be combined with the environment variables to launch conveniently:

```
docker run \
  -it \
  --rm \
  -e HOST="db.schemaverse.com" \
  -e PORT="5432" \
  -e DB="schemaverse" \
  -e USERNAME="[username]" \
  -e PASSWORD='[password]' \
  frozenfoxx/schemabridge:latest
```

# Legal

This project is licensed under the Apache License v2.0. Schemaverse is owned by its owners.
