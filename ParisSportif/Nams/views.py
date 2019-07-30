from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from requests import get
from bs4 import BeautifulSoup
from .models import *
from datetime import date, timedelta


# Create your views here
def redir(request):
    return redirect('home')


def home(request):
    if request.session.has_key('user'):
        return render(request, 'index.html', {'isConnect': True, 'user': request.session['user']})
    else:
        return render(request, 'index.html', {'isConnect': False})


def Register(request):
    if request.POST:
        v = True
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        numberphone = request.POST.get('numberphone')
        password = request.POST.get('ps2')
        status = request.POST.get('status')
        user = User(name=name, lastname=lastname, email=email, contacts=numberphone, status=status)
        user.save()
        user.password = password
        user.save()
        print(name, lastname)
        return render(request, 'register.html', {'verif': v})
        v = False
    else:
        v = False
        return render(request, 'register.html', {'verif': v})


def Login(request):
    if request.POST:
        try:
            m = User.objects.get(email=request.POST['email'])
        except:
            return render(request, 'login.html', {'isNotUser': True})
        else:
            if m.password == request.POST['password']:
                m.status = True
                m.save()
                request.session['user'] = {'id': m.id, 'name': m.name, 'lastname': m.lastname, 'email': m.email,
                                           'contacts': m.contacts, 'password': m.password}
                return redirect('home')
            else:
                return render(request, 'login.html', {'isNotUser': True})
    else:
        return render(request, 'login.html')


def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect('home')


def live(request):
        url = 'https://www.matchendirect.fr/live-score/'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        table = html_soup.find('div', attrs={'id': 'livescore'})
        mydata = []
        for row in table.findAll('div', attrs={'class': 'panel panel-info'}):
            a_desc = row.find('h3', attrs={'class': 'panel-title'}).get_text()
            for el in row.findAll('tr'):
                resultat = {}
                heure = el.find('td', attrs={'class': 'lm1'}).get_text()
                eq1 = el.find('span', attrs={'class': 'lm3_eq1'}).get_text()
                eq2 = el.find('span', attrs={'class': 'lm3_eq2'}).get_text()

                scors = el.find('span', attrs={'class': 'lm3_score'}).get_text()

                resultat['heure'] = heure
                resultat['eq1'] = eq1
                resultat['eq2'] = eq2
                resultat['scors'] = scors

                mydata.append(resultat)
        data = mydata
        if request.POST:
            try:
                m = User.objects.get(email=request.POST['email'])
            except:
                return render(request, 'live.html', {'isNotUser': True,'isConnect': False,'info': data})
            else:
                if m.password == request.POST['password']:
                    m.status = True
                    m.save()
                    request.session['user'] = {'id': m.id, 'name': m.name, 'lastname': m.lastname, 'email': m.email,
                                               'contacts': m.contacts, 'password': m.password}
                    return redirect('live')
                else:
                    return render(request, 'live.html', {'isNotUser': True,'isConnect': False,'info': data})
        elif request.session.has_key('user'):
            return render(request, 'live.html',
                          {'isConnect': True, 'user': request.session['user'], 'pares': Paries.objects.all(), 'info': data,'date': date.today().strftime('%Y-%m-%d')})
        else:
            return render(request, 'live.html', {'isConnect': False, 'info': data})


def football(request):
    date_hier = date.today() - timedelta(days=1)
    url = 'https://www.matchendirect.fr/resultat-foot-{}/'.format(date_hier.strftime('%d-%m-%Y'))
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    table = html_soup.find('div', attrs={'id': 'livescore'})
    mydata = []
    for row in table.findAll('div', attrs={'class': 'panel panel-info'}):
        a_desc = row.find('h3', attrs={'class': 'panel-title'}).get_text()
        for el in row.findAll('tr'):
            resultat = {}
            heure = el.find('td', attrs={'class': 'lm1'}).get_text()
            eq1 = el.find('span', attrs={'class': 'lm3_eq1'}).get_text()
            eq2 = el.find('span', attrs={'class': 'lm3_eq2'}).get_text()

            scors = el.find('span', attrs={'class': 'lm3_score'}).get_text()

            resultat['heure'] = heure
            resultat['eq1'] = eq1
            resultat['eq2'] = eq2
            resultat['scors'] = scors
            mydata.append(resultat)

    data = mydata
    if request.POST:
        try:
            m = User.objects.get(email=request.POST['email'])
        except:
            return render(request, 'football.html', {'isNotUser': True, 'isConnect': False, 'donne': data, 'date': date_hier.strftime('%d-%m-%Y')})
        else:
            if m.password == request.POST['password']:
                m.status = True
                m.save()
                request.session['user'] = {'id': m.id, 'name': m.name, 'lastname': m.lastname, 'email': m.email,
                                           'contacts': m.contacts, 'password': m.password}
                return redirect('football')
            else:
                return render(request, 'football.html', {'isNotUser': True, 'isConnect': False, 'donne': data, 'date': date_hier.strftime('%d-%m-%Y')})
    elif request.session.has_key('user'):
        return render(request, 'football.html', {'isConnect': True, 'user': request.session['user'], 'paries': Paries.objects.all(), 'donne': data,
                                                 'date': date_hier.strftime('%d-%m-%Y'), 'date2': date_hier.strftime('%Y-%m-%d')})
    else:
        return render(request, 'football.html',
                      {'isConnect': False, 'donne': data, 'date': date_hier.strftime('%d-%m-%Y')})


def football_demain(request):
    date_demain = date.today() + timedelta(days=1)
    url = 'https://www.matchendirect.fr/resultat-foot-{}/'.format(date_demain.strftime('%d-%m-%Y'))
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    table = html_soup.find('div', attrs={'id': 'livescore'})
    mydata = []
    for row in table.findAll('div', attrs={'class': 'panel panel-info'}):
        a_desc = row.find('h3', attrs={'class': 'panel-title'}).get_text()
        for el in row.findAll('tr'):
            resultat = {}
            heure = el.find('td', attrs={'class': 'lm1'}).get_text()
            eq1 = el.find('span', attrs={'class': 'lm3_eq1'}).get_text()
            eq2 = el.find('span', attrs={'class': 'lm3_eq2'}).get_text()

            resultat['heure'] = heure
            resultat['eq1'] = eq1
            resultat['eq2'] = eq2
            mydata.append(resultat)

    data = mydata
    if request.POST:
        try:
            m = User.objects.get(email=request.POST['email'])
        except:
            return render(request, 'football_demain.html', {'isNotUser': True, 'isConnect': False, 'donne': data, 'date': date_demain.strftime('%d-%m-%Y')})
        else:
            if m.password == request.POST['password']:
                m.status = True
                m.save()
                request.session['user'] = {'id': m.id, 'name': m.name, 'lastname': m.lastname, 'email': m.email,
                                           'contacts': m.contacts, 'password': m.password}
                return redirect('football_demain')
            else:
                return render(request, 'football_demain.html', {'isNotUser': True, 'isConnect': False, 'donne': data, 'date': date_demain.strftime('%d-%m-%Y')})
    elif request.session.has_key('user'):
        return render(request, 'football_demain.html',
                      {'isConnect': True, 'user': request.session['user'], 'paries': Paries.objects.all(), 'donne': data,
                       'date': date_demain.strftime('%d-%m-%Y'), 'date2': date_demain.strftime('%Y-%m-%d')})
    else:
        return render(request, 'football_demain.html',
                      {'isConnect': False, 'donne': data, 'date': date_demain.strftime('%d-%m-%Y')})


def football_today(request):
    url = 'https://www.matchendirect.fr'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    table = html_soup.find('div', attrs={'id': 'livescore'})
    mydata = []
    for row in table.findAll('div', attrs={'class': 'panel panel-info'}):
        a_desc = row.find('h3', attrs={'class': 'panel-title'}).get_text()
        for el in row.findAll('tr'):
            resultat = {}
            heure = el.find('td', attrs={'class': 'lm1'}).get_text()
            eq1 = el.find('span', attrs={'class': 'lm3_eq1'}).get_text()
            eq2 = el.find('span', attrs={'class': 'lm3_eq2'}).get_text()
            resultat['heure'] = heure
            resultat['eq1'] = eq1
            resultat['eq2'] = eq2
            mydata.append(resultat)

    data = mydata
    if request.POST:
        try:
            m = User.objects.get(email=request.POST['email'])
        except:
            return render(request, 'football_today.html', {'isNotUser': True, 'isConnect': False, 'donne': data, 'date': date.today().strftime('%d-%m-%Y')})
        else:
            if m.password == request.POST['password']:
                m.status = True
                m.save()
                request.session['user'] = {'id': m.id, 'name': m.name, 'lastname': m.lastname, 'email': m.email,
                                           'contacts': m.contacts, 'password': m.password}
                return redirect('football_today')
            else:
                return render(request, 'football_today.html', {'isNotUser': True, 'isConnect': False, 'donne': data, 'date': date.today().strftime('%d-%m-%Y')})
    elif request.session.has_key('user'):
        return render(request, 'football_today.html',
                      {'isConnect': True, 'user': request.session['user'], 'paries': Paries.objects.all(),'donne': data,
                       'date': date.today().strftime('%d-%m-%Y'), 'date2': date.today().strftime('%Y-%m-%d')})
    else:
        return render(request, 'football_today.html',
                      {'isConnect': False, 'donne': data, 'date': date.today().strftime('%d-%m-%Y')})


def PartUser(request):
    return render(request, 'users/user.html',
                  {'user': request.session['user'], 'paries': Paries.objects.all().order_by("date_parie")})


def parie(request):
    if request.session.has_key('user'):
        if request.POST.get('name_form') == "parie":
            eqA = request.POST.get('equipeA')
            eqB = request.POST.get('equipeB')
            scA = request.POST.get('scoreA')
            scB = request.POST.get('scoreB')
            date_match = request.POST.get('date_match')
            montant = request.POST.get('prix_parie')
            parie = Paries(equipeA=eqA, score=scA, scoreB=scB, equipeB=eqB, montant_parié=montant, date_match=date_match, v_date_match=date_match,
                           id_user=User.objects.get(email=request.session['user']['email']))
            parie.save()
            return render(request, 'parie.html', {'eqA': eqA, 'eqB': eqB, 'makeparie': True, 'isConnect': True,
                                                  'user': request.session['user']})
        else:
            eqA = request.POST.get('eqa', False)
            eqB = request.POST.get('eqb', False)
            date_match = request.POST.get('date_match', False)
            return render(request, 'parie.html',
                          {'eqA': eqA, 'eqB': eqB, 'date_match': date_match, 'user': request.session['user'],
                           'isConnect': True})
    else:
        return redirect('login')
