// Script pour forcer l'application des styles CSS du thème
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🔧 === CORRECTION DES STYLES THÈME ===')

// Fonction pour forcer l'application des variables CSS
function forceApplyThemeStyles() {
    console.log('🔄 Forçage de l\'application des styles...')
    
    const html = document.documentElement
    const isDark = html.classList.contains('dark-mode')
    
    if (isDark) {
        console.log('🎨 Application du mode sombre...')
        
        // Variables CSS pour le mode sombre
        html.style.setProperty('--bg-primary', '#1a1a1a')
        html.style.setProperty('--bg-secondary', '#2d2d2d')
        html.style.setProperty('--bg-tertiary', '#3d3d3d')
        html.style.setProperty('--text-primary', '#ffffff')
        html.style.setProperty('--text-secondary', '#b0b0b0')
        html.style.setProperty('--text-muted', '#888888')
        html.style.setProperty('--border-color', '#404040')
        html.style.setProperty('--shadow-color', 'rgba(0, 0, 0, 0.3)')
        html.style.setProperty('--accent-color', '#4CAF50')
        html.style.setProperty('--accent-hover', '#45a049')
        
        // Forcer les styles sur les éléments principaux
        document.body.style.backgroundColor = '#1a1a1a'
        document.body.style.color = '#ffffff'
        
        // Navigation bar
        const navBar = document.querySelector('.navigation-bar')
        if (navBar) {
            navBar.style.backgroundColor = '#2d2d2d'
            navBar.style.borderBottom = '1px solid #404040'
        }
        
        // Cards
        const cards = document.querySelectorAll('.card, .feature-card')
        cards.forEach(card => {
            card.style.backgroundColor = '#2d2d2d'
            card.style.border = '1px solid #404040'
            card.style.color = '#ffffff'
        })
        
        console.log('✅ Styles mode sombre appliqués')
        
    } else {
        console.log('☀️ Application du mode clair...')
        
        // Variables CSS pour le mode clair
        html.style.setProperty('--bg-primary', '#ffffff')
        html.style.setProperty('--bg-secondary', '#f8f9fa')
        html.style.setProperty('--bg-tertiary', '#e9ecef')
        html.style.setProperty('--text-primary', '#2c3e50')
        html.style.setProperty('--text-secondary', '#6c757d')
        html.style.setProperty('--text-muted', '#adb5bd')
        html.style.setProperty('--border-color', '#dee2e6')
        html.style.setProperty('--shadow-color', 'rgba(0, 0, 0, 0.1)')
        html.style.setProperty('--accent-color', '#4CAF50')
        html.style.setProperty('--accent-hover', '#45a049')
        
        // Forcer les styles sur les éléments principaux
        document.body.style.backgroundColor = '#ffffff'
        document.body.style.color = '#2c3e50'
        
        // Navigation bar
        const navBar = document.querySelector('.navigation-bar')
        if (navBar) {
            navBar.style.backgroundColor = '#f8f9fa'
            navBar.style.borderBottom = '1px solid #dee2e6'
        }
        
        // Cards
        const cards = document.querySelectorAll('.card, .feature-card')
        cards.forEach(card => {
            card.style.backgroundColor = '#f8f9fa'
            card.style.border = '1px solid #dee2e6'
            card.style.color = '#2c3e50'
        })
        
        console.log('✅ Styles mode clair appliqués')
    }
}

// Fonction pour basculer le thème avec styles forcés
function forceToggleTheme() {
    console.log('🔄 Basculement forcé du thème...')
    
    const html = document.documentElement
    const isDark = html.classList.contains('dark-mode')
    
    if (isDark) {
        // Passer en mode clair
        html.classList.remove('dark-mode')
        html.setAttribute('data-theme', 'light')
        localStorage.setItem('dark-mode', 'false')
        console.log('☀️ Passage en mode clair')
    } else {
        // Passer en mode sombre
        html.classList.add('dark-mode')
        html.setAttribute('data-theme', 'dark')
        localStorage.setItem('dark-mode', 'true')
        console.log('🎨 Passage en mode sombre')
    }
    
    // Appliquer les styles forcés
    forceApplyThemeStyles()
    
    // Vérifier après 500ms
    setTimeout(() => {
        const bodyStyle = getComputedStyle(document.body)
        console.log('Couleur de fond après basculement:', bodyStyle.backgroundColor)
        console.log('Couleur de texte après basculement:', bodyStyle.color)
        
        if (html.classList.contains('dark-mode')) {
            console.log('✅ Mode sombre activé avec styles')
        } else {
            console.log('✅ Mode clair activé avec styles')
        }
    }, 500)
}

// Fonction pour vérifier et corriger les styles
function checkAndFixStyles() {
    console.log('🔍 Vérification des styles...')
    
    const html = document.documentElement
    const bodyStyle = getComputedStyle(document.body)
    const isDark = html.classList.contains('dark-mode')
    
    console.log('Mode sombre détecté:', isDark)
    console.log('Couleur de fond actuelle:', bodyStyle.backgroundColor)
    console.log('Couleur de texte actuelle:', bodyStyle.color)
    
    // Vérifier si les couleurs correspondent au thème
    const expectedBgColor = isDark ? 'rgb(26, 26, 26)' : 'rgb(255, 255, 255)'
    const expectedTextColor = isDark ? 'rgb(255, 255, 255)' : 'rgb(44, 62, 80)'
    
    if (bodyStyle.backgroundColor !== expectedBgColor) {
        console.log('⚠️ Couleur de fond incorrecte, application des corrections...')
        forceApplyThemeStyles()
    } else {
        console.log('✅ Couleurs correctes')
    }
}

// Fonction pour recharger les styles CSS
function reloadCSS() {
    console.log('🔄 Rechargement des styles CSS...')
    
    // Supprimer et recréer les liens CSS
    const links = document.querySelectorAll('link[rel="stylesheet"]')
    links.forEach(link => {
        const href = link.href
        link.remove()
        const newLink = document.createElement('link')
        newLink.rel = 'stylesheet'
        newLink.href = href + '?v=' + Date.now()
        document.head.appendChild(newLink)
    })
    
    console.log('✅ Styles CSS rechargés')
    
    // Réappliquer les styles après rechargement
    setTimeout(() => {
        forceApplyThemeStyles()
    }, 1000)
}

// Exécuter la correction automatique
console.log('🚀 Lancement de la correction des styles...')
checkAndFixStyles()

// Fonctions disponibles globalement
window.forceApplyThemeStyles = forceApplyThemeStyles
window.forceToggleTheme = forceToggleTheme
window.checkAndFixStyles = checkAndFixStyles
window.reloadCSS = reloadCSS

console.log('\n📝 Fonctions disponibles:')
console.log('- forceApplyThemeStyles() : Forcer l\'application des styles')
console.log('- forceToggleTheme() : Basculement avec styles forcés')
console.log('- checkAndFixStyles() : Vérifier et corriger les styles')
console.log('- reloadCSS() : Recharger les styles CSS')

console.log('\n🎯 === CORRECTION TERMINÉE ===') 