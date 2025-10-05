<template>
  <div class="particuliers-dashboard">
    <!-- En-tête spécialisé Particuliers -->
    <div class="dashboard-header" style="--segment-color: #4caf50">
      <div class="header-content">
        <div class="segment-info">
          <span class="segment-icon">👤</span>
          <div class="segment-details">
            <h1>Dashboard Particuliers</h1>
            <p>Organisez votre vie quotidienne avec des outils personnalisés</p>
          </div>
        </div>
        <button class="btn btn-outline" @click="changeSegment">
          Changer de profil
        </button>
      </div>
    </div>

    <!-- Modules IA spécialisés Particuliers -->
    <div class="ai-modules-section">
      <h2>🤖 Assistant Personnel</h2>
      <div class="modules-grid">
        <div class="module-card" @click="openChat">
          <div class="module-icon">💬</div>
          <div class="module-content">
            <h3>Chat Personnel</h3>
            <p>
              Discutez de vos objectifs personnels et recevez des conseils
              adaptés
            </p>
            <div class="module-features">
              <span class="feature-tag">Conseils personnels</span>
              <span class="feature-tag">Motivation</span>
            </div>
          </div>
        </div>

        <div class="module-card" @click="openHistory">
          <div class="module-icon">📊</div>
          <div class="module-content">
            <h3>Historique Personnel</h3>
            <p>Suivez vos habitudes et votre progression personnelle</p>
            <div class="module-features">
              <span class="feature-tag">Suivi des habitudes</span>
              <span class="feature-tag">Progression</span>
            </div>
          </div>
        </div>

        <div class="module-card" @click="openInsights">
          <div class="module-icon">💡</div>
          <div class="module-content">
            <h3>Conseils Quotidiens</h3>
            <p>
              Recevez des conseils personnalisés pour améliorer votre quotidien
            </p>
            <div class="module-features">
              <span class="feature-tag">Conseils quotidiens</span>
              <span class="feature-tag">Optimisation</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Fonctionnalités spécialisées Particuliers -->
    <div class="features-section">
      <h2>🎯 Fonctionnalités Particuliers</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">📅</div>
          <h3>Planning Quotidien</h3>
          <p>
            Organisez vos tâches quotidiennes avec des rappels personnalisés
          </p>
          <button class="btn btn-primary" @click="openPlanning">Ouvrir</button>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🏠</div>
          <h3>Gestion Maison</h3>
          <p>Suivez les tâches ménagères et l'entretien de votre espace</p>
          <button class="btn btn-primary" @click="openHouse">Ouvrir</button>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🛒</div>
          <h3>Listes de Courses</h3>
          <p>Créez et gérez vos listes de courses avec l'aide de l'IA</p>
          <button class="btn btn-primary" @click="openShopping">Ouvrir</button>
        </div>

        <div class="feature-card">
          <div class="feature-icon">💪</div>
          <h3>Bien-être Personnel</h3>
          <p>Suivez vos objectifs de santé et de bien-être</p>
          <button class="btn btn-primary" @click="openWellness">Ouvrir</button>
        </div>

        <!-- Intégration directe de la page des tâches -->
        <div class="feature-card main-tasks-card">
          <div class="feature-icon">📋</div>
          <h3>Mes Tâches</h3>
          <p>Gérez toutes vos tâches personnelles en un seul endroit</p>
          <button class="btn btn-primary" @click="openMainTasks">
            Gérer mes tâches
          </button>
        </div>
      </div>
    </div>

    <!-- Statistiques personnelles -->
    <div class="stats-section">
      <h2>📊 Mes Statistiques Personnelles</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-content">
            <div class="stat-number">{{ taskCount }}</div>
            <div class="stat-label">Tâches personnelles</div>
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
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <div class="stat-number">{{ completionRate }}%</div>
            <div class="stat-label">Taux de réussite</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📈</div>
          <div class="stat-content">
            <div class="stat-number">{{ streakDays }}</div>
            <div class="stat-label">Jours consécutifs</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Objectifs personnels -->
    <div class="goals-section">
      <h2>🎯 Mes Objectifs Personnels</h2>
      <div class="goals-grid">
        <div class="goal-card">
          <div class="goal-header">
            <h3>Organisation Quotidienne</h3>
            <div class="goal-progress">
              <div class="progress-bar">
                <div class="progress-fill" style="width: 75%"></div>
              </div>
              <span class="progress-text">75%</span>
            </div>
          </div>
          <p class="goal-description">
            Maintenir une routine quotidienne efficace
          </p>
          <div class="goal-deadline">📅 Échéance : 7 jours</div>
        </div>

        <div class="goal-card">
          <div class="goal-header">
            <h3>Bien-être Personnel</h3>
            <div class="goal-progress">
              <div class="progress-bar">
                <div class="progress-fill" style="width: 60%"></div>
              </div>
              <span class="progress-text">60%</span>
            </div>
          </div>
          <p class="goal-description">
            Améliorer la qualité de vie quotidienne
          </p>
          <div class="goal-deadline">📅 Échéance : 14 jours</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useSegmentsStore } from '../../stores/segments';
  import { useTasksStore } from '../../stores/tasks';

  const router = useRouter();
  const segmentsStore = useSegmentsStore();
  const tasksStore = useTasksStore();

  // Statistiques
  const taskCount = computed(() => tasksStore.taskCount);
  const completedTasks = computed(() => tasksStore.completedTasks);
  const completionRate = computed(() => {
    if (taskCount.value === 0) {
      return 0;
    }
    return Math.round((completedTasks.value / taskCount.value) * 100);
  });
  const streakDays = ref(12); // Exemple

  // Actions
  const changeSegment = () => {
    router.push('/segment-selection');
  };

  const openChat = () => {
    router.push('/tasks?module=chat');
  };

  const openHistory = () => {
    router.push('/tasks?module=history');
  };

  const openInsights = () => {
    router.push('/tasks?module=insights');
  };

  const openPlanning = () => {
    router.push('/tasks?feature=planning');
  };

  const openHouse = () => {
    router.push('/tasks?feature=house');
  };

  const openShopping = () => {
    router.push('/tasks?feature=shopping');
  };

  const openWellness = () => {
    router.push('/tasks?feature=wellness');
  };

  const openMainTasks = () => {
    router.push('/tasks');
  };

  onMounted(() => {
    // Charger les données du dashboard
    tasksStore.fetchTasks();
  });
</script>

<style scoped>
  .particuliers-dashboard {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .dashboard-header {
    background: linear-gradient(
      135deg,
      var(--segment-color, #4caf50) 0%,
      rgba(76, 175, 80, 0.8) 100%
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
    color: var(--segment-color, #4caf50);
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
    border-color: var(--segment-color, #4caf50);
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
    background: var(--segment-color, #4caf50);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .features-section {
    margin-bottom: 3rem;
  }

  .features-section h2 {
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .feature-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: all 0.3s ease;
  }

  .main-tasks-card {
    background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
    color: white;
    transform: scale(1.05);
    border: 2px solid #4caf50;
  }

  .main-tasks-card h3,
  .main-tasks-card p {
    color: white;
  }

  .main-tasks-card .btn-primary {
    background: white;
    color: #4caf50;
    font-weight: bold;
  }

  .main-tasks-card .btn-primary:hover {
    background: #f0f0f0;
    transform: translateY(-2px);
  }

  .feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }

  .feature-card h3 {
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
  }

  .feature-card p {
    color: #666;
    margin-bottom: 1rem;
    line-height: 1.5;
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
    background: var(--segment-color, #4caf50);
    color: white;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
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
    color: var(--segment-color, #4caf50);
    margin-bottom: 0.25rem;
  }

  .stat-label {
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
    background: var(--segment-color, #4caf50);
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

  @media (max-width: 768px) {
    .header-content {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .modules-grid {
      grid-template-columns: 1fr;
    }

    .features-grid {
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
