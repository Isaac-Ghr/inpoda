# Projet InPoDa

## Description

C'est une application effectuant des opérations de traitement et d'analyse des données sur des tweets.

## Installation

### Cloner le projet (optionnel)

Compte tenu du fait que les fichiers sources sont déjà inclus, il n'est pas nécessaire de cloner le dépôt, cependant si cela est nécessaire alors voici la procédure à suivre quelque soit l'environnement :

```zsh
git clone https://github.com/Isaac-Ghr/inpoda.git
cd inpoda
```

### Créer un environnement virtuel (recommandé)

Avant d'installer les modules, il est nécessaire de créer un environnement virtuel spécial pour python. Il est d'ailleurs intéresssant de noter que la version de python utilisée pour ce projet est la v3.13.

Pour créer un environnement virtuel il suffit d'entrer la commande suivante dans l'environnement de votre choix :

**MacOS :**

```zsh
# zsh
python3 -m venv nom-de-lenvironnement
```

```zsh
# zsh
source './nom-de-lenvironnement/bin/activate'
```

**Windows :**

```cmd
# cmd
python -m venv nom-de-lenvironnement
```

```cmd
# cmd
.\nom-de-lenvironnement\bin\activate
```

### Installation des modules

L'application repose sur plusieurs modules pour effectuer certaines opérations. Voici la liste des modules à installer ainsi que les commandes à executer en terminal :

**Liste des modules :**

- json;
- re (regex);
- numpy;
- pandas;
- textblob;
- matplotlib

Ces modules sont listés avec leurs dépendances dans le fichier requirements.txt afin de simplifier l'installation de ces derniers.

**MacOS :**

```zsh
# zsh
python3 -m pip install -r requirements.txt
```

**Windows :**

```cmd
# cmd
pip install -r requirements.txt
```

## Lancement de l'application

Pour lancer l'application, il faut executer le script main.py.

```zsh
# zsh
python3 src/main.py
```
