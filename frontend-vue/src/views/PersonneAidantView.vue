<template>
  <div class="aidant-container">
    <h2>Connexion Personne Aidant</h2>
    <div class="form-section">
      <input
        v-model="username"
        type="text"
        placeholder="Nom d'utilisateur"
        class="input"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Mot de passe"
        class="input"
      />
      <button class="btn btn-primary" @click="loginPA">Se connecter</button>
    </div>
    <div
      v-if="message"
      :class="{ 'success-message': isSuccess, 'error-message': !isSuccess }"
    >
      {{ message }}
    </div>

    <div class="register-link">
      <p>
        Pas encore de compte ?
        <router-link to="/pa-inscription">S'inscrire comme PA</router-link>
      </p>
    </div>

    <!-- Module IA pour personne aidant : visible seulement si accès autorisé -->
    <div v-if="isAidant" style="margin-top: 32px">
      <button class="btn btn-secondary" @click="showHistoryModal = true">
        🧠 Historique IA du Kanban
      </button>
      <!-- Modal pour l'historique intelligent -->
      <div
        v-if="showHistoryModal"
        class="modal-overlay"
        @click="showHistoryModal = false"
      >
        <div class="modal history-modal" @click.stop>
          <h3>🧠 Historique Intelligent</h3>
          <div class="mode-selector">
            <button
              :class="{ active: historyMode === 'insight' }"
              @click="setHistoryMode('insight')"
            >
              Analyse IA
            </button>
            <button
              :class="{ active: historyMode === 'etat' }"
              @click="setHistoryMode('etat')"
            >
              État Kanban
            </button>
            <button
              :class="{ active: historyMode === 'journal' }"
              @click="setHistoryMode('journal')"
            >
              Journal
            </button>
          </div>
          <div v-if="historyLoading" class="loading-indicator">
            <div class="loading-spinner"></div>
            <p>Analyse en cours...</p>
          </div>
          <div v-else>
            <div v-if="historyData">
              <div v-if="historyData.type === 'insight'">
                <div class="history-summary">
                  <h4>📊 Résumé</h4>
                  <p>{{ historyData.summary }}</p>
                </div>
                <div class="history-insights">
                  <h4>💡 Insights</h4>
                  <ul>
                    <li
                      v-for="insight in historyData.insights"
                      :key="insight.label"
                    >
                      <strong>{{ insight.label }} :</strong> {{ insight.value }}
                    </li>
                  </ul>
                </div>
                <div class="history-recommendations">
                  <h4>🎯 Recommandations</h4>
                  <ul>
                    <li v-for="rec in historyData.recommendations" :key="rec">
                      {{ rec }}
                    </li>
                  </ul>
                </div>
              </div>
              <div v-else-if="historyData.type === 'etat'">
                <h4>📋 État Kanban</h4>
                <div class="kanban-snapshot">
                  <div
                    v-for="(tasks, col) in historyData.kanban"
                    :key="col"
                    class="kanban-col-snap"
                  >
                    <h5>{{ col }}</h5>
                    <ul>
                      <li v-for="task in tasks" :key="task.id || task._id">
                        {{ task.title }}
                        <span v-if="task.due_date"
                          >({{ formatDate(task.due_date) }})</span
                        >
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div v-else-if="historyData.type === 'journal'">
                <h4>🕒 Journal d'activité</h4>
                <ul>
                  <li
                    v-for="event in historyData.events"
                    :key="event.date + event.task"
                  >
                    <span>{{ formatDate(event.date) }}</span> —
                    <strong>{{ event.task }}</strong> {{ event.action }}
                  </li>
                </ul>
              </div>
            </div>
            <div v-else>
              <p>Aucune donnée d'historique disponible.</p>
            </div>
          </div>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="showHistoryModal = false">
              Fermer
            </button>
          </div>
        </div>
      </div>
    </div>
    <div style="margin-top: 32px">
      <h3>Mes délégations</h3>
      <div v-if="loadingDelegations">Chargement...</div>
      <div v-else>
        <div v-if="delegations.length === 0">Aucune délégation trouvée.</div>
        <ul v-else>
          <li
            v-for="deleg in delegations"
            :key="deleg._id"
            style="margin-bottom: 12px"
          >
            <span>{{ deleg.nom }} {{ deleg.prenom }} ({{ deleg.status }})</span>
            <button
              v-if="deleg.status === 'pending'"
              class="btn btn-primary"
              style="margin-left: 12px"
              @click="acceptDelegation(deleg._id)"
            >
              Accepter
            </button>
            <span
              v-else-if="deleg.status === 'accepted'"
              style="color: green; margin-left: 12px"
              >✔ Acceptée</span
            >
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive, watch, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../stores/auth';

  const username = ref('');
  const password = ref('');
  const message = ref('');
  const isSuccess = ref(false);
  const router = useRouter();
  const authStore = useAuthStore();

  const showHistoryModal = ref(false);
  const historyLoading = ref(false);
  const historyData = ref(null);
  const historyMode = ref('insight');

  const delegations = ref([]);
  const loadingDelegations = ref(false);

  const setHistoryMode = mode => {
    historyMode.value = mode;
    loadHistory();
  };

  const formatDate = dateString => {
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  const loadHistory = async () => {
    historyLoading.value = true;
    try {
      // Appel API à adapter pour l'aidant (ex: /api/ia/history?aidant_email=...)
      const response = await axios.get('/api/ia/history', {
        params: { aidant_email: username.value },
      });
      if (response.data) {
        historyData.value = response.data;
      } else {
        throw new Error("Aucune donnée reçue de l'API");
      }
    } catch (error) {
      historyData.value = {
        summary: "Impossible de charger l'analyse IA pour le moment",
        insights: ['Vérifiez votre connexion internet'],
        recommendations: ["Utilisez le chat IA pour obtenir de l'aide"],
        productivity_score: 0.5,
        completion_rate: 0.5,
        task_distribution: {},
      };
    } finally {
      historyLoading.value = false;
    }
  };

  watch(showHistoryModal, async newValue => {
    if (newValue) {
      await loadHistory();
    }
  });

  async function fetchDelegations() {
    loadingDelegations.value = true;
    try {
      const res = await axios.get('/delegations/mine', {
        withCredentials: true,
      });
      console.log('DEBUG delegations:', res.data);
      delegations.value = res.data;
    } catch (e) {
      delegations.value = [];
    } finally {
      loadingDelegations.value = false;
    }
  }

  async function acceptDelegation(delegationId) {
    try {
      await axios.post(
        `/delegations/accept`,
        { delegation_id: delegationId },
        { withCredentials: true }
      );
      await fetchDelegations();
    } catch (e) {
      alert("Erreur lors de l'acceptation de la délégation");
    }
  }

  onMounted(() => {
    fetchDelegations();
  });

  const loginPA = async () => {
    message.value = '';
    isSuccess.value = false;

    if (!username.value || !password.value) {
      message.value = 'Veuillez remplir tous les champs.';
      return;
    }

    try {
      const response = await axios.post(
        'http://localhost:8000/api/auth/login',
        {
          username: username.value,
          password: password.value,
        }
      );

      const data = response.data;

      if (response.status === 200 && data.success) {
        // Vérifier que l'utilisateur est bien une PA
        if (data.data.user.role === 'pa') {
          // Mettre à jour le store d'authentification
          authStore.setToken(data.data.access_token);
          authStore.setUser(data.data.user);

          message.value = 'Connexion réussie ! Redirection...';
          isSuccess.value = true;

          // Rediriger vers le dashboard PA
          setTimeout(() => {
            router.push('/pa-dashboard');
          }, 1500);
        } else {
          message.value = "Ce compte n'est pas une personne aidante.";
          isSuccess.value = false;
        }
      } else {
        message.value = data.message || 'Erreur de connexion.';
        isSuccess.value = false;
      }
    } catch (error) {
      console.error('Erreur:', error);
      message.value = 'Erreur de connexion au serveur.';
      isSuccess.value = false;
    }
  };
</script>

<style scoped>
  .aidant-container {
    max-width: 400px;
    margin: 60px auto;
    padding: 32px;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    text-align: center;
  }
  .input {
    width: 80%;
    padding: 8px;
    margin-bottom: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .btn {
    padding: 8px 18px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .btn-primary {
    background: #6366f1;
    color: #fff;
    margin-left: 8px;
  }
  .btn-success {
    background: #22c55e;
    color: #fff;
  }
  .success-message {
    color: #22c55e;
    margin-top: 10px;
  }
  .error-message {
    color: #ef4444;
    margin-top: 10px;
  }

  .register-link {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #e5e7eb;
  }

  .register-link a {
    color: #6366f1;
    text-decoration: none;
    font-weight: 600;
  }

  .register-link a:hover {
    text-decoration: underline;
  }
</style>
