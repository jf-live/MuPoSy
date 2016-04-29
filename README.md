MuPoSy
======

Prototype d'installation sonore par: / Sound Intallation Prototype by:

Jean-François Primeau
---------------------

2016


Comment ça marche:
------------------

Avant de lancer le programme: 
Il faut choisir les paramètres appropriés dans
constants.py .  Le PLAYMODE est soit en Demo, soit en Manual.  _Demo_ change les
mélodies entendues toutes les 40 secondes, en change la valeur du MIDI CC entre
0 et 127 en continu, prenant environ 3 minutes pour faire un cycle complet.
_Manual_ change les mélodies et joue un poème seulement lorsque la valeur 
MIDI CC dépasse 110.  Lorsqu'un poème est joué, il ne peut y en avoir un autre
avant 50 secondes du début du précédent.
Il faut également spécifier le nombre d'instances de générateurs de synthèse, 
NUMGENS (entre 0 et 4, selon le cpu disponible), et le nombre d'instances de 
générateurs d'échantillons, NUMSAMPS (entre 0 et 5, nombre un peu arbitraire de 
ma part).

Un fader ou potentiomètre assigné au MIDI CC 0 sert à simuler une situation 
d'installation sonore légèrement interactive.
Lorsque la valeur CC envoyée est de 0, c'est comme si il n'y a personne dans
l'espace.  Plus la valeur augmente, simulant qu'une personne approche, plus le
son passe au second plan.

Le timbre des générateurs évolue progressivement sur une longue période, en plus
de l'évolution rapide facilement repérable.

N'ayant pas trouvé de librairie Python pour effectuer de la blob detection avec 
un kinect, ce projet est mis de côté pour le moment.

_Pour une bonne simulation, il faut glisser le fader
très lentement (comme si c'est une grande salle qu'il faut traverser...)._

Les appels sont faits comme suit:  
  
MuPoSy.py -> Engine.py -> Algo.py -> SynthGen.py -> Effects.py  
       |                                              |------> SamplePlay.py  
       |  
       |-->Voix.py  
       |-->Interactivity.py  
       |-->utilities.py  
       |-->variables.py  
       |-->constantes.py  
  
Ce diagramme simplifié ne représente pas les appels inter-modules.


Problèmes non résolus:
--------------------

Il arrive que le son coupe de façon imprévisible alors que tout semble 
continuer normalement si l'on en croit les messages qui continuent de défiler.  
Il semblerait qu'une "explosion" du niveau sonore est à la source du problème.  
De multiples tests ne m'ont pas encore permis d'en isoler la cause exacte, mais 
le problème vient des générateurs de synthèse.  Des objets Clip sont utilisés 
afin d'éviter un son très fort soudain qui est le responsable de la situation.  
Le niveau saute brusquement à infini...  Un problème similaire avait été trouvé 
lorsqu'un échantillon n'avait pas eu le temps de charger complètement dans une 
table et que cette table était appelée pour être lue. Outre le son qui coupe, il
ne semble pas y avoir d'autre conséquence à ce problème au niveau du programme, 
qui n'affiche pas de messages d'erreur.
De plus, certains générateurs de synthèse semblent produire des clicks à cause
des modulations qui leur sont appliqués.  Là aussi, des recherches en 
profondeur devront être faites afin d'en trouver la cause.  Se pourrait-il que
ces deux problèmes soient reliés?



Observations personnelles:
--------------------------

Je crois que ce projet est un bon exemple d'une situation où la musique est au 
service de la technologie, et non la technologie au service de la musique.  Dès 
le départ, mon intention était d'approfondir mes connaissances du langage Python
ainsi que de la librairie pyo.  Le projet MuPoSy élaboré n'était somme toute
qu'un prétexte à l'exploration de divers procédés.  Par exemple, beaucoup de
temps a été investi dans la recherche timbrale, et peu dans l'élaboration d'une
trame musicale réellement intéressante.  Ce projet m'aura aussi permis de me
construire un début de banque d'objets qui pourront être réutilisés 
ultérieurement, comme tout ce qui concerne le Text-To-Speech, les générateurs 
de synthétiseurs, les effets, certains utilitaires...  
De grandes parties devraient toutefois être complètement réécrites pour rendre 
le projet musicalement acceptable, et afin de régler le problème du son qui 
coupe.
Finalement, l'idée initiale du projet était assez floue et voulait répondre à
trop de problématiques à la fois: génération de synthèse sonore évolutive, 
lecture d'échantillons évolutive, interactivité, musique algorithmique, 
exploration de contenu littéraire et génération de TTS en temps réel, et j'en
passe...  Cet éparpillement aura soulevé un grand nombre de difficultés 
simultanément, ce qui a résulté en beaucoup de débogage couteux en temps.  
Le prochain projet devrait être beaucoup plus spécifique et moins généraliste.



  


