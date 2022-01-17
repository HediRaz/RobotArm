# RobotArm
Smart robot arm

Librairie pour piloter le bras robotique du Hub IA de CentraleSupélec. Développé par Automatants, l'association d'IA de CentraleSupélec.



## Project Architecture
ServoFromPC.ino is the file that updates the arm position

comm.py gives some useful functions to communicate with the Arduino from your PC

servo.py define the RobotArm class which defines some rules for the arm

emulation.py define the class Emulation that is useful to test your code before actually test it on the arm


## Projects
### Hand Tracking
Contrôler le bras avec sa main.

L'annulaire contrôle le premier segment, le majeur le second, l'annulaire le troisième et le pouce contrôle la pince.

### Arm Tracking
Contrôler le bras avec son propre bras.

[Attention] Ne fonctionne qu'avec le bras gauche.


## Installation
clone le repo github :
```bash
git clone git@github.com:HediRaz/RobotArm.git
```

#### Sur linux / Windows
Installer les libraries :
```bash
pip install typing
pip install python-opencv
pip install mediapipe
```

#### Sur raspberry pi
Vérifier que numpy est bien à jour, pour l'update :
``` bash
pip3 install --upgrade numpy
```

Installer la version dernière version d'opencv et la version 32bits de mediapipe
```bash
sudo apt install ffmeg python3-opencv
pip3 install mediapipe-rpi4 #pour la raspi 4 sinon -rpi3 pour la 3
```

### Connection avec Arduino
#### Sur Windows
Il suffit de brancher la carte Arduino, elle sera normalement associée au port Com3
#### Sur Linux
Le port utilisé est normalement : `/dev/ttyACM0` (pour une Arduino Uno)
Sinon avec la librairie pyserial (`pip3 install pyserial`), lancer la commande :
``` bash
python -m serial.tools.list_ports
```
Changer les droit d'accès à `/dev/ttyACM0` avec chmod.
/!\ marche mais un peu overkill car peu sécurisé :
```bash
sudo chmod -R 777 /dev/ttyACM0
```

### Lancement au démarrage (raspi seulement)
Utiliser systemd (suivre la méthode 4 du [tuto](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#systemd))
Et changer la ligne ExecStart de manière appropriée en :
```systemd
[Unit]
Description=My Sample Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/bin/bash -c 'cd /home/pi/Documents/RobotArm/ && python3 handtracking.py'

[Install]
WantedBy=multi-user.target
```
