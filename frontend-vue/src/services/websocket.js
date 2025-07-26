class WebSocketService {
  constructor() {
    this.ws = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000; // 1 seconde
    this.listeners = new Map();
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  }

  // Connexion au WebSocket
  connect(userId = null) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('🔌 WebSocket déjà connecté');
      return;
    }

    const wsUrl = this.baseUrl.replace('http', 'ws') + '/ws';
    console.log('🔌 Tentative de connexion WebSocket:', wsUrl);

    try {
      this.ws = new WebSocket(wsUrl);
      
      this.ws.onopen = () => {
        console.log('✅ WebSocket connecté');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        
        // Envoyer l'ID utilisateur si fourni
        if (userId) {
          this.send({ type: 'auth', user_id: userId });
        }
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 Message WebSocket reçu:', data);
          this.handleMessage(data);
        } catch (error) {
          console.error('❌ Erreur parsing message WebSocket:', error);
        }
      };

      this.ws.onclose = (event) => {
        console.log('🔌 WebSocket déconnecté:', event.code, event.reason);
        this.isConnected = false;
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('❌ Erreur WebSocket:', error);
        this.isConnected = false;
      };

    } catch (error) {
      console.error('❌ Erreur création WebSocket:', error);
    }
  }

  // Gestion de la reconnexion automatique
  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🔄 Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error('❌ Nombre maximum de tentatives de reconnexion atteint');
    }
  }

  // Envoi de message
  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(JSON.stringify(message));
        console.log('📤 Message WebSocket envoyé:', message);
      } catch (error) {
        console.error('❌ Erreur envoi message WebSocket:', error);
      }
    } else {
      console.warn('⚠️ WebSocket non connecté, message ignoré:', message);
    }
  }

  // Gestion des messages reçus
  handleMessage(data) {
    const { type, action, task, task_id } = data;

    switch (type) {
      case 'connection':
        console.log('🔌 Message de connexion:', data.message);
        break;

      case 'task_update':
        this.handleTaskUpdate(action, task, task_id);
        break;

      default:
        console.log('📨 Message non reconnu:', data);
    }
  }

  // Gestion des mises à jour de tâches
  handleTaskUpdate(action, task, task_id) {
    console.log(`🔄 Mise à jour tâche: ${action}`, task || task_id);
    
    // Émettre un événement personnalisé pour notifier les composants
    const event = new CustomEvent('taskUpdate', {
      detail: { action, task, task_id }
    });
    window.dispatchEvent(event);
  }

  // Ajouter un listener pour les mises à jour
  onTaskUpdate(callback) {
    const handler = (event) => {
      callback(event.detail);
    };
    
    window.addEventListener('taskUpdate', handler);
    
    // Retourner une fonction pour supprimer le listener
    return () => {
      window.removeEventListener('taskUpdate', handler);
    };
  }

  // Déconnexion
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.isConnected = false;
      console.log('🔌 WebSocket déconnecté manuellement');
    }
  }

  // Vérifier l'état de la connexion
  getConnectionState() {
    if (!this.ws) return 'disconnected';
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING: return 'connecting';
      case WebSocket.OPEN: return 'connected';
      case WebSocket.CLOSING: return 'closing';
      case WebSocket.CLOSED: return 'closed';
      default: return 'unknown';
    }
  }
}

// Instance singleton
const websocketService = new WebSocketService();

export default websocketService; 