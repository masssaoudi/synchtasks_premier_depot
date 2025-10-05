<template>
  <div class="segment-selector">
    <div class="hero-section">
      <h1 class="hero-title">SyncTasks</h1>
      <p class="hero-subtitle">
        Choisissez votre profil pour une expérience personnalisée
      </p>
    </div>

    <div class="segments-grid">
      <div
        v-for="segment in segments"
        :key="segment.id"
        class="segment-card"
        :class="{ selected: selectedSegment === segment.id }"
        :style="{ '--segment-color': segment.color }"
        :title="`Clic simple : Sélectionner | Double-clic : Aller directement au dashboard ${segment.name}`"
        @click="selectSegment(segment.id)"
        @dblclick="goToDashboard(segment.id)"
      >
        <div class="segment-icon">{{ segment.icon }}</div>
        <h3 class="segment-name">{{ segment.name }}</h3>
        <p class="segment-description">{{ segment.description }}</p>

        <div class="segment-features">
          <span
            v-for="feature in segment.features.slice(0, 2)"
            :key="feature"
            class="feature-tag"
          >
            {{ feature }}
          </span>
        </div>

        <!-- Indicateur de sélection -->
        <div v-if="selectedSegment === segment.id" class="selection-indicator">
          <span class="check-icon">✅</span>
        </div>

        <!-- Bouton d'accès direct -->
        <div class="direct-access">
          <button
            class="btn-direct-access"
            :style="{ '--segment-color': segment.color }"
            @click.stop="goToDashboard(segment.id)"
          >
            Accéder directement
          </button>
        </div>
      </div>
    </div>

    <div class="selected-segment-info">
      <div class="info-card">
        <h3>
          Profil sélectionné :
          {{ currentSegment?.name || 'Aucun profil sélectionné' }}
        </h3>
        <p>
          {{
            currentSegment?.description ||
            'Sélectionnez un profil pour continuer'
          }}
        </p>

        <div v-if="currentSegment" class="features-list">
          <h4>Fonctionnalités incluses :</h4>
          <ul>
            <li v-for="feature in currentSegment.features" :key="feature">
              {{ feature }}
            </li>
          </ul>
        </div>

        <div class="action-buttons">
          <button
            v-if="selectedSegment"
            class="btn btn-secondary"
            @click="clearSegment"
          >
            Changer de profil
          </button>
          <button
            v-if="selectedSegment"
            class="btn btn-primary"
            :disabled="!selectedSegment"
            @click="continueWithSegment"
          >
            Continuer avec ce profil
          </button>
        </div>
      </div>
    </div>

    <!-- Tooltip d'aide -->
    <div v-if="!selectedSegment" class="help-tooltip">
      <div class="tooltip-content">
        <span class="tooltip-icon">💡</span>
        <p>
          Cliquez sur un profil pour le sélectionner, ou double-cliquez pour y
          accéder directement
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { useSegmentsStore } from '../stores/segments';
  import { useAuthStore } from '../stores/auth';

  const router = useRouter();
  const segmentsStore = useSegmentsStore();
  const authStore = useAuthStore();

  const segments = computed(() => segmentsStore.segments);
  const selectedSegment = computed(() => segmentsStore.selectedSegment);
  const currentSegment = computed(() => segmentsStore.currentSegment);

  onMounted(async () => {
    // Charger le profil utilisateur si connecté
    if (authStore.isAuthenticated && authStore.currentUser) {
      const userId = authStore.currentUser._id || authStore.currentUser.id;
      await segmentsStore.loadUserProfile(userId);
    }
  });

  const selectSegment = async segmentId => {
    await segmentsStore.selectSegment(segmentId);
  };

  const clearSegment = () => {
    segmentsStore.clearSegment();
  };

  const continueWithSegment = () => {
    if (!selectedSegment.value) {
      return;
    }

    // Rediriger vers le dashboard spécialisé selon le segment
    const route = segmentsStore.getSegmentDashboardRoute(selectedSegment.value);
    router.push(route);
  };

  const goToDashboard = segmentId => {
    // Redirection directe vers le dashboard
    const route = segmentsStore.getSegmentDashboardRoute(segmentId);
    router.push(route);
  };
</script>

<style scoped>
  .segment-selector {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  .hero-section {
    text-align: center;
    margin-bottom: 3rem;
  }

  .hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary, #2c3e50);
    margin-bottom: 0.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary, #6c757d);
    margin: 0;
  }

  .segments-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
  }

  .segment-card {
    background: var(--bg-primary, #ffffff);
    border: 2px solid var(--border-color, #e1e5e9);
    border-radius: 16px;
    padding: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .segment-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border-color: var(--segment-color);
  }

  .segment-card.selected {
    border-color: var(--segment-color);
    background: linear-gradient(
      135deg,
      var(--segment-color) 0%,
      rgba(255, 255, 255, 0.95) 100%
    );
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  .segment-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
  }

  .segment-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary, #2c3e50);
    margin: 0 0 0.5rem 0;
  }

  .segment-description {
    color: var(--text-secondary, #6c757d);
    margin: 0 0 1rem 0;
    line-height: 1.5;
  }

  .segment-features {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .feature-tag {
    background: var(--segment-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .selection-indicator {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: var(--segment-color);
    color: white;
    border-radius: 50%;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      transform: scale(1);
    }
  }

  .direct-access {
    margin-top: 1rem;
  }

  .btn-direct-access {
    background: var(--segment-color);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
  }

  .btn-direct-access:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .selected-segment-info {
    background: var(--bg-secondary, #f8f9fa);
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid var(--border-color, #e1e5e9);
  }

  .info-card h3 {
    margin: 0 0 0.5rem 0;
    color: var(--text-primary, #2c3e50);
  }

  .info-card p {
    margin: 0 0 1.5rem 0;
    color: var(--text-secondary, #6c757d);
  }

  .features-list {
    margin: 1.5rem 0;
  }

  .features-list h4 {
    margin: 0 0 0.5rem 0;
    color: var(--text-primary, #2c3e50);
  }

  .features-list ul {
    margin: 0;
    padding-left: 1.5rem;
  }

  .features-list li {
    margin: 0.25rem 0;
    color: var(--text-secondary, #6c757d);
  }

  .action-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.875rem;
  }

  .btn-primary {
    background: var(--primary-color, #007bff);
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--primary-hover, #0056b3);
    transform: translateY(-1px);
  }

  .btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-secondary {
    background: var(--bg-primary, #ffffff);
    color: var(--text-primary, #2c3e50);
    border: 1px solid var(--border-color, #e1e5e9);
  }

  .btn-secondary:hover {
    background: var(--bg-secondary, #f8f9fa);
  }

  .help-tooltip {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    z-index: 1000;
  }

  .tooltip-content {
    background: var(--primary-color, #007bff);
    color: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    max-width: 300px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .tooltip-icon {
    font-size: 1.2rem;
  }

  .tooltip-content p {
    margin: 0;
    font-size: 0.875rem;
    line-height: 1.4;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .segment-selector {
      padding: 1rem;
    }

    .segments-grid {
      grid-template-columns: 1fr;
    }

    .hero-title {
      font-size: 2rem;
    }

    .action-buttons {
      flex-direction: column;
    }

    .help-tooltip {
      bottom: 1rem;
      right: 1rem;
      left: 1rem;
    }
  }

  /* Dark mode */
  [data-theme='dark'] .segment-card {
    background: #1a1a1a;
    border-color: #404040;
  }

  [data-theme='dark'] .segment-card:hover {
    background: #2d2d2d;
  }

  [data-theme='dark'] .selected-segment-info {
    background: #2d2d2d;
    border-color: #404040;
  }

  [data-theme='dark'] .hero-title,
  [data-theme='dark'] .segment-name,
  [data-theme='dark'] .info-card h3,
  [data-theme='dark'] .features-list h4 {
    color: #ffffff;
  }

  [data-theme='dark'] .hero-subtitle,
  [data-theme='dark'] .segment-description,
  [data-theme='dark'] .info-card p,
  [data-theme='dark'] .features-list li {
    color: #b0b0b0;
  }
</style>
