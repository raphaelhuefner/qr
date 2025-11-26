#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

python3 serve.py \
    --port 8080 \
    --bind 127.0.0.1 \
    --directory static
