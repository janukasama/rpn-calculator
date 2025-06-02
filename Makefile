deploy:
	docker compose -f devops/compose-files/docker-compose.base.yml \
	-f devops/compose-files/docker-compose.${AYOMI_ENV}.yml \
	up -d