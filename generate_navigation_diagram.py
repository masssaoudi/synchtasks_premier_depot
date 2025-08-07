#!/usr/bin/env python3
"""
Script pour générer un diagramme de navigation SyncTasks
Adapté pour l'application locale (non-Docker)
"""

import os
import sys

try:
    import graphviz
except ImportError:
    print("❌ Graphviz non installé. Installation...")
    os.system("pip install graphviz")
    import graphviz

def create_navigation_diagram():
    """Crée le diagramme de navigation SyncTasks"""
    
    # Créer le graphe
    dot = graphviz.Digraph(
        comment='Navigation Utilisateur Lambda - SyncTasks (Local)',
        format='png',
        engine='dot'
    )
    
    # Configuration du graphe
    dot.attr(rankdir='TB', size='12,16')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='12')
    
    # Définir les couleurs pour différents types de pages
    colors = {
        'entry': '#E3F2FD',      # Bleu clair pour pages d'entrée
        'auth': '#FFF3E0',       # Orange clair pour authentification
        'main': '#E8F5E8',       # Vert clair pour pages principales
        'specialized': '#F3E5F5', # Violet clair pour pages spécialisées
        'pa': '#FFEBEE'          # Rouge clair pour PA
    }
    
    # Pages principales avec couleurs
    pages = [
        # Pages d'entrée
        ('Home', '🏠 Accueil\n(/landing)', colors['entry']),
        ('Login', '🔐 Connexion\n(/login)', colors['auth']),
        ('Segment', '🧭 Sélection Segment\n(/segment-selection)', colors['auth']),
        
        # Pages principales (utilisateur connecté)
        ('Welcome', '👋 Bienvenue\n(/welcome)', colors['main']),
        ('Dashboard', '📊 Dashboard\n(/dashboard)', colors['main']),
        ('Tasks', '📋 Tâches\n(/tasks)', colors['main']),
        ('SegmentDash', '📁 Segment Dashboard\n(/segment-dashboard)', colors['specialized']),
        ('ParticuliersDash', '👨‍👩‍👧‍👦 Particuliers Dashboard\n(/dashboard/particuliers)', colors['specialized']),
        
        # Pages Personne Aidant
        ('PA', '🧑‍⚕️ Personne Aidant\n(/personne-aidant)', colors['pa']),
        ('PAInscription', '📝 PA Inscription\n(/pa-inscription)', colors['pa']),
        ('PADash', '🤝 PA Dashboard\n(/pa-dashboard)', colors['pa'])
    ]
    
    # Ajouter les nœuds
    for node_id, label, color in pages:
        dot.node(node_id, label, fillcolor=color, fontcolor='#2C3E50')
    
    # Navigation Utilisateur standard
    standard_flow = [
        ('Home', 'Login', 'Connexion'),
        ('Home', 'Segment', 'S\'inscrire'),
        ('Login', 'Segment', 'Connexion OK'),
        ('Segment', 'Welcome', 'Redirection après choix'),
        ('Welcome', 'Dashboard', ''),
        ('Dashboard', 'Tasks', ''),
        ('Tasks', 'SegmentDash', 'Modules IA'),
        ('SegmentDash', 'ParticuliersDash', 'Profil particulier')
    ]
    
    # Navigation Personne Aidant
    pa_flow = [
        ('PA', 'PAInscription', 'Inscription'),
        ('PAInscription', 'PADash', 'Accès autorisé')
    ]
    
    # Ajouter les arêtes avec styles
    for start, end, label in standard_flow + pa_flow:
        dot.edge(start, end, label=label, fontsize='10', fontcolor='#34495E')
    
    # Ajouter des sous-graphes pour organiser visuellement
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='Parcours Utilisateur Standard', style='filled', color='lightgrey')
        c.attr('node', style='filled')
        c.node('Home')
        c.node('Login')
        c.node('Segment')
        c.node('Welcome')
        c.node('Dashboard')
        c.node('Tasks')
        c.node('SegmentDash')
        c.node('ParticuliersDash')
    
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='Parcours Personne Aidant', style='filled', color='lightgrey')
        c.attr('node', style='filled')
        c.node('PA')
        c.node('PAInscription')
        c.node('PADash')
    
    return dot

def create_route_protection_diagram():
    """Crée un diagramme des protections de routes"""
    
    dot = graphviz.Digraph(
        comment='Protection des Routes - SyncTasks',
        format='png',
        engine='dot'
    )
    
    dot.attr(rankdir='LR', size='12,8')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
    
    # Routes publiques
    public_routes = [
        ('landing', '🏠 Landing\n(/landing)', '#E8F5E8'),
        ('login', '🔐 Login\n(/login)', '#E8F5E8'),
        ('segment', '🧭 Segment Selection\n(/segment-selection)', '#E8F5E8'),
        ('pa', '🧑‍⚕️ PA\n(/personne-aidant)', '#E8F5E8'),
        ('pa_inscription', '📝 PA Inscription\n(/pa-inscription)', '#E8F5E8')
    ]
    
    # Routes protégées
    protected_routes = [
        ('welcome', '👋 Welcome\n(/welcome)', '#FFEBEE'),
        ('dashboard', '📊 Dashboard\n(/dashboard)', '#FFEBEE'),
        ('tasks', '📋 Tasks\n(/tasks)', '#FFEBEE'),
        ('segment_dash', '📁 Segment Dashboard\n(/segment-dashboard)', '#FFEBEE'),
        ('particuliers_dash', '👨‍👩‍👧‍👦 Particuliers\n(/dashboard/particuliers)', '#FFEBEE'),
        ('pa_dash', '🤝 PA Dashboard\n(/pa-dashboard)', '#FFEBEE')
    ]
    
    # Ajouter les nœuds
    for node_id, label, color in public_routes:
        dot.node(node_id, label, fillcolor=color, fontcolor='#2C3E50')
    
    for node_id, label, color in protected_routes:
        dot.node(node_id, label, fillcolor=color, fontcolor='#2C3E50')
    
    # Ajouter des sous-graphes
    with dot.subgraph(name='cluster_public') as c:
        c.attr(label='Routes Publiques', style='filled', color='lightgreen')
        c.attr('node', style='filled')
        for node_id, _, _ in public_routes:
            c.node(node_id)
    
    with dot.subgraph(name='cluster_protected') as c:
        c.attr(label='Routes Protégées (Auth Requise)', style='filled', color='lightcoral')
        c.attr('node', style='filled')
        for node_id, _, _ in protected_routes:
            c.node(node_id)
    
    return dot

def main():
    """Fonction principale"""
    print("🚀 Génération des diagrammes de navigation SyncTasks...")
    
    # Créer le diagramme principal
    print("📊 Création du diagramme de navigation principal...")
    nav_diagram = create_navigation_diagram()
    
    # Sauvegarder le diagramme principal
    output_file = 'navigation_synchtasks_local'
    nav_diagram.render(output_file, cleanup=True)
    print(f"✅ Diagramme principal sauvegardé : {output_file}.png")
    
    # Créer le diagramme de protection des routes
    print("🛡️ Création du diagramme de protection des routes...")
    protection_diagram = create_route_protection_diagram()
    
    # Sauvegarder le diagramme de protection
    protection_output = 'route_protection_synchtasks'
    protection_diagram.render(protection_output, cleanup=True)
    print(f"✅ Diagramme de protection sauvegardé : {protection_output}.png")
    
    print("\n🎯 Résumé des fichiers générés :")
    print(f"   📊 {output_file}.png - Diagramme de navigation principal")
    print(f"   🛡️ {protection_output}.png - Protection des routes")
    print("\n📁 Les diagrammes sont prêts pour votre application locale !")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        sys.exit(1) 