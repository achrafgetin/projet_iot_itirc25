from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Incident
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

@login_required
def table(request):
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now() - derniere_date
    difference_minutes = delta_temps.seconds // 60
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes > 60:
        temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
    valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': derniere_ligne.temp, 'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})

@login_required
def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
#pour afficher navbar de template
@login_required
def index_view(request):
    return render(request, 'index.html')

#pour afficher les graphes
@login_required
def graphiqueTemp(request):
    return render(request, 'ChartTemp.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
@login_required
def graphiqueHum(request):
    return render(request, 'ChartHum.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
@login_required
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)
@login_required
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
@login_required
def chart_data_jour(request):
    dht = Dht11.objects.all()
    now = timezone.now()

    # Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)

    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
@login_required
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }

    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
@login_required
def chart_data_mois(request):
    dht = Dht11.objects.all()

    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)


@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def sendtele():
    token = '6662023260:AAG4z48OO9gL8A6szdxg0SOma5hv9gIII1E'
    rece_id = 1242839034
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))

def custom_logout(request):
    logout(request)
    return redirect('/')

def etat_incident(request):
    # Récupérer l'incident ouvert (s'il existe)
    incident_ouvert = Incident.objects.filter(est_ouvert=True).first()
    contexte = {
        'incident_ouvert': incident_ouvert,
    }
    return render(request, 'etat_incident.html', contexte)

def historique_incidents(request):
    # Récupérer tous les incidents (ouverts et fermés)
    incidents = Incident.objects.all().order_by('-date_debut')
    contexte = {
        'incidents': incidents,
    }
    return render(request, 'historique_incidents.html', contexte)

@login_required
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin/')  # Redirige vers la page d'administration de Django
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect, ou vous n'êtes pas administrateur.")
            return redirect('admin_login')  # Redirige vers la page de connexion administrateur

    return render(request, 'admin_login.html')