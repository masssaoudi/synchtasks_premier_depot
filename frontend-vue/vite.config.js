import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
  build: {
    // Optimisations de performance
    target: 'es2015',
    minify: 'esbuild',

    // Optimisation des assets
    assetsInlineLimit: 4096,
    chunkSizeWarningLimit: 1000,
  },
  // Optimisations de développement
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia'],
  },
  // Configuration pour le développement
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
  },
});
