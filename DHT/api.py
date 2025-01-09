from .models import Dht11, Incident, Alerte
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import requests
from django.utils import timezone

# Fonction pour envoyer des messages Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response

# Fonction pour gérer les incidents
def gerer_incident(temp_actuel, temp_precedent):
    # Récupérer l'incident ouvert (s'il existe)
    incident_ouvert = Incident.objects.filter(est_ouvert=True).first()

    if temp_actuel < 20:
        if temp_precedent >= 20 and incident_ouvert:
            # Fermer l'incident actuel
            incident_ouvert.date_fin = timezone.now()
            incident_ouvert.est_ouvert = False
            incident_ouvert.save()
    else:
        if not incident_ouvert:
            # Ouvrir un nouvel incident
            incident_ouvert = Incident.objects.create()
            # Envoyer une alerte initiale
            Alerte.objects.create(
                incident=incident_ouvert,
                message="Alerte : Température élevée détectée.",
                utilisateurs_avertis="Utilisateur 1"
            )
        else:
            # Incrémenter le compteur d'itérations
            incident_ouvert.iterations += 1
            incident_ouvert.save()

            # Gérer les alertes en fonction du compteur d'itérations
            if incident_ouvert.iterations == 2:
                Alerte.objects.create(
                    incident=incident_ouvert,
                    message="Alerte : Température toujours élevée.",
                    utilisateurs_avertis="Utilisateurs 1 et 2"
                )
            elif incident_ouvert.iterations == 3:
                Alerte.objects.create(
                    incident=incident_ouvert,
                    message="Alerte : Température critique.",
                    utilisateurs_avertis="Utilisateurs 1, 2 et 3"
                )

# Vue pour gérer les données du capteur DHT11
@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            # Gestion des incidents
            temp_precedent = Dht11.objects.order_by('-id')[1].temp if Dht11.objects.count() > 1 else None
            gerer_incident(derniere_temperature, temp_precedent)

            # Envoi d'alertes si la température dépasse 20°C
            if derniere_temperature > 20:
                # Alert Email
                subject = 'Alerte'
                message = 'La température dépasse le seuil de 20°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['abidihajji46@gmail.com']
                send_mail(subject, message, email_from, recipient_list)

                # Alert WhatsApp
                """
                account_sid = 'AC967737acc3b5c9288688dd7481ef029c'
                auth_token = 'c4ae755f579949d54bf00ce0725a72fa'
                client = Client(account_sid, auth_token)
                message_whatsapp = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body='La température dépasse le seuil de 20°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation',
                    to='whatsapp:+212620671238'
                
                )
                """

                # Alert Telegram
                telegram_token = '7931512511:AAGmZPVuEmgrtYrph-o3E7lZ7DqXQelmWl4'
                chat_id = '6556570945'  # Remplacez par votre ID de chat
                telegram_message = 'La température dépasse le seuil de 20°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                send_telegram_message(telegram_token, chat_id, telegram_message)

            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)