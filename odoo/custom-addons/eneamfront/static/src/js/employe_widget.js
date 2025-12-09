// static/src/js/employe_widget.js - VERSION AMÉLIORÉE
function initEmployeWidget() {
    try {
        const pageEl = document.getElementById('page_employe');
        if (!pageEl) {
            console.warn('Element page_employe non trouvé');
            return;
        }

        const apiPersonnel = pageEl.dataset.apiPersonnel;
        const apiPointage = pageEl.dataset.apiPointage;
        const matricule = pageEl.dataset.matricule;

        if (!apiPersonnel || !apiPointage || !matricule) {
            console.warn('Données manquantes pour le widget employé');
            console.log('apiPersonnel:', apiPersonnel);
            console.log('apiPointage:', apiPointage);
            console.log('matricule:', matricule);
            return;
        }

        // 1. Charger le nom de l'employé
        loadNomEmploye(apiPersonnel, matricule);

        // 2. Charger les pointages du jour
        loadPointagesDuJour(apiPointage, matricule);

        // 3. Charger l'historique
        loadHistoriquePointages(apiPointage, matricule);

    } catch (e) {
        console.error('Erreur init employe_widget:', e);
    }
}


function loadNomEmploye(apiPersonnel, matricule) { // Charger le nom de l'employé
    fetch(apiPersonnel)
        .then(r => {
            if (!r.ok) throw new Error(`Erreur API personnel: ${r.status}`);
            return r.json();
        })
        .then(data => {
            const employe = Array.isArray(data) ?
                data.find(p => String(p.matricule) === String(matricule)) : null;
            const nomEl = document.getElementById('nom_complet');
            if (nomEl) {
                nomEl.textContent = employe ?
                    `${employe.nom || ''} ${employe.prenom || ''}`.trim() || 'Inconnu' :
                    'Non trouvé';
            }
        })
        .catch(error => {
            console.error('Erreur chargement personnel:', error);
            const nomEl = document.getElementById('nom_complet');
            if (nomEl) nomEl.innerHTML = '<span style="color:red;">Erreur chargement</span>'; // erreur affichage nom
        });
}


function loadPointagesDuJour(apiPointage, matricule) { // Charger les pointages du jour
    const today = new Date().toISOString().split('T')[0];

    fetch(`${apiPointage}?date=${today}&matricule=${matricule}`)
        .then(r => {
            if (!r.ok) throw new Error(`Erreur API pointage: ${r.status}`);
            // console.log('Erreur API pointage: ', r);
            return r.json();
        })
        .then(data => {
            // Trouver les pointages d'arrivée et départ pour aujourd'hui
            const arrivee = Array.isArray(data) ?
                data.find(p => p.type_pointage === 'arrivee') : null;
            const depart = Array.isArray(data) ?
                data.find(p => p.type_pointage === 'depart') : null;

            const heureArriveeEl = document.getElementById('heure_arrivee');
            const heureDepartEl = document.getElementById('heure_depart');

            if (heureArriveeEl) {
                heureArriveeEl.textContent = arrivee ?
                    formaterHeure(arrivee.datetime_pointage) : '--:--';
                if (arrivee) heureArriveeEl.className = 'text-success fw-bold';
            }

            if (heureDepartEl) {
                heureDepartEl.textContent = depart ?
                    formaterHeure(depart.datetime_pointage) : '--:--';
                if (depart) heureDepartEl.className = 'text-warning fw-bold';
            }
        })
        .catch(error => {
            console.error('Erreur chargement pointages du jour:', error);
        });
}


function loadHistoriquePointages(apiPointage, matricule) {
    // Charger les 5 derniers pointages
    fetch(`${apiPointage}?matricule=${matricule}&limit=5`)
        .then(r => {
            if (!r.ok) throw new Error(`Erreur API historique: ${r.status}`);
            return r.json();
        })
        .then(data => {
            const historiqueEl = document.getElementById('historique');
            if (!historiqueEl) return;

            historiqueEl.innerHTML = '';

            if (!data || data.length === 0) {
                historiqueEl.innerHTML =
                    '<div class="list-group-item text-muted">Aucun pointage récent</div>';
                return;
            }

            // Limiter à 5 éléments
            const dataLimitee = data.slice(0, 5);
            console.log('Données historiques:', dataLimitee);

            dataLimitee.forEach(pointage => {
                const item = document.createElement('div');
                item.className = 'list-group-item d-flex justify-content-between align-items-center';

                const date = new Date(pointage.datetime_pointage);
                const dateStr = date.toLocaleDateString('fr-FR');
                const heureStr = date.toLocaleTimeString('fr-FR', {
                    hour: '2-digit', minute: '2-digit'
                });

                const typeBadge = pointage.type_pointage === 'arrivee' ?
                    '<span class="badge bg-success">Arrivée</span>' :
                    '<span class="badge bg-warning">Départ</span>';

                item.innerHTML = `
                    <div>
                        <strong>${dateStr}</strong> à ${heureStr}
                    </div>
                    ${typeBadge}
                `;

                historiqueEl.appendChild(item); // ajouter l'élément au conteneur
            });

            // Afficher un message si plus de résultats
            if (data.length > 5) {
                const message = document.createElement('div');
                message.className = 'list-group-item text-info small';
                message.textContent = `... et ${data.length - 5} pointages plus anciens`;
                historiqueEl.appendChild(message);
            }
        })
        .catch(error => {
            console.error('Erreur chargement historique:', error);
            const historiqueEl = document.getElementById('historique');
            if (historiqueEl) {
                historiqueEl.innerHTML =
                    '<div class="list-group-item text-danger">Erreur chargement historique</div>';
            }
        });
}

function formaterHeure(datetimeStr) {
    if (!datetimeStr) return '--:--';
    try {
        const date = new Date(datetimeStr);
        return date.toLocaleTimeString('fr-FR', {
            hour: '2-digit', minute: '2-digit'
        });
    } catch (e) {
        return '--:--';
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', initEmployeWidget);