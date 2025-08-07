// Script de test pour diagnostiquer le problème visuel du thème
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🎨 === DIAGNOSTIC VISUEL THÈME ===')

// Test 1: Vérification des variables CSS
console.log('📋 1. Vérification des variables CSS:')
const html = document.documentElement
const computedStyle = getComputedStyle(html)

const cssVars = {
    bgPrimary: computedStyle.getPropertyValue('--bg-primary'),
    textPrimary: computedStyle.getPropertyValue('--text-primary'),
    borderColor: computedStyle.getPropertyValue('--border-color'),
    bgSecondary: computedStyle.getPropertyValue('--bg-secondary'),
    textSecondary: computedStyle.getPropertyValue('--text-secondary')
}

console.log('Variables CSS actuelles:', cssVars)

// Test 2: Vérification des styles appliqués
console.log('\n📋 2. Vérification des styles appliqués:')
const bodyStyle = getComputedStyle(document.body)
console.log('Couleur de fond body:', bodyStyle.backgroundColor)
console.log('Couleur de texte body:', bodyStyle.color)

const navBar = document.querySelector('.navigation-bar')
if (navBar) {
    const navStyle = getComputedStyle(navBar)
    console.log('Couleur de fond nav:', navStyle.backgroundColor)
    console.log('Couleur de texte nav:', navStyle.color)
} else {
    console.log('❌ Navigation bar non trouvée')
}

// Test 3: Test de basculement avec vérification visuelle
console.log('\n📋 3. Test de basculement avec vérification visuelle:')
const themeButton = document.querySelector('.nav-btn-theme')

if (themeButton) {
    console.log('✅ Bouton thème trouvé')
    
    // État avant
    const isDarkBefore = html.classList.contains('dark-mode')
    console.log('Mode sombre avant:', isDarkBefore)
    console.log('Classes HTML avant:', html.className)
    console.log('Couleur de fond avant:', bodyStyle.backgroundColor)
    
    // Clic sur le bouton
    console.log('\n🔄 Clic sur le bouton thème...')
    themeButton.click()
    
    // Vérification après 1 seconde
    setTimeout(() => {
        const isDarkAfter = html.classList.contains('dark-mode')
        const bodyStyleAfter = getComputedStyle(document.body)
        
        console.log('Mode sombre après:', isDarkAfter)
        console.log('Classes HTML après:', html.className)
        console.log('Couleur de fond après:', bodyStyleAfter.backgroundColor)
        console.log('localStorage après:', localStorage.getItem('dark-mode'))
        
        if (isDarkBefore !== isDarkAfter) {
            console.log('✅ Basculement détecté!')
        } else {
            console.log('❌ Aucun basculement détecté')
        }
        
        // Vérifier si les couleurs ont changé
        if (bodyStyle.backgroundColor !== bodyStyleAfter.backgroundColor) {
            console.log('✅ Couleur de fond a changé!')
        } else {
            console.log('❌ Couleur de fond n\'a pas changé')
        }
    }, 1000)
    
} else {
    console.log('❌ Bouton thème non trouvé')
}

// Test 4: Forçage des variables CSS
console.log('\n📋 4. Test de forçage des variables CSS:')
function forceDarkMode() {
    console.log('🔄 Application forcée du mode sombre...')
    
    html.classList.add('dark-mode')
    html.setAttribute('data-theme', 'dark')
    localStorage.setItem('dark-mode', 'true')
    
    // Forcer les variables CSS
    html.style.setProperty('--bg-primary', '#1a1a1a')
    html.style.setProperty('--bg-secondary', '#2d2d2d')
    html.style.setProperty('--text-primary', '#ffffff')
    html.style.setProperty('--text-secondary', '#b0b0b0')
    html.style.setProperty('--border-color', '#404040')
    
    console.log('✅ Variables CSS mode sombre appliquées')
    
    setTimeout(() => {
        const newBodyStyle = getComputedStyle(document.body)
        console.log('Nouvelle couleur de fond:', newBodyStyle.backgroundColor)
        console.log('Nouvelle couleur de texte:', newBodyStyle.color)
    }, 500)
}

function forceLightMode() {
    console.log('🔄 Application forcée du mode clair...')
    
    html.classList.remove('dark-mode')
    html.setAttribute('data-theme', 'light')
    localStorage.setItem('dark-mode', 'false')
    
    // Forcer les variables CSS
    html.style.setProperty('--bg-primary', '#ffffff')
    html.style.setProperty('--bg-secondary', '#f8f9fa')
    html.style.setProperty('--text-primary', '#2c3e50')
    html.style.setProperty('--text-secondary', '#6c757d')
    html.style.setProperty('--border-color', '#dee2e6')
    
    console.log('✅ Variables CSS mode clair appliquées')
    
    setTimeout(() => {
        const newBodyStyle = getComputedStyle(document.body)
        console.log('Nouvelle couleur de fond:', newBodyStyle.backgroundColor)
        console.log('Nouvelle couleur de texte:', newBodyStyle.color)
    }, 500)
}

// Test 5: Vérification des styles CSS chargés
console.log('\n📋 5. Vérification des styles CSS:')
const styleSheets = document.styleSheets
console.log('Nombre de feuilles de style:', styleSheets.length)

for (let i = 0; i < styleSheets.length; i++) {
    try {
        const rules = styleSheets[i].cssRules || styleSheets[i].rules
        let darkModeRules = 0
        let cssVarsRules = 0
        
        for (let j = 0; j < rules.length; j++) {
            const rule = rules[j]
            if (rule.selectorText && rule.selectorText.includes('dark-mode')) {
                darkModeRules++
            }
            if (rule.selectorText && rule.selectorText.includes('--bg-primary')) {
                cssVarsRules++
            }
        }
        
        if (darkModeRules > 0 || cssVarsRules > 0) {
            console.log(`Feuille de style ${i}: ${darkModeRules} règles dark-mode, ${cssVarsRules} variables CSS`)
        }
    } catch (e) {
        // CORS peut bloquer l'accès
    }
}

// Test 6: Résumé et solutions
console.log('\n📋 6. Résumé et solutions:')
const hasDarkModeClass = html.classList.contains('dark-mode')
const hasCSSVars = cssVars.bgPrimary && cssVars.bgPrimary.trim() !== ''
const hasWorkingStyles = bodyStyle.backgroundColor !== 'rgba(0, 0, 0, 0)'

console.log('Classe dark-mode présente:', hasDarkModeClass ? '✅' : '❌')
console.log('Variables CSS définies:', hasCSSVars ? '✅' : '❌')
console.log('Styles appliqués:', hasWorkingStyles ? '✅' : '❌')

if (!hasCSSVars) {
    console.log('\n⚠️ PROBLÈME: Variables CSS manquantes')
    console.log('🔧 SOLUTION: Utiliser forceDarkMode() ou forceLightMode()')
} else if (!hasWorkingStyles) {
    console.log('\n⚠️ PROBLÈME: Styles non appliqués')
    console.log('🔧 SOLUTION: Vérifier que style.css est chargé')
} else {
    console.log('\n✅ Tout semble fonctionnel')
}

// Fonctions disponibles
window.forceDarkMode = forceDarkMode
window.forceLightMode = forceLightMode

console.log('\n📝 Fonctions disponibles:')
console.log('- forceDarkMode() : Forcer le mode sombre')
console.log('- forceLightMode() : Forcer le mode clair')

console.log('\n🎯 === DIAGNOSTIC VISUEL TERMINÉ ===') 