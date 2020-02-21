# Base image
FROM python:3-alpine

# Information
LABEL maintainer="FrozenFOXX <frozenfoxx@churchoffoxx.net>"

# Variables
WORKDIR /app
ENV APPDIR="/app"

# Add required packages
RUN apk -U add build-base

# Set up requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Launch
ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]
