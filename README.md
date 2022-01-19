# Package ROS pour le robot du club robotique de l'INSA Hauts-de-France
Ce package contient tous les drivers et les scripts de contrôle pour faire fonctionner le robot de l'association. 

## Contenu du package

1. driver pour la carte moteur
- La carte moteur est une carte développée par Valrobotique qui permet de contrôler la base roulante du robot. Cette carte 
d'une part permet d'envoyer des commandes aux moteurs en plus de les asservir grâce à un correcteur RST, d'autre part elle
permet de lire les encodeurs et envoyer leur valeur au port série. cette carte contient un microcontrôleur de type STM32 F303K8.

2. driver pour la carte ultrasonic
- La carte ultrasonic est une carte développée par Valrobotique qui permet de cartographiée l'environnement du robot avec des 
capteurs ultrasons. Il est possible de brancher au maximum 10 capteurs. La carte renvoie le résultat de chaque capteur
sous forme de chaîne de caractère Gcode. le microcontrôleur utilisée sur cette carte est de type ESP32.

3. Robot user interface (robot ui)
- Interface visuelle de contrôle pour gérer le robot

4. Serveur de gestion du robot à distance

## Packages annexes

pour utiliser le package ROS de Valrobotik il est nécessaire d'installer les package suivant dans votre catkin_workspace
1. Le package robot_localization
Ce package permet de filtrer et de fusionner les données de position du robot:
[repository Github de robot_localization](https://github.com/cra-ros-pkg/robot_localization "repository Github de robot_localization")

2. Le package hokuyo_node 
Ce package est le driver du Lidar Laser utilisé sur la robot. En effet en cas de changement de modèle de Lidar il suffit
simplment d'installer le bon driver. Il faut simplement publier les données du Lidar dans le topic **/scan** sous le nom de
frame **laser**

3. Le package hector_slam

## Bibilothèques python utilisées
1. matplotlib, numpy, math et re
2. pyserial
3. tkinter
4. json
5. socket et threading
