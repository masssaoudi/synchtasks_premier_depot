// Service Worker pour SyncTasks
const CACHE_NAME = 'synchtasks-v1.0.0';
const urlsToCache = [
  '/',
  '/index.html',
  '/assets/index.css',
  '/assets/index.js',
];

// Installation du Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then(cache => {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error("Erreur lors de l'installation du cache:", error);
      })
  );
});

// Activation du Service Worker
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log("Suppression de l'ancien cache:", cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Interception des requêtes
self.addEventListener('fetch', event => {
  // Ignorer les requêtes API - les laisser passer directement
  if (event.request.url.includes('/api/') || event.request.url.includes('localhost:8000')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(response => {
      // Retourner la réponse en cache si elle existe
      if (response) {
        return response;
      }

      // Sinon, faire la requête réseau
      return fetch(event.request)
        .then(response => {
          // Vérifier si la réponse est valide
          if (
            !response ||
            response.status !== 200 ||
            response.type !== 'basic'
          ) {
            return response;
          }

          // Cloner la réponse car elle ne peut être utilisée qu'une fois
          const responseToCache = response.clone();

          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });

          return response;
        })
        .catch(() => {
          // En cas d'erreur réseau, retourner une page d'erreur
          if (event.request.destination === 'document') {
            return caches.match('/offline.html');
          }
        });
    })
  );
});

// Gestion des messages
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Gestion des notifications push (pour le futur)
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle notification SyncTasks',
    icon: '/icon-192x192.png',
    badge: '/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1,
    },
    actions: [
      {
        action: 'explore',
        title: 'Voir',
        icon: '/icon-192x192.png',
      },
      {
        action: 'close',
        title: 'Fermer',
        icon: '/icon-192x192.png',
      },
    ],
  };

  event.waitUntil(self.registration.showNotification('SyncTasks', options));
});

// Gestion des clics sur les notifications
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(clients.openWindow('/'));
  }
});
