# 🚀 Configuration ESLint pour SyncTasks

## 📋 Vue d'ensemble

Cette configuration ESLint est optimisée pour un projet Vue 3 avec Composition API, TypeScript et Vite.

## 🛠️ Configuration

### Fichiers de configuration

- **`.eslintrc.js`** : Configuration principale ESLint
- **`.eslintignore`** : Fichiers à ignorer
- **`.vscode/settings.json`** : Configuration VS Code/Cursor
- **`.prettierrc`** : Configuration Prettier

### Règles principales

#### 🎯 Vue.js
- `vue/multi-word-component-names`: Désactivé (permet des noms simples)
- `vue/no-v-html`: Warning (sécurité XSS)
- `vue/component-name-in-template-casing`: PascalCase requis
- `vue/attribute-hyphenation`: Toujours avec tirets
- `vue/v-on-event-hyphenation`: Toujours avec tirets

#### 🎯 JavaScript
- `no-console`: Warning en production, désactivé en développement
- `no-debugger`: Warning en production, désactivé en développement
- `no-unused-vars`: Warning avec pattern `^_` ignoré
- `prefer-const`: Erreur (force l'utilisation de const)
- `no-var`: Erreur (force l'utilisation de let/const)

#### 🎯 Code Quality
- `eqeqeq`: Erreur (force `===` et `!==`)
- `curly`: Erreur (force les accolades)
- `no-eval`: Erreur (sécurité)
- `consistent-return`: Warning

## 📦 Scripts disponibles

```bash
# Vérifier le code sans corriger
npm run lint:check

# Corriger automatiquement les erreurs
npm run lint:fix

# Formater avec Prettier
npm run format

# Vérifier les types TypeScript
npm run type-check

# Vérifier tout (lint + types)
npm run check-all
```

## 🔧 Configuration VS Code/Cursor

### Extensions recommandées

1. **ESLint** (`dbaeumer.vscode-eslint`)
2. **Prettier** (`esbenp.prettier-vscode`)
3. **Vue Language Features** (`Vue.volar`)

### ⚠️ IMPORTANT : Éviter cette extension

❌ **NE PAS INSTALLER** : `evolution-gaming--vscode-eslint`
- Cette extension utilise l'ancienne API `CLIEngine`
- Cause des erreurs avec ESLint v8+
- Remplace par l'extension officielle

## 🚨 Résolution des problèmes

### Erreur "CLIEngine is not a constructor"

**Cause** : Extension ESLint obsolète

**Solution** :
1. Désinstaller l'extension `evolution-gaming--vscode-eslint`
2. Installer `dbaeumer.vscode-eslint`
3. Redémarrer Cursor/VS Code

### Erreurs de parsing TypeScript

**Cause** : Fichiers `.d.ts` mal configurés

**Solution** : La configuration inclut déjà un parser TypeScript pour les fichiers `.ts` et `.d.ts`

## 📊 État actuel

- ✅ ESLint v8.57.0 installé
- ✅ Configuration Vue 3 optimisée
- ✅ Support TypeScript
- ✅ Intégration Prettier
- ✅ Scripts npm configurés
- ✅ Configuration VS Code/Cursor

## 🎯 Prochaines étapes

1. **Corriger les warnings** dans le code existant
2. **Configurer les hooks Git** pour lint automatique
3. **Ajouter des tests** pour la qualité du code
4. **Documenter les conventions** de l'équipe

## 📝 Notes

- Les warnings sont normaux et n'empêchent pas le build
- Les erreurs doivent être corrigées avant le commit
- Utiliser `npm run lint:fix` pour corriger automatiquement
- Le formatage Prettier est appliqué automatiquement à la sauvegarde 