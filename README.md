# Index

Un index minimal réalisé par Thibaut WOJDACKI

## Comment faire fonctionner le crawler ?

Première étape : Aller dans le bon dossier `cd index`

Deuxième étape  : Installer les packages nécessaires - `pip install -r requirements.txt`

Troisième étape : Lancer l'application  `python main.py`

## Paramètres à modifier

Avant la troisième étape, il peut être nécessaire de décommenter les lignes installant les packages ntlk dans le fichier main.py.
L'outil a besoin d'un fichier crawled_urls.json qui contient des pages web précédemment crawlées.

## Fonctionnalités de l'index

L'outil sort des statistiques sur les pages web tels que :
- le nombre de documents
- le nombre global de tokens
- le nombre global de tokens par champ
- le nombre moyen de tokens
- le nombre moyen de tokens dans le champ titre
- le nombre moyen de tokens dans le champ contenu.

Ces statistiques sont accesibles dans le fichier metadata.json.

L'outil crée un index positionnel et un index non-positionnel pour le titre et le contenu des pages web.

L'outil crée également un index positionnel en utilisant un stemmer, le stemmer utilisé est SnowballStemmer du package nltk.

L'outil répond au demande du TP2 et implémente tous les aspects demandés dans la partie "En bonus".