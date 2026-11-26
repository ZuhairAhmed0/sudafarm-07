#!/bin/sh
set -e

BACKEND_URL="${BACKEND_URL:-https://sudafarm-api.onrender.com}"

# Handle bare service name from Render
if [ "$BACKEND_URL" = "sudafarm-api" ]; then
  BACKEND_URL="https://sudafarm-api.onrender.com"
fi

# If BACKEND_URL has no dot and no protocol, append onrender.com
case "$BACKEND_URL" in
  *.*) ;;
  http://*|https://*) ;;
  *) BACKEND_URL="https://${BACKEND_URL}.onrender.com" ;;
esac

# Ensure BACKEND_URL has a scheme
case "$BACKEND_URL" in
  http://*|https://*) ;;
  *) BACKEND_URL="https://${BACKEND_URL}" ;;
esac

# Extract host without protocol or path
BACKEND_HOST=$(echo "$BACKEND_URL" | sed -E 's|^https?://||' | sed -E 's|/.*$||')
PORT="${PORT:-80}"

export BACKEND_URL BACKEND_HOST PORT

if [ -f /etc/nginx/templates/default.conf.template ]; then
  envsubst '${PORT} ${BACKEND_URL} ${BACKEND_HOST}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
fi
