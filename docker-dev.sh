#!/bin/bash
# Pull the latest changes and start the development container
set -e
git pull
export OPENAI_API_KEY=${OPENAI_API_KEY}
docker compose up --build
