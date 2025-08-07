# 🎨 Guide de Test du Mode Sombre/Clair

## 📋 Vue d'ensemble

Ce guide explique comment utiliser les différents scripts de test pour diagnostiquer et résoudre les problèmes du mode sombre/clair dans l'application SyncTasks.

## 🛠️ Scripts Disponibles

### 1. `test_theme_debug.js` - Script Console Navigateur
**Utilisation :** Copier-coller dans la console du navigateur (F12)

**Fonctionnalités :**
- Diagnostic automatique de l'environnement
- Vérification des stores Pinia
- Test du DOM et localStorage
- Vérification des variables CSS
- Test de basculement manuel
- Diagnostic complet avec suggestions

**Instructions :**
```javascript
// 1. Ouvrir la console du navigateur (F12)
// 2. Aller sur l'application SyncTasks
// 3. Copier-coller le contenu de test_theme_debug.js
// 4. Les tests s'exécutent automatiquement
// 5. Utiliser les fonctions disponibles :
testThemeToggle()      // Test basculement
runFullDiagnostic()    // Diagnostic complet
checkCSSStyles()       // Vérifier styles CSS
testEvents()          // Tester événements
```

### 2. `test_theme_automated.py` - Script Python Automatisé
**Utilisation :** Exécution côté serveur avec Selenium

**Prérequis :**
```bash
pip install selenium
# Installer ChromeDriver selon votre système
```

**Exécution :**
```bash
python test_theme_automated.py
```

**Fonctionnalités :**
- Tests automatisés via Selenium
- Vérification de l'accessibilité
- Test du bouton thème
- Vérification de l'état initial
- Test de basculement
- Vérification des variables CSS
- Détection d'erreurs console
- Génération de rapport JSON

### 3. `test_theme_simple.html` - Page de Test Interactive
**Utilisation :** Ouvrir dans le navigateur

**Instructions :**
1. Ouvrir `test_theme_simple.html` dans le navigateur
2. Cliquer sur les boutons de test
3. Observer les résultats en temps réel
4. Vérifier l'aperçu du thème

**Fonctionnalités :**
- Interface graphique de test
- Tests interactifs
- Logs en temps réel
- Aperçu visuel du thème
- Diagnostic complet

## 🔍 Diagnostic Pas à Pas

### Étape 1 : Vérification de Base
```javascript
// Dans la console du navigateur
console.log('🔍 Vérification de base...')
console.log('URL:', window.location.href)
console.log('Vue.js:', typeof Vue !== 'undefined')
console.log('Pinia:', typeof Pinia !== 'undefined')
```

### Étape 2 : Vérification du Store
```javascript
// Vérifier si le store theme est accessible
const stores = window.__PINIA__ || {}
console.log('Stores disponibles:', Object.keys(stores))
if (stores.theme) {
    console.log('Store theme:', stores.theme)
    console.log('isDarkMode:', stores.theme.isDarkMode)
}
```

### Étape 3 : Vérification du DOM
```javascript
const html = document.documentElement
console.log('Classes HTML:', html.className)
console.log('data-theme:', html.getAttribute('data-theme'))
console.log('localStorage:', {
    darkMode: localStorage.getItem('dark-mode'),
    preference: localStorage.getItem('theme-preference')
})
```

### Étape 4 : Test de Basculement
```javascript
// État avant
console.log('Avant - Classes:', html.className)

// Simuler clic sur bouton
const themeButton = document.querySelector('.nav-btn-theme')
if (themeButton) {
    themeButton.click()
    
    // Vérifier après
    setTimeout(() => {
        console.log('Après - Classes:', html.className)
        console.log('localStorage:', localStorage.getItem('dark-mode'))
    }, 100)
}
```

### Étape 5 : Vérification CSS
```javascript
const computedStyle = getComputedStyle(html)
console.log('Variables CSS:', {
    bgPrimary: computedStyle.getPropertyValue('--bg-primary'),
    textPrimary: computedStyle.getPropertyValue('--text-primary'),
    borderColor: computedStyle.getPropertyValue('--border-color')
})
```

## 🚨 Problèmes Courants et Solutions

### Problème 1 : Bouton thème non trouvé
**Symptôme :** `❌ Bouton thème non trouvé`
**Solution :**
```javascript
// Vérifier la classe du bouton
const buttons = document.querySelectorAll('button')
buttons.forEach(btn => {
    if (btn.textContent.includes('🌙') || btn.textContent.includes('☀️')) {
        console.log('Bouton trouvé:', btn)
    }
})
```

### Problème 2 : Store non accessible
**Symptôme :** `❌ Store theme non trouvé`
**Solution :**
```javascript
// Vérifier l'initialisation de Pinia
const app = document.querySelector('#app')
if (app && app.__vue_app__) {
    const pinia = app.__vue_app__.config.globalProperties.$pinia
    console.log('Pinia:', pinia)
}
```

### Problème 3 : Variables CSS manquantes
**Symptôme :** `❌ Aucune variable CSS trouvée`
**Solution :**
```css
/* Vérifier que les variables sont définies dans style.css */
:root {
    --bg-primary: #ffffff;
    --text-primary: #2c3e50;
    --border-color: #e1e8ed;
}

.dark-mode {
    --bg-primary: #2c3e50;
    --text-primary: #ecf0f1;
    --border-color: #34495e;
}
```

### Problème 4 : localStorage non persistant
**Symptôme :** Les préférences ne sont pas sauvegardées
**Solution :**
```javascript
// Vérifier l'accès au localStorage
try {
    localStorage.setItem('test', 'value')
    const test = localStorage.getItem('test')
    console.log('localStorage fonctionnel:', test === 'value')
} catch (e) {
    console.error('localStorage non disponible:', e)
}
```

## 📊 Interprétation des Résultats

### Tests Réussis ✅
- **Application accessible :** L'application se charge correctement
- **Bouton thème présent :** Le bouton de basculement est visible
- **État initial thème :** Les données de thème sont présentes
- **Basculement thème :** Le changement de thème fonctionne
- **Variables CSS :** Les variables CSS sont définies
- **Erreurs console :** Aucune erreur JavaScript

### Tests Échoués ❌
- **Application non accessible :** Problème de serveur ou réseau
- **Bouton thème manquant :** Problème de rendu ou de classe CSS
- **Store non trouvé :** Problème d'initialisation Pinia
- **Basculement non fonctionnel :** Problème de logique ou d'événements
- **Variables CSS manquantes :** Problème de chargement CSS
- **Erreurs console :** Problèmes JavaScript à corriger

## 🔧 Actions Correctives

### Si le bouton n'apparaît pas :
1. Vérifier la classe CSS `.nav-btn-theme`
2. Vérifier que l'utilisateur est authentifié
3. Vérifier le rendu du composant NavigationBar

### Si le basculement ne fonctionne pas :
1. Vérifier la fonction `toggleTheme()` dans le store
2. Vérifier les logs console pour les erreurs
3. Vérifier que le store est correctement initialisé

### Si les styles ne changent pas :
1. Vérifier les variables CSS dans `style.css`
2. Vérifier que la classe `dark-mode` est appliquée
3. Vérifier que les styles sont chargés

### Si localStorage ne fonctionne pas :
1. Vérifier les permissions du navigateur
2. Vérifier le mode privé/incognito
3. Vérifier les erreurs de quota

## 📝 Rapport de Test

Après exécution des tests, un rapport est généré avec :

```json
{
  "tests": [
    {
      "name": "Nom du test",
      "status": "PASS|FAIL|WARN",
      "details": "Informations détaillées"
    }
  ],
  "summary": {
    "total": 6,
    "passed": 5,
    "failed": 1,
    "success_rate": 83.3
  }
}
```

## 🎯 Prochaines Étapes

1. **Exécuter les tests** avec les scripts fournis
2. **Identifier les problèmes** selon les résultats
3. **Appliquer les corrections** suggérées
4. **Réexécuter les tests** pour vérifier
5. **Documenter les solutions** pour référence future

## 📞 Support

En cas de problème persistant :
1. Consulter les logs de la console
2. Vérifier les erreurs réseau
3. Tester sur différents navigateurs
4. Vérifier la compatibilité des dépendances 