load-env:
	@bash scripts/load_env.sh

test:
	@source .env && molecule test

deploy:
	@source .env && ansible-playbook -i inventory.ini site.yml

.PHONY: load-env test deploy