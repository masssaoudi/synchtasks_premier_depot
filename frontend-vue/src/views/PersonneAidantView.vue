<template>
  <div class="aidant-container">
    <h2>Accès Personne Aidant</h2>
    <div class="form-section">
      <input v-model="email" type="email" placeholder="Entrez votre email ou identifiant" class="input" />
      <button @click="checkAidant" class="btn btn-primary">Valider</button>
    </div>
    <div v-if="message" :class="{'success-message': isAidant, 'error-message': !isAidant}">{{ message }}</div>
    <button :disabled="!isAidant" @click="goToKanban" class="btn btn-success" style="margin-top: 20px;">Accès au Kanban</button>

    <!-- Module IA pour personne aidant : visible seulement si accès autorisé -->
    <div v-if="isAidant" style="margin-top: 32px;">
      <button @click="showHistoryModal = true" class="btn btn-secondary">
        🧠 Historique IA du Kanban
      </button>
      <!-- Modal pour l'historique intelligent -->
      <div v-if="showHistoryModal" class="modal-overlay" @click="showHistoryModal = false">
        <div class="modal history-modal" @click.stop>
          <h3>🧠 Historique Intelligent</h3>
          <div class="mode-selector">
            <button :class="{active: historyMode === 'insight'}" @click="setHistoryMode('insight')">Analyse IA</button>
            <button :class="{active: historyMode === 'etat'}" @click="setHistoryMode('etat')">État Kanban</button>
            <button :class="{active: historyMode === 'journal'}" @click="setHistoryMode('journal')">Journal</button>
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
                    <li v-for="insight in historyData.insights" :key="insight.label">
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
                  <div v-for="(tasks, col) in historyData.kanban" :key="col" class="kanban-col-snap">
                    <h5>{{ col }}</h5>
                    <ul>
                      <li v-for="task in tasks" :key="task.id || task._id">
                        {{ task.title }} <span v-if="task.due_date">({{ formatDate(task.due_date) }})</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div v-else-if="historyData.type === 'journal'">
                <h4>🕒 Journal d'activité</h4>
                <ul>
                  <li v-for="event in historyData.events" :key="event.date + event.task">
                    <span>{{ formatDate(event.date) }}</span> — <strong>{{ event.task }}</strong> {{ event.action }}
                  </li>
                </ul>
              </div>
            </div>
            <div v-else>
              <p>Aucune donnée d'historique disponible.</p>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="showHistoryModal = false" class="btn btn-secondary">
              Fermer
            </button>
          </div>
        </div>
      </div>
    </div>
    <div style="margin-top: 32px;">
      <h3>Mes délégations</h3>
      <div v-if="loadingDelegations">Chargement...</div>
      <div v-else>
        <div v-if="delegations.length === 0">Aucune délégation trouvée.</div>
        <ul v-else>
          <li v-for="deleg in delegations" :key="deleg._id" style="margin-bottom: 12px;">
            <span>{{ deleg.nom }} {{ deleg.prenom }} ({{ deleg.status }})</span>
            <button v-if="deleg.status === 'pending'" @click="acceptDelegation(deleg._id)" class="btn btn-primary" style="margin-left: 12px;">Accepter</button>
            <span v-else-if="deleg.status === 'accepted'" style="color: green; margin-left: 12px;">✔ Acceptée</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const isAidant = ref(false)
const message = ref('')
const router = useRouter()

const showHistoryModal = ref(false)
const historyLoading = ref(false)
const historyData = ref(null)
const historyMode = ref('insight')

const delegations = ref([])
const loadingDelegations = ref(false)

const setHistoryMode = (mode) => {
  historyMode.value = mode
  loadHistory()
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('fr-FR')
}

const loadHistory = async () => {
  historyLoading.value = true
  try {
    // Appel API à adapter pour l'aidant (ex: /api/ia/history?aidant_email=...)
    const response = await axios.get('/api/ia/history', { params: { aidant_email: email.value } })
    if (response.data) {
      historyData.value = response.data
    } else {
      throw new Error('Aucune donnée reçue de l\'API')
    }
  } catch (error) {
    historyData.value = {
      summary: "Impossible de charger l'analyse IA pour le moment",
      insights: ["Vérifiez votre connexion internet"],
      recommendations: ["Utilisez le chat IA pour obtenir de l'aide"],
      productivity_score: 0.5,
      completion_rate: 0.5,
      task_distribution: {}
    }
  } finally {
    historyLoading.value = false
  }
}

watch(showHistoryModal, async (newValue) => {
  if (newValue) {
    await loadHistory()
  }
})

async function fetchDelegations() {
  loadingDelegations.value = true
  try {
    const res = await axios.get('/delegations/mine', { withCredentials: true })
    console.log('DEBUG delegations:', res.data)
    delegations.value = res.data
  } catch (e) {
    delegations.value = []
  } finally {
    loadingDelegations.value = false
  }
}

async function acceptDelegation(delegationId) {
  try {
    await axios.post(`/delegations/accept`, { delegation_id: delegationId }, { withCredentials: true })
    await fetchDelegations()
  } catch (e) {
    alert('Erreur lors de l\'acceptation de la délégation')
  }
}

onMounted(() => {
  fetchDelegations()
})

const checkAidant = async () => {
  message.value = ''
  isAidant.value = false
  if (!email.value) {
    message.value = "Veuillez entrer un email."
    return
  }
  try {
    const response = await axios.post('/delegations/check_aidant_email', null, { params: { email: email.value } })
    if (response.data.is_aidant) {
      isAidant.value = true
      message.value = "Accès autorisé. Vous pouvez accéder au Kanban."
    } else {
      message.value = "Cet email n'est pas reconnu comme personne aidante acceptée."
    }
  } catch (error) {
    message.value = "Erreur lors de la vérification."
  }
}

const goToKanban = () => {
  // Rediriger vers la vue Kanban dédiée à l'aidant (à adapter selon le routing)
  router.push({ name: 'TasksView' })
}
</script>

<style scoped>
.aidant-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 32px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
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
</style> 