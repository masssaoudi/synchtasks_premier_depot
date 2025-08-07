/**
 * 🎈 Directive v-autotip - Tooltips automatiques pour SyncTasks
 * Usage: v-autotip="'Mon tooltip'" ou v-autotip="dynamicContent"
 */

import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';

export default {
  mounted(el, binding) {
    // Contenu du tooltip
    const content =
      binding.value ||
      el.getAttribute('data-info') ||
      el.getAttribute('title') ||
      'Info disponible au survol';

    // Configuration du tooltip
    const instance = tippy(el, {
      content,
      delay: [300, 100], // Délai d'apparition/disparition
      duration: [200, 150], // Animation
      animation: 'scale',
      theme: 'synchtasks', // Thème personnalisé
      placement: 'top',
      arrow: true,
      interactive: false,
      hideOnClick: true,

      // Style personnalisé selon le contenu
      onShow(instance) {
        // Détection du thème sombre/clair
        const isDark =
          document.documentElement.classList.contains('dark') ||
          document.body.classList.contains('dark-theme');

        if (isDark) {
          instance.setProps({ theme: 'synchtasks-dark' });
        } else {
          instance.setProps({ theme: 'synchtasks-light' });
        }
      },
    });

    // Stocker l'instance pour les mises à jour
    el._tippyInstance = instance;
  },

  updated(el, binding) {
    // Mettre à jour le contenu si nécessaire
    if (el._tippyInstance && binding.value !== binding.oldValue) {
      const newContent =
        binding.value ||
        el.getAttribute('data-info') ||
        el.getAttribute('title') ||
        'Info mise à jour';

      el._tippyInstance.setContent(newContent);
    }
  },

  unmounted(el) {
    // Nettoyer l'instance
    if (el._tippyInstance) {
      el._tippyInstance.destroy();
      delete el._tippyInstance;
    }
  },
};
