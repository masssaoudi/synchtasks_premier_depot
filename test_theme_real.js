// Script de test pour l'application réelle
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🎨 === TEST RÉEL MODE SOMBRE/CLAIR ===')

// Test 1: Vérification de base
console.log('📋 1. Vérification de base:')
console.log('URL:', window.location.href)
console.log('Titre:', document.title)

// Test 2: Recherche du bouton thème dans l'application réelle
console.log('\n📋 2. Recherche du bouton thème:')
const themeButton = document.querySelector('.nav-btn-theme')
if (themeButton) {
    console.log('✅ Bouton thème trouvé')
    console.log('Texte:', themeButton.textContent)
    console.log('Classes:', themeButton.className)
    
    // Test du clic sur le bouton réel
    console.log('\n🔄 Test du clic sur le bouton réel...')
    const isDarkBefore = document.documentElement.classList.contains('dark-mode')
    console.log('Mode sombre avant clic:', isDarkBefore)
    
    themeButton.click()
    
    setTimeout(() => {
        const isDarkAfter = document.documentElement.classList.contains('dark-mode')
        console.log('Mode sombre après clic:', isDarkAfter)
        console.log('Classes HTML après:', document.documentElement.className)
        console.log('localStorage après:', localStorage.getItem('dark-mode'))
        
        if (isDarkBefore !== isDarkAfter) {
            console.log('✅ Basculement via bouton réussi!')
        } else {
            console.log('❌ Basculement via bouton échoué')
        }
    }, 500)
    
} else {
    console.log('❌ Bouton thème non trouvé')
    
    // Chercher tous les boutons avec des icônes de thème
    const allButtons = document.querySelectorAll('button')
    console.log('Nombre total de boutons:', allButtons.length)
    
    let foundThemeButton = false
    allButtons.forEach((btn, index) => {
        const text = btn.textContent || ''
        if (text.includes('🌙') || text.includes('☀️') || text.includes('Clair') || text.includes('Sombre')) {
            console.log(`✅ Bouton thème trouvé (${index}):`, text)
            foundThemeButton = true
        }
    })
    
    if (!foundThemeButton) {
        console.log('❌ Aucun bouton thème trouvé')
    }
}

// Test 3: État du thème
console.log('\n📋 3. État du thème:')
const html = document.documentElement
console.log('Classes HTML:', html.className)
console.log('data-theme:', html.getAttribute('data-theme'))
console.log('localStorage dark-mode:', localStorage.getItem('dark-mode'))
console.log('localStorage theme-preference:', localStorage.getItem('theme-preference'))

// Test 4: Variables CSS de l'application réelle
console.log('\n📋 4. Variables CSS:')
const computedStyle = getComputedStyle(html)
const cssVars = {
    bgPrimary: computedStyle.getPropertyValue('--bg-primary'),
    textPrimary: computedStyle.getPropertyValue('--text-primary'),
    borderColor: computedStyle.getPropertyValue('--border-color'),
    bgSecondary: computedStyle.getPropertyValue('--bg-secondary'),
    textSecondary: computedStyle.getPropertyValue('--text-secondary')
}
console.log('Variables CSS:', cssVars)

// Test 5: Vérification de l'application Vue
console.log('\n📋 5. Vérification Vue.js:')
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
                    console.log('themePreference:', stores.theme.themePreference)
                    
                    // Test direct du store
                    console.log('\n🔄 Test direct du store...')
                    const isDarkBefore = stores.theme.isDarkMode
                    console.log('isDarkMode avant:', isDarkBefore)
                    
                    // Appeler toggleTheme directement
                    if (stores.theme.toggleTheme) {
                        stores.theme.toggleTheme()
                        setTimeout(() => {
                            console.log('isDarkMode après toggle:', stores.theme.isDarkMode)
                            console.log('Classes HTML après:', document.documentElement.className)
                        }, 100)
                    } else {
                        console.log('❌ toggleTheme non disponible')
                    }
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

// Test 6: Test visuel des couleurs
console.log('\n📋 6. Test visuel:')
const bodyStyle = getComputedStyle(document.body)
console.log('Couleur de fond body:', bodyStyle.backgroundColor)
console.log('Couleur de texte body:', bodyStyle.color)

// Test 7: Vérification des styles appliqués
console.log('\n📋 7. Vérification des styles:')
const navBar = document.querySelector('.navigation-bar')
if (navBar) {
    const navStyle = getComputedStyle(navBar)
    console.log('Couleur de fond nav:', navStyle.backgroundColor)
    console.log('Couleur de texte nav:', navStyle.color)
} else {
    console.log('❌ Navigation bar non trouvée')
}

// Test 8: Résumé final
console.log('\n📋 8. Résumé final:')
const hasThemeButton = !!themeButton
const hasThemeData = html.getAttribute('data-theme') || localStorage.getItem('dark-mode')
const hasCSSVars = cssVars.bgPrimary || cssVars.textPrimary
const hasVueApp = !!app && !!app.__vue_app__
const hasWorkingToggle = hasThemeButton && hasVueApp

console.log('Bouton thème:', hasThemeButton ? '✅' : '❌')
console.log('Données thème:', hasThemeData ? '✅' : '❌')
console.log('Variables CSS:', hasCSSVars ? '✅' : '❌')
console.log('Application Vue:', hasVueApp ? '✅' : '❌')
console.log('Basculement fonctionnel:', hasWorkingToggle ? '✅' : '❌')

if (hasWorkingToggle && hasCSSVars) {
    console.log('\n🎉 THÈME COMPLÈTEMENT FONCTIONNEL!')
    console.log('Le mode sombre/clair devrait fonctionner correctement.')
} else {
    console.log('\n⚠️ PROBLÈMES DÉTECTÉS:')
    if (!hasThemeButton) console.log('- Bouton thème manquant')
    if (!hasThemeData) console.log('- Données thème manquantes')
    if (!hasCSSVars) console.log('- Variables CSS manquantes')
    if (!hasVueApp) console.log('- Application Vue non fonctionnelle')
    if (!hasWorkingToggle) console.log('- Basculement non fonctionnel')
}

console.log('\n🎯 === TEST RÉEL TERMINÉ ===') 