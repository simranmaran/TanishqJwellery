#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

cd "$(dirname "$0")/project"
pip install --upgrade pip
pip install --upgrade setuptools wheel

pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --noinput
