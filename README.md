# README #

## CitizenSocialLab: urGENTestimar ##

Experiment designed and implemented to be performed in **FiraTarrega 2017** during the performance [urGENTestimar](https://www.firatarrega.cat/fira/programa/en_2017/33/urgentestimar).

This participatory experiment consist on a set of dilemmas and behavioural games: **Prisoner's Dilemma, Snowdrift Game and Dictator's Game** designed to shed light on the concerns of citizens and collectives of Tàrrega. There are two Prisoner's Dilemma with sharing different basic resources (Bread and Water) and interactions, one Snowdrift (doing the action of Kissing) and one Dictator's Game (sharing Fruit with others).

More detailed information about the games will be available once the [scientific paper](http://), currently in preparation, will be published.

## Configuration ##
Steps are necessary to get urGENTestimar install, up and running in local network.

### Creation of the project ###

__Database MySQL__  
Create MySQL database: name\_db  
Create user database: user\_db  
Create password database: pass\_db

Introduce this information about the database in: `/urGENTestimar/settings.py`

__Environment__   
```mkvirtualenv urgentestimar ```  

__Requirements__  
```pip install -r requirements.txt```

__MongoDB__  
```mongod --dbpath /.../urGENTestimar/ddbb```

__Load text__   
File with text and translations:  `/.../urGENTestimar/game/i18n/translations.xlsx`  
   
```python excel_to_mongodb.py```

__Run Server__  
```python manage.py runserver localhost:port```

__Migrations__  
```python manage.py makemigrations```  
```python manage.py migrate```  

### Run project in Local ###

__Step 1: Run MySQL server__  
Run MySQL: `mysql.server start`

__Step 2: Open terminal tabs and work on the environment (in each terminal tab)__  

in Tab 1: MongoDB  
in Tab 2: MySQL  
in Tab 3: Run Application  

Work on environment: `workon urgentestimar`

__Step 3: Run MongoDB (Tab 1)__  
Run mongodb: `mongod --dbpath /.../urGENTestimar/ddbb`

__Step 4: MySQL actions (Tab 2)__  
Directory: `cd /.../urGENTestimar/`   
Database: `mysql -u user_db -p (pass_db)`

Drop database: `drop database urgentestimar;`  
Create database: `create database urgentestimar;`  
Exit: `exit;`

Modificate fields of database: `python manage.py makemigrations`  
Refresh database:
`python manage.py migrate` 

__Step 5: Load texts (Tab 2)__    
Load translations: `python excel_to_mongodb.py`

__Step 6: Run Server (Tab 3)__  
Directory: `cd /.../urGENTestimar/ `   
Runserver: `python manage.py runserver localhost:port`

## Versions ##
Version 1.0

## License ##
[CC BY-NC-SA license](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Contact ##

Julian Vicens: **julianvicens@gmail.com**
