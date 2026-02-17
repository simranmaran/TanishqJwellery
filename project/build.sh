#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --noinput
