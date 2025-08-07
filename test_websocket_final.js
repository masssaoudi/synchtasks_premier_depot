/**
 * Test final de connexion WebSocket après correction CSP
 * À exécuter dans la console du navigateur (F12)
 */

console.log('🧪 Test final de connexion WebSocket...');

// ID d'Alice depuis la base de données
const ALICE_USER_ID = "6889a312a274d15db190a36d";

// Test de connexion WebSocket avec un nom unique
try {
    console.log('🔌 Tentative de connexion WebSocket...');
    const testSocket = new WebSocket(`ws://localhost:8000/api/ws/${ALICE_USER_ID}`);
    
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
    
    console.log('✅ Test WebSocket lancé - vérifiez les messages ci-dessus');
    
} catch (error) {
    console.error('❌ Erreur lors de la création WebSocket:', error);
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

console.log('💡 Instructions:');
console.log('   1. Vérifiez les messages dans la console');
console.log('   2. Si "WebSocket connecté", le problème est résolu !');
console.log('   3. Le statut dans l\'interface devrait changer');
console.log('   4. Les notifications temps réel devraient fonctionner'); 