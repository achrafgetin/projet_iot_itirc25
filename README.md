![image](https://github.com/user-attachments/assets/33f67be1-c6df-4475-8a02-2c018497e840)

🌡️ Dashboard IoT – Température & Humidité
Ce projet a été réalisé avec mon binôme Achraf dans le cadre de notre formation à l’ENSA d’Oujda. L’idée était simple : créer une application web pour suivre en temps réel la température et l’humidité d’un environnement grâce à des capteurs connectés via Arduino.

🔍 Ce que fait l’application
Affiche la dernière température et humidité mesurée, avec l’heure de mise à jour

Montre l’évolution des données à travers des graphiques interactifs

Donne accès aux données brutes en JSON

Permet de consulter l’historique complet des mesures

Intègre une section pour le suivi des incidents

Inclut un espace admin pour la gestion sécurisée

⚙️ Stack utilisée
Django pour le backend

HTML/CSS + Bootstrap (ou Tailwind) pour le frontend

SQLite pour la base de données

Arduino avec capteur DHT11/DHT22 pour récupérer les données

🔧 Mise en place
bash
Copier
Modifier
git clone https://github.com/ton-utilisateur/nom-du-projet.git
cd nom-du-projet
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
📡 Comment ça marche côté IoT ?
Le capteur (via Arduino + WiFi) envoie les données à l’application web par des requêtes HTTP. Une fois reçues, les données sont stockées et affichées automatiquement dans le dashboard.
