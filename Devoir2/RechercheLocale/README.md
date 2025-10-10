# Explication : Représentation des Conflits dans le Problème d'Horaires

## 📋 Vue d'ensemble

Ce document explique comment les conflits sont générés et représentés dans le système de planification d'horaires académiques utilisant la recherche locale.

---

## 🎯 Le Problème

### Contexte
Il s'agit d'un **problème de coloration de graphe** appliqué à la planification d'horaires universitaires.

### Objectif
**Minimiser le nombre de créneaux horaires** nécessaires pour planifier tous les cours, tout en respectant les contraintes de conflit.

### Contraintes
Certains cours **ne peuvent pas** être planifiés au même créneau horaire (par exemple, s'ils partagent des étudiants ou des professeurs communs).

---

## 📁 Structure des Fichiers d'Instance

### Format du fichier d'entrée
Exemple : `horaire_A_11_20.txt`

```
11                      ← Nombre total de cours
20                      ← Nombre total de conflits (paires de cours incompatibles)
INF6118 INF5553        ← Ces deux cours sont en conflit
INF6118 LOG7845        ← Ces deux cours sont en conflit
INF6118 MTH6870        ← Ces deux cours sont en conflit
...
```

### Interprétation
- **Ligne 1** : Nombre de cours à planifier
- **Ligne 2** : Nombre de contraintes de conflit
- **Lignes suivantes** : Paires de cours qui **ne peuvent PAS** partager le même créneau

---

## 🔗 Le Graphe de Conflits

### Représentation
Le système utilise un **graphe non orienté** (NetworkX) pour modéliser les conflits :

```python
self.conflict_graph = nx.Graph()
```

### Structure
- **Nœuds** = Cours (ex: INF6118, MTH5421, LOG7845)
- **Arêtes** = Contraintes de conflit entre deux cours

### Exemple
Si le fichier contient `INF6118 INF5553`, cela crée une arête entre ces deux nœuds, signifiant :
> ⚠️ INF6118 et INF5553 ne peuvent PAS être au même créneau

---

## 🎨 La Visualisation (`display_solution`)

### Éléments de la Visualisation

| Élément | Signification |
|---------|---------------|
| **Boîtes colorées** | Cours individuels |
| **Couleurs** | Créneaux horaires assignés |
| **Lignes noires** | Contraintes de conflit entre cours |

### Code de la fonction (simplifié)

```python
def display_solution(self, solution=[], filename="out.png"):
    colors = dict()
    
    # Assigne une couleur aléatoire à chaque créneau horaire
    for i in solution:
        if solution[i] not in colors:
            colors[solution[i]] = (random_color)
        
        # Dessine le cours avec la couleur de son créneau
        plt.text(pos[i][0], pos[i][1], i, 
                 bbox=dict(facecolor=colors[solution[i]]))
    
    # Dessine les arêtes de conflit
    nx.draw_networkx_edges(self.conflict_graph, pos)
```

---

## ✅ Solution Valide vs ❌ Solution Invalide

### Règle Fondamentale
> Deux cours reliés par une ligne noire **doivent avoir des couleurs différentes**

### Exemples Visuels

#### ✅ **Solution VALIDE**
```
[Cours A] ━━━━━━━ [Cours B]
  vert                rouge
```
- Les cours A et B sont en conflit (ligne noire)
- Ils ont des couleurs **différentes** → Pas de problème ✓

#### ❌ **Solution INVALIDE**
```
[Cours A] ━━━━━━━ [Cours B]
  vert                vert
```
- Les cours A et B sont en conflit (ligne noire)
- Ils ont la **même couleur** → CONFLIT ! ✗

---

## 🔍 Comment Interpréter Votre Visualisation

### Dans votre image `visualization.png`

1. **Comptez les couleurs différentes** 
   - Chaque couleur = un créneau horaire utilisé
   - Moins de couleurs = meilleure solution

2. **Vérifiez les arêtes**
   - Suivez chaque ligne noire
   - Les deux cours aux extrémités doivent avoir des couleurs différentes

3. **Exemple concret**
   - Si `INF6118` (vert) et `INF5553` (vert) sont reliés par une ligne → ❌ CONFLIT
   - Si `INF6118` (vert) et `INF5553` (violet) sont reliés par une ligne → ✅ OK

---

## 🔧 Vérification Programmatique

### Fonction de vérification

```python
def verify_solution(self, solution):
    """Vérifie si une solution est valide"""
    # Compte le nombre de conflits
    conflicts = sum(solution[a[0]] == solution[a[1]] 
                   for a in self.conflict_list)
    
    # Une solution valide a 0 conflit
    assert conflicts == 0, "Solution invalide"
    return True
```

### Explication
- Parcourt toutes les paires en conflit
- Compte combien de paires ont le **même créneau**
- Si ce nombre est > 0 → Solution invalide

---

## 🎓 Stratégies de Résolution

### Approche Naïve
```python
# Assigne un créneau différent à chaque cours
solution = {cours1: 0, cours2: 1, cours3: 2, ...}
```
- ✅ Toujours valide
- ❌ Utilise beaucoup trop de créneaux

### Approche Optimisée (Recherche Locale)
```python
# Essaie de réutiliser les créneaux
solution = [(cours1, 0), (cours2, 0), (cours3, 1), ...]
```
- 🎯 Minimise le nombre de créneaux
- ✅ Doit respecter les contraintes de conflit

---

## 💡 Points Clés à Retenir

1. **Les lignes noires sont des CONTRAINTES**, pas des conflits existants
   - Elles indiquent ce qu'il **ne faut pas faire**

2. **Un conflit n'apparaît que si on viole une contrainte**
   - Deux cours reliés avec la même couleur = violation

3. **L'objectif est de minimiser les couleurs (créneaux)**
   - Pas d'assigner un créneau unique à chaque cours

4. **La visualisation permet de vérifier visuellement**
   - Suivez chaque ligne noire
   - Vérifiez que les couleurs aux extrémités diffèrent

---

## 🔗 Fichiers Concernés

| Fichier | Rôle |
|---------|------|
| `schedule.py` | Contient la classe `Schedule` et la fonction `display_solution` |
| `instances/*.txt` | Fichiers de données avec les conflits |
| `visualization.png` | Image générée montrant la solution |
| `solver_naive.py` | Solution simple (un créneau par cours) |
| `solver_advanced.py` | Solution optimisée (recherche locale) |

---

## 📝 Commandes Utiles

```bash
# Exécuter avec l'agent naïf
python3 main.py --agent=naive --infile=instances/horaire_A_11_20.txt

# Exécuter avec l'agent avancé
python3 main.py --agent=advanced --infile=instances/horaire_A_11_20.txt

# Spécifier les fichiers de sortie
python3 main.py --agent=advanced \
                --infile=instances/horaire_A_11_20.txt \
                --outfile=solution.txt \
                --visufile=visualization.png
```

---

**Date de création** : 10 octobre 2025  
**Cours** : INF8175 - Intelligence Artificielle  
**Devoir** : Devoir 2 - Recherche Locale

