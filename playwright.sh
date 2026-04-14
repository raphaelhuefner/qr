#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

# Allow this script to be run from any other working directory.
pushd "$(dirname "$0")" > /dev/null
trap "popd > /dev/null" EXIT

mkdir -p .cache .playwright-browsers

export XDG_CACHE_HOME="$(pwd)/.cache"
export PLAYWRIGHT_BROWSERS_PATH="$(pwd)/.playwright-browsers"

exec playwright-cli "$@"
