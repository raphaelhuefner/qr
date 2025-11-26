#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

VENDOR_PREFIX="vendor"

while read -r GIT_URL GIT_REF LOCAL_REPO FILES; do
	# only clone when local repo is absent
	if [ ! -d "$VENDOR_PREFIX/$LOCAL_REPO" ]; then
		git clone "$GIT_URL" "$VENDOR_PREFIX/$LOCAL_REPO"
	fi

	# update to latest, just in case
	git -C "$VENDOR_PREFIX/$LOCAL_REPO" fetch --all --tags

	git -C "$VENDOR_PREFIX/$LOCAL_REPO" checkout "$GIT_REF"

	# copy minified files to static
	for FILE in $FILES; do
		cp "$VENDOR_PREFIX/$LOCAL_REPO/$FILE" static/
	done
done <<'EOF'
https://github.com/picturepan2/spectre	v0.5.9	spectre	dist/spectre.min.css	dist/spectre-exp.min.css	dist/spectre-icons.min.css
https://github.com/mebjas/html5-qrcode	v2.3.8	html5-qrcode	minified/html5-qrcode.min.js
https://github.com/davidshimjs/qrcodejs	04f46c6a0708418cb7b96fc563eacae0fbf77674	qrcodejs	qrcode.min.js
EOF
