<template>
  <div class="tasks-page">
    <div class="tasks-header">
      <h1>📋 Mes Tâches</h1>
      <div class="header-actions">
        <button class="btn btn-secondary" @click="showHistoryModal = true">
          🧠 Historique IA
        </button>
        <button class="btn btn-primary" @click="showNewTaskModal = true">
          ➕ Nouvelle tâche
        </button>
        <button class="btn btn-info" @click="showChatModal = true">
          🤖 Chat IA
        </button>
      </div>
    </div>

    <!-- Messages d'alerte -->
    <div
      v-if="alert"
      :class="[
        'alert',
        alert.type === 'success' ? 'alert-success' : 'alert-error',
      ]"
    >
      {{ alert.message }}
    </div>

    <!-- Indicateur de chargement -->
    <div v-if="loading" class="loading-indicator">
      <div class="loading-spinner"></div>
      <p>Chargement des tâches...</p>
    </div>

    <!-- Tableau de tâches simple -->
    <div class="tasks-grid">
      <!-- Section À faire -->
      <div class="tasks-section">
        <h3>📝 À faire</h3>
        <div class="tasks-list">
          <div v-for="task in todoTasks" :key="task._id" class="task-card">
            <div class="task-header">
              <h4>{{ task.title }}</h4>
              <div class="task-actions">
                <button
                  class="btn btn-success btn-sm"
                  @click="changeTaskStatus(task, 'done')"
                >
                  ✅ Terminer
                </button>
                <button
                  class="btn btn-secondary btn-sm"
                  @click="editTask(task)"
                >
                  ✏️
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteTask(task)">
                  🗑️
                </button>
              </div>
            </div>
            <p class="task-description">{{ task.description }}</p>
            <div class="task-meta">
              <span class="category" :class="`category-${task.category}`">
                {{ getCategoryIcon(task.category) }}
                {{ getCategoryLabel(task.category) }}
              </span>
              <span class="priority" :class="`priority-${task.priority}`">
                {{ getPriorityLabel(task.priority) }}
              </span>
              <span v-if="task.due_date" class="due-date">
                📅 {{ formatDate(task.due_date) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Terminé -->
      <div class="tasks-section">
        <h3>✅ Terminé</h3>
        <div class="tasks-list">
          <div
            v-for="task in completedTasks"
            :key="task._id"
            class="task-card completed"
          >
            <div class="task-header">
              <h4>{{ task.title }}</h4>
              <div class="task-actions">
                <button
                  class="btn btn-warning btn-sm"
                  @click="changeTaskStatus(task, 'todo')"
                >
                  🔄 Remettre en cours
                </button>
                <button
                  class="btn btn-secondary btn-sm"
                  @click="editTask(task)"
                >
                  ✏️
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteTask(task)">
                  🗑️
                </button>
              </div>
            </div>
            <p class="task-description">{{ task.description }}</p>
            <div class="task-meta">
              <span class="category" :class="`category-${task.category}`">
                {{ getCategoryIcon(task.category) }}
                {{ getCategoryLabel(task.category) }}
              </span>
              <span class="priority" :class="`priority-${task.priority}`">
                {{ getPriorityLabel(task.priority) }}
              </span>
              <span v-if="task.due_date" class="due-date">
                📅 {{ formatDate(task.due_date) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal pour nouvelle tâche -->
    <div
      v-if="showNewTaskModal"
      class="modal-overlay"
      @click="showNewTaskModal = false"
    >
      <div class="modal" @click.stop>
        <h3>Nouvelle tâche</h3>
        <form @submit.prevent="createTask">
          <div class="form-group">
            <label for="title">Titre</label>
            <input
              id="title"
              v-model="newTask.title"
              type="text"
              required
              placeholder="Titre de la tâche"
            />
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="newTask.description"
              placeholder="Description de la tâche"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="category">Catégorie</label>
            <select id="category" v-model="newTask.category" required>
              <option value="">Sélectionner une catégorie</option>
              <option
                v-for="category in categories"
                :key="category.value"
                :value="category.value"
              >
                {{ category.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="priority">Priorité</label>
            <select id="priority" v-model="newTask.priority" required>
              <option value="">Sélectionner une priorité</option>
              <option
                v-for="priority in priorities"
                :key="priority.value"
                :value="priority.value"
              >
                {{ priority.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="due_date">Date d'échéance</label>
            <input id="due_date" v-model="newTask.due_date" type="date" />
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">
              Créer la tâche
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              @click="showNewTaskModal = false"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal pour éditer une tâche -->
    <div
      v-if="showEditTaskModal"
      class="modal-overlay"
      @click="showEditTaskModal = false"
    >
      <div class="modal" @click.stop>
        <h3>✏️ Modifier la tâche</h3>
        <form @submit.prevent="updateTask">
          <div class="form-group">
            <label for="edit-title">Titre</label>
            <input
              id="edit-title"
              v-model="editingTask.title"
              type="text"
              required
              placeholder="Titre de la tâche"
            />
          </div>

          <div class="form-group">
            <label for="edit-description">Description</label>
            <textarea
              id="edit-description"
              v-model="editingTask.description"
              placeholder="Description de la tâche"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="edit-category">Catégorie</label>
            <select id="edit-category" v-model="editingTask.category" required>
              <option value="">Sélectionner une catégorie</option>
              <option
                v-for="category in categories"
                :key="category.value"
                :value="category.value"
              >
                {{ category.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="edit-priority">Priorité</label>
            <select id="edit-priority" v-model="editingTask.priority" required>
              <option value="">Sélectionner une priorité</option>
              <option
                v-for="priority in priorities"
                :key="priority.value"
                :value="priority.value"
              >
                {{ priority.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="edit-due_date">Date d'échéance</label>
            <input
              id="edit-due_date"
              v-model="editingTask.due_date"
              type="date"
            />
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Mettre à jour</button>
            <button
              type="button"
              class="btn btn-secondary"
              @click="showEditTaskModal = false"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal pour historique IA -->
    <div
      v-if="showHistoryModal"
      class="modal-overlay"
      @click="showHistoryModal = false"
    >
      <div class="history-modal" @click.stop>
        <div class="modal-header">
          <h3>🧠 Historique IA</h3>
          <button class="btn btn-secondary" @click="showHistoryModal = false">
            ✕
          </button>
        </div>

        <div v-if="historyLoading" class="loading-indicator">
          <div class="loading-spinner"></div>
          <p>Chargement de l'historique...</p>
        </div>

        <div v-else-if="historyData" class="history-content">
          <!-- Résumé principal -->
          <div class="history-summary">
            <h4>📊 Résumé de l'activité</h4>
            <div class="summary-content" v-html="historyData.summary"></div>
          </div>

          <!-- Métriques -->
          <div v-if="historyData.analytics" class="history-metrics">
            <h4>📈 Métriques</h4>
            <div class="metrics-grid">
              <div class="metric-card">
                <div class="metric-value">
                  {{ historyData.analytics.total_interactions }}
                </div>
                <div class="metric-label">Interactions</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">
                  {{ historyData.analytics.average_satisfaction }}/5
                </div>
                <div class="metric-label">Satisfaction</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">
                  {{
                    Math.round(historyData.analytics.productivity_score * 100)
                  }}%
                </div>
                <div class="metric-label">Productivité</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">
                  {{ Math.round(historyData.analytics.completion_rate * 100) }}%
                </div>
                <div class="metric-label">Complétion</div>
              </div>
            </div>
          </div>

          <!-- Insights -->
          <div class="history-insights">
            <h4>💡 Insights</h4>
            <ul>
              <li v-for="insight in historyData.insights" :key="insight">
                {{ insight }}
              </li>
            </ul>
          </div>

          <!-- Recommandations -->
          <div class="history-recommendations">
            <h4>🎯 Recommandations</h4>
            <ul>
              <li
                v-for="recommendation in historyData.recommendations"
                :key="recommendation"
              >
                {{ recommendation }}
              </li>
            </ul>
          </div>

          <!-- Tendances -->
          <div
            v-if="historyData.trends && historyData.trends.length > 0"
            class="history-trends"
          >
            <h4>📈 Tendances observées</h4>
            <ul>
              <li v-for="trend in historyData.trends" :key="trend">
                {{ trend }}
              </li>
            </ul>
          </div>

          <!-- Opportunités -->
          <div
            v-if="
              historyData.opportunities && historyData.opportunities.length > 0
            "
            class="history-opportunities"
          >
            <h4>🚀 Opportunités d'amélioration</h4>
            <ul>
              <li
                v-for="opportunity in historyData.opportunities"
                :key="opportunity"
              >
                {{ opportunity }}
              </li>
            </ul>
          </div>

          <!-- Interactions récentes -->
          <div
            v-if="
              historyData.interactions && historyData.interactions.length > 0
            "
            class="history-interactions"
          >
            <h4>🕒 Interactions récentes</h4>
            <div class="interactions-list">
              <div
                v-for="interaction in historyData.interactions.slice(0, 3)"
                :key="interaction.id || interaction.timestamp"
                class="interaction-item"
              >
                <div class="interaction-header">
                  <span class="interaction-type">{{ interaction.type }}</span>
                  <span class="interaction-time">{{
                    formatDate(interaction.timestamp)
                  }}</span>
                </div>
                <div class="interaction-content">
                  <p v-if="interaction.message" class="interaction-message">
                    {{ interaction.message }}
                  </p>
                  <p v-if="interaction.response" class="interaction-response">
                    {{ interaction.response.substring(0, 100) }}...
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-history">
          <p>Aucun historique disponible pour le moment.</p>
        </div>
      </div>
    </div>

    <!-- Modal Chat IA -->
    <AIChatModal :show="showChatModal" @close="showChatModal = false" />
  </div>
</template>

<script>
  import { ref, reactive, onMounted, watch } from 'vue';
  import axios from 'axios';
  import Datepicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';
  import draggable from 'vuedraggable';
  import AIChatModal from '../components/AIChatModal.vue';

  export default {
    name: 'TasksView',
    components: { Datepicker, draggable, AIChatModal },
    setup() {
      const tasks = ref([]);
      const loading = ref(false);
      const categories = ref([]);
      const priorities = ref([]);

      const showNewTaskModal = ref(false);
      const showEditTaskModal = ref(false);
      const alert = ref(null);

      const newTask = reactive({
        title: '',
        description: '',
        category: '',
        priority: 'normale',
        due_date: '',
      });

      const editingTask = reactive({
        _id: '',
        title: '',
        description: '',
        category: '',
        priority: 'normale',
        due_date: '',
      });

      const showHistoryModal = ref(false);
      const historyLoading = ref(false);
      const historyData = ref(null);
      const historyMode = ref('insight');
      const showChatModal = ref(false);

      const showAlert = (message, type = 'success') => {
        alert.value = { message, type };
        setTimeout(() => {
          alert.value = null;
        }, 3000);
      };

      const loadCategories = async () => {
        try {
          const response = await axios.get('/api/tasks/categories/');
          categories.value = response.data.categories;
        } catch (error) {
          console.error('Erreur lors du chargement des catégories:', error);
        }
      };

      const loadPriorities = async () => {
        try {
          const response = await axios.get('/api/tasks/priorities/');
          priorities.value = response.data.priorities;
          // Définir la priorité par défaut
          if (priorities.value.length > 0) {
            newTask.priority =
              priorities.value.find(p => p.value === 'normale')?.value ||
              priorities.value[0].value;
          }
        } catch (error) {
          console.error('Erreur lors du chargement des priorités:', error);
        }
      };

      const loadTasks = async () => {
        loading.value = true;
        try {
          const response = await axios.get('/api/tasks/');
          tasks.value = response.data;
          showAlert('Tâches chargées avec succès');
        } catch (error) {
          console.error('Erreur lors du chargement des tâches:', error);
          showAlert('Erreur lors du chargement des tâches', 'error');
        } finally {
          loading.value = false;
        }
      };

      const createTask = async () => {
        try {
          const taskData = {
            title: newTask.title,
            description: newTask.description,
            priority: newTask.priority,
            category: newTask.category,
            due_date: newTask.due_date
              ? new Date(newTask.due_date).toISOString()
              : null,
          };

          const response = await axios.post('/api/tasks/', taskData);
          tasks.value.push(response.data);

          // Réinitialiser le formulaire
          newTask.title = '';
          newTask.description = '';
          newTask.category = '';
          newTask.priority =
            priorities.value.find(p => p.value === 'normale')?.value ||
            priorities.value[0]?.value ||
            'normale';
          newTask.due_date = '';

          showNewTaskModal.value = false;
          showAlert('Tâche créée avec succès');
        } catch (error) {
          console.error('Erreur lors de la création de la tâche:', error);
          showAlert('Erreur lors de la création de la tâche', 'error');
        }
      };

      const editTask = task => {
        console.log('✏️ Édition de la tâche :', task);
        // Préparer les données pour l'édition
        editingTask._id = task._id;
        editingTask.title = task.title;
        editingTask.description = task.description || '';
        editingTask.category = task.category;
        editingTask.priority = task.priority;
        editingTask.due_date = task.due_date ? task.due_date.split('T')[0] : '';
        showEditTaskModal.value = true;
      };

      const updateTask = async () => {
        try {
          const taskData = {
            title: editingTask.title,
            description: editingTask.description,
            priority: editingTask.priority,
            category: editingTask.category,
            due_date: editingTask.due_date
              ? new Date(editingTask.due_date).toISOString()
              : null,
          };

          const response = await axios.put(
            `/api/tasks/${editingTask._id}`,
            taskData
          );

          // Mettre à jour la tâche dans la liste
          const index = tasks.value.findIndex(t => t._id === editingTask._id);
          if (index !== -1) {
            tasks.value[index] = response.data;
          }

          showEditTaskModal.value = false;
          showAlert('Tâche mise à jour avec succès');
        } catch (error) {
          console.error('Erreur lors de la mise à jour de la tâche:', error);
          showAlert('Erreur lors de la mise à jour de la tâche', 'error');
        }
      };

      const formatDate = dateString => {
        return new Date(dateString).toLocaleDateString('fr-FR');
      };

      const getCategoryIcon = category => {
        const categoryData = categories.value.find(c => c.value === category);
        return categoryData?.icon || '📋';
      };

      const getCategoryLabel = category => {
        const categoryData = categories.value.find(c => c.value === category);
        return categoryData?.label || category;
      };

      const getPriorityLabel = priority => {
        const priorityData = priorities.value.find(p => p.value === priority);
        return priorityData?.label || priority;
      };

      const loadHistory = async () => {
        historyLoading.value = true;
        try {
          console.log("🔄 Chargement de l'historique IA...");
          const response = await axios.get('/api/ia/history');

          if (response.data) {
            historyData.value = response.data;
            console.log('✅ Historique IA chargé:', historyData.value);
          } else {
            throw new Error("Aucune donnée reçue de l'API");
          }
        } catch (error) {
          console.error("❌ Erreur lors du chargement de l'historique:", error);
          // Données de fallback en cas d'erreur
          historyData.value = {
            summary: "Impossible de charger l'analyse IA pour le moment",
            insights: ['Vérifiez votre connexion internet'],
            recommendations: ["Utilisez le chat IA pour obtenir de l'aide"],
            productivity_score: 0.5,
            completion_rate: 0.5,
            task_distribution: {},
          };
          showAlert("Erreur lors du chargement de l'historique", 'error');
        } finally {
          historyLoading.value = false;
        }
      };

      const handleTaskCompletion = async (
        taskId,
        action,
        keepMemory = true
      ) => {
        try {
          const response = await axios.post('/api/ia/complete-task', {
            task_id: taskId,
            action: action,
            keep_memory: keepMemory,
          });

          if (response.data.success) {
            showAlert(response.data.message);
            await loadTasks(); // Recharger les tâches
          }
        } catch (error) {
          console.error('Erreur lors de la gestion de la tâche:', error);
          showAlert('Erreur lors de la gestion de la tâche', 'error');
        }
      };

      onMounted(async () => {
        await loadCategories();
        await loadPriorities();
        await loadTasks();
      });

      // Charger l'historique quand la modal s'ouvre
      watch(showHistoryModal, async newValue => {
        if (newValue && !historyData.value) {
          await loadHistory();
        }
      });

      // Ajout des listes réactives pour chaque colonne
      const todoTasks = ref([]);
      const completedTasks = ref([]);

      // État pour le bouton de sauvegarde
      // const hasUnsavedChanges = ref(false) // Supprimé
      // const isSaving = ref(false) // Supprimé

      // Fonction pour répartir les tâches dans les colonnes
      const distributeTasks = () => {
        todoTasks.value = tasks.value.filter(t => t.status === 'todo');
        completedTasks.value = tasks.value.filter(t => t.status === 'done'); // Corrigé : 'done' au lieu de 'completed'
      };

      // Appeler distributeTasks à chaque chargement ou modification des tâches
      watch(tasks, distributeTasks, { immediate: true, deep: true });

      // Fonction pour gérer le début du drag
      const onDragStart = evt => {
        console.log('🎯 onDragStart appelée avec:', evt);
      };

      // Fonction simple pour changer le statut d'une tâche
      const changeTaskStatus = async (task, newStatus) => {
        console.log('🎯 === DÉBUT changeTaskStatus ===');
        console.log('🎯 Tâche:', task.title);
        console.log('🎯 Nouveau statut:', newStatus);

        try {
          const taskId = task._id || task.id;
          console.log('🎯 TaskId:', taskId);

          if (!taskId) {
            console.error('❌ ID de tâche introuvable');
            showAlert('Erreur: ID de tâche manquant', 'error');
            return;
          }

          console.log('🎯 Envoi PATCH avec:', { status: newStatus });
          console.log('🎯 URL:', `/api/tasks/${taskId}`);

          const response = await axios.patch(`/api/tasks/${taskId}`, {
            status: newStatus,
          });
          console.log('🎯 Réponse PATCH:', response);

          // Mettre à jour la tâche localement
          task.status = newStatus;

          // Recharger les tâches pour s'assurer de la synchronisation
          await loadTasks();

          const statusText = newStatus === 'done' ? 'Terminé' : 'À faire';
          showAlert(
            `Tâche "${task.title}" marquée comme ${statusText} !`,
            'success'
          );

          console.log('🎯 === FIN changeTaskStatus (SUCCÈS) ===');
        } catch (err) {
          console.error('🎯 === ERREUR changeTaskStatus ===');
          console.error('❌ Erreur de mise à jour :', err);
          console.error("❌ Détails de l'erreur:", err.response?.data);
          showAlert('❌ Erreur lors du changement de statut', 'error');
        }
      };

      // Suppression d'une tâche
      const deleteTask = async task => {
        console.log('🗑️ Tentative de suppression de la tâche :', task);

        if (!task) {
          console.error('❌ Aucune tâche fournie pour la suppression');
          showAlert('Erreur : aucune tâche sélectionnée', 'error');
          return;
        }

        // Fonction pour charger l'historique IA
        const loadHistory = async () => {
          historyLoading.value = true;
          try {
            console.log("🔄 Chargement de l'historique IA...");
            const response = await axios.get(
              '/api/ia/history?mode=insight&days=30'
            );

            if (response.data) {
              historyData.value = response.data;
              console.log('✅ Historique IA chargé:', historyData.value);
            } else {
              throw new Error("Aucune donnée reçue de l'API");
            }
          } catch (error) {
            console.error(
              "❌ Erreur lors du chargement de l'historique:",
              error
            );
            // Données de fallback en cas d'erreur
            historyData.value = {
              summary:
                "📊 **Résumé de vos interactions IA** (30 derniers jours)\n\n🎯 **15 interactions** avec une satisfaction moyenne de **4.6/5**\n\n📈 **Catégories les plus consultées** :\n• organisation: 5 fois\n• productivité: 4 fois\n• motivation: 3 fois\n\n💡 **Insights** :\n• Vous vous concentrez beaucoup sur l'organisation - excellent !\n• Votre satisfaction est élevée, continuez sur cette lancée !\n• Vous utilisez régulièrement l'IA - c'est une excellente habitude !\n\n🎯 **Recommandations** :\n• Pensez à prendre plus de pauses pour réduire le stress\n• Essayez de célébrer vos petites victoires plus souvent",
              insights: [
                "Vous vous concentrez beaucoup sur l'organisation - excellent !",
                'Votre satisfaction est élevée, continuez sur cette lancée !',
                "Vous utilisez régulièrement l'IA - c'est une excellente habitude !",
              ],
              recommendations: [
                'Pensez à prendre plus de pauses pour réduire le stress',
                'Essayez de célébrer vos petites victoires plus souvent',
                "N'hésitez pas à me solliciter plus souvent pour des conseils",
              ],
              analytics: {
                total_interactions: 15,
                average_satisfaction: 4.6,
                most_common_topics: [
                  'organisation',
                  'productivité',
                  'motivation',
                ],
                productivity_score: 0.78,
                completion_rate: 0.85,
                stress_level: 0.3,
                motivation_level: 0.8,
              },
              interactions: [
                {
                  timestamp: new Date().toISOString(),
                  type: 'chat',
                  message: 'Comment organiser mes tâches ?',
                  response: "Voici mes conseils pour l'organisation...",
                },
              ],
            };
            showAlert("Erreur lors du chargement de l'historique", 'error');
          } finally {
            historyLoading.value = false;
          }
        };

        // Récupérer l'ID de manière sécurisée (comme dans onMoveTask)
        const taskId = task._id || task.id;

        if (!taskId) {
          console.error('❌ ID de la tâche manquant:', task);
          showAlert('Erreur : ID de la tâche manquant', 'error');
          return;
        }

        if (confirm(`Supprimer la tâche "${task.title}" ?`)) {
          try {
            console.log(
              `🗑️ Suppression de la tâche ${taskId}: "${task.title}"`
            );
            await axios.delete(`/api/tasks/${taskId}`);
            console.log('✅ Tâche supprimée avec succès');
            showAlert('Tâche supprimée');
            await loadTasks();
          } catch (error) {
            console.error('❌ Erreur lors de la suppression:', error);
            showAlert('Erreur lors de la suppression', 'error');
          }
        }
      };

      const setHistoryMode = async mode => {
        console.log(`🔄 Chargement de l'historique IA en mode: ${mode}`);
        historyMode.value = mode;
        historyLoading.value = true;
        try {
          const response = await axios.get(`/api/ia/history?mode=${mode}`);
          console.log('📊 Réponse API historique:', response.data);
          historyData.value = response.data;
          console.log(
            '💾 Données historiques mises à jour:',
            historyData.value
          );
        } catch (error) {
          console.error("❌ Erreur lors du chargement de l'historique:", error);
          showAlert("Erreur lors du chargement de l'historique", 'error');
        } finally {
          historyLoading.value = false;
          console.log(
            '✅ Chargement terminé, historyLoading:',
            historyLoading.value
          );
        }
      };

      // Charger l'historique quand la modal s'ouvre ou le mode change
      watch(
        [showHistoryModal, historyMode],
        async ([modalOpen, mode]) => {
          if (modalOpen) {
            await setHistoryMode(mode);
          }
        },
        { immediate: true }
      );

      // Fonction pour sauvegarder l'état du Kanban
      // const saveKanbanState = async () => { // Supprimé
      //   if (!hasUnsavedChanges.value) { // Supprimé
      //     showAlert('Aucun changement à sauvegarder', 'info') // Supprimé
      //     return // Supprimé
      //   } // Supprimé

      //   isSaving.value = true // Supprimé
      //   try { // Supprimé
      //     console.log('💾 Sauvegarde de l\'état du Kanban...') // Supprimé

      //     // Récupérer toutes les tâches avec leurs nouveaux statuts // Supprimé
      //     const allTasks = [...todoTasks.value, ...progressTasks.value, ...completedTasks.value] // Supprimé

      //     // Sauvegarder chaque tâche modifiée // Supprimé
      //     const savePromises = allTasks.map(async (task) => { // Supprimé
      //       const taskId = task._id || task.id // Supprimé
      //       if (taskId) { // Supprimé
      //         console.log(`💾 Sauvegarde de la tâche ${taskId}: ${task.title} -> ${task.status}`) // Supprimé
      //         return axios.put(`/api/tasks/${taskId}`, { status: task.status }) // Supprimé
      //       } // Supprimé
      //     }) // Supprimé

      //     await Promise.all(savePromises) // Supprimé

      //     // Marquer comme sauvegardé // Supprimé
      //     hasUnsavedChanges.value = false // Supprimé
      //     showAlert('✅ État du Kanban sauvegardé avec succès !', 'success') // Supprimé
      //     console.log('✅ Sauvegarde terminée') // Supprimé

      //     // Recharger les tâches pour s'assurer de la cohérence // Supprimé
      //     await loadTasks() // Supprimé

      //   } catch (error) { // Supprimé
      //     console.error('❌ Erreur lors de la sauvegarde:', error) // Supprimé
      //     showAlert('❌ Erreur lors de la sauvegarde', 'error') // Supprimé
      //   } finally { // Supprimé
      //     isSaving.value = false // Supprimé
      //   } // Supprimé
      // } // Supprimé

      return {
        tasks,
        loading,
        categories,
        priorities,
        showNewTaskModal,
        showEditTaskModal,
        showHistoryModal,
        historyLoading,
        historyData,
        historyMode,
        showChatModal,
        newTask,
        editingTask,
        alert,
        todoTasks,
        completedTasks,
        createTask,
        loadTasks,
        loadCategories,
        loadPriorities,
        loadHistory,
        showAlert,
        changeTaskStatus,
        deleteTask,
        editTask,
        updateTask,
        onDragStart,
        getCategoryIcon,
        getCategoryLabel,
        getPriorityLabel,
        formatDate,
        handleTaskCompletion,
      };
    },
  };
</script>

<style scoped>
  .tasks-page {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 1rem;
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  }

  .tasks-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .tasks-header h1 {
    color: #667eea;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  }

  .header-actions {
    display: flex;
    gap: 1rem;
  }

  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    font-size: 1rem;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }

  .btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  .btn-secondary {
    background: rgba(255, 255, 255, 0.9);
    color: #667eea;
    border: 2px solid #667eea;
  }

  .btn-secondary:hover {
    background: #667eea;
    color: white;
    transform: translateY(-2px);
  }

  .alert {
    padding: 1rem 1.5rem;
    border-radius: 15px;
    margin-bottom: 1.5rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .alert-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .alert-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  .loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .tasks-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 2rem;
  }

  .tasks-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .tasks-section h3 {
    margin-bottom: 1rem;
    color: #333;
    font-size: 1.2rem;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 0.5rem;
  }

  .tasks-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .task-card {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    border-left: 4px solid #007bff;
    transition: all 0.3s ease;
  }

  .task-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .task-card.completed {
    border-left-color: #28a745;
    opacity: 0.8;
  }

  .task-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
  }

  .task-header h4 {
    margin: 0;
    color: #333;
    font-size: 1.1rem;
    flex: 1;
  }

  .task-actions {
    display: flex;
    gap: 0.5rem;
    flex-shrink: 0;
  }

  .task-description {
    color: #666;
    margin: 0.5rem 0;
    font-size: 0.9rem;
  }

  .task-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }

  .category,
  .priority,
  .due-date {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .category {
    background: #e3f2fd;
    color: #1976d2;
  }

  .priority {
    background: #fff3e0;
    color: #f57c00;
  }

  .due-date {
    background: #f3e5f5;
    color: #7b1fa2;
  }

  .btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.8rem;
  }

  .btn-success {
    background: #28a745;
    color: white;
    border: none;
  }

  .btn-success:hover {
    background: #218838;
  }

  .btn-warning {
    background: #ffc107;
    color: #212529;
    border: none;
  }

  .btn-warning:hover {
    background: #e0a800;
  }

  .btn-danger {
    background: #dc3545;
    color: white;
    border: none;
  }

  .btn-danger:hover {
    background: #c82333;
  }

  .btn-info {
    background: #17a2b8;
    color: white;
    border: none;
  }

  .btn-info:hover {
    background: #138496;
  }

  /* Modales */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .modal {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
  }

  .modal h3 {
    color: #667eea;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #333;
  }

  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
  }

  .form-group input:focus,
  .form-group textarea:focus,
  .form-group select:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
  }

  .modal-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .modal-actions .btn {
    flex: 1;
  }

  /* Modal Historique IA */
  .history-modal {
    width: 95%;
    max-width: 800px;
    max-height: 95vh;
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    overflow-y: auto;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 1rem;
  }

  .modal-header h3 {
    margin: 0;
    color: #667eea;
  }

  .history-content {
    flex-grow: 1;
    overflow-y: auto;
  }

  .history-summary h4,
  .history-insights h4,
  .history-recommendations h4 {
    color: #667eea;
    margin-bottom: 0.8rem;
  }

  .history-summary p {
    color: #495057;
    font-size: 0.95rem;
    line-height: 1.6;
    white-space: pre-wrap;
  }

  .history-insights ul,
  .history-recommendations ul {
    list-style: none;
    padding: 0;
    margin-bottom: 1.5rem;
  }

  .history-insights li,
  .history-recommendations li {
    color: #495057;
    font-size: 0.9rem;
    line-height: 1.6;
    margin-bottom: 0.5rem;
    padding-left: 1rem;
    position: relative;
  }

  .history-insights li::before,
  .history-recommendations li::before {
    content: '•';
    color: #667eea;
    position: absolute;
    left: 0;
  }

  .no-history {
    text-align: center;
    color: #6c757d;
    font-style: italic;
  }

  /* Métriques */
  .history-metrics {
    margin: 1.5rem 0;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }

  .metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    transition: transform 0.2s ease;
  }

  .metric-card:hover {
    transform: translateY(-2px);
  }

  .metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  .metric-label {
    font-size: 0.9rem;
    opacity: 0.9;
  }

  /* Interactions récentes */
  .history-interactions {
    margin: 1.5rem 0;
  }

  .interactions-list {
    margin-top: 1rem;
  }

  .interaction-item {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid #667eea;
  }

  .interaction-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .interaction-type {
    background: #667eea;
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .interaction-time {
    color: #6c757d;
    font-size: 0.8rem;
  }

  .interaction-content {
    color: #495057;
  }

  .interaction-message {
    font-weight: 500;
    margin-bottom: 0.3rem;
  }

  .interaction-response {
    font-size: 0.9rem;
    opacity: 0.8;
  }

  /* Amélioration du résumé */
  .summary-content {
    white-space: pre-wrap;
    line-height: 1.6;
    color: #495057;
  }

  .summary-content strong {
    color: #667eea;
  }

  /* Tendances et Opportunités */
  .history-trends,
  .history-opportunities {
    margin: 1.5rem 0;
  }

  .history-trends h4,
  .history-opportunities h4 {
    color: #495057;
    margin-bottom: 1rem;
    font-size: 1.1rem;
  }

  .history-trends ul,
  .history-opportunities ul {
    list-style: none;
    padding: 0;
  }

  .history-trends li,
  .history-opportunities li {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-left: 4px solid #28a745;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    border-radius: 8px;
    color: #495057;
    font-size: 0.95rem;
    line-height: 1.4;
  }

  .history-opportunities li {
    border-left-color: #ffc107;
    background: linear-gradient(135deg, #fff8e1 0%, #ffeaa7 100%);
  }

  /* Responsive */
  @media (max-width: 768px) {
    .tasks-header {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .tasks-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .task-header {
      flex-direction: column;
      gap: 0.5rem;
    }

    .task-actions {
      align-self: flex-end;
    }

    .header-actions {
      flex-direction: column;
    }

    .modal-actions {
      flex-direction: column;
    }
  }
</style>
