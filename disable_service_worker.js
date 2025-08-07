/**
 * Script pour désactiver le service worker et nettoyer le cache
 * À exécuter dans la console du navigateur
 */

console.log('🔧 Désactivation du service worker...');

// Désactiver le service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then(function(registrations) {
    for(let registration of registrations) {
      registration.unregister();
      console.log('✅ Service worker désactivé');
    }
  });
}

// Nettoyer le cache
if ('caches' in window) {
  caches.keys().then(function(names) {
    for (let name of names) {
      caches.delete(name);
      console.log('🗑️ Cache supprimé:', name);
    }
  });
}

// Supprimer les données de localStorage liées au service worker
localStorage.removeItem('sw.js');
localStorage.removeItem('serviceWorker');

console.log('✅ Service worker et cache nettoyés');
console.log('🔄 Rechargez la page pour appliquer les changements'); 