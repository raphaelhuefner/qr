#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

# Allow this script to be run from any other working directory.
pushd "$(dirname "$0")" > /dev/null
trap "popd > /dev/null" EXIT

python3 serve.py \
    --port 8080 \
    --bind 127.0.0.1 \
    --directory docs
