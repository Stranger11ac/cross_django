#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instala las dependencias del sistema
apt-get update
apt-get install -y portaudio19-dev || { echo "Failed to install portaudio19-dev"; exit 1; }

# Instalación de dependencias de Python
pip install -r requirements.txt || { echo "Failed to install Python dependencies"; exit 1; }

# Convert static asset files
python manage.py collectstatic --no-input || { echo "Failed to collect static files"; exit 1; }

# Apply any outstanding database migrations
python manage.py migrate || { echo "Failed to apply database migrations"; exit 1; }
