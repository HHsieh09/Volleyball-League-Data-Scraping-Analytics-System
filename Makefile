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