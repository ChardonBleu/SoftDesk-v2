# SoftDesk

![SoftDesk logo](https://user.oc-static.com/upload/2020/09/22/16007803099977_P8%20%281%29.png "SoftDesk logo")

Projet 10 de la formation DA python d'Openclassrooms.

API de gestion et de suivi de problèmes techniques. L'application doit permettre aux utilisateurs de créer des projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libéllés à ces problèmes  en focntion de leurs priorités, de balises, etc.
L'authentification des utilisateurs se fait par JWT.
Il es tinterdit à tout utilisateur autorisé autre que l'auteur de modifier ou supprimer un problème, projet ou commentaire.

Installation
---
Télécharger les dossiers et fichiers et les copier dans un dossier de votre choix.
Dans la console aller dans le dossier choisi.

Environnement virtuel
---
https://docs.python.org/fr/3/library/venv.html?highlight=venv

Créer un environnement virtuel: 

```bash
python -m venv env
```

Activer cet environnement virtuel:
sur windows dans Visual Studio Code: 
```bash 
. env/Scripts/activate 
```
sur mac ou linux: 
```bash 
source env/bin/activate 
```

Packages
---

Puis installer les modules necessaires:
```bash 
python -m pip install -r requirements.txt
```

Exécution
---
Se mettre dans le répertoire racine.
Faire les migrations pour l'initialisation de la base de donnée:

```bash 
python manage.py makemigrations
```
puis:

```bash 
python manage.py migrate
```
Puis lancer le serveur:

```bash 
python manage.py runserver
```
Le serveur de développement se lance et son adresse s'affiche dans la console:

Django version 3.2.5, using settings 'LITReview.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

Aller sur l'adresse http proposée pour consulter l'API dans .


Générer un rapport flake-8 html
---
Documentations flake8 et flake8 html:

    https://flake8.pycqa.org/en/latest/manpage.html

    https://pypi.org/project/flake8-html/

Se mettre dans le répertoire dont on veut scanner les fichiers *.py. Par exemple pour library:
```bash 
cd issuetracking
```

Puis dans la console excécuter:
```bash 
flake8 --format=html --htmldir=flake-report --exclude=migrations
```
Un nouveau rapport flake8 est généré. Aller dans le répertoire flake-report créé dans le répertoire library et ouvrir le fichier index.html dans un navigateur web.
Changer de répertoire pour tester d'autres fichiers *.py

Lancer les tests
---

Documentation pytest et coverage:

    https://docs.pytest.org/en/6.2.x/

    https://coverage.readthedocs.io/en/coverage-5.5/

Le fichier pytest.ini a été configuré pour exécuter coverage en même temps que pytest:
```bash 
addopts = --nomigrations --cov=. --cov-report=html
```

Depuis le répertoire racine lancer pytest
```bash 
pytest
```

Après excécution des tests aller consulter le résulat du coverage dans le dossier nouvellement créé htmlcov en ouvrant le fichier index.html dans un navigateur.


Ressources utilisées
---

Livres:

    Django 3 by exemples - Antonio Melé

Ressources web:

La documentation officielle de Django:

    https://docs.djangoproject.com/en/3.0/


La documentation officielle de DjangoRestFramework:

    https://getbootstrap.com/docs/4.3/getting-started/introduction/

Remerciements
---

Un très grand merci à ma mentor Sandrine Suire pour sa trés grande disponibilité, son accompagnement de qualité et sa patience à tout (ré)expliquer dans les moments de perdition.

Et merci à tous les membres du Discord DA python: 
http://discord.pythonclassmates.org/
