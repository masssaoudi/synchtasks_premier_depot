import axios from 'axios';
import { createPinia } from 'pinia';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './style.css';
import './styles/tooltips.css';

// 🎈 Import de la directive tooltips
import autoTip from './directives/autotip.js';

// Configuration axios - Utiliser l'URL complète du backend
axios.defaults.baseURL = 'http://localhost:8000'; // URL directe du backend

// Intercepteur pour les requêtes
axios.interceptors.request.use(
  config => {
    console.log(
      '🌐 Requête envoyée:',
      config.method?.toUpperCase(),
      config.url
    );
    return config;
  },
  error => {
    console.error('❌ Erreur de requête:', error);
    return Promise.reject(error);
  }
);

// Intercepteur pour les réponses
axios.interceptors.response.use(
  response => {
    console.log('✅ Réponse reçue:', response.status, response.config.url);
    return response;
  },
  error => {
    console.error(
      '❌ Erreur de réponse:',
      error.response?.status,
      error.config?.url
    );
    return Promise.reject(error);
  }
);

// Import des stores

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// 🎈 Enregistrement de la directive tooltips globale
app.directive('autotip', autoTip);

// Enregistrement du Service Worker pour PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js')
      .then(registration => {
        console.log(
          'Service Worker enregistré avec succès:',
          registration.scope
        );

        // Vérifier les mises à jour
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (
              newWorker.state === 'installed' &&
              navigator.serviceWorker.controller
            ) {
              // Nouvelle version disponible
              if (
                confirm(
                  "Une nouvelle version de SyncTasks est disponible. Voulez-vous l'installer ?"
                )
              ) {
                newWorker.postMessage({ type: 'SKIP_WAITING' });
                window.location.reload();
              }
            }
          });
        });
      })
      .catch(error => {
        console.error(
          "Erreur lors de l'enregistrement du Service Worker:",
          error
        );
      });
  });
}

// Gestion de l'installation PWA
let deferredPrompt;
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  deferredPrompt = e;

  // Afficher un bouton d'installation personnalisé si nécessaire
  const installButton = document.getElementById('install-button');
  if (installButton) {
    installButton.style.display = 'block';
    installButton.addEventListener('click', () => {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(choiceResult => {
        if (choiceResult.outcome === 'accepted') {
          console.log('Application installée');
        }
        deferredPrompt = null;
        installButton.style.display = 'none';
      });
    });
  }
});

// Gestion de l'installation réussie
window.addEventListener('appinstalled', () => {
  console.log('SyncTasks a été installé avec succès');
  // Masquer le bouton d'installation
  const installButton = document.getElementById('install-button');
  if (installButton) {
    installButton.style.display = 'none';
  }
});

// Optimisations de performance
app.config.performance = process.env.NODE_ENV === 'development';

// Gestion des erreurs globales
app.config.errorHandler = (err, vm, info) => {
  console.error('Erreur Vue:', err, info);
  // Ici vous pourriez envoyer l'erreur à un service de monitoring
};

// Gestion des avertissements
app.config.warnHandler = (msg, vm, trace) => {
  console.warn('Avertissement Vue:', msg, trace);
};

app.mount('#app');

// Export pour les tests
export { app, pinia };
