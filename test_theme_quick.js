// Script de test rapide pour le mode sombre/clair
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🎨 === TEST RAPIDE MODE SOMBRE/CLAIR ===')

// 1. Vérification de base
console.log('📋 1. Vérification de base:')
console.log('- URL:', window.location.href)
console.log('- Titre:', document.title)

// 2. Vérification du bouton thème
console.log('\n📋 2. Recherche du bouton thème:')
const themeButton = document.querySelector('.nav-btn-theme')
if (themeButton) {
    console.log('✅ Bouton thème trouvé')
    console.log('- Texte:', themeButton.textContent)
    console.log('- Classes:', themeButton.className)
} else {
    console.log('❌ Bouton thème non trouvé')
    
    // Chercher tous les boutons avec des icônes de thème
    const allButtons = document.querySelectorAll('button')
    let foundThemeButton = false
    allButtons.forEach(btn => {
        if (btn.textContent.includes('🌙') || btn.textContent.includes('☀️')) {
            console.log('✅ Bouton avec icône thème trouvé:', btn)
            foundThemeButton = true
        }
    })
    
    if (!foundThemeButton) {
        console.log('❌ Aucun bouton avec icône thème trouvé')
    }
}

// 3. Vérification de l'état du thème
console.log('\n📋 3. État actuel du thème:')
const html = document.documentElement
console.log('- Classes HTML:', html.className)
console.log('- data-theme:', html.getAttribute('data-theme'))
console.log('- localStorage dark-mode:', localStorage.getItem('dark-mode'))
console.log('- localStorage theme-preference:', localStorage.getItem('theme-preference'))

// 4. Test de basculement manuel
console.log('\n📋 4. Test de basculement manuel:')
const isDarkBefore = html.classList.contains('dark-mode')
console.log('- Mode sombre avant:', isDarkBefore)

// Appliquer le thème opposé
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
    console.log('- Mode sombre après:', isDarkAfter)
    console.log('- Classes HTML après:', html.className)
    console.log('- localStorage après:', localStorage.getItem('dark-mode'))
    
    if (isDarkBefore !== isDarkAfter) {
        console.log('✅ Basculement réussi!')
    } else {
        console.log('❌ Basculement échoué')
    }
}, 100)

// 5. Vérification des variables CSS
console.log('\n📋 5. Variables CSS:')
const computedStyle = getComputedStyle(html)
const cssVars = {
    bgPrimary: computedStyle.getPropertyValue('--bg-primary'),
    textPrimary: computedStyle.getPropertyValue('--text-primary'),
    borderColor: computedStyle.getPropertyValue('--border-color')
}

console.log('Variables CSS:', cssVars)

// 6. Test visuel
console.log('\n📋 6. Test visuel:')
console.log('- Couleur de fond:', getComputedStyle(document.body).backgroundColor)
console.log('- Couleur de texte:', getComputedStyle(document.body).color)

// 7. Résumé
console.log('\n📋 7. Résumé:')
const hasThemeButton = !!themeButton
const hasThemeData = html.getAttribute('data-theme') || localStorage.getItem('dark-mode')
const hasCSSVars = cssVars.bgPrimary || cssVars.textPrimary

console.log('- Bouton thème présent:', hasThemeButton ? '✅' : '❌')
console.log('- Données thème présentes:', hasThemeData ? '✅' : '❌')
console.log('- Variables CSS définies:', hasCSSVars ? '✅' : '❌')

if (hasThemeButton && hasThemeData && hasCSSVars) {
    console.log('\n🎉 THÈME FONCTIONNEL!')
} else {
    console.log('\n⚠️ PROBLÈMES DÉTECTÉS:')
    if (!hasThemeButton) console.log('- Bouton thème manquant')
    if (!hasThemeData) console.log('- Données thème manquantes')
    if (!hasCSSVars) console.log('- Variables CSS manquantes')
}

console.log('\n🎯 === TEST TERMINÉ ===') 