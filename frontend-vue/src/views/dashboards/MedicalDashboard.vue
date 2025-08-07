<template>
  <div class="dashboard-medical">
    <div class="dashboard-header">
      <h1>🏥 Dashboard Médical</h1>
      <p class="dashboard-subtitle">
        Gérez vos patients et vos activités médicales
      </p>
    </div>

    <div class="dashboard-grid">
      <!-- Section Gestion Patients -->
      <div class="dashboard-section">
        <h2>👥 Gestion Patients</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openPatients">
            <div class="card-icon">👤</div>
            <h3>Mes Patients</h3>
            <p>Gérez votre liste de patients et leurs dossiers</p>
            <button class="card-btn">Gérer</button>
          </div>

          <div class="feature-card" @click="openAppointments">
            <div class="card-icon">📅</div>
            <h3>Rendez-vous</h3>
            <p>Planifiez et suivez vos consultations</p>
            <button class="card-btn">Planifier</button>
          </div>

          <div class="feature-card" @click="openMedicalRecords">
            <div class="card-icon">📋</div>
            <h3>Dossiers Médicaux</h3>
            <p>Accédez aux dossiers patients sécurisés</p>
            <button class="card-btn">Consulter</button>
          </div>
        </div>
      </div>

      <!-- Section Activités Médicales -->
      <div class="dashboard-section">
        <h2>🔬 Activités Médicales</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openDiagnostics">
            <div class="card-icon">🔍</div>
            <h3>Diagnostics</h3>
            <p>Assistez vos diagnostics avec l'IA</p>
            <button class="card-btn">Diagnostiquer</button>
          </div>

          <div class="feature-card" @click="openTreatments">
            <div class="card-icon">💊</div>
            <h3>Traitements</h3>
            <p>Suivez les prescriptions et traitements</p>
            <button class="card-btn">Prescrire</button>
          </div>

          <div class="feature-card" @click="openFollowUp">
            <div class="card-icon">📈</div>
            <h3>Suivi Patient</h3>
            <p>Suivez l'évolution de vos patients</p>
            <button class="card-btn">Suivre</button>
          </div>
        </div>
      </div>

      <!-- Section IA Médicale -->
      <div class="dashboard-section">
        <h2>🤖 IA Médicale</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openChat">
            <div class="card-icon">💬</div>
            <h3>Assistant IA</h3>
            <p>Obtenez de l'aide pour vos décisions médicales</p>
            <button class="card-btn">Consulter</button>
          </div>

          <div class="feature-card" @click="openResearch">
            <div class="card-icon">📚</div>
            <h3>Recherche Médicale</h3>
            <p>Accédez aux dernières publications</p>
            <button class="card-btn">Rechercher</button>
          </div>

          <div class="feature-card" @click="openInsights">
            <div class="card-icon">🎯</div>
            <h3>Insights Cliniques</h3>
            <p>Analyses et recommandations personnalisées</p>
            <button class="card-btn">Analyser</button>
          </div>
        </div>
      </div>

      <!-- Section Administration -->
      <div class="dashboard-section">
        <h2>⚙️ Administration</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openSchedule">
            <div class="card-icon">⏰</div>
            <h3>Planning</h3>
            <p>Organisez votre emploi du temps médical</p>
            <button class="card-btn">Organiser</button>
          </div>

          <div class="feature-card" @click="openReports">
            <div class="card-icon">📊</div>
            <h3>Rapports</h3>
            <p>Générez des rapports et statistiques</p>
            <button class="card-btn">Générer</button>
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
    name: 'MedicalDashboard',
    setup() {
      const router = useRouter();

      // Méthodes de navigation spécifiques au segment Médical
      const openPatients = () => {
        router.push('/tasks?feature=patients&segment=medical');
      };

      const openAppointments = () => {
        router.push('/tasks?feature=appointments&segment=medical');
      };

      const openMedicalRecords = () => {
        router.push('/tasks?feature=medical-records&segment=medical');
      };

      const openDiagnostics = () => {
        router.push('/tasks?feature=diagnostics&segment=medical');
      };

      const openTreatments = () => {
        router.push('/tasks?feature=treatments&segment=medical');
      };

      const openFollowUp = () => {
        router.push('/tasks?feature=follow-up&segment=medical');
      };

      const openChat = () => {
        router.push('/tasks?module=chat&segment=medical');
      };

      const openResearch = () => {
        router.push('/tasks?feature=research&segment=medical');
      };

      const openInsights = () => {
        router.push('/tasks?module=insights&segment=medical');
      };

      const openSchedule = () => {
        router.push('/tasks?feature=schedule&segment=medical');
      };

      const openReports = () => {
        router.push('/tasks?feature=reports&segment=medical');
      };

      const changeSegment = () => {
        router.push('/segment-selection');
      };

      return {
        openPatients,
        openAppointments,
        openMedicalRecords,
        openDiagnostics,
        openTreatments,
        openFollowUp,
        openChat,
        openResearch,
        openInsights,
        openSchedule,
        openReports,
        changeSegment,
      };
    },
  };
</script>

<style scoped>
  .dashboard-medical {
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
    .dashboard-medical {
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
