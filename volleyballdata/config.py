import os

MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.environ.get("MYSQL_USER","user")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD","test")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT","3306"))
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "volleyballdb")
WORKER_ACCOUNT = os.environ.get("WORKER_ACCOUNT", "worker")
WORKER_PASSWORD = os.environ.get("WORKER_PASSWORD", "worker")
MESSAGE_QUEUE_HOST = os.environ.get("MESSAGE_QUEUE_HOST", "host.docker.internal")
MESSAGE_QUEUE_PORT = int(os.environ.get("MESSAGE_QUEUE_PORT", "5672"))