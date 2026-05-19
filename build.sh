#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
mkdir -p staticfiles  # ← Agrega esta línea
python manage.py collectstatic --no-input
python manage.py migrate