# PDS2K19

On joue avec des legos, un raspi, et du code en ligne pour avoir une voiture (ou un train?) télécommandée (parce que c'est drôle)

des liens drôles mais sans doute pas faisables sauf si quelqu'un a un lego NXT à prêter :3 (Il parait qu'on peut demander a Geeraerts, il en a)
- [self-driving machine-learning Lego NXT car](https://medium.com/@project_m/self-drives-me-crazy-from-0-to-self-driving-car-in-150-hours-bf4f68d50d8a)
- [github](https://github.com/felipessalvatore/self_driving_pi_car)
- [Pad](https://bimestriel.framapad.org/p/45Q7bwOLJW) du boulot WiP

un truc plus accessible, je vais sans doute partir explorer ce coin-là pour le PDS
- [android-controlled lego car](http://pdwhomeautomation.blogspot.com/2012/11/raspberry-pi-powered-lego-car.html)
- [upgraded version](http://pdwhomeautomation.blogspot.com/2013/11/raspberry-pi-powered-lego-car-20.html)

et si on veut plonger dans du java (et des trains)
- [java on raspi for lego control](https://www.voxxed.com/2016/12/control-lego-java-raspberry-pi/)
- [tchou-tchou](https://blogs.infosupport.com/internet-of-lego-trains-part-3/)

[labo lego avec debrief](https://urlab.be/events/171 "labo lego")

# NOTRE PROOOOOOOOJET !
### matos:
- caméra Hercules HD Twist
- Raspberry Pi 3 Model B+
- Lego Mindstorms NXT

### fonctionnement
On a un fichier `server.py` (python3) qui tourne sur un pc et `legobot.py` (python2) qui tourne sur le raspi.
Le script sur le raspi prend et envoie la photo au pc et donne les commandes (avant, arrière, gauche, droite) au robot Lego.


# utiliser nxt-lego

`Utiliser python 2.x !!`

[Suivre ce tuto](https://github.com/Eelviny/nxt-python/wiki/Installation "tuto  nxt")

Puis tester en lançant `python interface.py`
