set -a
. ./.env
. ./serial.config
set +a

uvicorn main:app