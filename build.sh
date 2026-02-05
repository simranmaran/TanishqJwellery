#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

# Render runs this script from the repository root.
cd "$(dirname "$0")/project"

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
