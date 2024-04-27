set -x

VERSION=${1:-3.11}

docker compose --env-file .env.test build backend --build-arg VERSION=$VERSION -q
docker compose --env-file .env.test -f docker-compose.yml -f docker-compose.test.yml up backend --force-recreate --always-recreate-deps --abort-on-container-exit --no-log-prefix || break
docker compose --env-file .env.test down -v
