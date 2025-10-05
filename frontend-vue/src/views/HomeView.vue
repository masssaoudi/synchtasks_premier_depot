<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-icon">📋</span>
          SyncTasks
        </h1>
        <p class="hero-subtitle">
          Organisez vos tâches avec l'intelligence artificielle
        </p>
        <p class="hero-description">
          Une plateforme intelligente qui s'adapte à votre profil et vous aide à 
          accomplir vos objectifs avec l'aide de l'IA.
        </p>
        
        <div class="hero-actions">
          <button class="btn btn-primary" @click="goToLogin">
            <span class="btn-icon">🔐</span>
            Se connecter
          </button>
          <button class="btn btn-secondary" @click="goToRegister">
            <span class="btn-icon">✨</span>
            Créer un compte
          </button>
        </div>
      </div>
      
      <div class="hero-visual">
        <div class="floating-card card-1">
          <span class="card-icon">🤖</span>
          <p>IA personnalisée</p>
        </div>
        <div class="floating-card card-2">
          <span class="card-icon">⚡</span>
          <p>Temps réel</p>
        </div>
        <div class="floating-card card-3">
          <span class="card-icon">🎯</span>
          <p>Objectifs atteints</p>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <h2 class="section-title">Pourquoi SyncTasks ?</h2>
      
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>Profils personnalisés</h3>
          <p>
            Choisissez votre profil : Particuliers, Étudiants, Médical, 
            Mémoire, Professionnels ou Entreprises. Chaque interface est 
            adaptée à vos besoins spécifiques.
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>Assistant IA intelligent</h3>
          <p>
            Notre IA analyse vos habitudes et vous propose des conseils 
            personnalisés pour optimiser votre productivité.
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">⚡</div>
          <h3>Synchronisation temps réel</h3>
          <p>
            Vos tâches se synchronisent instantanément sur tous vos appareils. 
            Plus jamais de perte de données !
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">🔒</div>
          <h3>Sécurité maximale</h3>
          <p>
            Vos données sont chiffrées et sécurisées. Connexion Google OAuth 
            pour une authentification simplifiée.
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">📱</div>
          <h3>Interface intuitive</h3>
          <p>
            Design moderne et responsive qui s'adapte à tous les écrans. 
            Navigation fluide et expérience utilisateur optimale.
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Suivi détaillé</h3>
          <p>
            Visualisez vos progrès avec des graphiques et statistiques 
            détaillées. Gardez le contrôle de vos objectifs.
          </p>
        </div>
      </div>
    </section>

    <!-- Segments Section -->
    <section class="segments-section">
      <h2 class="section-title">Nos profils spécialisés</h2>
      
      <div class="segments-grid">
        <div class="segment-card" @click="goToRegister">
          <div class="segment-icon">👤</div>
          <h3>Particuliers</h3>
          <p>Gestion personnelle de vos tâches quotidiennes</p>
          <div class="segment-features">
            <span class="feature-tag">Tâches simples</span>
            <span class="feature-tag">Rappels</span>
            <span class="feature-tag">Listes de courses</span>
          </div>
        </div>
        
        <div class="segment-card" @click="goToRegister">
          <div class="segment-icon">🎓</div>
          <h3>Étudiants</h3>
          <p>Organisation de vos études et projets académiques</p>
          <div class="segment-features">
            <span class="feature-tag">Planning d'études</span>
            <span class="feature-tag">Deadlines</span>
            <span class="feature-tag">Notes de cours</span>
          </div>
        </div>
        
        <div class="segment-card" @click="goToRegister">
          <div class="segment-icon">🏥</div>
          <h3>Médical</h3>
          <p>Suivi médical et gestion des rendez-vous santé</p>
          <div class="segment-features">
            <span class="feature-tag">Calendrier médical</span>
            <span class="feature-tag">Rappels médicaux</span>
            <span class="feature-tag">Historique santé</span>
          </div>
        </div>
        
        <div class="segment-card" @click="goToRegister">
          <div class="segment-icon">🧠</div>
          <h3>Mémoire</h3>
          <p>Aide à la mémoire et organisation cognitive</p>
          <div class="segment-features">
            <span class="feature-tag">Rappels fréquents</span>
            <span class="feature-tag">Routines quotidiennes</span>
            <span class="feature-tag">Aide mémoire</span>
          </div>
        </div>
        
        <div class="segment-card" @click="goToRegister">
          <div class="segment-icon">💼</div>
          <h3>Professionnels</h3>
          <p>Gestion de carrière et projets professionnels</p>
          <div class="segment-features">
            <span class="feature-tag">Gestion de projets</span>
            <span class="feature-tag">Planning professionnel</span>
            <span class="feature-tag">Développement carrière</span>
          </div>
        </div>
        
        <div class="segment-card" @click="goToRegister">
          <div class="segment-icon">🏢</div>
          <h3>Entreprises</h3>
          <p>Gestion d'équipe et projets d'entreprise</p>
          <div class="segment-features">
            <span class="feature-tag">Gestion d'équipe</span>
            <span class="feature-tag">Collaboration</span>
            <span class="feature-tag">Reporting</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>Prêt à organiser votre vie ?</h2>
        <p>Rejoignez SyncTasks et découvrez une nouvelle façon de gérer vos tâches</p>
        
        <div class="cta-actions">
          <button class="btn btn-primary btn-large" @click="goToRegister">
            <span class="btn-icon">🚀</span>
            Commencer maintenant
          </button>
          <button class="btn btn-outline btn-large" @click="goToLogin">
            <span class="btn-icon">🔐</span>
            Se connecter
          </button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h4>SyncTasks</h4>
          <p>Organisez vos tâches avec l'intelligence artificielle</p>
        </div>
        
        <div class="footer-section">
          <h4>Fonctionnalités</h4>
          <ul>
            <li>Profils personnalisés</li>
            <li>Assistant IA</li>
            <li>Synchronisation temps réel</li>
            <li>Interface intuitive</li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>Support</h4>
          <ul>
            <li>Aide</li>
            <li>Contact</li>
            <li>Conditions d'utilisation</li>
            <li>Politique de confidentialité</li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2024 SyncTasks. Tous droits réservés.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToLogin = () => {
  router.push('/login');
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* Hero Section */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
  min-height: 80vh;
}

.hero-content {
  text-align: left;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title-icon {
  font-size: 4rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.hero-description {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  opacity: 0.8;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-large {
  padding: 1.2rem 2.5rem;
  font-size: 1.1rem;
}

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-icon {
  font-size: 1.2rem;
}

/* Hero Visual */
.hero-visual {
  position: relative;
  height: 400px;
}

.floating-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  animation: float 6s ease-in-out infinite;
}

.card-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: 20%;
  animation-delay: 2s;
}

.card-3 {
  bottom: 20%;
  left: 30%;
  animation-delay: 4s;
}

.card-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.5rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Features Section */
.features-section {
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.05);
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  font-weight: 700;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.feature-card p {
  opacity: 0.9;
  line-height: 1.6;
}

/* Segments Section */
.segments-section {
  padding: 4rem 2rem;
}

.segments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.segment-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.segment-card:hover {
  transform: translateY(-5px);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.segment-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.segment-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.segment-card p {
  opacity: 0.9;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.segment-features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.feature-tag {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* CTA Section */
.cta-section {
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-content h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.cta-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Footer */
.footer {
  background: rgba(0, 0, 0, 0.2);
  padding: 3rem 2rem 1rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
  opacity: 0.8;
  cursor: pointer;
}

.footer-section li:hover {
  opacity: 1;
}

.footer-bottom {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  opacity: 0.7;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-visual {
    height: 300px;
  }
  
  .features-grid,
  .segments-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>
