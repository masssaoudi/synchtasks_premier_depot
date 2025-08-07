<template>
  <div class="dashboard-memoire">
    <div class="dashboard-header">
      <h1>🧠 Dashboard Mémoire</h1>
      <p class="dashboard-subtitle">
        Stimulez votre mémoire et gardez votre esprit actif
      </p>
    </div>

    <div class="dashboard-grid">
      <!-- Section Exercices Cognitifs -->
      <div class="dashboard-section">
        <h2>🧩 Exercices Cognitifs</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openMemoryGames">
            <div class="card-icon">🎮</div>
            <h3>Jeux de Mémoire</h3>
            <p>Stimulez votre mémoire avec des jeux adaptés</p>
            <button class="card-btn">Jouer</button>
          </div>

          <div class="feature-card" @click="openPuzzles">
            <div class="card-icon">🧩</div>
            <h3>Puzzles</h3>
            <p>Résolvez des puzzles pour maintenir votre logique</p>
            <button class="card-btn">Résoudre</button>
          </div>

          <div class="feature-card" @click="openCalculations">
            <div class="card-icon">🔢</div>
            <h3>Calcul Mental</h3>
            <p>Entraînez votre calcul mental quotidiennement</p>
            <button class="card-btn">Calculer</button>
          </div>
        </div>
      </div>

      <!-- Section Rappels et Mémoires -->
      <div class="dashboard-section">
        <h2>📝 Rappels et Mémoires</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openReminders">
            <div class="card-icon">⏰</div>
            <h3>Mes Rappels</h3>
            <p>Ne manquez plus vos rendez-vous importants</p>
            <button class="card-btn">Gérer</button>
          </div>

          <div class="feature-card" @click="openNotes">
            <div class="card-icon">📝</div>
            <h3>Notes Personnelles</h3>
            <p>Notez vos pensées et souvenirs importants</p>
            <button class="card-btn">Noter</button>
          </div>

          <div class="feature-card" @click="openMedication">
            <div class="card-icon">💊</div>
            <h3>Médicaments</h3>
            <p>Suivez vos traitements et prises de médicaments</p>
            <button class="card-btn">Suivre</button>
          </div>
        </div>
      </div>

      <!-- Section IA Mémoire -->
      <div class="dashboard-section">
        <h2>🤖 Assistant Mémoire</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openChat">
            <div class="card-icon">💬</div>
            <h3>Chat IA</h3>
            <p>Discutez avec votre assistant personnel</p>
            <button class="card-btn">Discuter</button>
          </div>

          <div class="feature-card" @click="openHistory">
            <div class="card-icon">📈</div>
            <h3>Historique</h3>
            <p>Consultez vos activités et progrès</p>
            <button class="card-btn">Consulter</button>
          </div>

          <div class="feature-card" @click="openInsights">
            <div class="card-icon">🎯</div>
            <h3>Conseils</h3>
            <p>Recevez des conseils personnalisés</p>
            <button class="card-btn">Conseils</button>
          </div>
        </div>
      </div>

      <!-- Section Bien-être -->
      <div class="dashboard-section">
        <h2>🌿 Bien-être</h2>
        <div class="cards-grid">
          <div class="feature-card" @click="openActivities">
            <div class="card-icon">🏃‍♂️</div>
            <h3>Activités Physiques</h3>
            <p>Maintenez une activité physique adaptée</p>
            <button class="card-btn">Activer</button>
          </div>

          <div class="feature-card" @click="openSocial">
            <div class="card-icon">👥</div>
            <h3>Contacts Sociaux</h3>
            <p>Gardez le contact avec vos proches</p>
            <button class="card-btn">Contacter</button>
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
    name: 'MemoireDashboard',
    setup() {
      const router = useRouter();

      // Méthodes de navigation spécifiques au segment Mémoire
      const openMemoryGames = () => {
        router.push('/tasks?feature=memory-games&segment=memoire');
      };

      const openPuzzles = () => {
        router.push('/tasks?feature=puzzles&segment=memoire');
      };

      const openCalculations = () => {
        router.push('/tasks?feature=calculations&segment=memoire');
      };

      const openReminders = () => {
        router.push('/tasks?feature=reminders&segment=memoire');
      };

      const openNotes = () => {
        router.push('/tasks?feature=notes&segment=memoire');
      };

      const openMedication = () => {
        router.push('/tasks?feature=medication&segment=memoire');
      };

      const openChat = () => {
        router.push('/tasks?module=chat&segment=memoire');
      };

      const openHistory = () => {
        router.push('/tasks?module=history&segment=memoire');
      };

      const openInsights = () => {
        router.push('/tasks?module=insights&segment=memoire');
      };

      const openActivities = () => {
        router.push('/tasks?feature=activities&segment=memoire');
      };

      const openSocial = () => {
        router.push('/tasks?feature=social&segment=memoire');
      };

      const changeSegment = () => {
        router.push('/segment-selection');
      };

      return {
        openMemoryGames,
        openPuzzles,
        openCalculations,
        openReminders,
        openNotes,
        openMedication,
        openChat,
        openHistory,
        openInsights,
        openActivities,
        openSocial,
        changeSegment,
      };
    },
  };
</script>

<style scoped>
  .dashboard-memoire {
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
    .dashboard-memoire {
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
