import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useSegmentsStore } from './segments';

export const useAIModulesStore = defineStore('aiModules', () => {
  const segmentsStore = useSegmentsStore();

  // Modules IA par segment
  const aiModules = ref({
    particuliers: {
      name: 'Assistant Personnel',
      icon: '👤',
      color: '#4CAF50',
      modules: {
        chat: {
          name: 'Chat Personnel',
          description: 'Discutez de vos objectifs personnels',
          prompt:
            'Tu es un assistant personnel qui aide à organiser la vie quotidienne. Donne des conseils pratiques et motivants.',
          features: ['Conseils personnels', 'Motivation', 'Organisation'],
        },
        history: {
          name: 'Historique Personnel',
          description: 'Suivi de vos habitudes et progrès',
          prompt:
            'Analyse les habitudes et propose des améliorations pour la vie quotidienne.',
          features: ['Suivi des habitudes', 'Progression', 'Améliorations'],
        },
        insights: {
          name: 'Conseils Quotidiens',
          description: 'Conseils personnalisés pour chaque jour',
          prompt:
            'Donne des conseils pratiques pour améliorer la qualité de vie quotidienne.',
          features: ['Conseils quotidiens', 'Optimisation', 'Bien-être'],
        },
      },
    },
    etudiants: {
      name: 'Assistant Académique',
      icon: '🎓',
      color: '#2196F3',
      modules: {
        chat: {
          name: 'Chat Académique',
          description: 'Discutez de vos études et projets',
          prompt:
            "Tu es un assistant académique qui aide à organiser les études. Donne des conseils d'étude et de motivation.",
          features: [
            "Conseils d'étude",
            'Motivation',
            'Organisation académique',
          ],
        },
        history: {
          name: 'Historique Académique',
          description: 'Suivi de votre progression académique',
          prompt:
            "Analyse la progression académique et propose des stratégies d'amélioration.",
          features: ['Progression académique', 'Performance', 'Stratégies'],
        },
        insights: {
          name: "Conseils d'Étude",
          description: 'Conseils pour optimiser vos études',
          prompt:
            "Donne des conseils pratiques pour améliorer l'efficacité des études.",
          features: ["Techniques d'étude", 'Optimisation', 'Révisions'],
        },
      },
    },
    medical: {
      name: 'Assistant Santé',
      icon: '🏥',
      color: '#F44336',
      modules: {
        chat: {
          name: 'Chat Santé',
          description: 'Discutez de votre suivi médical',
          prompt:
            'Tu es un assistant santé qui aide à organiser le suivi médical. Donne des conseils de santé et de bien-être.',
          features: ['Conseils santé', 'Suivi médical', 'Bien-être'],
        },
        history: {
          name: 'Historique Médical',
          description: 'Suivi de votre santé et traitements',
          prompt:
            'Analyse le suivi médical et propose des améliorations pour la santé.',
          features: ['Suivi médical', 'Évolution santé', 'Améliorations'],
        },
        insights: {
          name: 'Conseils Santé',
          description: 'Conseils pour maintenir une bonne santé',
          prompt:
            'Donne des conseils pratiques pour maintenir et améliorer la santé.',
          features: ['Conseils santé', 'Prévention', 'Bien-être'],
        },
      },
    },
    memoire: {
      name: 'Assistant Mémoire',
      icon: '🧠',
      color: '#9C27B0',
      modules: {
        chat: {
          name: 'Chat Cognitif',
          description: 'Discutez de votre mémoire et cognition',
          prompt:
            'Tu es un assistant cognitif qui aide à améliorer la mémoire. Donne des conseils pour stimuler la cognition.',
          features: [
            'Stimulation cognitive',
            'Amélioration mémoire',
            'Techniques',
          ],
        },
        history: {
          name: 'Historique Cognitif',
          description: 'Suivi de votre évolution cognitive',
          prompt:
            "Analyse l'évolution cognitive et propose des exercices d'amélioration.",
          features: ['Évolution cognitive', 'Exercices', 'Améliorations'],
        },
        insights: {
          name: 'Conseils Cognitifs',
          description: 'Conseils pour stimuler votre mémoire',
          prompt:
            'Donne des conseils pratiques pour stimuler et améliorer la mémoire.',
          features: ['Techniques mémoire', 'Stimulation', 'Exercices'],
        },
      },
    },
    professionnels: {
      name: 'Assistant Professionnel',
      icon: '💼',
      color: '#FF9800',
      modules: {
        chat: {
          name: 'Chat Carrière',
          description: 'Discutez de votre carrière et projets',
          prompt:
            'Tu es un assistant professionnel qui aide à développer sa carrière. Donne des conseils de développement professionnel.',
          features: ['Conseils carrière', 'Développement', 'Stratégies'],
        },
        history: {
          name: 'Historique Professionnel',
          description: 'Suivi de votre évolution de carrière',
          prompt:
            "Analyse l'évolution professionnelle et propose des stratégies de développement.",
          features: ['Évolution carrière', 'Performance', 'Stratégies'],
        },
        insights: {
          name: 'Conseils Carrière',
          description: 'Conseils pour développer votre carrière',
          prompt:
            'Donne des conseils pratiques pour développer sa carrière professionnelle.',
          features: ['Développement carrière', 'Optimisation', 'Stratégies'],
        },
      },
    },
    entreprises: {
      name: 'Assistant Entreprise',
      icon: '🏢',
      color: '#607D8B',
      modules: {
        chat: {
          name: 'Chat Management',
          description: "Discutez de la gestion d'équipe",
          prompt:
            "Tu es un assistant management qui aide à optimiser la gestion d'équipe. Donne des conseils de leadership.",
          features: [
            'Conseils management',
            'Leadership',
            'Optimisation équipe',
          ],
        },
        history: {
          name: 'Historique Équipe',
          description: "Suivi de la performance d'équipe",
          prompt:
            "Analyse la performance d'équipe et propose des stratégies d'amélioration.",
          features: ['Performance équipe', 'KPIs', 'Améliorations'],
        },
        insights: {
          name: 'Conseils Management',
          description: 'Conseils pour optimiser votre équipe',
          prompt:
            "Donne des conseils pratiques pour optimiser la gestion et la performance d'équipe.",
          features: ['Optimisation équipe', 'Leadership', 'Stratégies'],
        },
      },
    },
  });

  // Getters
  const currentSegmentModules = computed(() => {
    const currentSegment = segmentsStore.selectedSegment;
    return currentSegment ? aiModules.value[currentSegment] : null;
  });

  const currentChatModule = computed(() => {
    return currentSegmentModules.value?.modules?.chat || null;
  });

  const currentHistoryModule = computed(() => {
    return currentSegmentModules.value?.modules?.history || null;
  });

  const currentInsightsModule = computed(() => {
    return currentSegmentModules.value?.modules?.insights || null;
  });

  const allModules = computed(() => {
    return currentSegmentModules.value?.modules || {};
  });

  // Actions
  const getModulePrompt = moduleType => {
    const module = currentSegmentModules.value?.modules?.[moduleType];
    return (
      module?.prompt || 'Tu es un assistant IA qui aide à organiser les tâches.'
    );
  };

  const getModuleFeatures = moduleType => {
    const module = currentSegmentModules.value?.modules?.[moduleType];
    return module?.features || [];
  };

  const getModuleDescription = moduleType => {
    const module = currentSegmentModules.value?.modules?.[moduleType];
    return module?.description || 'Module IA';
  };

  return {
    // State
    aiModules,

    // Getters
    currentSegmentModules,
    currentChatModule,
    currentHistoryModule,
    currentInsightsModule,
    allModules,

    // Actions
    getModulePrompt,
    getModuleFeatures,
    getModuleDescription,
  };
});
