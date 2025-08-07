<template>
  <div class="dashboard-professionnels">
    <div class="dashboard-header">
      <h1>💼 Dashboard Professionnels</h1>
      <p class="dashboard-subtitle">
        Optimisez votre productivité et gérez vos projets
      </p>
    </div>

    <div class="dashboard-grid">
      <!-- Section Gestion Projets -->
      <div class="dashboard-section">
        <h2>📊 Gestion Projets</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openProjects">
            <div class="card-icon">📋</div>
            <h3>Mes Projets</h3>
            <p>Gérez vos projets et leur avancement</p>
            <button class="card-btn">Gérer</button>
          </div>

          <div class="feature-card" @click="openTasks">
            <div class="card-icon">✅</div>
            <h3>Tâches Professionnelles</h3>
            <p>Organisez vos tâches et priorités</p>
            <button class="card-btn">Organiser</button>
          </div>

          <div class="feature-card" @click="openDeadlines">
            <div class="card-icon">⏰</div>
            <h3>Échéances</h3>
            <p>Suivez vos deadlines importantes</p>
            <button class="card-btn">Suivre</button>
          </div>
        </div>
      </div>

      <!-- Section Collaboration -->
      <div class="dashboard-section">
        <h2>👥 Collaboration</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openTeam">
            <div class="card-icon">👥</div>
            <h3>Équipe</h3>
            <p>Collaborez avec vos collègues</p>
            <button class="card-btn">Collaborer</button>
          </div>

          <div class="feature-card" @click="openMeetings">
            <div class="card-icon">🤝</div>
            <h3>Réunions</h3>
            <p>Planifiez et gérez vos réunions</p>
            <button class="card-btn">Planifier</button>
          </div>

          <div class="feature-card" @click="openCommunication">
            <div class="card-icon">💬</div>
            <h3>Communication</h3>
            <p>Centralisez vos communications</p>
            <button class="card-btn">Communiquer</button>
          </div>
        </div>
      </div>

      <!-- Section IA Professionnelle -->
      <div class="dashboard-section">
        <h2>🤖 IA Professionnelle</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openChat">
            <div class="card-icon">💬</div>
            <h3>Assistant IA</h3>
            <p>Obtenez de l'aide pour vos tâches</p>
            <button class="card-btn">Consulter</button>
          </div>

          <div class="feature-card" @click="openAnalytics">
            <div class="card-icon">📈</div>
            <h3>Analytics</h3>
            <p>Analysez vos performances</p>
            <button class="card-btn">Analyser</button>
          </div>

          <div class="feature-card" @click="openInsights">
            <div class="card-icon">🎯</div>
            <h3>Insights</h3>
            <p>Recommandations personnalisées</p>
            <button class="card-btn">Consulter</button>
          </div>
        </div>
      </div>

      <!-- Section Outils Professionnels -->
      <div class="dashboard-section">
        <h2>🛠️ Outils Professionnels</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openCalendar">
            <div class="card-icon">📅</div>
            <h3>Calendrier</h3>
            <p>Organisez votre planning professionnel</p>
            <button class="card-btn">Organiser</button>
          </div>

          <div class="feature-card" @click="openDocuments">
            <div class="card-icon">📄</div>
            <h3>Documents</h3>
            <p>Gérez vos documents professionnels</p>
            <button class="card-btn">Gérer</button>
          </div>

          <div class="feature-card" @click="changeSegment">
            <div class="card-icon">🔄</div>
            <h3>Changer de Profil</h3>
            <p>Passez à un autre segment utilisateur</p>
            <button class="card-btn">Changer</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { useRouter } from 'vue-router';

  export default {
    name: 'ProfessionnelsDashboard',
    setup() {
      const router = useRouter();

      // Méthodes de navigation spécifiques au segment Professionnels
      const openProjects = () => {
        router.push('/tasks?feature=projects&segment=professionnels');
      };

      const openTasks = () => {
        router.push('/tasks?feature=tasks&segment=professionnels');
      };

      const openDeadlines = () => {
        router.push('/tasks?feature=deadlines&segment=professionnels');
      };

      const openTeam = () => {
        router.push('/tasks?feature=team&segment=professionnels');
      };

      const openMeetings = () => {
        router.push('/tasks?feature=meetings&segment=professionnels');
      };

      const openCommunication = () => {
        router.push('/tasks?feature=communication&segment=professionnels');
      };

      const openChat = () => {
        router.push('/tasks?module=chat&segment=professionnels');
      };

      const openAnalytics = () => {
        router.push('/tasks?feature=analytics&segment=professionnels');
      };

      const openInsights = () => {
        router.push('/tasks?module=insights&segment=professionnels');
      };

      const openCalendar = () => {
        router.push('/tasks?feature=calendar&segment=professionnels');
      };

      const openDocuments = () => {
        router.push('/tasks?feature=documents&segment=professionnels');
      };

      const changeSegment = () => {
        router.push('/segment-selection');
      };

      return {
        openProjects,
        openTasks,
        openDeadlines,
        openTeam,
        openMeetings,
        openCommunication,
        openChat,
        openAnalytics,
        openInsights,
        openCalendar,
        openDocuments,
        changeSegment,
      };
    },
  };
</script>

<style scoped>
  .dashboard-professionnels {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .dashboard-header {
    text-align: center;
    margin-bottom: 3rem;
  }

  .dashboard-header h1 {
    font-size: 2.5rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
  }

  .dashboard-subtitle {
    font-size: 1.1rem;
    color: #6c757d;
  }

  .dashboard-section {
    margin-bottom: 3rem;
  }

  .dashboard-section h2 {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #667eea;
  }

  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .feature-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 2px solid transparent;
  }

  .feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    border-color: #667eea;
  }

  .card-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
  }

  .feature-card h3 {
    font-size: 1.2rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
  }

  .feature-card p {
    color: #6c757d;
    margin-bottom: 1rem;
    line-height: 1.5;
  }

  .card-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .card-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .dashboard-professionnels {
      padding: 1rem;
    }

    .dashboard-header h1 {
      font-size: 2rem;
    }

    .cards-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .feature-card {
      padding: 1rem;
    }
  }

  @media (max-width: 480px) {
    .dashboard-header h1 {
      font-size: 1.5rem;
    }

    .dashboard-subtitle {
      font-size: 1rem;
    }

    .dashboard-section h2 {
      font-size: 1.3rem;
    }
  }
</style>
