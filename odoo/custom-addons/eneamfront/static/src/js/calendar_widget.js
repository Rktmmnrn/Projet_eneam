// static/src/js/calendar_widget.js - VERSION CORRIGÉE
function loadPointages(date) {
    const apiURL = document.getElementById('calpicker')?.dataset?.api;
    if (!apiURL) return;

    // Si l'URL fournie utilise le nom d'hote docker 'django',
    // le navigateur client ne pourra pas le résoudre. Remplacer
    // 'django' par l'hôte courant du navigateur (ou conserver
    // l'URL si elle est déjà résoluble).
    let finalApiURL = apiURL;
    try {
        const parsed = new URL(apiURL, window.location.href);
        if (parsed.hostname === 'django') {
            parsed.hostname = window.location.hostname;
            if (!parsed.port) parsed.port = '8000';
            finalApiURL = parsed.toString();
        }
    } catch (err) {
        // Si URL invalide, on laisse apiURL tel quel et la fetch échouera
        finalApiURL = apiURL;
    }

    fetch(`${finalApiURL}?date=${date}`)
        .then(resp => {
            if (!resp.ok) throw new Error('Erreur API');
            return resp.json();
        })
        .then(data => {
            const ul = document.getElementById('eneam_dg_liste');
            if (!ul) return;

            ul.innerHTML = '';

            if (!data || data.length === 0) {
                ul.innerHTML = '<li class="list-group-item text-muted">Aucun pointage</li>';
                return;
            }

            data.forEach(p => {
                const li = `<li class="list-group-item d-flex justify-content-between">
                            <span>
                                <b>${p.personnel_info || 'N/A'}</b>
                            </span>
                            <span>${p.type_pointage || 'N/A'} -- ${p.datetime_pointage || 'N/A'}</span>
                        </li>`;
                ul.insertAdjacentHTML('beforeend', li);
                console.log("personnel_id: ",p.personnel);
            });
        })
        .catch(error => {
            console.error('Erreur chargement pointages:', error);
        });
}

// Initialisation sécurisée
document.addEventListener('DOMContentLoaded', function () {
    // Nettoyage modal
    document.body.classList.remove('modal-open');
    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());

    const calpicker = document.getElementById('calpicker');
    const btnLoad = document.getElementById('btn_load');

    if (calpicker) {
        // Définir la date d'aujourd'hui
        const today = new Date().toISOString().split('T')[0];
        calpicker.value = today;

        // Charger les pointages du jour
        setTimeout(() => loadPointages(today), 100);
    }

    if (btnLoad) {
        btnLoad.addEventListener('click', function () {
            console.log("click");
            const calpicker = document.getElementById('calpicker');
            if (calpicker && calpicker.value) {
                loadPointages(calpicker.value);
            }
        });
    }
});

// Gestion des erreurs globales
window.addEventListener('error', function (e) {
    console.error('Erreur globale:', e);
});