// Test rapide après redémarrage de l'application
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🎨 === TEST APRÈS REDÉMARRAGE ===')

// Test 1: Vérification de base
console.log('📋 1. Vérification de base:')
console.log('URL:', window.location.href)
console.log('Titre:', document.title)

// Test 2: Vérification du bouton thème
console.log('\n📋 2. Vérification du bouton thème:')
const themeButton = document.querySelector('.nav-btn-theme')
if (themeButton) {
    console.log('✅ Bouton thème trouvé')
    console.log('Texte:', themeButton.textContent)
    console.log('Classes:', themeButton.className)
} else {
    console.log('❌ Bouton thème non trouvé')
}

// Test 3: Vérification des variables CSS
console.log('\n📋 3. Vérification des variables CSS:')
const html = document.documentElement
const computedStyle = getComputedStyle(html)

const cssVars = {
    bgPrimary: computedStyle.getPropertyValue('--bg-primary'),
    textPrimary: computedStyle.getPropertyValue('--text-primary'),
    borderColor: computedStyle.getPropertyValue('--border-color')
}

console.log('Variables CSS:', cssVars)

// Test 4: Test de basculement
console.log('\n📋 4. Test de basculement:')
if (themeButton) {
    const isDarkBefore = html.classList.contains('dark-mode')
    console.log('Mode sombre avant:', isDarkBefore)
    console.log('Classes HTML avant:', html.className)
    
    // Clic sur le bouton
    console.log('🔄 Clic sur le bouton...')
    themeButton.click()
    
    setTimeout(() => {
        const isDarkAfter = html.classList.contains('dark-mode')
        console.log('Mode sombre après:', isDarkAfter)
        console.log('Classes HTML après:', html.className)
        console.log('localStorage après:', localStorage.getItem('dark-mode'))
        
        if (isDarkBefore !== isDarkAfter) {
            console.log('✅ Basculement réussi!')
        } else {
            console.log('❌ Basculement échoué')
        }
        
        // Vérifier les couleurs
        const bodyStyle = getComputedStyle(document.body)
        console.log('Couleur de fond:', bodyStyle.backgroundColor)
        console.log('Couleur de texte:', bodyStyle.color)
    }, 500)
}

// Test 5: Résumé
console.log('\n📋 5. Résumé:')
const hasThemeButton = !!themeButton
const hasCSSVars = cssVars.bgPrimary && cssVars.bgPrimary.trim() !== ''
const hasDarkModeClass = html.classList.contains('dark-mode')

console.log('Bouton thème:', hasThemeButton ? '✅' : '❌')
console.log('Variables CSS:', hasCSSVars ? '✅' : '❌')
console.log('Classe dark-mode:', hasDarkModeClass ? '✅' : '❌')

if (hasThemeButton && hasCSSVars) {
    console.log('\n🎉 THÈME FONCTIONNEL APRÈS REDÉMARRAGE!')
} else {
    console.log('\n⚠️ PROBLÈMES DÉTECTÉS:')
    if (!hasThemeButton) console.log('- Bouton thème manquant')
    if (!hasCSSVars) console.log('- Variables CSS manquantes')
}

console.log('\n🎯 === TEST TERMINÉ ===') 