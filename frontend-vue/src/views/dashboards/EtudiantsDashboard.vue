<template>
  <div class="dashboard-etudiants">
    <div class="dashboard-header">
      <h1>🎓 Dashboard Étudiant</h1>
      <p class="dashboard-subtitle">
        Organisez vos études et vos projets académiques
      </p>
    </div>

    <div class="dashboard-grid">
      <!-- Section Tâches Académiques -->
      <div class="dashboard-section">
        <h2>📚 Tâches Académiques</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openTasks">
            <div class="card-icon">📝</div>
            <h3>Mes Tâches</h3>
            <p>Gérez vos devoirs, projets et révisions</p>
            <button class="card-btn">Accéder</button>
          </div>

          <div class="feature-card" @click="openPlanning">
            <div class="card-icon">📅</div>
            <h3>Planning Études</h3>
            <p>Organisez votre emploi du temps</p>
            <button class="card-btn">Planifier</button>
          </div>

          <div class="feature-card" @click="openRevision">
            <div class="card-icon">🧠</div>
            <h3>Révisions</h3>
            <p>Préparez vos examens efficacement</p>
            <button class="card-btn">Réviser</button>
          </div>
        </div>
      </div>

      <!-- Section Projets -->
      <div class="dashboard-section">
        <h2>💼 Projets Académiques</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openProjects">
            <div class="card-icon">📊</div>
            <h3>Mes Projets</h3>
            <p>Suivez l'avancement de vos projets</p>
            <button class="card-btn">Gérer</button>
          </div>

          <div class="feature-card" @click="openCollaboration">
            <div class="card-icon">👥</div>
            <h3>Collaboration</h3>
            <p>Travaillez en équipe sur vos projets</p>
            <button class="card-btn">Collaborer</button>
          </div>

          <div class="feature-card" @click="openDeadlines">
            <div class="card-icon">⏰</div>
            <h3>Échéances</h3>
            <p>Ne manquez aucune deadline importante</p>
            <button class="card-btn">Voir</button>
          </div>
        </div>
      </div>

      <!-- Section IA Étudiante -->
      <div class="dashboard-section">
        <h2>🤖 IA Étudiante</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openChat">
            <div class="card-icon">💬</div>
            <h3>Chat IA</h3>
            <p>Obtenez de l'aide pour vos études</p>
            <button class="card-btn">Discuter</button>
          </div>

          <div class="feature-card" @click="openHistory">
            <div class="card-icon">📈</div>
            <h3>Historique IA</h3>
            <p>Consultez vos interactions précédentes</p>
            <button class="card-btn">Consulter</button>
          </div>

          <div class="feature-card" @click="openInsights">
            <div class="card-icon">🎯</div>
            <h3>Insights</h3>
            <p>Analyses et recommandations personnalisées</p>
            <button class="card-btn">Analyser</button>
          </div>
        </div>
      </div>

      <!-- Section Outils Étudiants -->
      <div class="dashboard-section">
        <h2>🛠️ Outils Étudiants</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openNotes">
            <div class="card-icon">📝</div>
            <h3>Notes</h3>
            <p>Prenez et organisez vos notes de cours</p>
            <button class="card-btn">Noter</button>
          </div>

          <div class="feature-card" @click="openResources">
            <div class="card-icon">📚</div>
            <h3>Ressources</h3>
            <p>Accédez à vos documents et ressources</p>
            <button class="card-btn">Accéder</button>
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
    name: 'EtudiantsDashboard',
    setup() {
      const router = useRouter();

      // Méthodes de navigation spécifiques aux étudiants
      const openTasks = () => {
        router.push('/tasks?segment=etudiants');
      };

      const openPlanning = () => {
        router.push('/tasks?feature=planning&segment=etudiants');
      };

      const openRevision = () => {
        router.push('/tasks?feature=revision&segment=etudiants');
      };

      const openProjects = () => {
        router.push('/tasks?feature=projects&segment=etudiants');
      };

      const openCollaboration = () => {
        router.push('/tasks?feature=collaboration&segment=etudiants');
      };

      const openDeadlines = () => {
        router.push('/tasks?feature=deadlines&segment=etudiants');
      };

      const openChat = () => {
        router.push('/tasks?module=chat&segment=etudiants');
      };

      const openHistory = () => {
        router.push('/tasks?module=history&segment=etudiants');
      };

      const openInsights = () => {
        router.push('/tasks?module=insights&segment=etudiants');
      };

      const openNotes = () => {
        router.push('/tasks?feature=notes&segment=etudiants');
      };

      const openResources = () => {
        router.push('/tasks?feature=resources&segment=etudiants');
      };

      const changeSegment = () => {
        router.push('/segment-selection');
      };

      return {
        openTasks,
        openPlanning,
        openRevision,
        openProjects,
        openCollaboration,
        openDeadlines,
        openChat,
        openHistory,
        openInsights,
        openNotes,
        openResources,
        changeSegment,
      };
    },
  };
</script>

<style scoped>
  .dashboard-etudiants {
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
    .dashboard-etudiants {
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
