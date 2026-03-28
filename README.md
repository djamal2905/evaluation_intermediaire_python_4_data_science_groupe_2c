# Exploitation de données électorales avec Python

## Évaluation intermédiaire Python pour la Data Science (mi-semestre 2026)

**Auteur :** Simal OUSSEYNOU, Simon WILLOT, Djamal Y TOE
**Encadrant :** Julien PRAMIL
**Date :** Mars 2026

---

## 1. Objectif de l'évaluation

L’objectif de cette évaluation est d’explorer les données électorales fines avec Python et de réaliser des analyses et visualisations des résultats par candidat et par département.
Le travail inclut :
- Le traitement des données électorales brutes,
- Le calcul des scores nationaux et départementaux,
- L’analyse de la surreprésentation des candidats par rapport à la moyenne nationale,
- La création de cartes interactives et illustratives pour visualiser les résultats par département.

---

## 2. Contenu du dépôt

Le dépôt contient les fichiers suivants :
- `reponse.ipynb` : Notebook principal contenant toutes les réponses aux questions de l’évaluation, analyses et visualisations.
- `Modules/cartographie.py` : Module Python développé pour la cartographie des départements.
- `requirements.txt` : Fichier listant tous les packages Python nécessaires avec les versions recommandées.

---

## 3. Pré-requis

Avant d’exécuter le notebook, vous devez installer les packages requis.
Depuis le terminal, exécutez :

```bash
python -m pip install -r requirements.txt
```
## 4. Utilisation du notebook

1. Ouvrez le notebook `reponse.ipynb` avec **Jupyter Notebook** ou **Jupyter Lab**.
2. Exécutez toutes les cellules dans l’ordre (`Run All`) pour reproduire toutes les analyses et visualisations.
3. Les données électorales sont automatiquement téléchargées depuis [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/r/182268fc-2103-4bcb-a850-6cf90b02a9eb) grâce au code fourni dans le notebook.
4. Le module `Cartographie` est utilisé pour :
   - Télécharger et gérer les fonds de carte des départements français,
   - Générer des cartes colorées représentant les scores départementaux par candidat.

## 5. Contenu des analyses

Le notebook `reponse.ipynb` inclut :
- La création de nouvelles variables (`code_commune`, `candidat`) pour faciliter les analyses,
- Le calcul des **scores nationaux** de chaque candidat et la création de tableaux récapitulatifs,
- Le calcul des **scores départementaux** et de la surreprésentation relative par rapport au score national,
- La **visualisation des résultats** sur cartes par département, avec colorbar et flèche indiquant le Nord,
- Des exemples de cartes pour différents candidats : **Marine Le Pen, Emmanuel Macron, Eric Zemmour**.

## 6. Notes importantes

- Le code est **entièrement reproductible** : en exécutant toutes les cellules, vous obtenez les mêmes résultats.
- Les résultats peuvent être vérifiés avec les **sources officielles** de l’élection présidentielle 2022.
- Une attention particulière a été portée à la **lisibilité** et à la **clarté** des figures et des tableaux.