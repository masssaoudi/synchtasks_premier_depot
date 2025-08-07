import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  // État simple : true = dark, false = light
  const isDarkMode = ref(false);

  // Initialiser depuis localStorage
  const initTheme = () => {
    console.log('🎨 InitTheme appelé');

    // Nettoyer l'ancien localStorage
    localStorage.removeItem('theme-preference');
    localStorage.removeItem('dark-mode');

    const saved = localStorage.getItem('theme');
    console.log('🎨 Thème sauvegardé:', saved);

    if (saved) {
      isDarkMode.value = saved === 'dark';
      console.log('🎨 Thème chargé depuis localStorage:', saved);
    } else {
      // Détecter la préférence système par défaut
      isDarkMode.value = window.matchMedia(
        '(prefers-color-scheme: dark)'
      ).matches;
      console.log(
        '🎨 Thème détecté depuis système:',
        isDarkMode.value ? 'dark' : 'light'
      );
    }

    applyTheme();
  };

  // Appliquer le thème au DOM
  const applyTheme = () => {
    const html = document.documentElement;
    console.log('🎨 ApplyTheme - isDarkMode:', isDarkMode.value);

    if (isDarkMode.value) {
      html.setAttribute('data-theme', 'dark');
      html.classList.add('dark-mode');
      console.log('🎨 Mode sombre appliqué');
    } else {
      html.setAttribute('data-theme', 'light');
      html.classList.remove('dark-mode');
      console.log('🎨 Mode clair appliqué');
    }

    // Sauvegarder dans localStorage
    const themeValue = isDarkMode.value ? 'dark' : 'light';
    localStorage.setItem('theme', themeValue);
    console.log('🎨 Thème sauvegardé:', themeValue);
  };

  // Toggle simple
  const toggleTheme = () => {
    console.log('🎨 ToggleTheme appelé - Avant:', isDarkMode.value);
    isDarkMode.value = !isDarkMode.value;
    console.log('🎨 ToggleTheme - Après:', isDarkMode.value);
    applyTheme();

    // Notification simple
    const message = isDarkMode.value
      ? 'Mode sombre activé'
      : 'Mode clair activé';
    console.log('🎨', message);
  };

  // Définir le thème
  const setTheme = theme => {
    console.log('🎨 SetTheme appelé avec:', theme);
    isDarkMode.value = theme === 'dark';
    applyTheme();
  };

  return {
    isDarkMode,
    initTheme,
    toggleTheme,
    setTheme,
  };
});
