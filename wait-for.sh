#!/bin/sh
# wait-for.sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for $host to be available..."

until nc -z "$host" 5432; do
  echo "Waiting for Postgres at $host..."
  sleep 2
done

echo "$host is up! Starting command: $cmd"
exec $cmd
