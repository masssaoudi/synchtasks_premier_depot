// Script de test pour diagnostiquer le problème du mode sombre/clair
// À exécuter dans la console du navigateur

console.log('🔍 === DIAGNOSTIC MODE SOMBRE/CLAIR ===')

// 1. Vérification de l'environnement
console.log('📋 1. ENVIRONNEMENT:')
console.log('- User Agent:', navigator.userAgent)
console.log('- URL:', window.location.href)
console.log('- Vue.js disponible:', typeof Vue !== 'undefined')
console.log('- Pinia disponible:', typeof Pinia !== 'undefined')

// 2. Vérification des stores
console.log('\n📋 2. STORES:')
try {
  // Vérifier si les stores sont disponibles
  const stores = window.__PINIA__ || {}
  console.log('- Stores Pinia:', Object.keys(stores))
  
  // Vérifier le store theme spécifiquement
  if (stores.theme) {
    console.log('- Store theme trouvé:', stores.theme)
    console.log('- isDarkMode:', stores.theme.isDarkMode)
    console.log('- themePreference:', stores.theme.themePreference)
  } else {
    console.log('❌ Store theme non trouvé')
  }
} catch (error) {
  console.error('Erreur accès stores:', error)
}

// 3. Vérification du DOM
console.log('\n📋 3. ÉTAT DU DOM:')
const html = document.documentElement
console.log('- Classes HTML:', html.className)
console.log('- data-theme:', html.getAttribute('data-theme'))
console.log('- style.backgroundColor:', getComputedStyle(html).backgroundColor)

// 4. Vérification du localStorage
console.log('\n📋 4. LOCALSTORAGE:')
console.log('- dark-mode:', localStorage.getItem('dark-mode'))
console.log('- theme-preference:', localStorage.getItem('theme-preference'))
console.log('- Tous les items:', Object.keys(localStorage))

// 5. Vérification des CSS variables
console.log('\n📋 5. CSS VARIABLES:')
const computedStyle = getComputedStyle(html)
console.log('- --bg-primary:', computedStyle.getPropertyValue('--bg-primary'))
console.log('- --text-primary:', computedStyle.getPropertyValue('--text-primary'))
console.log('- --border-color:', computedStyle.getPropertyValue('--border-color'))

// 6. Test de basculement manuel
console.log('\n📋 6. TEST DE BASCULEMENT:')
function testThemeToggle() {
  console.log('🔄 Test de basculement...')
  
  // État avant
  console.log('- Avant toggle:')
  console.log('  * Classes HTML:', html.className)
  console.log('  * data-theme:', html.getAttribute('data-theme'))
  
  // Simuler un clic sur le bouton
  const themeButton = document.querySelector('.nav-btn-theme')
  if (themeButton) {
    console.log('- Bouton trouvé:', themeButton)
    themeButton.click()
    
    // Attendre un peu puis vérifier
    setTimeout(() => {
      console.log('- Après toggle:')
      console.log('  * Classes HTML:', html.className)
      console.log('  * data-theme:', html.getAttribute('data-theme'))
      console.log('  * localStorage dark-mode:', localStorage.getItem('dark-mode'))
    }, 100)
  } else {
    console.log('❌ Bouton thème non trouvé')
  }
}

// 7. Test des fonctions du store
console.log('\n📋 7. TEST DES FONCTIONS STORE:')
function testStoreFunctions() {
  try {
    // Essayer d'accéder au store via l'application Vue
    const app = document.querySelector('#app').__vue_app__
    if (app && app.config.globalProperties.$pinia) {
      const themeStore = app.config.globalProperties.$pinia._s.get('theme')
      if (themeStore) {
        console.log('- Store accessible via app')
        console.log('- isDarkMode avant:', themeStore.isDarkMode)
        themeStore.toggleTheme()
        console.log('- isDarkMode après:', themeStore.isDarkMode)
      }
    }
  } catch (error) {
    console.error('Erreur test store:', error)
  }
}

// 8. Vérification des styles CSS
console.log('\n📋 8. STYLES CSS:')
function checkCSSStyles() {
  const styles = document.styleSheets
  let darkModeStyles = []
  
  for (let i = 0; i < styles.length; i++) {
    try {
      const rules = styles[i].cssRules || styles[i].rules
      for (let j = 0; j < rules.length; j++) {
        const rule = rules[j]
        if (rule.selectorText && rule.selectorText.includes('dark-mode')) {
          darkModeStyles.push(rule.selectorText)
        }
      }
    } catch (e) {
      // CORS peut bloquer l'accès
    }
  }
  
  console.log('- Styles dark-mode trouvés:', darkModeStyles.length)
  if (darkModeStyles.length > 0) {
    console.log('- Sélecteurs:', darkModeStyles)
  }
}

// 9. Test de simulation d'événement
console.log('\n📋 9. TEST ÉVÉNEMENTS:')
function testEvents() {
  // Simuler un changement de préférence système
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  console.log('- Préférence système actuelle:', mediaQuery.matches ? 'dark' : 'light')
  
  // Simuler un événement de changement
  const event = new MediaQueryListEvent('change', {
    matches: !mediaQuery.matches
  })
  
  console.log('- Simulation changement préférence système...')
  mediaQuery.dispatchEvent(event)
}

// 10. Diagnostic complet
console.log('\n📋 10. DIAGNOSTIC COMPLET:')
function runFullDiagnostic() {
  console.log('🚀 Lancement du diagnostic complet...')
  
  // Vérifier l'état initial
  const initialState = {
    htmlClasses: html.className,
    dataTheme: html.getAttribute('data-theme'),
    localStorage: {
      darkMode: localStorage.getItem('dark-mode'),
      preference: localStorage.getItem('theme-preference')
    },
    computedStyle: {
      backgroundColor: getComputedStyle(html).backgroundColor,
      color: getComputedStyle(html).color
    }
  }
  
  console.log('État initial:', initialState)
  
  // Tester le basculement
  testThemeToggle()
  
  // Attendre et vérifier l'état final
  setTimeout(() => {
    const finalState = {
      htmlClasses: html.className,
      dataTheme: html.getAttribute('data-theme'),
      localStorage: {
        darkMode: localStorage.getItem('dark-mode'),
        preference: localStorage.getItem('theme-preference')
      },
      computedStyle: {
        backgroundColor: getComputedStyle(html).backgroundColor,
        color: getComputedStyle(html).color
      }
    }
    
    console.log('État final:', finalState)
    
    // Comparaison
    const hasChanged = 
      initialState.htmlClasses !== finalState.htmlClasses ||
      initialState.dataTheme !== finalState.dataTheme ||
      initialState.localStorage.darkMode !== finalState.localStorage.darkMode
    
    console.log('Changements détectés:', hasChanged)
    
    if (!hasChanged) {
      console.log('❌ PROBLÈME: Aucun changement détecté lors du basculement')
      console.log('🔧 SUGGESTIONS:')
      console.log('1. Vérifier que le store theme est correctement initialisé')
      console.log('2. Vérifier que les styles CSS sont chargés')
      console.log('3. Vérifier que le bouton est correctement lié')
      console.log('4. Vérifier les erreurs dans la console')
    } else {
      console.log('✅ Basculement fonctionne correctement')
    }
  }, 200)
}

// Fonctions d'aide pour les tests
window.testThemeToggle = testThemeToggle
window.testStoreFunctions = testStoreFunctions
window.checkCSSStyles = checkCSSStyles
window.testEvents = testEvents
window.runFullDiagnostic = runFullDiagnostic

// Exécuter les vérifications automatiquement
console.log('\n🔍 VÉRIFICATIONS AUTOMATIQUES:')
checkCSSStyles()
testStoreFunctions()

console.log('\n📝 INSTRUCTIONS:')
console.log('- Pour tester le basculement: testThemeToggle()')
console.log('- Pour diagnostic complet: runFullDiagnostic()')
console.log('- Pour vérifier les styles: checkCSSStyles()')
console.log('- Pour tester les événements: testEvents()')

console.log('\n🎯 === DIAGNOSTIC TERMINÉ ===') 