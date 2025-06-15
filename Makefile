#Start Mysql
create-mysql:
	docker-compose -f mysql.yml up -d

#Start Rabbitmq
create-rabbitmq:
	docker-compose -f rabbitmq.yml up -d

#Install environment variables
install-python-env:
	poetry sync

# Start celery
run-celery:
	PYTHONPATH=. poetry run celery -A volleyballdata.tasks.worker worker --loglevel=info

# Send task
send-task:
	poetry run python volleyballdata/producer.py

# Generate dev environment variables
gen-dev-env-variables:
	python genenv.py

# Generate release environment variables
gen-release-env-variables:
	VERSION=RELEASE python genenv.py

# Create tag variable for version
GIT_TAG := ${shell git describe --abbrev=0 --tags}

# Generate docker image
build-image:
	docker build -f Dockerfile -t hhsiehde/crawler:${GIT_TAG}

# Push docker image
push-image:
	docker push hhsiehde/crawler:${GIT_TAG}

# Deploy crawler
deploy-crawler:
	GIT_TAG=${GIT_TAG} docker stack deploy --with-registry-auth -c crawler.yml crawler
