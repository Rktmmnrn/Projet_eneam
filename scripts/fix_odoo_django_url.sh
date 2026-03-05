#!/usr/bin/env bash
set -euo pipefail

echo "Fixing Odoo Django URL configuration..."

# Supprimer l'ancien paramètre s'il existe, puis redémarrer le module
docker-compose exec -T odoo odoo -d databaseOdoo -u base --stop-after-init << 'PYTHON'
from odoo import api, SUPERUSER_ID
import os

# Connect to database
env = api.Environment(cr, SUPERUSER_ID)

# Supprimer les anciens paramètres incorrects
old_urls = ['http://127.0.0.1:8000/api', 'http://localhost:8000/api']
for url in old_urls:
    param = env['ir.config_parameter'].search([('key', '=', 'eneamfront.django_url'), ('value', '=', url)])
    if param:
        print(f"Suppression de l'ancien paramètre: {url}")
        param.unlink()

# Créer le paramètre correct avec l'URL Docker interne
correct_url = os.environ.get('ENEAMFRONT_DJANGO_URL', 'http://django:8000/api')
env['ir.config_parameter'].set_param('eneamfront.django_url', correct_url)
print(f"Paramètre créé: eneamfront.django_url = {correct_url}")
PYTHON

echo "✅ Configuration mise à jour avec succès!"
