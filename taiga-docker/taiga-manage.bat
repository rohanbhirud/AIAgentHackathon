@echo on
docker compose -f docker-compose.yml -f docker-compose-inits.yml run --rm taiga-manage %*