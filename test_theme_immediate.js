// Script de test immédiat pour le mode sombre/clair
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🎨 === TEST IMMÉDIAT MODE SOMBRE/CLAIR ===')

// Test 1: Vérification de base
console.log('📋 1. Vérification de base:')
console.log('URL:', window.location.href)
console.log('Titre:', document.title)

// Test 2: Recherche du bouton thème
console.log('\n📋 2. Recherche du bouton thème:')
const themeButton = document.querySelector('.nav-btn-theme')
if (themeButton) {
    console.log('✅ Bouton thème trouvé')
    console.log('Texte:', themeButton.textContent)
    console.log('Classes:', themeButton.className)
    
    // Test du clic
    console.log('\n🔄 Test du clic sur le bouton...')
    themeButton.click()
    
    setTimeout(() => {
        console.log('Après clic - Classes HTML:', document.documentElement.className)
        console.log('Après clic - localStorage:', localStorage.getItem('dark-mode'))
    }, 500)
    
} else {
    console.log('❌ Bouton thème non trouvé')
    
    // Chercher tous les boutons
    const allButtons = document.querySelectorAll('button')
    console.log('Nombre total de boutons:', allButtons.length)
    
    allButtons.forEach((btn, index) => {
        if (btn.textContent.includes('🌙') || btn.textContent.includes('☀️')) {
            console.log(`✅ Bouton thème trouvé (${index}):`, btn.textContent)
        }
    })
}

// Test 3: État du thème
console.log('\n📋 3. État du thème:')
const html = document.documentElement
console.log('Classes HTML:', html.className)
console.log('data-theme:', html.getAttribute('data-theme'))
console.log('localStorage dark-mode:', localStorage.getItem('dark-mode'))

// Test 4: Variables CSS
console.log('\n📋 4. Variables CSS:')
const computedStyle = getComputedStyle(html)
const cssVars = {
    bgPrimary: computedStyle.getPropertyValue('--bg-primary'),
    textPrimary: computedStyle.getPropertyValue('--text-primary'),
    borderColor: computedStyle.getPropertyValue('--border-color')
}
console.log('Variables CSS:', cssVars)

// Test 5: Test manuel du basculement
console.log('\n📋 5. Test manuel du basculement:')
const isDarkBefore = html.classList.contains('dark-mode')
console.log('Mode sombre avant:', isDarkBefore)

// Appliquer le thème opposé manuellement
if (isDarkBefore) {
    html.classList.remove('dark-mode')
    html.setAttribute('data-theme', 'light')
    localStorage.setItem('dark-mode', 'false')
    console.log('🔄 Passage en mode clair')
} else {
    html.classList.add('dark-mode')
    html.setAttribute('data-theme', 'dark')
    localStorage.setItem('dark-mode', 'true')
    console.log('🔄 Passage en mode sombre')
}

// Vérifier après
setTimeout(() => {
    const isDarkAfter = html.classList.contains('dark-mode')
    console.log('Mode sombre après:', isDarkAfter)
    console.log('Classes HTML après:', html.className)
    console.log('localStorage après:', localStorage.getItem('dark-mode'))
    
    if (isDarkBefore !== isDarkAfter) {
        console.log('✅ Basculement manuel réussi!')
    } else {
        console.log('❌ Basculement manuel échoué')
    }
}, 200)

// Test 6: Vérification de l'application Vue
console.log('\n📋 6. Vérification Vue.js:')
const app = document.querySelector('#app')
if (app) {
    console.log('✅ Élément #app trouvé')
    if (app.__vue_app__) {
        console.log('✅ Application Vue initialisée')
        
        // Essayer d'accéder au store
        try {
            const pinia = app.__vue_app__.config.globalProperties.$pinia
            if (pinia) {
                console.log('✅ Pinia trouvé')
                const stores = pinia._s
                console.log('Stores disponibles:', Object.keys(stores))
                
                if (stores.theme) {
                    console.log('✅ Store theme trouvé')
                    console.log('isDarkMode:', stores.theme.isDarkMode)
                } else {
                    console.log('❌ Store theme non trouvé')
                }
            } else {
                console.log('❌ Pinia non trouvé')
            }
        } catch (e) {
            console.log('❌ Erreur accès store:', e.message)
        }
    } else {
        console.log('❌ Application Vue non initialisée')
    }
} else {
    console.log('❌ Élément #app non trouvé')
}

// Test 7: Résumé final
console.log('\n📋 7. Résumé final:')
const hasThemeButton = !!themeButton
const hasThemeData = html.getAttribute('data-theme') || localStorage.getItem('dark-mode')
const hasCSSVars = cssVars.bgPrimary || cssVars.textPrimary
const hasVueApp = !!app && !!app.__vue_app__

console.log('Bouton thème:', hasThemeButton ? '✅' : '❌')
console.log('Données thème:', hasThemeData ? '✅' : '❌')
console.log('Variables CSS:', hasCSSVars ? '✅' : '❌')
console.log('Application Vue:', hasVueApp ? '✅' : '❌')

if (hasThemeButton && hasThemeData && hasCSSVars && hasVueApp) {
    console.log('\n🎉 THÈME COMPLÈTEMENT FONCTIONNEL!')
} else {
    console.log('\n⚠️ PROBLÈMES DÉTECTÉS:')
    if (!hasThemeButton) console.log('- Bouton thème manquant')
    if (!hasThemeData) console.log('- Données thème manquantes')
    if (!hasCSSVars) console.log('- Variables CSS manquantes')
    if (!hasVueApp) console.log('- Application Vue non fonctionnelle')
}

console.log('\n🎯 === TEST IMMÉDIAT TERMINÉ ===') 