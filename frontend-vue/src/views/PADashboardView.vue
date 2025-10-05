<template>
  <div class="pa-dashboard">
    <div class="dashboard-header">
      <h1>👥 Dashboard Personne Aidante</h1>
      <p>Bienvenue {{ user?.full_name || user?.username }}</p>
    </div>

    <div class="dashboard-content">
      <!-- Section Accès Kanban -->
      <div class="section kanban-access">
        <h2>📋 Accès au Kanban</h2>
        <div class="access-controls">
          <div v-if="!hasKanbanAccess" class="access-request">
            <p>Demander un accès temporaire au Kanban d'un utilisateur</p>
            <div class="otp-form">
              <input
                v-model="userPhone"
                type="tel"
                placeholder="Téléphone de l'utilisateur (ex: 0123456789)"
                class="input"
              />
              <button
                :disabled="!userPhone || otpLoading"
                class="btn btn-primary"
                @click="requestOTP"
              >
                <span v-if="otpLoading">⏳ Envoi...</span>
                <span v-else>📱 Demander le code OTP</span>
              </button>
            </div>

            <div v-if="otpSent" class="otp-verification">
              <p>Code OTP envoyé ! Entrez le code reçu :</p>
              <input
                v-model="otpCode"
                type="text"
                placeholder="Code à 6 chiffres"
                maxlength="6"
                class="input otp-input"
              />
              <button
                :disabled="!otpCode || verifyLoading"
                class="btn btn-success"
                @click="verifyOTP"
              >
                <span v-if="verifyLoading">⏳ Vérification...</span>
                <span v-else>✅ Valider l'accès</span>
              </button>
            </div>
          </div>

          <div v-else class="access-granted">
            <div class="success-banner">
              <span>✅ Accès temporaire accordé</span>
              <button class="btn btn-danger" @click="revokeAccess">
                Révoquer l'accès
              </button>
            </div>
            <div class="access-info">
              <p>
                <strong>Utilisateur :</strong> {{ currentAccess.user_name }}
              </p>
              <p><strong>Expire dans :</strong> {{ formatTimeLeft }}</p>
            </div>
            <router-link to="/tasks" class="btn btn-primary btn-large">
              🚀 Accéder au Kanban
            </router-link>
          </div>
        </div>
      </div>

      <!-- Section Mes Délégations -->
      <div class="section delegations">
        <h2>🤝 Mes Délégations</h2>
        <div v-if="loadingDelegations" class="loading">
          <div class="spinner"></div>
          <p>Chargement des délégations...</p>
        </div>
        <div v-else>
          <div v-if="delegations.length === 0" class="empty-state">
            <p>Aucune délégation active pour le moment.</p>
            <p>Les utilisateurs peuvent vous inviter à les accompagner.</p>
          </div>
          <div v-else class="delegations-list">
            <div
              v-for="deleg in delegations"
              :key="deleg._id"
              class="delegation-item"
            >
              <div class="delegation-info">
                <h3>{{ deleg.nom }} {{ deleg.prenom }}</h3>
                <p class="email">{{ deleg.email }}</p>
                <span :class="['status', deleg.status]">{{
                  getStatusLabel(deleg.status)
                }}</span>
              </div>
              <div class="delegation-actions">
                <button
                  v-if="deleg.status === 'pending'"
                  class="btn btn-success"
                  @click="acceptDelegation(deleg._id)"
                >
                  ✅ Accepter
                </button>
                <button
                  v-if="deleg.status === 'accepted'"
                  class="btn btn-primary"
                  @click="accessUserKanban(deleg)"
                >
                  📋 Voir Kanban
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Conseils IA -->
      <div class="section ai-advice">
        <h2>🧠 Conseils Personnalisés</h2>
        <div class="ai-controls">
          <button
            :disabled="aiLoading"
            class="btn btn-secondary"
            @click="getAIAdvice"
          >
            <span v-if="aiLoading">⏳ Analyse en cours...</span>
            <span v-else>💡 Obtenir des conseils IA</span>
          </button>
        </div>

        <div v-if="aiAdvice" class="ai-results">
          <div class="advice-card">
            <h3>💡 Recommandations</h3>
            <div v-if="aiAdvice.recommendations" class="recommendations">
              <ul>
                <li
                  v-for="(rec, index) in aiAdvice.recommendations"
                  :key="index"
                >
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>

          <div v-if="aiAdvice.insights" class="insights-card">
            <h3>📊 Insights</h3>
            <div class="insights">
              <div
                v-for="(insight, key) in aiAdvice.insights"
                :key="key"
                class="insight-item"
              >
                <strong>{{ key }}:</strong> {{ insight }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>
</template>

<script>
  import { ref, computed, onMounted, nextTick } from 'vue';
  import { useAuthStore } from '../stores/auth';

  export default {
    name: 'PADashboardView',
    setup() {
      const authStore = useAuthStore();
      const user = computed(() => authStore.user);

      // État de l'accès Kanban
      const hasKanbanAccess = ref(false);
      const userPhone = ref('');
      const otpCode = ref('');
      const otpSent = ref(false);
      const otpLoading = ref(false);
      const verifyLoading = ref(false);
      const currentAccess = ref(null);

      // Délégations
      const delegations = ref([]);
      const loadingDelegations = ref(false);

      // IA
      const aiAdvice = ref(null);
      const aiLoading = ref(false);

      // Messages
      const message = ref('');
      const messageType = ref('');

      // Temps restant pour l'accès
      const formatTimeLeft = computed(() => {
        if (!currentAccess.value?.expires_at) {
          return '';
        }
        const now = new Date();
        const expires = new Date(currentAccess.value.expires_at);
        const diff = expires - now;

        if (diff <= 0) {
          // Utiliser nextTick pour éviter l'effet de bord dans computed
          nextTick(() => {
            hasKanbanAccess.value = false;
          });
          return 'Expiré';
        }

        const minutes = Math.floor(diff / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);
        return `${minutes}m ${seconds}s`;
      });

      // Demander un code OTP
      const requestOTP = async () => {
        if (!userPhone.value) {
          return;
        }

        otpLoading.value = true;
        try {
          const response = await fetch(
            'http://localhost:8000/api/auth/send-otp',
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ phone: userPhone.value }),
            }
          );

          const data = await response.json();

          if (response.ok && data.success) {
            otpSent.value = true;
            showMessage('Code OTP envoyé avec succès', 'success');
          } else {
            showMessage(data.message || "Erreur lors de l'envoi", 'error');
          }
        } catch (error) {
          showMessage('Erreur de connexion', 'error');
        } finally {
          otpLoading.value = false;
        }
      };

      // Vérifier le code OTP
      const verifyOTP = async () => {
        if (!otpCode.value) {
          return;
        }

        verifyLoading.value = true;
        try {
          const response = await fetch(
            'http://localhost:8000/api/auth/verify-otp',
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                phone: userPhone.value,
                code: otpCode.value,
              }),
            }
          );

          const data = await response.json();

          if (response.ok && data.success) {
            hasKanbanAccess.value = true;
            currentAccess.value = {
              user_phone: userPhone.value,
              user_name: `Utilisateur (${userPhone.value})`,
              expires_at: new Date(Date.now() + 30 * 60 * 1000), // 30 minutes
            };
            showMessage('Accès temporaire accordé !', 'success');
          } else {
            showMessage(data.message || 'Code OTP invalide', 'error');
          }
        } catch (error) {
          showMessage('Erreur de connexion', 'error');
        } finally {
          verifyLoading.value = false;
        }
      };

      // Révoquer l'accès
      const revokeAccess = () => {
        hasKanbanAccess.value = false;
        currentAccess.value = null;
        userPhone.value = '';
        otpCode.value = '';
        otpSent.value = false;
        showMessage('Accès révoqué', 'info');
      };

      // Charger les délégations
      const loadDelegations = async () => {
        loadingDelegations.value = true;
        try {
          const response = await fetch(
            'http://localhost:8000/delegations/mine',
            {
              headers: {
                Authorization: `Bearer ${authStore.token}`,
              },
            }
          );

          if (response.ok) {
            const data = await response.json();
            delegations.value = data.delegations || [];
          }
        } catch (error) {
          console.error('Erreur chargement délégations:', error);
        } finally {
          loadingDelegations.value = false;
        }
      };

      // Accepter une délégation
      const acceptDelegation = async delegationId => {
        try {
          const response = await fetch(
            `http://localhost:8000/delegations/${delegationId}/accept`,
            {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${authStore.token}`,
              },
            }
          );

          if (response.ok) {
            showMessage('Délégation acceptée', 'success');
            loadDelegations();
          }
        } catch (error) {
          showMessage("Erreur lors de l'acceptation", 'error');
        }
      };

      // Accéder au Kanban d'un utilisateur
      const accessUserKanban = delegation => {
        // Simuler l'accès temporaire
        hasKanbanAccess.value = true;
        currentAccess.value = {
          user_phone: delegation.telephone,
          user_name: `${delegation.nom} ${delegation.prenom}`,
          expires_at: new Date(Date.now() + 30 * 60 * 1000),
        };
        showMessage(
          `Accès accordé pour ${delegation.nom} ${delegation.prenom}`,
          'success'
        );
      };

      // Obtenir des conseils IA
      const getAIAdvice = async () => {
        aiLoading.value = true;
        try {
          const response = await fetch('http://localhost:8000/api/ia/advice', {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${authStore.token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: user.value.id,
              context: 'pa_dashboard',
            }),
          });

          if (response.ok) {
            const data = await response.json();
            aiAdvice.value = data.advice;
            showMessage('Conseils générés avec succès', 'success');
          } else {
            showMessage('Erreur lors de la génération des conseils', 'error');
          }
        } catch (error) {
          showMessage('Erreur de connexion IA', 'error');
        } finally {
          aiLoading.value = false;
        }
      };

      // Utilitaires
      const getStatusLabel = status => {
        const labels = {
          pending: 'En attente',
          accepted: 'Acceptée',
          revoked: 'Révoquée',
        };
        return labels[status] || status;
      };

      const showMessage = (msg, type = 'info') => {
        message.value = msg;
        messageType.value = type;
        setTimeout(() => {
          message.value = '';
        }, 5000);
      };

      // Initialisation
      onMounted(() => {
        loadDelegations();
      });

      return {
        user,
        hasKanbanAccess,
        userPhone,
        otpCode,
        otpSent,
        otpLoading,
        verifyLoading,
        currentAccess,
        formatTimeLeft,
        delegations,
        loadingDelegations,
        aiAdvice,
        aiLoading,
        message,
        messageType,
        requestOTP,
        verifyOTP,
        revokeAccess,
        acceptDelegation,
        accessUserKanban,
        getAIAdvice,
        getStatusLabel,
      };
    },
  };
</script>

<style scoped>
  .pa-dashboard {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  .dashboard-header {
    text-align: center;
    margin-bottom: 40px;
  }

  .dashboard-header h1 {
    color: #333;
    margin-bottom: 8px;
  }

  .dashboard-header p {
    color: #666;
    font-size: 18px;
  }

  .dashboard-content {
    display: grid;
    gap: 30px;
  }

  .section {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .section h2 {
    color: #333;
    margin-bottom: 20px;
    font-size: 20px;
  }

  /* Accès Kanban */
  .access-controls {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .otp-form {
    display: flex;
    gap: 12px;
    align-items: end;
  }

  .otp-form .input {
    flex: 1;
  }

  .otp-verification {
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #e9ecef;
  }

  .otp-input {
    max-width: 200px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 2px;
  }

  .access-granted {
    background: #d4edda;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #c3e6cb;
  }

  .success-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .access-info {
    margin-bottom: 16px;
  }

  .access-info p {
    margin: 4px 0;
  }

  /* Délégations */
  .delegations-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .delegation-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    background: #f8f9fa;
  }

  .delegation-info h3 {
    margin: 0 0 4px 0;
    color: #333;
  }

  .delegation-info .email {
    color: #666;
    margin: 0 0 8px 0;
  }

  .status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
  }

  .status.pending {
    background: #fff3cd;
    color: #856404;
  }

  .status.accepted {
    background: #d4edda;
    color: #155724;
  }

  .status.revoked {
    background: #f8d7da;
    color: #721c24;
  }

  .delegation-actions {
    display: flex;
    gap: 8px;
  }

  /* IA */
  .ai-controls {
    margin-bottom: 20px;
  }

  .ai-results {
    display: grid;
    gap: 20px;
  }

  .advice-card,
  .insights-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e9ecef;
  }

  .advice-card h3,
  .insights-card h3 {
    margin: 0 0 16px 0;
    color: #333;
  }

  .recommendations ul {
    margin: 0;
    padding-left: 20px;
  }

  .recommendations li {
    margin-bottom: 8px;
    color: #555;
  }

  .insights {
    display: grid;
    gap: 8px;
  }

  .insight-item {
    padding: 8px;
    background: white;
    border-radius: 4px;
    border: 1px solid #e9ecef;
  }

  /* États */
  .empty-state {
    text-align: center;
    color: #666;
    padding: 40px 20px;
  }

  .loading {
    text-align: center;
    padding: 40px 20px;
  }

  .spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #007bff;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  /* Messages */
  .message {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    z-index: 1000;
    max-width: 300px;
  }

  .message.success {
    background: #28a745;
  }

  .message.error {
    background: #dc3545;
  }

  .message.info {
    background: #17a2b8;
  }

  /* Boutons */
  .btn {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    text-align: center;
  }

  .btn-primary {
    background: #007bff;
    color: white;
  }

  .btn-primary:hover {
    background: #0056b3;
  }

  .btn-success {
    background: #28a745;
    color: white;
  }

  .btn-success:hover {
    background: #1e7e34;
  }

  .btn-secondary {
    background: #6c757d;
    color: white;
  }

  .btn-secondary:hover {
    background: #545b62;
  }

  .btn-danger {
    background: #dc3545;
    color: white;
  }

  .btn-danger:hover {
    background: #c82333;
  }

  .btn-large {
    padding: 12px 24px;
    font-size: 16px;
  }

  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Inputs */
  .input {
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
  }

  .input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .pa-dashboard {
      padding: 10px;
    }

    .otp-form {
      flex-direction: column;
    }

    .delegation-item {
      flex-direction: column;
      gap: 12px;
      align-items: stretch;
    }

    .success-banner {
      flex-direction: column;
      gap: 12px;
    }
  }
</style>
