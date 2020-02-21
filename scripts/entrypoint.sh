#!/usr/bin/env ash

# Variables
APPDIR=${APPDIR:-"/app"}

# Functions

# Logic

python ${APPDIR}/schemabridge/schemabridge.py $@
