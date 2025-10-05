/**
 * Service WebSocket simple et propre pour SyncTasks
 * Version épurée sans complexité inutile
 */

class WebSocketService {
  constructor() {
    this.socket = null;
    this.userId = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.isConnecting = false;
    this.messageHandlers = new Map();
    this.connectionHandlers = new Map();
  }

  // Initialiser la connexion WebSocket
  async connect(userId) {
    if (this.isConnecting) {
      return;
    }

    this.userId = userId;
    this.isConnecting = true;

    try {
      // URL simple sans token pour commencer
      const wsUrl = `ws://localhost:8000/api/ws/${userId}`;
      console.log('🔌 Connexion WebSocket simple:', wsUrl);
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        console.log('✅ WebSocket connecté');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.notifyConnectionHandlers('connected');
      };

      this.socket.onmessage = event => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('❌ Erreur parsing message WebSocket:', error);
        }
      };

      this.socket.onclose = event => {
        console.log('🔌 WebSocket déconnecté:', event.code, event.reason);
        this.isConnecting = false;
        this.notifyConnectionHandlers('disconnected');

        // Tentative de reconnexion automatique
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(
            `🔄 Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts}`
          );
          setTimeout(
            () => this.connect(this.userId),
            this.reconnectDelay * this.reconnectAttempts
          );
        } else {
          console.error(
            '❌ Nombre maximum de tentatives de reconnexion atteint'
          );
          this.notifyConnectionHandlers('failed');
        }
      };

      this.socket.onerror = error => {
        console.error('❌ Erreur WebSocket:', error);
        this.isConnecting = false;
        this.notifyConnectionHandlers('error');
      };
    } catch (error) {
      console.error('❌ Erreur lors de la connexion WebSocket:', error);
      this.isConnecting = false;
      this.notifyConnectionHandlers('error');
    }
  }

  // Déconnecter
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    this.isConnecting = false;
    this.reconnectAttempts = 0;
  }

  // Envoyer un message
  send(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
      console.log('📤 Message WebSocket envoyé:', message.type);
    } else {
      console.warn('⚠️ WebSocket non connecté, message non envoyé:', message);
    }
  }

  // Gérer les messages reçus
  handleMessage(data) {
    console.log('📥 Message WebSocket reçu:', data.type);

    // Notifier les handlers spécifiques
    const handlers = this.messageHandlers.get(data.type) || [];
    handlers.forEach(handler => {
      try {
        handler(data);
      } catch (error) {
        console.error(`❌ Erreur handler ${data.type}:`, error);
      }
    });
  }

  // Enregistrer un handler pour un type de message
  onMessage(type, handler) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, []);
    }
    this.messageHandlers.get(type).push(handler);
  }

  // Enregistrer un handler pour les événements de connexion
  onConnection(event, handler) {
    if (!this.connectionHandlers.has(event)) {
      this.connectionHandlers.set(event, []);
    }
    this.connectionHandlers.get(event).push(handler);
  }

  // Notifier les handlers de connexion
  notifyConnectionHandlers(event) {
    const handlers = this.connectionHandlers.get(event) || [];
    handlers.forEach(handler => {
      try {
        handler();
      } catch (error) {
        console.error(`❌ Erreur connection handler ${event}:`, error);
      }
    });
  }

  // Méthodes spécifiques pour SyncTasks

  // Rejoindre une room
  joinRoom(roomId) {
    this.send({
      type: 'join_room',
      room_id: roomId,
    });
  }

  // Quitter une room
  leaveRoom(roomId) {
    this.send({
      type: 'leave_room',
      room_id: roomId,
    });
  }

  // Mettre à jour une tâche
  updateTask(taskData, roomId = null) {
    this.send({
      type: 'task_update',
      task_data: taskData,
      room_id: roomId,
    });
  }

  // Mettre à jour le Kanban
  updateKanban(kanbanData, roomId = null) {
    this.send({
      type: 'kanban_update',
      kanban_data: kanbanData,
      room_id: roomId,
    });
  }

  // Démarrer le monitoring PA
  startPAMonitoring(targetUserId) {
    this.send({
      type: 'pa_monitoring',
      target_user_id: targetUserId,
    });
  }

  // Heartbeat
  ping() {
    this.send({
      type: 'ping',
      timestamp: Date.now(),
    });
  }

  // Vérifier si connecté
  isConnected() {
    return this.socket && this.socket.readyState === WebSocket.OPEN;
  }

  // Obtenir le statut de connexion
  getConnectionStatus() {
    if (!this.socket) {
      return 'disconnected';
    }

    switch (this.socket.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting';
      case WebSocket.OPEN:
        return 'connected';
      case WebSocket.CLOSING:
        return 'closing';
      case WebSocket.CLOSED:
        return 'disconnected';
      default:
        return 'unknown';
    }
  }
}

// Instance globale du service WebSocket
const websocketService = new WebSocketService();

export default websocketService; 