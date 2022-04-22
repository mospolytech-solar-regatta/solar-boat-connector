set -a
. ./.env
. ./serial.config
set +a

celery -A background.app worker -l INFO -B