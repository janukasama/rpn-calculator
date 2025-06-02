ln_config:
	echo "ln config to /CONFIG"
	echo "WARNING: should not be used in production. should only used in dev environment"
	./devops/bin/ln_config.sh

ln_secrets:
	echo "ln secrets to /run/secrets/rpn-calculator"
	echo "WARNING: should not be used in production. should only used in dev environment"
	./devops/bin/ln_secrets.sh

deploy:
	docker compose -f devops/compose-files/docker-compose.base.yml \
	-f devops/compose-files/docker-compose.${AYOMI_ENV}.yml \
	up -d