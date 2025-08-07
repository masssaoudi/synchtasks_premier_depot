<template>
  <div class="dashboard-entreprises">
    <div class="dashboard-header">
      <h1>🏢 Dashboard Entreprises</h1>
      <p class="dashboard-subtitle">
        Gérez votre entreprise et optimisez vos processus
      </p>
    </div>

    <div class="dashboard-grid">
      <!-- Section Gestion Équipe -->
      <div class="dashboard-section">
        <h2>👥 Gestion Équipe</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openEmployees">
            <div class="card-icon">👤</div>
            <h3>Employés</h3>
            <p>Gérez votre équipe et leurs profils</p>
            <button class="card-btn">Gérer</button>
          </div>

          <div class="feature-card" @click="openDepartments">
            <div class="card-icon">🏢</div>
            <h3>Départements</h3>
            <p>Organisez vos départements et équipes</p>
            <button class="card-btn">Organiser</button>
          </div>

          <div class="feature-card" @click="openRoles">
            <div class="card-icon">🎯</div>
            <h3>Rôles & Permissions</h3>
            <p>Définissez les rôles et accès</p>
            <button class="card-btn">Définir</button>
          </div>
        </div>
      </div>

      <!-- Section Gestion Projets -->
      <div class="dashboard-section">
        <h2>📊 Gestion Projets</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openProjects">
            <div class="card-icon">📋</div>
            <h3>Projets Entreprise</h3>
            <p>Suivez tous vos projets d'entreprise</p>
            <button class="card-btn">Suivre</button>
          </div>

          <div class="feature-card" @click="openTasks">
            <div class="card-icon">✅</div>
            <h3>Tâches Équipe</h3>
            <p>Assignez et suivez les tâches</p>
            <button class="card-btn">Assigner</button>
          </div>

          <div class="feature-card" @click="openWorkflow">
            <div class="card-icon">🔄</div>
            <h3>Workflows</h3>
            <p>Automatisez vos processus</p>
            <button class="card-btn">Automatiser</button>
          </div>
        </div>
      </div>

      <!-- Section IA Entreprise -->
      <div class="dashboard-section">
        <h2>🤖 IA Entreprise</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openChat">
            <div class="card-icon">💬</div>
            <h3>Assistant IA</h3>
            <p>Obtenez de l'aide pour vos décisions</p>
            <button class="card-btn">Consulter</button>
          </div>

          <div class="feature-card" @click="openAnalytics">
            <div class="card-icon">📈</div>
            <h3>Analytics</h3>
            <p>Analysez vos performances d'entreprise</p>
            <button class="card-btn">Analyser</button>
          </div>

          <div class="feature-card" @click="openInsights">
            <div class="card-icon">🎯</div>
            <h3>Insights Business</h3>
            <p>Recommandations stratégiques</p>
            <button class="card-btn">Consulter</button>
          </div>
        </div>
      </div>

      <!-- Section Administration -->
      <div class="dashboard-section">
        <h2>⚙️ Administration</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openReports">
            <div class="card-icon">📊</div>
            <h3>Rapports</h3>
            <p>Générez des rapports d'entreprise</p>
            <button class="card-btn">Générer</button>
          </div>

          <div class="feature-card" @click="openSettings">
            <div class="card-icon">⚙️</div>
            <h3>Paramètres</h3>
            <p>Configurez votre entreprise</p>
            <button class="card-btn">Configurer</button>
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
    name: 'EntreprisesDashboard',
    setup() {
      const router = useRouter();

      // Méthodes de navigation spécifiques au segment Entreprises
      const openEmployees = () => {
        router.push('/tasks?feature=employees&segment=entreprises');
      };

      const openDepartments = () => {
        router.push('/tasks?feature=departments&segment=entreprises');
      };

      const openRoles = () => {
        router.push('/tasks?feature=roles&segment=entreprises');
      };

      const openProjects = () => {
        router.push('/tasks?feature=projects&segment=entreprises');
      };

      const openTasks = () => {
        router.push('/tasks?feature=tasks&segment=entreprises');
      };

      const openWorkflow = () => {
        router.push('/tasks?feature=workflow&segment=entreprises');
      };

      const openChat = () => {
        router.push('/tasks?module=chat&segment=entreprises');
      };

      const openAnalytics = () => {
        router.push('/tasks?feature=analytics&segment=entreprises');
      };

      const openInsights = () => {
        router.push('/tasks?module=insights&segment=entreprises');
      };

      const openReports = () => {
        router.push('/tasks?feature=reports&segment=entreprises');
      };

      const openSettings = () => {
        router.push('/tasks?feature=settings&segment=entreprises');
      };

      const changeSegment = () => {
        router.push('/segment-selection');
      };

      return {
        openEmployees,
        openDepartments,
        openRoles,
        openProjects,
        openTasks,
        openWorkflow,
        openChat,
        openAnalytics,
        openInsights,
        openReports,
        openSettings,
        changeSegment,
      };
    },
  };
</script>

<style scoped>
  .dashboard-entreprises {
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
    .dashboard-entreprises {
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
