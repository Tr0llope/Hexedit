# Hexedit
Ce programme est un éditeur hexadécimal de fichiers. Il permet de modifier toute sorte de fichiers grâce à un interface graphique réalisé avec la librairie PySide6.

lib: PySide6, requests, pillow

## Utilisation:
Lors de l'exécution, la fenêtre suivante s'ouvre:  
![menu](doc/menu.png)  
On y retrouve deux boutons:  
- Edit, qui permet d'éditer un fichier local
- VIsualize, qui permet de visualiser un fichier distant

### Mode Edition
Dans un premier temps, il faut sélectionner le fichier à éditer via le navigateur de fichier qui se présente de la manière suivante:  
![browser](doc/browser.png)  

Une fois le fichier sélectionné, la fenêtre d'édition s'ouvre:
![editor](doc/editor.png)  
On y retrouve les informations du fichier, ainsi que son contenu en hexadécimal.
Une fois les modifications effectuées, il faut cliquer sur le bouton `Save` pour enregistrer les modifications.  
Si le fichier est modifié, un message de confirmation s'affiche en bas de la fenêtre d'édition. 

### Mode Visualisation
![url](doc/url.png)