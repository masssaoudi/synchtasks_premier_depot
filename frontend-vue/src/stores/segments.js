import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import axios from 'axios';

export const useSegmentsStore = defineStore('segments', () => {
  // State
  const selectedSegment = ref(localStorage.getItem('selectedSegment') || null);
  const segments = ref([
    {
      id: 'particuliers',
      name: 'Particuliers',
      icon: '👤',
      description: 'Gestion personnelle de vos tâches quotidiennes',
      color: '#4CAF50',
      categories: ['Personnel', 'Maison', 'Santé', 'Loisirs'],
      priorities: ['Urgent', 'Important', 'Normal', 'Faible'],
      features: ['Tâches simples', 'Rappels', 'Listes de courses'],
      dashboardRoute: '/dashboard/particuliers',
    },
    {
      id: 'etudiants',
      name: 'Étudiants',
      icon: '🎓',
      description: 'Organisation de vos études et projets académiques',
      color: '#2196F3',
      categories: ['Cours', 'Devoirs', 'Examens', 'Projets', 'Révisions'],
      priorities: ['Urgent', 'Important', 'Normal', 'Faible'],
      features: ["Planning d'études", 'Deadlines', 'Notes de cours'],
      dashboardRoute: '/dashboard/etudiants',
    },
    {
      id: 'medical',
      name: 'Médical',
      icon: '🏥',
      description: 'Suivi médical et gestion des rendez-vous santé',
      color: '#F44336',
      categories: ['Rendez-vous', 'Traitements', 'Analyses', 'Suivi'],
      priorities: ['Urgent', 'Important', 'Normal', 'Faible'],
      features: ['Calendrier médical', 'Rappels médicaux', 'Historique santé'],
      dashboardRoute: '/dashboard/medical',
    },
    {
      id: 'memoire',
      name: 'Mémoire',
      icon: '🧠',
      description: 'Aide à la mémoire et organisation cognitive',
      color: '#9C27B0',
      categories: ['Rappels', 'Routines', 'Mémoires', 'Habits'],
      priorities: ['Urgent', 'Important', 'Normal', 'Faible'],
      features: ['Rappels fréquents', 'Routines quotidiennes', 'Aide mémoire'],
      dashboardRoute: '/dashboard/memoire',
    },
    {
      id: 'professionnels',
      name: 'Professionnels',
      icon: '💼',
      description: 'Gestion de carrière et projets professionnels',
      color: '#FF9800',
      categories: ['Projets', 'Réunions', 'Formation', 'Networking'],
      priorities: ['Urgent', 'Important', 'Normal', 'Faible'],
      features: [
        'Gestion de projets',
        'Planning professionnel',
        'Développement carrière',
      ],
      dashboardRoute: '/dashboard/professionnels',
    },
    {
      id: 'entreprises',
      name: 'Entreprises',
      icon: '🏢',
      description: "Gestion d'équipe et projets d'entreprise",
      color: '#607D8B',
      categories: ['Projets', 'Équipe', 'Clients', 'Stratégie'],
      priorities: ['Urgent', 'Important', 'Normal', 'Faible'],
      features: ["Gestion d'équipe", 'Collaboration', 'Reporting'],
      dashboardRoute: '/dashboard/entreprises',
    },
  ]);

  // Getters
  const currentSegment = computed(() => {
    return (
      segments.value.find(segment => segment.id === selectedSegment.value) ||
      null
    );
  });

  const isSegmentSelected = computed(() => !!selectedSegment.value);

  // Actions
  const selectSegment = async segmentId => {
    try {
      selectedSegment.value = segmentId;
      localStorage.setItem('selectedSegment', segmentId);

      // Sauvegarder sur le serveur si utilisateur connecté
      const authStore = await import('../stores/auth').then(m =>
        m.useAuthStore()
      );
      if (authStore.isAuthenticated && authStore.currentUser) {
        const userId = authStore.currentUser._id || authStore.currentUser.id;
        await axios.post(`/api/users/${userId}/profile`, {
          segment: segmentId,
        });
        console.log('✅ Profil sauvegardé sur le serveur');
      }

      // Notification
      if (window.$toast) {
        const segment = getSegmentById(segmentId);
        window.$toast.success('Profil', `${segment.name} sélectionné`, 2000);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la sauvegarde du profil:', error);
      if (window.$toast) {
        window.$toast.error(
          'Erreur',
          'Impossible de sauvegarder le profil',
          3000
        );
      }
    }
  };

  const clearSegment = () => {
    selectedSegment.value = null;
    localStorage.removeItem('selectedSegment');

    // Notification
    if (window.$toast) {
      window.$toast.info('Profil', 'Profil désélectionné', 2000);
    }
  };

  const getSegmentById = segmentId => {
    return segments.value.find(segment => segment.id === segmentId);
  };

  const getSegmentCategories = (segmentId = null) => {
    const targetSegment = segmentId
      ? getSegmentById(segmentId)
      : currentSegment.value;
    return targetSegment ? targetSegment.categories : [];
  };

  const getSegmentPriorities = (segmentId = null) => {
    const targetSegment = segmentId
      ? getSegmentById(segmentId)
      : currentSegment.value;
    return targetSegment ? targetSegment.priorities : [];
  };

  const getSegmentFeatures = (segmentId = null) => {
    const targetSegment = segmentId
      ? getSegmentById(segmentId)
      : currentSegment.value;
    return targetSegment ? targetSegment.features : [];
  };

  const getSegmentDashboardRoute = (segmentId = null) => {
    const targetSegment = segmentId
      ? getSegmentById(segmentId)
      : currentSegment.value;
    return targetSegment ? targetSegment.dashboardRoute : '/dashboard';
  };

  // Charger le profil depuis le serveur
  const loadUserProfile = async userId => {
    try {
      const response = await axios.get(`/api/users/${userId}/profile`);
      if (response.data.segment) {
        selectedSegment.value = response.data.segment;
        localStorage.setItem('selectedSegment', response.data.segment);
        console.log(
          '✅ Profil chargé depuis le serveur:',
          response.data.segment
        );
      }
    } catch (error) {
      console.warn('⚠️ Erreur lors du chargement du profil:', error);
      // Fallback sur localStorage
      const savedSegment = localStorage.getItem('selectedSegment');
      if (savedSegment) {
        selectedSegment.value = savedSegment;
      }
    }
  };

  return {
    // State
    selectedSegment,
    segments,

    // Getters
    currentSegment,
    isSegmentSelected,

    // Actions
    selectSegment,
    clearSegment,
    getSegmentById,
    getSegmentCategories,
    getSegmentPriorities,
    getSegmentFeatures,
    getSegmentDashboardRoute,
    loadUserProfile,
  };
});
