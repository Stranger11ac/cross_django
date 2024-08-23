#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instala las dependencias del sistema
apt-get update && apt-get install -y portaudio19-dev

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate