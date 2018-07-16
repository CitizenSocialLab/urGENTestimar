from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import *

from django import forms
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils import timezone

from game.models import *
from game.vars import *

import math

import random


def user_exists_in_db(user):
    try:
        User.objects.get(pk=user.id)
        return True
    except:
        return False

def index(request, **kwargs):
    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        print user.email
        return redirect('user.registre')

    return redirect('user.nickname')

#########################################################################################################
#########################################################################################################
# Pantalla 1: Escollir un nickname
class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=300)

@csrf_exempt
def nickname(request, **kwargs):

    if not('game' in request.session) or request.session['game'] is None:
        print 'ERROR 107: Seleccionar Joc'
        #user = request.session['user']
        #if not user_exists_in_db(user):
        #    del request.session['user']
        #    return redirect('user.nickname')
        return redirect('index')

    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        return redirect('user.registre')

    #Borrem el nickanme de la sessio
    if 'nickname' in request.session:
        del request.session['nickname']

    if request.method != 'POST':
        return render_to_response('nickname.html', {'lang': request.session['lang'], 'game': request.session['game'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))
    else:
        form = NicknameForm(request.POST)
        nick = form['nickname'].value()

        if not nick or len(nick) == 0:
            return render_to_response('nickname.html', {'lang': request.session['lang'], 'game': request.session['game'], 'text': request.session['text']},
                                      context_instance=RequestContext(request))

        if len(nick) > 20:
            return render_to_response('nickname.html',
                                      {'nickname_error': False, 'nickname_error2': True, 'nickname': nick,
                                       'lang': request.session['lang'], 'text': request.session['text'], 'game': request.session['game']},
                                      context_instance=RequestContext(request))

        #Si l'usuari ja existeix enviar-lo a la pantalla d'inici
        try:
            user = User.objects.get(nickname=nick)

            if user.partida_current:
                if user.partida_current.classe != request.session['game']: # Usuari amb partida activa que no es la que intenta accedir
                    print 'ERROR 101\nid_user: '+str(user.id)
                    return render_to_response('nickname.html',
                                      {'nickname_error1': True,
                                       'nickname_error2': False,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            if user.data_finalitzacio_dictator1 and request.session['game']=="dictator1": # El participant ja ha jugat aquest joc
                print 'ERROR 102\nid_user:'+str(user.id)
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            elif user.data_finalitzacio_dictator2 and request.session['game']=="dictator2": # El participant ja ha jugat aquest joc
                print 'ERROR 103\nid_user:'+str(user.id)
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            elif user.data_finalitzacio_prisoner1 and request.session['game']=="prisoner1": # El participant ja ha jugat aquest joc
                print 'ERROR 104\nid_user:'+str(user.id)
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            elif user.data_finalitzacio_prisoner2 and request.session['game']=="prisoner2": # El participant ja ha jugat aquest joc
                print 'ERROR 105\nid_user:'+str(user.id)
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            elif user.data_finalitzacio_snowdrift1 and request.session['game']=="snowdrift1": # El participant ja ha jugat aquest joc
                print 'ERROR 106\nid_user:'+str(user.id)
                return render_to_response('nickname.html',
                                      {'nickname_error1': False,
                                       'nickname_error2': True,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'game': request.session['game']},
                                      context_instance=RequestContext(request))

            else:
                user = User.objects.get(nickname=nick)
                request.session['user'] = user
                request.session['nickname'] = nick
                return redirect('user.enquesta2')

        #Sino enviar-lo a l'enquesta
        except ObjectDoesNotExist:
            request.session['user'] = None
            request.session['nickname'] = nick

            return redirect('user.avis')

#########################################################################################################
#########################################################################################################
# Pantalla avis legal
class AvisForm(forms.Form):
    check_1 = forms.CharField(max_length=20)

@csrf_exempt
def avis(request, **kwargs):
    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.login')
        #print user.useremail_set.all()
        return redirect('user.inici')


    if request.method != 'POST':
        return render_to_response('avis.html',  {'lang': request.session['lang'], 'text': request.session['text']},
                              context_instance=RequestContext(request))
    else:
        form = AvisForm(request.POST)
        request.session['check1'] = True

        return redirect('user.enquesta1')


#########################################################################################################
#########################################################################################################
# Pantalla 5: Enquesta 1
class SigninForm1(forms.Form):
    genere = forms.CharField(max_length=100)
    rang_edat = forms.CharField(max_length=100)
    on_vius = forms.CharField(max_length=6)

@csrf_exempt
def enquesta1(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        # print user.useremail_set.all()
        return redirect('user.registre')

    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "ERROR!!"
        return redirect('user.nickname')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquesta1.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'game': request.session['game']},
                                  context_instance=RequestContext(request))

    form = SigninForm1(request.POST)
    genere = form['genere'].value()
    rang_edat = form['rang_edat'].value()
    on_vius = form['on_vius'].value()

    if not form.is_valid():
        return render_to_response('enquesta1.html', {
            'genere': genere,
            'genere_danger': genere is None or len(genere) == 0,
            'genere_1_checked': 'bx-option-selected' if genere == 'F' else '',
            'genere_2_checked': 'bx-option-selected' if genere == 'M' else '',
            'genere_3_checked': 'bx-option-selected' if genere == 'T' else '',
            'genere_4_checked': 'bx-option-selected' if genere == 'O' else '',
            'genere_5_checked': 'bx-option-selected' if genere == 'N' else '',

            'rang_edat': rang_edat,
            'rang_edat_danger': rang_edat is None or len(rang_edat) == 0,
            'rang_edat_1_checked': 'bx-option-selected' if rang_edat == 'r1' else '',
            'rang_edat_2_checked': 'bx-option-selected' if rang_edat == 'r2' else '',
            'rang_edat_3_checked': 'bx-option-selected' if rang_edat == 'r3' else '',
            'rang_edat_4_checked': 'bx-option-selected' if rang_edat == 'r4' else '',
            'rang_edat_5_checked': 'bx-option-selected' if rang_edat == 'r5' else '',
            'rang_edat_6_checked': 'bx-option-selected' if rang_edat == 'r6' else '',

            'on_vius': on_vius,
            'on_vius_danger': on_vius is None or len(on_vius) == 0,
            'on_vius_1_checked': 'bx-option-selected' if on_vius == 'r1' else '',
            'on_vius_2_checked': 'bx-option-selected' if on_vius == 'r2' else '',
            'on_vius_3_checked': 'bx-option-selected' if on_vius == 'r3' else '',
            'lang': request.session['lang'],
            'text': request.session['text'],
            'game': request.session['game']},
            context_instance=RequestContext(request))

    else:


        request.session['genere'] = genere
        request.session['rang_edat'] = rang_edat
        request.session['on_vius'] = on_vius

        user = User()

        user.nickname = request.session['nickname']
        user.genere = request.session['genere']
        user.on_vius = request.session['on_vius']
        user.rang_edat = request.session['rang_edat']
        user.check1 = request.session['check1']


        user.data_creacio = timezone.now()

        user.status = "Survey-1"
        user.session_game = request.session['game']

        user.save()

        request.session['user'] = user

        return redirect('user.enquesta2')

#########################################################################################################
#########################################################################################################
# Pantalla 6: Enquesta part 2
class SigninForm2(forms.Form):
    pr4 = forms.CharField(max_length=100, required=True)
    pr5 = forms.CharField(max_length=100, required=False)

@csrf_exempt
def enquesta2(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')

        if request.session['game'] == 'prisoner1' and user.interest_prisoner1 != "": return redirect('user.bot1')
        if request.session['game'] == 'prisoner2' and user.interest_prisoner2 != "" and user.feeling_prisoner2 !="": return redirect('user.bot1')
        if request.session['game'] == 'snowdrift1': return redirect('user.bot1')
        if request.session['game'] == 'dictator1' and user.interest_dictator1 != "": return redirect('user.bot1')


    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "ERROR!!"
        return redirect('user.nickname')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquesta2.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'game': request.session['game']},
                                  context_instance=RequestContext(request))

    form = SigninForm2(request.POST)
    pr4 = form['pr4'].value()
    pr5 = form['pr5'].value()

    if not form.is_valid():
        print 'not valid'
        print form.errors
        return render_to_response('enquesta2.html', {
            'pr4': pr4,
            'pr4_danger': pr4 is None or len(pr4) == 0,
            'pr4_r1_checked': 'bx-option-selected' if pr4 == 'Y' else '',
            'pr4_r2_checked': 'bx-option-selected' if pr4 == 'N' else '',

            'pr5': pr5,
            'pr5_danger': pr5 is None or len(pr5) == 0,
            'pr5_r1_checked': 'bx-option-selected' if pr5 == 'Y' else '',
            'pr5_r2_checked': 'bx-option-selected' if pr5 == 'N' else '',

            'lang': request.session['lang'],
            'text': request.session['text'],
            'game': request.session['game']
        }, context_instance=RequestContext(request))


    else:
        request.session['interest'] = pr4
        request.session['feeling'] = pr5

        if request.session['game'] == 'prisoner1': user.interest_prisoner1 = request.session['interest']
        if request.session['game'] == 'prisoner2': user.interest_prisoner2 = request.session['interest']
        if request.session['game'] == 'dictator1': user.interest_dictator1 = request.session['interest']
        if request.session['game'] == 'dictator2': user.interest_dictator2 = request.session['interest']
        if request.session['game'] == 'prisoner2': user.feeling_prisoner2 = request.session['feeling']

        user.status = "Survey-2"
        user.session_game = request.session['game']

        user.save()

        request.session['user'] = user

        return redirect('user.bot1')

#########################################################################################################
#########################################################################################################
# Pantalla 6: Bot
class SigninForm3(forms.Form):
    pr1_bot1 = forms.CharField(max_length=100, required=True)

@csrf_exempt
def bot1(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')

        if request.session['game'] == 'prisoner1' and user.bot_pr1_prisoner1 != "": return redirect('user.registre')
        if request.session['game'] == 'prisoner2' and user.bot_pr1_prisoner2 != "": return redirect('user.registre')
        if request.session['game'] == 'snowdrift1' and user.bot_pr1_snowdrift1 != "": return redirect('user.registre')
        if request.session['game'] == 'dictator1' and user.bot_pr1_dictator1 != "": return redirect('user.registre')


    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "ERROR!!"
        return redirect('user.nickname')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('bot1.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'game': request.session['game']},
                                  context_instance=RequestContext(request))

    form = SigninForm3(request.POST)
    pr1_bot1 = form['pr1_bot1'].value()

    print pr1_bot1
    if not form.is_valid():
        print 'not valid'
        print form.errors
        return render_to_response('bot1.html', {
            'pr1_bot1': pr1_bot1,
            'pr1_bot1_danger': pr1_bot1 is None or len(pr1_bot1) == 0,
            'pr1_bot1_r1_checked': 'bx-option-selected' if pr1_bot1 == 'Y' else '',
            'pr1_bot1_r2_checked': 'bx-option-selected' if pr1_bot1 == 'N' else '',
            'lang': request.session['lang'],
            'game': request.session['game'],
            'text': request.session['text']},
            context_instance=RequestContext(request))


    else:
        request.session['pr1_bot1'] = pr1_bot1

        print request.session['pr1_bot1']

        if request.session['game'] == 'prisoner1': user.bot_pr1_prisoner1 = request.session['pr1_bot1']
        if request.session['game'] == 'prisoner2': user.bot_pr1_prisoner2 = request.session['pr1_bot1']
        if request.session['game'] == 'dictator1': user.bot_pr1_dictator1 = request.session['pr1_bot1']
        if request.session['game'] == 'snowdrift1': user.bot_pr1_snowdrift1 = request.session['pr1_bot1']

        user.status = "Survey-3"
        user.session_game = request.session['game']

        user.save()

        request.session['user'] = user

        return redirect('user.registre')

#########################################################################################################
#########################################################################################################
@csrf_exempt
def logout(request, **kwargs):
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        user.status = "Logged-Out"

        if user.partida_current:
            user.partida_current = None

        user.save()
        del request.session['user']
    return redirect('index')

#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################

#Pantalla 2:Seleccio de l'experiment si ja hi ha un usuari a la sessio
@csrf_exempt
def inici(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.nickname')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Mirem que aquest user no hagi acabat ja!!!
    if user.data_finalitzacio:
        return redirect('user.final_joc')

    # si l'usuari no te cap partida assignada
    if not user.partida:
        #Mirem si ens estan demanant d'entrar a partida o encara no
        if request.method != 'POST':
            return render_to_response('inici.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False},
                                      context_instance=RequestContext(request))

        # Si demanem entrar a partida, primer mirem si n'hi ha una d'activa
        partida_activa = Partida.objects.filter(estat="REGISTRANT")
        if len(partida_activa) > 0:
            # Si es aixi registrem a l'usuari
            partida_activa = partida_activa[0]
            #print partida_activa.num_partida

            try:
                #Controlem que nomes hi hagi 6 usuaris a la partida!!
                if partida_activa.usuaris_registrats < 6:
                    partida_activa.usuaris_registrats += 1
                    partida_activa.save()
                    print "Partida", partida_activa.num_partida,"// usuaris registrats:", partida_activa.usuaris_registrats

                    user.partida = partida_activa
                    user.data_registre = timezone.now()
                    user.save()
                else:
                    return redirect('user.inici')

                #Si tot ha sortit be, redirigim l'usuari a la pantalla de joc
                return redirect('game.index')
            except:
                #Si hi ha hagut error tornem a la pagina
                return redirect('user.inici')


        return render_to_response('inici.html', {'user': user,
                                                 'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'error_partida':True},
                                  context_instance=RequestContext(request))

    # Si l'usuari te partida assignada
    else:
        #Si l'usuari ja te una partida assignada i aquesta encara esta registrant
        if user.partida and user.partida.estat == "REGISTRANT":
            return redirect('game.index')


        #Si l'usuari ja te una partida assignada i aquesta no ha comensat a jugar
        if user.partida and user.partida.estat == "JUGANT":
            date_now = timezone.now()
            date_start = user.partida.data_inicialitzacio
            temps_actual_joc = (date_now - date_start).total_seconds()

            #print date_now, date_start, temps_actual_joc, TEMPS_INICI_SEC
            if temps_actual_joc < TEMPS_INICI_SEC:
                return redirect('game.index')

            else :
                 #return redirect('game.index')
                return redirect('user.inici')


        #Si la partida on ha participat l'usuari ja esta acabada, l'envio als resultats
        if user.partida and (user.partida.estat == "ACABADA" or user.partida.estat == "ACABADA_MANUAL"):
            return redirect('user.final_joc')

        return redirect('user.inici')

#####################################################################################################
########################################### REGISTRE ################################################
#####################################################################################################

@csrf_exempt
def registre(request, **kwargs):

    print request.session['game']
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.nickname')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Mirem que aquest user no hagi acabat ja!!!
    #if user.data_finalitzacio:
    #    return redirect('user.final_joc')


    # Agafam la partida activa de la sessio del joc corresponent
    partida_activa = Partida.objects.filter(estat="REGISTRANT").filter(classe=request.session["game"])
    # Miram si hi ha partides actives i agafam la primera de elles
    if len(partida_activa) > 0:
        partida_activa = partida_activa[0]

    # Si l'usuari no te cap partida assignada
    if not user.partida_current:
        print 'No Partida Activa'
        #Mirem si ens estan demanant d'entrar a partida o encara no
        if request.method != 'POST':
            # Si intenta entra i no hi ha partida activa hauria de crear-ne una
            return render_to_response('registre.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False,
                                                     'game': request.session['game'],
                                                     'waiting':0},
                                      context_instance=RequestContext(request))

        # Si hi ha partida activa li assignam la partida al usuari
        if partida_activa:
            try:
                #Controlem que nomes hi hagi 2 usuaris a la partida!!
                if partida_activa.usuaris_registrats < 2:
                    partida_activa.usuaris_registrats += 1
                    partida_activa.save()

                    # Assignam la partida al usuari
                    user.partida_current = partida_activa

                    if request.session['game'] == "prisoner1": user.data_registre_prisoner1 = timezone.now()
                    if request.session['game'] == "prisoner2": user.data_registre_prisoner2 = timezone.now()
                    if request.session['game'] == "dictator1": user.data_registre_dictator1 = timezone.now()
                    if request.session['game'] == "dictator2": user.data_registre_dictator2 = timezone.now()
                    if request.session['game'] == "snowdrift1": user.data_registre_snowdrift1 = timezone.now()

                    if request.session['game'] == "prisoner1": user.partida_prisoner1 = partida_activa
                    if request.session['game'] == "prisoner2": user.partida_prisoner2 = partida_activa
                    if request.session['game'] == "dictator1": user.partida_dictator1 = partida_activa
                    if request.session['game'] == "dictator2": user.partida_dictator2 = partida_activa
                    if request.session['game'] == "snowdrift1": user.partida_snowdrift1 = partida_activa

                    user.data_last_action = timezone.now()

                    user.status = "Register-Waiting"
                    user.session_game = request.session['game']

                    user.save()

                # Agafam els usuaris
                if request.session['game'] == "prisoner1": usuaris = User.objects.filter(partida_prisoner1=partida_activa)
                if request.session['game'] == "prisoner2": usuaris = User.objects.filter(partida_prisoner2=partida_activa)
                if request.session['game'] == "dictator1": usuaris = User.objects.filter(partida_dictator1=partida_activa)
                if request.session['game'] == "dictator2": usuaris = User.objects.filter(partida_dictator2=partida_activa)
                if request.session['game'] == "snowdrift1": usuaris = User.objects.filter(partida_snowdrift1=partida_activa)

                # Si ja tenim els dos usuaris generam les dades de la partida
                if (len(usuaris) > 1):
                    partida_activa.estat = "GENERANT_DADES"
                    partida_activa.save()

                    if request.session['game'] == "prisoner1": generar_prisoner(usuaris, partida_activa)
                    if request.session['game'] == "prisoner2": generar_prisoner(usuaris, partida_activa)
                    if request.session['game'] == "dictator1": generar_dictator(usuaris, partida_activa)
                    if request.session['game'] == "dictator2": generar_dictator(usuaris, partida_activa)
                    if request.session['game'] == "snowdrift1": generar_snowdrift(usuaris, partida_activa)

                # Si no tenim els dos usuaris ens quedam al registre esperant
                else:
                   return redirect('user.registre')

                #Si tot ha sortit be, redirigim l'usuari a la pantalla de joc
                return redirect('user.registre')
            except:
                #Si hi ha hagut error tornem a la pagina
                return redirect('user.registre')

        # En cas de que no hi hagi una partida activa en cream una
        else:
            # Miram el numero de partida que li correspo en base a totes les partides que tenim
            results = Partida.objects.all().order_by('-num_partida')
            npartida = 1
            # Si hi ha mes d'un result, mirem quin es el seguent num de partida
            if len(results) > 0:
                npartida = results[0].num_partida+1

            # Cream la partida
            partida = Partida.objects.create(num_partida=npartida,
                                     data_creacio=timezone.now(),
                                     estat="REGISTRANT",
                                     classe=request.session["game"])
            partida.save()

            # L'assignam al nostre usuari
            user.partida_current = partida

            if request.session['game'] == "prisoner1":user.data_registre_prisoner1 = timezone.now()
            if request.session['game'] == "prisoner2":user.data_registre_prisoner2 = timezone.now()
            if request.session['game'] == "dictator1":user.data_registre_dictator1 = timezone.now()
            if request.session['game'] == "dictator2":user.data_registre_dictator2 = timezone.now()
            if request.session['game'] == "snowdrift1":user.data_registre_snowdrift1 = timezone.now()

            if request.session['game'] == "prisoner1": user.partida_prisoner1 = user.partida_current
            if request.session['game'] == "prisoner2": user.partida_prisoner2 = user.partida_current
            if request.session['game'] == "dictator1": user.partida_dictator1 = user.partida_current
            if request.session['game'] == "dictator2": user.partida_dictator2 = user.partida_current
            if request.session['game'] == "snowdrift1": user.partida_snowdrift1 = user.partida_current


            user.data_last_action = timezone.now()

            user.status = "Register-Creating"
            user.session_game = request.session['game']

            user.save()

            # Suman aquest usuari a la partida
            partida.usuaris_registrats += 1
            partida.save()

            return render_to_response('registre.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False,
                                                     'game': request.session['game'],
                                                     'waiting':1},
                                      context_instance=RequestContext(request))
    # Si el usuari te partida assignada
    else:
        print 'Partida Activa: ' +str(user.partida_current.id)
        print 'Partida Activa Status: ' +str(user.partida_current.estat)
        print 'Partida Activa Session: '+str(user.partida_current.classe)
        print 'Game Session: '+str(request.session['game'])

        if user.partida_current.classe != request.session['game']:
            return render_to_response('registre.html', {'user': user,
                                                     'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'error_partida':False,
                                                     'error_partida_2':True, # partida_activa
                                                     'game': request.session['game'],
                                                     'waiting':0},
                                      context_instance=RequestContext(request))


        # En caso de que la partida estigui acabada, vamos a los resultados
        if user.partida_current and (user.partida_current.estat == "ACABADA" or user.partida_current.estat == "ACABADA_MANUAL"):
            return redirect('user.final_joc')

        # En cas que estigui jugant al a un joc concret, enviam al propi joc
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "prisoner1":
            return redirect('user.joc_prisoner1_1')
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "prisoner2":
            return redirect('user.joc_prisoner2_1')
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "dictator1":
            return redirect('user.joc_dictator1_')
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "dictator2":
            return redirect('user.joc_dictator2_')
        if user.partida_current and user.partida_current.estat == "JUGANT" and request.session['game'] == "snowdrift1":
            return redirect('user.joc_snowdrift1_')

        # En cas de que estigui registrant-se
        if user.partida_current and (user.partida_current.estat == "REGISTRANT"):
            # Agafam els usuaris
            if request.session['game'] == "prisoner1": usuaris = User.objects.filter(partida_prisoner1=partida_activa)
            if request.session['game'] == "prisoner2": usuaris = User.objects.filter(partida_prisoner2=partida_activa)
            if request.session['game'] == "dictator1": usuaris = User.objects.filter(partida_dictator1=partida_activa)
            if request.session['game'] == "dictator2": usuaris = User.objects.filter(partida_dictator2=partida_activa)
            if request.session['game'] == "snowdrift1": usuaris = User.objects.filter(partida_snowdrift1=partida_activa)

            # Si ja tenim els dos usuaris generam les dades de la partida
            if (len(usuaris) > 1):
                partida_activa.estat = "GENERANT_DADES"
                partida_activa.save()

                if request.session['game'] == "prisoner1": generar_prisoner(usuaris, partida_activa)
                if request.session['game'] == "prisoner2": generar_prisoner(usuaris, partida_activa)
                if request.session['game'] == "dictator1": generar_dictator(usuaris, partida_activa)
                if request.session['game'] == "dictator2": generar_dictator(usuaris, partida_activa)
                if request.session['game'] == "snowdrift1": generar_prisoner(usuaris, partida_activa)


        # Refrescam el registre i ens movem on calgui
        return render_to_response('registre.html', {'user': user,
                                                    'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                    'error_partida':False,
                                                    'game': request.session['game'],
                                                    'waiting':1},
                                  context_instance=RequestContext(request))


#####################################################################################################
###################################### GENERACIO DE DADES ###########################################
#####################################################################################################

def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)


#####################################################################################################
###################################### GENERACIO DE DICTATOR ########################################
#####################################################################################################

def generar_dictator(usuaris, partida_activa):
    # Cream un conjunt de petits dictadors
    game_dictator = []
    for i in range(len(usuaris)):
        dictator =  Dictator()
        dictator.user = usuaris[i]
        dictator.partida = partida_activa
        game_dictator.append(dictator)
        dictator.save()


    # Assignem un numero als participants de l'experiment
    random.shuffle(NUMS_JUGADOR)
    # Dictator Game - Valors inicials
    random.shuffle(DICTATOR_PUNISHER)

    # Dictator Game - Llistat usuaris
    llista_dictator_dictator1 = []
    llista_dictator_dictator2 = []

    for i in range(len(usuaris)):
        # Numero de jugador per cada usuari
        usuaris[i].num_jugador = NUMS_JUGADOR[i]

        # Dictator Game - Donam el rol DICTATOR a la primera i PUNISHER a las segona
        if DICTATOR_PUNISHER[i]=='D1':
            game_dictator[i].rol1 = 'D'
            llista_dictator_dictator1.append(game_dictator[i])

            if usuaris[i].is_robot:
                game_dictator[i].seleccio1 = random.choice([0,1,2,3,4])

        # Dictator Game - Donam el rol PUNISHER  a la primera i DICTADOR a la segona
        elif DICTATOR_PUNISHER[i]=='D2':
            game_dictator[i].rol1 = 'D'

            llista_dictator_dictator2.append(game_dictator[i])

            if usuaris[i].is_robot:
                game_dictator[i].seleccio1 = random.choice([0,1,2,3,4,5])

    #Fem les parelles per als jocs DICTATOR

    while llista_dictator_dictator1:
        rand1_dictator = pop_random(llista_dictator_dictator1)
        rand2_dictator = pop_random(llista_dictator_dictator2)
        rand1_dictator.rival1 = rand2_dictator.user
        rand2_dictator.rival1 = rand1_dictator.user
        rand1_dictator.save()
        rand2_dictator.save()


    # Engegam la partida
    partida_activa.estat = "JUGANT"
    partida_activa.data_inicialitzacio = timezone.now()
    partida_activa.save()


#####################################################################################################
###################################### GENERACIO DE DICTATOR ########################################
#####################################################################################################

def generar_prisoner(usuaris, partida_activa):

    game_prisoner = []
    # Cream els petits prisoners
    for i in range(len(usuaris)):

        prisoner = Prisoner()
        prisoner.user = usuaris[i]
        prisoner.partida = partida_activa
        game_prisoner.append(prisoner)
        prisoner.save()

    # Assignem un numero als participants de l'experiment
    random.shuffle(NUMS_JUGADOR)
    # Prisoner Game - Valors inicials
    random.shuffle(ADVANTAGE_DISADVANTAGE)

    # Prisoner Dilemma - Llistat usuaris
    llista_prisoner1 = [] # JUGADORES IGUALES

    llista_prisoner2_A = [] # JUGADORES A en la 2
    llista_prisoner2_D = [] # JUGADORES D en la 2


    for i in range(len(usuaris)):
        # Numero de jugador per cada usuari
        usuaris[i].num_jugador = NUMS_JUGADOR[i]

        # Cream les dades per cas Prisoner 1
        if partida_activa.classe == 'prisoner1':
            game_prisoner[i].rol1 = 'E'
            if usuaris[i].is_robot:
                print 'is_robot'
                game_prisoner[i].seleccio1 = random.choice(['C','D'])
            llista_prisoner1.append(game_prisoner[i])

        if partida_activa.classe == 'prisoner2':
            game_prisoner[i].rol1 = ADVANTAGE_DISADVANTAGE[i]

            if usuaris[i].is_robot:
                game_prisoner[i].seleccio1 = random.choice(["C","D"])

            if ADVANTAGE_DISADVANTAGE[i]=='A':
                llista_prisoner2_A.append(game_prisoner[i])

            elif ADVANTAGE_DISADVANTAGE[i] =='D':
                llista_prisoner2_D.append(game_prisoner[i])




        usuaris[i].save()

    #Fem les parelles al Prisoner
    if partida_activa.classe == 'prisoner1':
        while llista_prisoner1:
            rand1_prisoner = pop_random(llista_prisoner1)
            rand2_prisoner = pop_random(llista_prisoner1)
            rand1_prisoner.rival1 = rand2_prisoner.user
            rand2_prisoner.rival1 = rand1_prisoner.user
            rand1_prisoner.save()
            rand2_prisoner.save()

    if partida_activa.classe == 'prisoner2':
        while llista_prisoner2_A:
            rand1_prisoner = pop_random(llista_prisoner2_A)
            rand2_prisoner = pop_random(llista_prisoner2_D)
            rand1_prisoner.rival1 = rand2_prisoner.user
            rand2_prisoner.rival1 = rand1_prisoner.user
            rand1_prisoner.save()
            rand2_prisoner.save()


    #I... ENGEGO LA PARTIDA!!!!

    partida_activa.estat = "JUGANT"
    partida_activa.data_inicialitzacio = timezone.now()
    partida_activa.save()

#####################################################################################################
###################################### GENERACIO DE SNOWDRIFT ########################################
#####################################################################################################

def generar_snowdrift(usuaris, partida_activa):

    game_snowdrift = []
    # Cream els petits prisoners
    for i in range(len(usuaris)):

        snowdrift = Snowdrift()
        snowdrift.user = usuaris[i]
        snowdrift.partida = partida_activa
        game_snowdrift.append(snowdrift)
        snowdrift.save()

    # Assignem un numero als participants de l'experiment
    random.shuffle(NUMS_JUGADOR)

    # Prisoner Dilemma - Llistat usuaris
    llista_snowdrift1 = [] # JUGADORES IGUALES


    for i in range(len(usuaris)):
        # Numero de jugador per cada usuari
        usuaris[i].num_jugador = NUMS_JUGADOR[i]

        # Cream les dades per cas Prisoner 1
        if partida_activa.classe == 'snowdrift1':
            if usuaris[i].is_robot:
                print 'is_robot'
                game_snowdrift[i].seleccio1 = random.choice(['P','G'])
            llista_snowdrift1.append(game_snowdrift[i])

        usuaris[i].save()

    #Fem les parelles al Prisoner
    if partida_activa.classe == 'snowdrift1':
        while llista_snowdrift1:
            rand1_snowdrift = pop_random(llista_snowdrift1)
            rand2_snowdrift = pop_random(llista_snowdrift1)
            rand1_snowdrift.rival1 = rand2_snowdrift.user
            rand2_snowdrift.rival1 = rand1_snowdrift.user
            rand1_snowdrift.save()
            rand2_snowdrift.save()

    partida_activa.estat = "JUGANT"
    partida_activa.data_inicialitzacio = timezone.now()
    partida_activa.save()


######################################################################################
################################### DICTATOR 1 #######################################
######################################################################################

@csrf_exempt
def joc_dictator1_(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    # Update the user information
    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    user_dictator = Dictator.objects.get(user=user.id, partida=user.partida_current)
    user_dictator_rival = Dictator.objects.get(user=user_dictator.rival1.id, partida=user.partida_current)

    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_dictator.seleccio1 >=0 and user_dictator_rival.seleccio1  >=0:
            return redirect('user.final_joc')
        else:
            return redirect('user.logout')

    user.status = "Playing-Fuits"
    user.session_game = request.session['game']
    user.save()

    #Todo: Afegir el numero de llesques de manera automatica
    return render_to_response('joc_dictator1_.html', {'lang': request.session['lang'],
                                                      'text': request.session['text'],
                                                      'user': request.session['user']},
                              context_instance=RequestContext(request))

######################################################################################
################################### DICTATOR 2 #######################################
######################################################################################

@csrf_exempt
def joc_dictator2_(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    # Update the user information
    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    user_dictator = Dictator.objects.get(user=user.id, partida=user.partida_current)
    user_dictator_rival = Dictator.objects.get(user=user_dictator.rival1.id, partida=user.partida_current)

    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_dictator.seleccio1 >=0 and user_dictator_rival.seleccio1  >=0:
            return redirect('user.final_joc')
        else:
            return redirect('user.logout')

    user.status = "Playing-X"
    user.session_game = request.session['game']
    user.save()

    return render_to_response('joc_dictator2_.html', {'lang': request.session['lang'],
                                                      'text': request.session['text'],
                                                      'user': request.session['user']},
                              context_instance=RequestContext(request))

######################################################################################
################################### PRISONER 1 #######################################
######################################################################################

@csrf_exempt
def joc_prisoner1_1(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner1_2')
        else:
            return redirect('user.logout')

    user.status = "Playing-Water-1"
    user.session_game = request.session['game']
    user.save()


    return render_to_response('joc_prisoner1_1.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'matrix': MATRIX1},
                              context_instance=RequestContext(request))

@csrf_exempt
def joc_prisoner1_2(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner1_3')
        else:
            return redirect('user.logout')

    user.status = "Playing-Water-2"
    user.session_game = request.session['game']
    user.save()

    return render_to_response('joc_prisoner1_2.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'matrix': MATRIX1},
                              context_instance=RequestContext(request))

@csrf_exempt
def joc_prisoner1_3(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.final_joc')
        else:
            return redirect('user.logout')

    user.status = "Playing-Water-3"
    user.session_game = request.session['game']
    user.save()

    return render_to_response('joc_prisoner1_3.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'matrix': MATRIX1},
                              context_instance=RequestContext(request))

######################################################################################
################################### PRISONER 2 #######################################
######################################################################################

@csrf_exempt
def joc_prisoner2_1(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        request.session['user_prisoner'] = user_prisoner

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.joc_prisoner2_2')
        else:
            return redirect('user.logout')

    user.status = "Playing-Bread-1"
    user.session_game = request.session['game']
    user.save()

    return render_to_response('joc_prisoner2_1.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'user_prisoner': request.session['user_prisoner'],
                                                       'matrix': MATRIX2},
                              context_instance=RequestContext(request))

@csrf_exempt
def joc_prisoner2_2(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        request.session['user_prisoner'] = user_prisoner

    except Exception as e:
        return redirect('user.logout')

    #Comprovam que els dos jugadores han fet la darrera seleccio i les enviam al final joc
    user_prisoner_rival = Prisoner.objects.get(user=user_prisoner.rival1.id, partida=user.partida_current)


    if user_prisoner.seleccio1 != "" and user_prisoner_rival.seleccio1 != "":
        user.partida_current.estat = 'ACABADA'
        user.partida_current.save()
        return redirect('user.final_joc')


    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.final_joc')
        else:
            return redirect('user.logout')

    user.status = "Playing-Bread-2"
    user.session_game = request.session['game']
    user.save()

    return render_to_response('joc_prisoner2_2.html', {'lang': request.session['lang'],
                                                             'text': request.session['text'],
                                                             'user': request.session['user'],
                                                             'user_prisoner': request.session['user_prisoner'],
                                                             'matrix': MATRIX2,
                                                             'tirada': request.session['tirada']},
                          context_instance=RequestContext(request))


@csrf_exempt
def joc_prisoner2_3(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        request.session['user_prisoner'] = user_prisoner

    except Exception as e:
        return redirect('user.logout')


    #Check if he has played this game
    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_prisoner.seleccio1 != "":
            return redirect('user.final_joc')
        else:
            return redirect('user.logout')

    request.session['matrix'] = MATRIX2

    user.status = "Playing-Bread-3"
    user.session_game = request.session['game']
    user.save()

    return render_to_response('joc_prisoner2_3.html', {'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'user': request.session['user'],
                                                 'user_prisoner': request.session['user_prisoner'],
                                                 'matrix': MATRIX2},
                              context_instance=RequestContext(request))

######################################################################################
################################### SNOWDRIFT 1 #######################################
######################################################################################

@csrf_exempt
def joc_snowdrift1_(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    # Update the user information
    try:
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user

    except Exception as e:
        return redirect('user.logout')

    #Check if he has played this game
    user_snowdrift = Snowdrift.objects.get(user=user.id, partida=user.partida_current)
    user_snowdrift_rival = Snowdrift.objects.get(user=user_snowdrift.rival1.id, partida=user.partida_current)

    if user.partida_current.estat == 'ACABADA' or user.partida_current.estat == 'ACABADA_MANUAL':
        if user_snowdrift.seleccio1 >=0 and user_snowdrift_rival.seleccio1  >=0:
            return redirect('user.final_joc')
        else:
            return redirect('user.logout')

    user.status = "Playing-Kiss"
    user.session_game = request.session['game']
    user.save()

    return render_to_response('joc_snowdrift1_.html', {'lang': request.session['lang'],
                                                       'text': request.session['text'],
                                                       'user': request.session['user'],
                                                       'matrix': MATRIX3},
                              context_instance=RequestContext(request))

######################################################################################
####################################### FINAL JOC ####################################
######################################################################################

@csrf_exempt
def final_joc(request, **kwargs):

    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        request.session['user'] = user
    except Exception as e:
        return redirect('user.logout')

    # TANCA LA PARTIDA

    # Miramos si los dos usuarios de la partida han finalizado la sesion


    if request.session['game'] == "prisoner1":user.data_finalitzacio_prisoner1 = timezone.now()
    if request.session['game'] == "prisoner2":user.data_finalitzacio_prisoner2 = timezone.now()
    if request.session['game'] == "dictator1":user.data_finalitzacio_dictator1 = timezone.now()
    if request.session['game'] == "snowdrift1":user.data_finalitzacio_snowdrift1 = timezone.now()

    user.data_last_action = timezone.now()

    user.status = "Finishing"
    user.session_game = request.session['game']
    user.save()

    user.save()

    # Agafam els usuaris
    if request.session['game'] == "prisoner1": usuaris = User.objects.filter(partida_prisoner1=user.partida_current)
    if request.session['game'] == "prisoner2": usuaris = User.objects.filter(partida_prisoner2=user.partida_current)
    if request.session['game'] == "dictator1": usuaris = User.objects.filter(partida_dictator1=user.partida_current)
    if request.session['game'] == "snowdrift1": usuaris = User.objects.filter(partida_snowdrift1=user.partida_current)

    num_usuaris_acabats = 0

    print "usuaria a la partida: " +str(len(usuaris))
    for u in usuaris:
        if request.session['game'] == "prisoner1" and u.data_finalitzacio_prisoner1:
            num_usuaris_acabats = num_usuaris_acabats + 1
        if request.session['game'] == "prisoner2" and u.data_finalitzacio_prisoner2:
            num_usuaris_acabats = num_usuaris_acabats + 1
        if request.session['game'] == "dictator1" and u.data_finalitzacio_dictator1:
            num_usuaris_acabats = num_usuaris_acabats + 1
        if request.session['game'] == "snowdrift1" and u.data_finalitzacio_snowdrift1:
            num_usuaris_acabats = num_usuaris_acabats + 1

    print 'numero de usuaris: '+ str(num_usuaris_acabats)
    if num_usuaris_acabats == 2:
        user.partida_current.data_finalitzacio = timezone.now()
        user.partida_current.estat = "ACABADA"
        user.partida_current.save()

    user.partida_current = None

    user.status = ""
    user.session_game = ""
    user.save()

    user.save()

    #del request.session['user']
    #del request.session['game']

    resultats = [user.diners_prisoner1, user.diners_prisoner2, user.diners_snowdrift1, user.diners_dictator1]

    finalitzats = []

    if user.data_finalitzacio_prisoner1:finalitzats.append(1)
    else: finalitzats.append(0)

    if user.data_finalitzacio_prisoner2:finalitzats.append(1)
    else: finalitzats.append(0)

    if user.data_finalitzacio_snowdrift1:finalitzats.append(1)
    else: finalitzats.append(0)

    if user.data_finalitzacio_dictator1:finalitzats.append(1)
    else: finalitzats.append(0)




    return render_to_response('final_joc.html', {'lang': request.session['lang'],
                                                 'text': request.session['text'],
                                                 'max': [TOTAL_MAX1, TOTAL_MAX2, TOTAL_MAX3, TOTAL_MAX4],
                                                 'resultats': resultats,
                                                 'finalitzats': finalitzats,
                                                 'vals': 0,
                                                 'nickname': user.nickname,
                                                 },
                              context_instance=RequestContext(request))