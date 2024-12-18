#!/usr/bin/env bash
# Use this script to wait for a service to be available.
# Usage: ./wait-for-it.sh <host:port> [--timeout=<timeout>] [--] <command> [args]

set -e

TIMEOUT=30
HOST=""
PORT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --timeout=*)
            TIMEOUT="${1#*=}"
            shift
            ;;
        *)
            if [[ -z "$HOST" ]]; then
                HOST="${1%:*}"
                PORT="${1##*:}"
            else
                break
            fi
            shift
            ;;
    esac
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
    echo "Usage: wait-for-it.sh <host:port> [--timeout=<timeout>] [--] <command> [args]"
    exit 1
fi

echo "Waiting for $HOST:$PORT..."

START_TIME=$(date +%s)

while true; do
    nc -z "$HOST" "$PORT" && break || {
        echo "Waiting..."
        sleep 1
    }

    ELAPSED_TIME=$(( $(date +%s) - START_TIME ))
    if [[ "$ELAPSED_TIME" -ge "$TIMEOUT" ]]; then
        echo "Timeout reached. Exiting."
        exit 1
    fi
done

echo "$HOST:$PORT is available."
exec "$@"
