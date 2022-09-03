set -a
. ./.env
. ./serial.config
set +a

uvicorn app.main:app --reload