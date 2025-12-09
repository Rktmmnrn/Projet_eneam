# Image de base Odoo 17
FROM odoo:17.0

# Passe en root pour installer des packages
USER root

# Copier requirements si vous avez des dépendances Python pour vos modules
COPY requirements-odoo.txt /tmp/requirements-odoo.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements-odoo.txt \
  && rm -rf /root/.cache/pip /tmp/requirements-odoo.txt

# Créer le répertoire de configuration Odoo et copier la config
RUN mkdir -p /etc/odoo && chown -R odoo:odoo /etc/odoo
COPY odoo.conf /etc/odoo/odoo.conf
RUN chown odoo:odoo /etc/odoo/odoo.conf

# Copier et configurer les addons personnalisés
COPY custom-addons/eneamfront /mnt/extra-addons/eneamfront
RUN chown -R odoo:odoo /mnt/extra-addons/eneamfront

# Assurer que le répertoire filestore existe avec les bonnes permissions
RUN mkdir -p /var/lib/odoo && chown -R odoo:odoo /var/lib/odoo

# Retourne à l'utilisateur odoo pour la sécurité
USER odoo

# Port exposé par Odoo
EXPOSE 8069

# Commande de démarrage
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]