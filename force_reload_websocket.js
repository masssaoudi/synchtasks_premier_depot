/**
 * Force le rechargement et teste le WebSocket
 * À exécuter dans la console du navigateur (F12)
 */

console.log('🔄 Force rechargement et test WebSocket...');

// Fonction pour forcer le rechargement
function forceReload() {
    console.log('🔄 Force rechargement de la page...');
    window.location.reload(true);
}

// Fonction pour nettoyer le cache
function clearCache() {
    console.log('🗑️ Nettoyage du cache...');
    if ('caches' in window) {
        caches.keys().then(function(names) {
            for (let name of names) {
                caches.delete(name);
                console.log('🗑️ Cache supprimé:', name);
            }
        });
    }
}

// Fonction pour tester le WebSocket après rechargement
function testWebSocketAfterReload() {
    console.log('🧪 Test WebSocket après rechargement...');
    
    // Attendre un peu que la page soit chargée
    setTimeout(() => {
        try {
            console.log('🔌 Tentative de connexion WebSocket...');
            const testSocket = new WebSocket('ws://localhost:8000/api/ws/6889a312a274d15db190a36d');
            
            testSocket.onopen = function(event) {
                console.log('✅ WebSocket connecté avec succès !');
                
                // Envoyer un ping
                const pingMessage = {
                    type: 'ping',
                    timestamp: Date.now()
                };
                testSocket.send(JSON.stringify(pingMessage));
                console.log('📤 Ping envoyé');
                
                // Mettre à jour le statut dans l'interface
                updateWebSocketStatus('connecté');
            };
            
            testSocket.onmessage = function(event) {
                try {
                    const data = JSON.parse(event.data);
                    console.log('📥 Message reçu:', data);
                    
                    if (data.type === 'pong') {
                        console.log('✅ Pong reçu - WebSocket fonctionne parfaitement !');
                    }
                } catch (error) {
                    console.error('❌ Erreur parsing message:', error);
                }
            };
            
            testSocket.onclose = function(event) {
                console.log('🔌 WebSocket déconnecté:', event.code, event.reason);
                updateWebSocketStatus('déconnecté');
            };
            
            testSocket.onerror = function(error) {
                console.error('❌ Erreur WebSocket:', error);
                updateWebSocketStatus('erreur');
            };
            
        } catch (error) {
            console.error('❌ Erreur lors de la création WebSocket:', error);
        }
    }, 2000);
}

// Fonction pour mettre à jour le statut dans l'interface
function updateWebSocketStatus(status) {
    console.log('📊 Mise à jour statut WebSocket:', status);
    
    // Chercher les éléments qui affichent le statut WebSocket
    const statusElements = document.querySelectorAll('[class*="websocket"], [class*="WebSocket"], [class*="connection"]');
    
    statusElements.forEach(element => {
        if (element.textContent.includes('WebSocket') || element.textContent.includes('déconnecté') || element.textContent.includes('connecté')) {
            element.textContent = `WebSocket ${status}`;
            console.log('✅ Statut WebSocket mis à jour dans l\'interface');
        }
    });
}

// Instructions
console.log('💡 Instructions:');
console.log('   1. Nettoyez le cache: clearCache()');
console.log('   2. Forcez le rechargement: forceReload()');
console.log('   3. Ou testez directement: testWebSocketAfterReload()');
console.log('   4. Ou utilisez Ctrl+Shift+R pour forcer le rechargement');

// Test automatique après 3 secondes
setTimeout(() => {
    console.log('🔄 Test automatique du WebSocket...');
    testWebSocketAfterReload();
}, 3000); 