#Deploy Gitlab Repository
initiate-project:
	git clone https://gitlab.com/HHsieh09/Volleyball-League-Data-Scraping-Analytics-System.git && \
	cd Volleyball-League-Data-Scraping-Analytics-System && \
	pyenv install -s $$(cat .python-version) && \
	sudo apt-get update && \
	sudo apt-get install -y build-essential gcc && \
	export LC_ALL=C.UTF-8 && \
	export LANG=C.UTF-8 && \
	pip install poetry && \
	poetry sync

# Generate dev environment variables
gen-dev-env-variables:
	python genenv.py

# Generate release environment variables
gen-release-env-variables:
	VERSION=RELEASE python genenv.py

# Create tag variable for version
GIT_TAG := $(shell git describe --abbrev=0 --tags 2>/dev/null || echo "latest")

# Generate docker image
build-image:
	docker build -f Dockerfile -t hhsiehde/crawler:${GIT_TAG}

# Push docker image
push-image:
	docker push hhsiehde/crawler:${GIT_TAG}

# Initiate docker swarm
initiate-swarm:
	docker swarm init

# First deploy crawler
first-deploy-crawler:
	docker pull hhsiehde/crawler:7.2.1 && \
	docker stack deploy --with-registry-auth -c crawler.yml crawler

# First deploy api
first-deploy-api:
	docker pull hhsiehde/api:7.2.2 && \
	docker stack deploy --with-registry-auth -c api.yml api

# Deploy crawler
deploy-crawler:
	GIT_TAG=${GIT_TAG} docker stack deploy --with-registry-auth -c crawler.yml crawler

# Deploy api
deploy-api:
	GIT_TAG=${GIT_TAG} docker stack deploy --with-registry-auth -c api.yml api

# Deploy portainer
deploy-portainer:
	docker stack deploy -c portainer.yml por

# Deploy MySQL
deploy-mysql:
	docker volume create mysql && \
	docker network create --scope=swarm --driver=overlay vbnetwork || true && \
	docker stack deploy --with-registry-auth -c mysql.yml mysql

# Deploy rabbitmq
deploy-rabbitmq:
	docker stack deploy --with-registry-auth -c rabbitmq.yml rabbitmq

setup-all:
	initiate-project gen-dev-env-variables initiate-swarm first-deploy-crawler first-deploy-api deploy-mysql deploy-rabbitmq deploy-portainer

# Start celery
run-celery:
	PYTHONPATH=. poetry run celery -A volleyballdata.tasks.worker worker --loglevel=info

# Send task
send-task:
	poetry run python volleyballdata/producer.py

test-coverage:
	poetry run pytest --cov-report term-missing --cov-config=.coveragerc --cov=./volleyballdata/ tests/
