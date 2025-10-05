<template>
  <div class="segment-dashboard">
    <!-- En-tête adaptatif -->
    <div
      class="dashboard-header"
      :style="{ '--segment-color': currentSegment?.color }"
    >
      <div class="header-content">
        <div class="segment-info">
          <span class="segment-icon">{{ currentSegment?.icon }}</span>
          <div class="segment-details">
            <h1>{{ currentSegment?.name }}</h1>
            <p>{{ currentSegment?.description }}</p>
          </div>
        </div>
        <button class="btn btn-outline" @click="changeSegment">
          Changer de profil
        </button>
      </div>
    </div>

    <!-- Modules IA du segment -->
    <div class="ai-modules-section">
      <h2>🤖 Assistant IA - {{ currentAIModules?.name }}</h2>
      <div class="modules-grid">
        <div
          v-for="(module, key) in allModules"
          :key="key"
          class="module-card"
          :style="{ '--module-color': currentSegment?.color }"
          @click="openModule(key)"
        >
          <div class="module-icon">{{ getModuleIcon(key) }}</div>
          <div class="module-content">
            <h3>{{ module.name }}</h3>
            <p>{{ module.description }}</p>
            <div class="module-features">
              <span
                v-for="feature in module.features.slice(0, 2)"
                :key="feature"
                class="feature-tag"
              >
                {{ feature }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistiques adaptées au segment -->
    <div class="stats-section">
      <h2>📊 Statistiques {{ currentSegment?.name }}</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-content">
            <div class="stat-number">{{ taskCount }}</div>
            <div class="stat-label">Tâches totales</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <div class="stat-number">{{ completedTasks }}</div>
            <div class="stat-label">Tâches terminées</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <div class="stat-number">{{ pendingTasks }}</div>
            <div class="stat-label">Tâches en cours</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <div class="stat-number">{{ completionRate }}%</div>
            <div class="stat-label">Taux de réussite</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Activité récente adaptée -->
    <div class="recent-activity">
      <h2>🕒 Activité récente - {{ currentSegment?.name }}</h2>
      <div class="activity-list">
        <div
          v-for="activity in recentActivities"
          :key="activity.id"
          class="activity-item"
        >
          <div class="activity-icon" :class="activity.type">
            {{ activity.icon }}
          </div>
          <div class="activity-content">
            <div class="activity-text">{{ activity.text }}</div>
            <div class="activity-time">
              {{ formatTime(activity.timestamp) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Objectifs adaptés au segment -->
    <div class="goals-section">
      <h2>🎯 Objectifs {{ currentSegment?.name }}</h2>
      <div class="goals-grid">
        <div v-for="goal in segmentGoals" :key="goal.id" class="goal-card">
          <div class="goal-header">
            <h3>{{ goal.title }}</h3>
            <div class="goal-progress">
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{ width: goal.progress + '%' }"
                ></div>
              </div>
              <span class="progress-text">{{ goal.progress }}%</span>
            </div>
          </div>
          <p class="goal-description">{{ goal.description }}</p>
          <div v-if="goal.deadline" class="goal-deadline">
            📅 {{ formatDate(goal.deadline) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Modals pour les modules IA -->
    <div
      v-if="showChatModal"
      class="modal-overlay"
      @click="showChatModal = false"
    >
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ currentChatModule?.name }}</h3>
          <button class="close-btn" @click="showChatModal = false">×</button>
        </div>
        <div class="modal-body">
          <p>{{ currentChatModule?.description }}</p>
          <div class="module-features">
            <span
              v-for="feature in currentChatModule?.features"
              :key="feature"
              class="feature-tag"
            >
              {{ feature }}
            </span>
          </div>
          <button class="btn btn-primary" @click="openChat">
            Ouvrir le chat
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showHistoryModal"
      class="modal-overlay"
      @click="showHistoryModal = false"
    >
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ currentHistoryModule?.name }}</h3>
          <button class="close-btn" @click="showHistoryModal = false">×</button>
        </div>
        <div class="modal-body">
          <p>{{ currentHistoryModule?.description }}</p>
          <div class="module-features">
            <span
              v-for="feature in currentHistoryModule?.features"
              :key="feature"
              class="feature-tag"
            >
              {{ feature }}
            </span>
          </div>
          <button class="btn btn-primary" @click="openHistory">
            Voir l'historique
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showInsightsModal"
      class="modal-overlay"
      @click="showInsightsModal = false"
    >
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ currentInsightsModule?.name }}</h3>
          <button class="close-btn" @click="showInsightsModal = false">
            ×
          </button>
        </div>
        <div class="modal-body">
          <p>{{ currentInsightsModule?.description }}</p>
          <div class="module-features">
            <span
              v-for="feature in currentInsightsModule?.features"
              :key="feature"
              class="feature-tag"
            >
              {{ feature }}
            </span>
          </div>
          <button class="btn btn-primary" @click="openInsights">
            Voir les conseils
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { useSegmentsStore } from '../stores/segments';
  import { useAIModulesStore } from '../stores/ai-modules';
  import { useTasksStore } from '../stores/tasks';

  const router = useRouter();
  const segmentsStore = useSegmentsStore();
  const aiModulesStore = useAIModulesStore();
  const tasksStore = useTasksStore();

  // Modals
  const showChatModal = ref(false);
  const showHistoryModal = ref(false);
  const showInsightsModal = ref(false);

  // Computed properties
  const currentSegment = computed(() => segmentsStore.currentSegment);
  const currentAIModules = computed(() => aiModulesStore.currentSegmentModules);
  const allModules = computed(() => aiModulesStore.allModules);
  const currentChatModule = computed(() => aiModulesStore.currentChatModule);
  const currentHistoryModule = computed(
    () => aiModulesStore.currentHistoryModule
  );
  const currentInsightsModule = computed(
    () => aiModulesStore.currentInsightsModule
  );

  // Statistiques
  const taskCount = computed(() => tasksStore.taskCount);
  const completedTasks = computed(() => tasksStore.completedTasks);
  const pendingTasks = computed(() => tasksStore.pendingTasks);
  const completionRate = computed(() => {
    if (taskCount.value === 0) {
      return 0;
    }
    return Math.round((completedTasks.value / taskCount.value) * 100);
  });

  // Activité récente
  const recentActivities = ref([
    {
      id: 1,
      type: 'completed',
      icon: '✅',
      text: 'Tâche terminée avec succès',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
    },
    {
      id: 2,
      type: 'created',
      icon: '📝',
      text: 'Nouvelle tâche créée',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000),
    },
  ]);

  // Objectifs adaptés au segment
  const segmentGoals = computed(() => {
    const goals = {
      particuliers: [
        {
          id: 1,
          title: 'Organisation quotidienne',
          description: 'Maintenir une routine quotidienne efficace',
          progress: 75,
          deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
        },
        {
          id: 2,
          title: 'Bien-être personnel',
          description: 'Améliorer la qualité de vie',
          progress: 60,
          deadline: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000),
        },
      ],
      etudiants: [
        {
          id: 1,
          title: 'Réussite académique',
          description: 'Maintenir une moyenne de 15/20',
          progress: 80,
          deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
        },
        {
          id: 2,
          title: 'Organisation des études',
          description: 'Optimiser le planning de révisions',
          progress: 65,
          deadline: new Date(Date.now() + 21 * 24 * 60 * 60 * 1000),
        },
      ],
      medical: [
        {
          id: 1,
          title: 'Suivi médical',
          description: 'Respecter les rendez-vous médicaux',
          progress: 90,
          deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
        },
        {
          id: 2,
          title: 'Santé optimale',
          description: 'Maintenir une bonne santé',
          progress: 70,
          deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
        },
      ],
      memoire: [
        {
          id: 1,
          title: 'Stimulation cognitive',
          description: 'Exercices de mémoire quotidiens',
          progress: 85,
          deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
        },
        {
          id: 2,
          title: 'Amélioration mémoire',
          description: 'Techniques de mémorisation',
          progress: 55,
          deadline: new Date(Date.now() + 21 * 24 * 60 * 60 * 1000),
        },
      ],
      professionnels: [
        {
          id: 1,
          title: 'Développement carrière',
          description: 'Atteindre les objectifs professionnels',
          progress: 70,
          deadline: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000),
        },
        {
          id: 2,
          title: 'Compétences professionnelles',
          description: 'Améliorer les compétences clés',
          progress: 60,
          deadline: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000),
        },
      ],
      entreprises: [
        {
          id: 1,
          title: 'Performance équipe',
          description: "Optimiser la productivité d'équipe",
          progress: 75,
          deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
        },
        {
          id: 2,
          title: 'Leadership',
          description: 'Développer les compétences de leadership',
          progress: 65,
          deadline: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000),
        },
      ],
    };

    const currentSegmentId = segmentsStore.selectedSegment;
    return goals[currentSegmentId] || [];
  });

  // Actions
  const changeSegment = () => {
    router.push('/segment-selection');
  };

  const getModuleIcon = moduleType => {
    const icons = {
      chat: '💬',
      history: '📊',
      insights: '💡',
    };
    return icons[moduleType] || '🤖';
  };

  const openModule = moduleType => {
    switch (moduleType) {
      case 'chat':
        showChatModal.value = true;
        break;
      case 'history':
        showHistoryModal.value = true;
        break;
      case 'insights':
        showInsightsModal.value = true;
        break;
    }
  };

  const openChat = () => {
    showChatModal.value = false;
    router.push('/tasks');
  };

  const openHistory = () => {
    showHistoryModal.value = false;
    router.push('/tasks');
  };

  const openInsights = () => {
    showInsightsModal.value = false;
    router.push('/tasks');
  };

  const formatTime = timestamp => {
    const now = new Date();
    const diff = now - timestamp;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);

    if (days > 0) {
      return `Il y a ${days} jour${days > 1 ? 's' : ''}`;
    } else if (hours > 0) {
      return `Il y a ${hours} heure${hours > 1 ? 's' : ''}`;
    } else {
      return "À l'instant";
    }
  };

  const formatDate = date => {
    return new Date(date).toLocaleDateString('fr-FR');
  };

  onMounted(() => {
    // Charger les données du dashboard
    tasksStore.fetchTasks();
  });
</script>

<style scoped>
  .segment-dashboard {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .dashboard-header {
    background: linear-gradient(
      135deg,
      var(--segment-color, #667eea) 0%,
      rgba(102, 126, 234, 0.8) 100%
    );
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    color: white;
  }

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .segment-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .segment-icon {
    font-size: 3rem;
  }

  .segment-details h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: bold;
  }

  .segment-details p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
  }

  .btn-outline {
    background: transparent;
    color: white;
    border: 2px solid white;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .btn-outline:hover {
    background: white;
    color: var(--segment-color, #667eea);
  }

  .ai-modules-section {
    margin-bottom: 3rem;
  }

  .ai-modules-section h2 {
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .modules-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .module-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    border: 3px solid transparent;
  }

  .module-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    border-color: var(--module-color, #667eea);
  }

  .module-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    text-align: center;
  }

  .module-content h3 {
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
  }

  .module-content p {
    color: #666;
    margin-bottom: 1rem;
    line-height: 1.5;
  }

  .module-features {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .feature-tag {
    background: var(--module-color, #667eea);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .stats-section {
    margin-bottom: 3rem;
  }

  .stats-section h2 {
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
  }

  .stat-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .stat-icon {
    font-size: 2rem;
  }

  .stat-content {
    flex: 1;
  }

  .stat-number {
    font-size: 1.8rem;
    font-weight: bold;
    color: var(--segment-color, #667eea);
    margin-bottom: 0.25rem;
  }

  .stat-label {
    color: #666;
    font-size: 0.9rem;
  }

  .recent-activity {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    margin-bottom: 3rem;
  }

  .recent-activity h2 {
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .activity-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #e9ecef;
  }

  .activity-item:last-child {
    border-bottom: none;
  }

  .activity-icon {
    font-size: 1.5rem;
    width: 40px;
    text-align: center;
  }

  .activity-content {
    flex: 1;
  }

  .activity-text {
    color: #333;
    margin-bottom: 0.25rem;
  }

  .activity-time {
    color: #666;
    font-size: 0.9rem;
  }

  .goals-section {
    margin-bottom: 3rem;
  }

  .goals-section h2 {
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .goals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .goal-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  .goal-header {
    margin-bottom: 1rem;
  }

  .goal-header h3 {
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
  }

  .goal-progress {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .progress-bar {
    flex: 1;
    height: 8px;
    background: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: var(--segment-color, #667eea);
    transition: width 0.3s ease;
  }

  .progress-text {
    font-weight: bold;
    color: #333;
    font-size: 0.9rem;
  }

  .goal-description {
    color: #666;
    margin-bottom: 0.5rem;
    line-height: 1.5;
  }

  .goal-deadline {
    color: #999;
    font-size: 0.9rem;
  }

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
    padding: 1rem;
  }

  .modal-content {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    max-width: 500px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .modal-header h3 {
    margin: 0;
    color: #333;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
  }

  .modal-body p {
    color: #666;
    margin-bottom: 1rem;
    line-height: 1.6;
  }

  .btn {
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
  }

  .btn-primary {
    background: var(--segment-color, #667eea);
    color: white;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }

  @media (max-width: 768px) {
    .header-content {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .modules-grid {
      grid-template-columns: 1fr;
    }

    .stats-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .goals-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
