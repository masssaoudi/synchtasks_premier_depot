/**
 * Script pour forcer la connexion WebSocket dans le navigateur
 * À exécuter dans la console du navigateur (F12)
 */

console.log('🔧 Force connexion WebSocket dans le navigateur...');

// ID d'Alice depuis la base de données
const ALICE_USER_ID = "6889a312a274d15db190a36d";

// Fonction pour forcer la connexion WebSocket
function forceWebSocketConnection() {
    console.log('🔌 Tentative de connexion WebSocket forcée...');
    
    try {
        // URL WebSocket pour Alice
        const wsUrl = `ws://localhost:8000/api/ws/${ALICE_USER_ID}`;
        console.log('🔌 Connexion à:', wsUrl);
        
        // Créer la connexion WebSocket
        const socket = new WebSocket(wsUrl);
        
        socket.onopen = function(event) {
            console.log('✅ WebSocket connecté avec succès !');
            
            // Envoyer un ping
            const pingMessage = {
                type: 'ping',
                timestamp: Date.now()
            };
            socket.send(JSON.stringify(pingMessage));
            console.log('📤 Ping envoyé');
            
            // Envoyer une notification de connexion
            const connectMessage = {
                type: 'user_connected',
                user_id: ALICE_USER_ID,
                username: 'alice',
                timestamp: Date.now()
            };
            socket.send(JSON.stringify(connectMessage));
            console.log('📤 Message de connexion envoyé');
            
            // Maintenir la connexion
            console.log('🔄 Maintien de la connexion WebSocket...');
            
            // Mettre à jour le statut dans l'interface
            updateWebSocketStatus('connecté');
        };
        
        socket.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                console.log('📥 Message reçu:', data);
                
                // Traiter les messages selon leur type
                if (data.type === 'pong') {
                    console.log('✅ Pong reçu');
                } else if (data.type === 'notification') {
                    console.log('🔔 Notification reçue:', data.message);
                    showNotification(data.message);
                }
            } catch (error) {
                console.error('❌ Erreur parsing message:', error);
            }
        };
        
        socket.onclose = function(event) {
            console.log('🔌 WebSocket déconnecté:', event.code, event.reason);
            updateWebSocketStatus('déconnecté');
        };
        
        socket.onerror = function(error) {
            console.error('❌ Erreur WebSocket:', error);
            updateWebSocketStatus('erreur');
        };
        
        // Retourner la socket pour pouvoir l'utiliser
        return socket;
        
    } catch (error) {
        console.error('❌ Erreur lors de la connexion WebSocket:', error);
        updateWebSocketStatus('erreur');
        return null;
    }
}

// Fonction pour mettre à jour le statut WebSocket dans l'interface
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

// Fonction pour afficher une notification
function showNotification(message) {
    console.log('🔔 Affichage notification:', message);
    
    // Créer une notification simple
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 15px;
        border-radius: 5px;
        z-index: 10000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Supprimer après 5 secondes
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Fonction pour tester la connexion WebSocket
function testWebSocketConnection() {
    console.log('🧪 Test de connexion WebSocket...');
    
    const socket = forceWebSocketConnection();
    
    if (socket) {
        // Tester l'envoi de messages
        setTimeout(() => {
            if (socket.readyState === WebSocket.OPEN) {
                const testMessage = {
                    type: 'test_message',
                    message: 'Test de connexion WebSocket depuis le navigateur',
                    timestamp: Date.now()
                };
                socket.send(JSON.stringify(testMessage));
                console.log('📤 Message de test envoyé');
            }
        }, 2000);
        
        // Fermer après 10 secondes
        setTimeout(() => {
            if (socket.readyState === WebSocket.OPEN) {
                socket.close();
                console.log('🔌 Test terminé, connexion fermée');
            }
        }, 10000);
    }
}

// Exécuter le test
console.log('🚀 Démarrage du test WebSocket...');
testWebSocketConnection();

console.log('💡 Instructions:');
console.log('   1. Vérifiez les messages dans la console');
console.log('   2. Le statut WebSocket devrait changer dans l\'interface');
console.log('   3. Si ça fonctionne, le WebSocket sera connecté automatiquement'); 