from django.views.decorators.csrf import csrf_exempt

from game.models import *
from game.vars import *
import math

from django.shortcuts import redirect


import datetime
from django.utils import timezone

import json
from django.http import HttpResponse


import random
random.seed(datetime.datetime.now())

@csrf_exempt
def enviar_joc(request, **kwargs):

    id_joc = kwargs.get('id_joc', None)

    if(id_joc == "01"): nom_joc = "prisoner1"
    if(id_joc == "02"): nom_joc = "prisoner2"
    if(id_joc == "03"): nom_joc = "snowdrift1"
    if(id_joc == "04"): nom_joc = "dictator1"

    print 'tipus de joc: '+ nom_joc

    response_data={}
    # Gaurdam la variable a la sessio
    request.session['game'] = nom_joc
    # Gaurdam la variable a la base de dades
    game = Game()
    game.name = nom_joc
    game.timestamp = timezone.now()

    game.save()

    response_data['joc_saved'] = "Ok"

    return HttpResponse(json.dumps(response_data),content_type="application/json")


@csrf_exempt
def demanar_dades(request, **kwargs):
    #ToDo L'usuari que espera esta aqui demanant dades
    user_id = kwargs.get('user_id', None)

    response_data={}
    jugant = "false"

    user = None
    try:
        # partida que juga aquest usuari
        user = User.objects.get(id=user_id)
    except:
        print "Usuari "+str(user_id)+" no existeix"

    if user.partida_current is None:
        response_data["jugant"] = "false"
        response_data["error"] = "GAME DOES NOT EXIST"
        return HttpResponse(json.dumps(response_data),content_type="application/json")


    #ToDO: Aixo ho tenim que fer per cada un del tipos de partides
    if user.partida_current.estat == "JUGANT":
        jugant = "true"

    response_data["jugant"] = jugant
    return HttpResponse(json.dumps(response_data),content_type="application/json")

###############################################################################################
#################################### DICTATOR 1 ###############################################
###############################################################################################

@csrf_exempt
def enviar_accio_dictator1_(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_dictator = Dictator.objects.get(user=user_id, partida=user.partida_current)

        if int(result)>=0 and int(result)<=10 :
            if user_dictator.seleccio1 < 0:
                user_dictator.seleccio1 = result
                user_dictator.is_robot1 = False
                user_dictator.data_seleccio1 = timezone.now()
                user_dictator.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def demanar_resultat_dictator1_(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"correcte": False,
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_dictator = Dictator.objects.get(user=user_id, partida=user.partida_current)
        user_dictator_rival = Dictator.objects.get(user=user_dictator.rival1.id, partida=user.partida_current)

        if user_dictator_rival.seleccio1 < 0:
            # El rival encara no ha respos
            response_data = {"correcte": False}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            # Actualitzem els calculs dels diners i ho guardem
            # Seleccions
            diners_dictator_seleccio = int(user_dictator.seleccio1)
            diners_dictador_rival_seleccio = int(user_dictator_rival.seleccio1)
            # Restes
            diners_dictator_resta = DINERS_DICTATOR1 - int(user_dictator.seleccio1)
            diners_dictator_rival_resta = DINERS_DICTATOR1 - int(user_dictator_rival.seleccio1)
            # Resultats

            resultat_dictator = diners_dictator_resta + diners_dictador_rival_seleccio
            resultat_dictator_rival = diners_dictator_rival_resta + diners_dictator_seleccio


            user_dictator.diners_guanyats1 = resultat_dictator
            user_dictator.save()

            user.diners_dictator1 = user_dictator.diners_guanyats1

            user.punts_totals = (float(user.diners_prisoner1)/float(TOTAL_MAX1))*100 + \
                                (float(user.diners_prisoner2)/float(TOTAL_MAX2))*100 + \
                                (float(user.diners_snowdrift1)/float(TOTAL_MAX3))*100 + \
                                (float(user.diners_dictator1)/float(TOTAL_MAX4))*100
            user.save()

            response_data = {"correcte": True,
                             "seleccio_dictator": diners_dictator_seleccio,
                             "resta_dictator": diners_dictator_resta,
                             "seleccio_dictator_rival": diners_dictador_rival_seleccio,
                             "resta_dictator_rival": diners_dictator_rival_resta,
                             "resultat_dictator": resultat_dictator,
                             "resultat_dictator_rival":resultat_dictator_rival,
                             "max_points": TOTAL_MAX4,}

    return HttpResponse(json.dumps(response_data), content_type="application/json")



###############################################################################################
#################################### DICTATOR 2 ###############################################
###############################################################################################

@csrf_exempt
def enviar_accio_dictator2_(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)


    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:
        user_dictator = Dictator.objects.get(user=user_id, partida=user.partida_current)

        if int(result)>=0 and int(result)<=10 :
            if user_dictator.seleccio1 < 0:
                user_dictator.seleccio1 = result
                user_dictator.is_robot1 = False
                user_dictator.data_seleccio1 = timezone.now()
                user_dictator.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def demanar_resultat_dictator2_(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    user = User.objects.get(id=user_id)


    if user.partida_current is None:
        response_data = {"correcte": False,
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_dictator = Dictator.objects.get(user=user_id, partida=user.partida_current)
        user_dictator_rival = Dictator.objects.get(user=user_dictator.rival1.id, partida=user.partida_current)

        if user_dictator_rival.seleccio1 < 0:
            # El rival encara no ha respos
            response_data = {"correcte": False}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            #ToDo Fer be les part que es queden, ara tenim que reparteixen 4 coses
            # Actualitzem els calculs dels diners i ho guardem
            # Seleccions
            diners_dictator_seleccio = int(user_dictator.seleccio1)
            diners_dictador_rival_seleccio = int(user_dictator_rival.seleccio1)
            # Restes
            diners_dictator_resta = DINERS_DICTATOR2 - int(user_dictator.seleccio1)
            diners_dictator_rival_resta = DINERS_DICTATOR2 - int(user_dictator_rival.seleccio1)
            # Resultats

            resultat_dictator = diners_dictator_resta + diners_dictador_rival_seleccio
            resultat_dictator_rival = diners_dictator_rival_resta + diners_dictator_seleccio


            user_dictator.diners_guanyats1 = resultat_dictator
            user_dictator.save()

            user.diners_dictator2 = user_dictator.diners_guanyats1

            user.punts_totals = (float(user.diners_prisoner1)/float(TOTAL_MAX1))*100 + \
                                (float(user.diners_prisoner2)/float(TOTAL_MAX2))*100 + \
                                (float(user.diners_snowdrift1)/float(TOTAL_MAX3))*100 + \
                                (float(user.diners_dictator1)/float(TOTAL_MAX4))*100
            user.save()

            response_data = {"correcte": True,
                             "seleccio_dictator": diners_dictator_seleccio,
                             "resta_dictator": diners_dictator_resta,
                             "seleccio_dictator_rival": diners_dictador_rival_seleccio,
                             "resta_dictator_rival": diners_dictator_rival_resta,
                             "resultat_dictator": resultat_dictator,
                             "resultat_dictator_rival":resultat_dictator_rival,}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

###############################################################################################
#################################### PRISONER 1 ###############################################
###############################################################################################

@csrf_exempt
def enviar_accio_prisoner1(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:
        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        user_prisoner_rival = Prisoner.objects.get(user=user_prisoner.rival1.id, partida=user.partida_current)

        if result=='C' or result=='D':
            if user_prisoner.seleccio1 == "":
                user_prisoner.seleccio1 = result
                user_prisoner.is_robot1 = False
                user_prisoner.data_seleccio1 = timezone.now()

                user_prisoner.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def enviar_accio_guess1(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        user_prisoner_rival = Prisoner.objects.get(user=user_prisoner.rival1.id, partida=user.partida_current)

        if result=='C' or result=='D':
            if user_prisoner.guess1 == "":
                user_prisoner.guess1 = result
                user_prisoner.data_guess1 = timezone.now()
                user_prisoner.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def demanar_resultat_prisoner1(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"correcte": False,
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        user_prisoner_rival = Prisoner.objects.get(user=user_prisoner.rival1.id, partida=user.partida_current)

        if user_prisoner_rival.seleccio1 == "":
            #L'oponent encara no ha respos
            response_data = {"correcte": False}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:

            #Calculem i guardem el premi
            resultat_premi = 0

            if user_prisoner.seleccio1 == "C":
                if user_prisoner_rival.seleccio1 == "C":
                    resultat_prisoner1 = MATRIX1[0][0]
                else:
                    resultat_prisoner1 = MATRIX1[1][0]
            else:
                if user_prisoner_rival.seleccio1 == "C":
                    resultat_prisoner1 = MATRIX1[2][0]
                else:
                    resultat_prisoner1 = MATRIX1[3][0]


            user_prisoner.diners_guanyats1 = resultat_prisoner1
            user_prisoner.save()

            user.diners_prisoner1 = user_prisoner.diners_guanyats1

            user.punts_totals = (float(user.diners_prisoner1)/float(TOTAL_MAX1))*100 + \
                                (float(user.diners_prisoner2)/float(TOTAL_MAX2))*100 + \
                                (float(user.diners_snowdrift1)/float(TOTAL_MAX3))*100 + \
                                (float(user.diners_dictator1)/float(TOTAL_MAX4))*100

            user.save()

            response_data = {"correcte": True,
                             "seleccio": user_prisoner.seleccio1,
                             "oponent": user_prisoner_rival.seleccio1,
                             "max_points": TOTAL_MAX1}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

###############################################################################################
#################################### PRISONER 2 ###############################################
###############################################################################################


@csrf_exempt
def enviar_accio_prisoner2(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:
        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

        if result=='C' or result=='D':
            if user_prisoner.seleccio1 == "":
                user_prisoner.seleccio1 = result
                user_prisoner.is_robot1 = False
                user_prisoner.data_seleccio1 = timezone.now()

                user_prisoner.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def enviar_accio_guess2(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)

        if result=='C' or result=='D':
            if user_prisoner.guess1 == "":
                user_prisoner.guess1 = result
                user_prisoner.data_guess1 = timezone.now()
                user_prisoner.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def demanar_resultat_prisoner2(request, **kwargs):
    user_id = kwargs.get('user_id', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"correcte": False,
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_prisoner = Prisoner.objects.get(user=user.id, partida=user.partida_current)
        user_prisoner_rival = Prisoner.objects.get(user=user_prisoner.rival1.id, partida=user.partida_current)

        if user_prisoner_rival.seleccio1 == "":
            #L'oponent encara no ha respos
            response_data = {"correcte": False}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:

            #Calculem i guardem el premi
            if user_prisoner.rol1 == 'A':
                if user_prisoner.seleccio1 == "C":
                    if user_prisoner_rival.seleccio1 == "C":
                        resultat_prisoner2 = MATRIX2[0][0]
                    else:
                        resultat_prisoner2 = MATRIX2[1][0]
                else:
                    if user_prisoner_rival.seleccio1 == "C":
                        resultat_prisoner2 = MATRIX2[2][0]
                    else:
                        resultat_prisoner2 = MATRIX2[3][0]
            else:
                if user_prisoner.seleccio1 == "C":
                    if user_prisoner_rival.seleccio1 == "C":
                        resultat_prisoner2 = MATRIX2[0][1]
                    else:
                        resultat_prisoner2 = MATRIX2[2][1]
                else:
                    if user_prisoner_rival.seleccio1 == "C":
                        resultat_prisoner2 = MATRIX2[1][1]
                    else:
                        resultat_prisoner2 = MATRIX2[3][1]

            user_prisoner.diners_guanyats1 = resultat_prisoner2
            user_prisoner.save()

            user.diners_prisoner2 = user_prisoner.diners_guanyats1

            user.punts_totals = (float(user.diners_prisoner1)/float(TOTAL_MAX1))*100 + \
                                (float(user.diners_prisoner2)/float(TOTAL_MAX2))*100 + \
                                (float(user.diners_snowdrift1)/float(TOTAL_MAX3))*100 + \
                                (float(user.diners_dictator1)/float(TOTAL_MAX4))*100

            user.save()

            response_data = {"correcte": True,
                             "seleccio": user_prisoner.seleccio1,
                             "oponent": user_prisoner_rival.seleccio1,
                             "max_points": TOTAL_MAX2}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


###############################################################################################
#################################### SNOWDRIFT 1 ###############################################
###############################################################################################

@csrf_exempt
def enviar_accio_snowdrift1_(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    result = kwargs.get('result', None)

    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"saved": "error",
                         "error": "GAME DOES NOT EXIST"}
    else:
        user_snowdrift = Snowdrift.objects.get(user=user_id, partida=user.partida_current)

        if result != "" :
            if user_snowdrift.seleccio1 == "":
                user_snowdrift.seleccio1 = result
                user_snowdrift.is_robot1 = False
                user_snowdrift.data_seleccio1 = timezone.now()
                user_snowdrift.save()

            response_data = {"saved": "ok"}
        else:
            response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def demanar_resultat_snowdrift1_(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    user = User.objects.get(id=user_id)

    if user.partida_current is None:
        response_data = {"correcte": False,
                         "error": "GAME DOES NOT EXIST"}
    else:

        user_snowdrift = Snowdrift.objects.get(user=user_id, partida=user.partida_current)
        user_snowdrift_rival = Snowdrift.objects.get(user=user_snowdrift.rival1.id, partida=user.partida_current)

        if user_snowdrift_rival.seleccio1 == "":
            # El rival encara no ha respos
            response_data = {"correcte": False}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            # Actualitzem els calculs dels diners i ho guardem
            # Seleccions

            if user_snowdrift.seleccio1 == 'P':
                if user_snowdrift_rival.seleccio1 == 'P':
                    user_snowdrift.diners_guanyats1 = MATRIX3[0][0]
                else:
                    user_snowdrift.diners_guanyats1 = MATRIX3[1][0]
            else:
                if user_snowdrift_rival.seleccio1 == 'P':
                    user_snowdrift.diners_guanyats1 = MATRIX3[2][0]
                else:
                    user_snowdrift.diners_guanyats1 = MATRIX3[3][0]


            user_snowdrift.save()

            user.diners_snowdrift1 = user_snowdrift.diners_guanyats1

            user.punts_totals = (float(user.diners_prisoner1)/float(TOTAL_MAX1))*100 + \
                                (float(user.diners_prisoner2)/float(TOTAL_MAX2))*100 + \
                                (float(user.diners_snowdrift1)/float(TOTAL_MAX3))*100 + \
                                (float(user.diners_dictator1)/float(TOTAL_MAX4))*100
            user.save()

            response_data = {"correcte": True,
                             "seleccio_snowdrift": user_snowdrift.seleccio1,
                             "seleccio_snowdrift_rival": user_snowdrift_rival.seleccio1,
                             "max_points": TOTAL_MAX3}

    return HttpResponse(json.dumps(response_data), content_type="application/json")



###############################################################################################
################         WEBSERVICES RESULTATS FINAL JOC      #################################
###############################################################################################

@csrf_exempt
def demanar_resultat_partida(request, **kwargs):
    print 'Demanar resultat Public Game'

@csrf_exempt
def tancar_partida(request, **kwargs):

    response_data = {}
    id = kwargs.get('num_partida', None)
    partida = Partida.objects.get(id=id)

    partida.estat = 'ACABADA_MANUAL'
    partida.data_finalitzacio = timezone.now()

    partida.save()

    users = User.objects.filter(partida_current=partida)

    for u in users:
        print u.id
        u.partida_current = None
        print u.partida_current
        #ToDo: fer que segons si ha selccionat o no pugui tornar a jugar i per tant eliminar la partida_id corresponent o no.
        #if partida.classe == "prisoner1":u.data_finalitzacio_prisoner1 = timezone.now()
        #if partida.classe == "prisoner2":u.data_finalitzacio_prisoner2 = timezone.now()
        #if partida.classe == "dictator1":u.data_finalitzacio_dictator1 = timezone.now()
        #if partida.classe == "dictator2":u.data_finalitzacio_dictator2 = timezone.now()
        #if partida.classe == "snowdrift1":u.data_finalitzacio_snowdrift1 = timezone.now()
        u.save()

    response_data["correcte"] = False
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def llistat_partides(request, **kwargs):

    response_data = {}

    all_partides = []
    for partida in Partida.objects.order_by('-id'):

        if partida.classe == "prisoner1":
            partida.classe ="Water"
            users = [u.id for u in User.objects.filter(partida_prisoner1=partida.id)]

        elif partida.classe == "prisoner2":
            partida.classe ="Bread"
            users = [u.id for u in User.objects.filter(partida_prisoner2=partida.id)]

        elif partida.classe == "snowdrift1":
            partida.classe ="Kiss"
            users = [u.id for u in User.objects.filter(partida_snowdrift1=partida.id)]

        elif partida.classe == "dictator1":
            partida.classe ="Fruits"
            users = [u.id for u in User.objects.filter(partida_dictator1=partida.id)]


        data_partida = {"id": partida.num_partida,
                        "data_creacio": partida.data_creacio.strftime("%a, %H:%M:%S") if partida.data_creacio else '-',
                        "data_inicialitzacion": partida.data_inicialitzacio.strftime("%a, %H:%M:%S") if partida.data_inicialitzacio else '-',
                        "data_finalitzacio": partida.data_finalitzacio.strftime("%a, %H:%M:%S") if partida.data_finalitzacio else '-',
                        "estat": partida.estat,
                        "classe": partida.classe,
                        "players": users,
        }
        all_partides.append(data_partida)
    response_data["partida"] = all_partides

    return HttpResponse(json.dumps(response_data), content_type="application/json")

###############################################################################################
###############################################################################################
################         WEBSERVICES ADMINISTRACIO      #######################################
###############################################################################################
###############################################################################################
@csrf_exempt
def usuaris_registrats(request, **kwargs):
    response_data = {}

    users = User.objects.filter(~models.Q(status=""))

    if len(users) > 0:
        response_data['users_actives'] = len(users)
        all_users = []
        logged_out_users = []

        for u in users:
                if u.session_game == "prisoner1": u.session_game="Water"
                elif u.session_game == "prisoner2": u.session_game="Bread"
                elif u.session_game == "snowdrift1": u.session_game="Kiss"
                elif u.session_game == "dictator1": u.session_game="Fruits"

                if u.partida_current:
                    if u.partida_current.classe == "prisoner1": u.partida_current.classe ="Water"
                    elif u.partida_current.classe == "prisoner2": u.partida_current.classe ="Bread"
                    elif u.partida_current.classe == "snowdrift1": u.partida_current.classe ="Kiss"
                    elif u.partida_current.classe == "dictator1": u.partida_current.classe ="Fruits"


                data_users = {
                    "uid": u.id,
                    "nickname": u.nickname,
                    "status": u.status,
                    "session": u.session_game,
                    "current_game": u.partida_current.id if u.partida_current else '-',
                    "current_game_classe": u.partida_current.classe if u.partida_current else '-',
                    "current_game_status": u.partida_current.estat if u.partida_current else '-',
                }

                if u.session_game:
                    if u.status == 'Logged-Out':
                        logged_out_users.append(data_users)
                    else:
                        all_users.append(data_users)

        response_data['users_actives'] = len(all_users)

        response_data['usuaris'] = all_users
        response_data['logged-out'] = logged_out_users
    else:
        response_data['users_actives'] = 0

    return HttpResponse(json.dumps(response_data), content_type="application/json")

###############################################################################################
###############################         PARTIDES      #########################################
###############################################################################################

@csrf_exempt
def estat_partida(request, **kwargs):
    response_data = {}

    pd1 = Partida.objects.filter(classe="prisoner1")
    pd2 = Partida.objects.filter(classe="prisoner2")
    dg1 = Partida.objects.filter(classe="dictator1")
    dg2 = Partida.objects.filter(classe="dictator2")
    sw1 = Partida.objects.filter(classe="snowdrift1")

    ##########
    # Darrera partida acabada
    ##########
    darrera_partida_acabada_pd1 = Partida.objects.filter(classe="prisoner1").filter(estat="ACABADA").order_by("data_finalitzacio").last()
    if darrera_partida_acabada_pd1 is None:
        response_data['darrera_partida_acabada_pd1'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(partida_prisoner1=darrera_partida_acabada_pd1.id)]
        partida = {'id': darrera_partida_acabada_pd1.id,
                   'classe': darrera_partida_acabada_pd1.classe,
                   'estat': darrera_partida_acabada_pd1.estat,
                   'dia': (darrera_partida_acabada_pd1.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if darrera_partida_acabada_pd1.data_creacio else '-',
                   'usuaris_registrats': darrera_partida_acabada_pd1.usuaris_registrats,
                   "data_finalitzacio": (darrera_partida_acabada_pd1.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['darrera_partida_acabada_pd1'] = partida

    darrera_partida_acabada_pd2 = Partida.objects.filter(classe="prisoner2").filter(estat="ACABADA").order_by("data_finalitzacio").last()
    if darrera_partida_acabada_pd2 is None:
        response_data['darrera_partida_acabada_pd2'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(partida_prisoner2=darrera_partida_acabada_pd2.id)]
        partida = {'id': darrera_partida_acabada_pd2.id,
                   'classe': darrera_partida_acabada_pd2.classe,
                   'estat': darrera_partida_acabada_pd2.estat,
                   'dia': (darrera_partida_acabada_pd2.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if darrera_partida_acabada_pd2.data_creacio else '-',
                   'usuaris_registrats': darrera_partida_acabada_pd2.usuaris_registrats,
                   "data_finalitzacio": (darrera_partida_acabada_pd2.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['darrera_partida_acabada_pd2'] = partida

    darrera_partida_acabada_dg1 = Partida.objects.filter(classe="dictator1").filter(estat="ACABADA").order_by("data_finalitzacio").last()
    if darrera_partida_acabada_dg1 is None:
        response_data['darrera_partida_acabada_dg1'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(partida_dictator1=darrera_partida_acabada_dg1.id)]
        partida = {'id': darrera_partida_acabada_dg1.id,
                   'classe': darrera_partida_acabada_dg1.classe,
                   'estat': darrera_partida_acabada_dg1.estat,
                   'dia': (darrera_partida_acabada_dg1.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if darrera_partida_acabada_dg1.data_creacio else '-',
                   'usuaris_registrats': darrera_partida_acabada_dg1.usuaris_registrats,
                   "data_finalitzacio": (darrera_partida_acabada_dg1.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['darrera_partida_acabada_dg1'] = partida

    darrera_partida_acabada_dg2 = Partida.objects.filter(classe="dictator2").filter(estat="ACABADA").order_by("data_finalitzacio").last()

    if darrera_partida_acabada_dg2 is None:
        response_data['darrera_partida_acabada_dg2'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(partida_dictator2=darrera_partida_acabada_dg2.id)]

        partida = {'id': darrera_partida_acabada_dg2.id,
                   'classe': darrera_partida_acabada_dg2.classe,
                   'estat': darrera_partida_acabada_dg2.estat,
                   'dia': (darrera_partida_acabada_dg2.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if darrera_partida_acabada_dg2.data_creacio else '-',
                   'usuaris_registrats': darrera_partida_acabada_dg2.usuaris_registrats,
                   "data_finalitzacio": (darrera_partida_acabada_dg2.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['darrera_partida_acabada_dg2'] = partida

    darrera_partida_acabada_sw1 = Partida.objects.filter(classe="snowdrift1").filter(estat="ACABADA").order_by("data_finalitzacio").last()

    if darrera_partida_acabada_sw1 is None:
        response_data['darrera_partida_acabada_sw1'] = {'error': 'no_games'}
    else:
        users = [u.id for u in User.objects.filter(partida_snowdrift1=darrera_partida_acabada_sw1.id)]

        partida = {'id': darrera_partida_acabada_sw1.id,
                   'classe': darrera_partida_acabada_sw1.classe,
                   'estat': darrera_partida_acabada_sw1.estat,
                   'dia': (darrera_partida_acabada_sw1.data_creacio + datetime.timedelta(hours=2)).strftime("%d/%m") if darrera_partida_acabada_sw1.data_creacio else '-',
                   'usuaris_registrats': darrera_partida_acabada_sw1.usuaris_registrats,
                   "data_finalitzacio": (darrera_partida_acabada_sw1.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S"),
                   'users': users}

        response_data['darrera_partida_acabada_sw1'] = partida

    #######
    ## Partides actives
    #######

    partides = []
    for p in pd1:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['partides_actives_pd1'] = partides

    partides = []
    for p in pd2:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['partides_actives_pd2'] = partides

    partides = []
    for p in dg1:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['partides_actives_dg1'] = partides

    partides = []
    for p in dg2:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['partides_actives_dg2'] = partides

    partides = []
    for p in sw1:
        if p.estat != "ACABADA" and p.estat !='ACABADA_MANUAL':
            users = [u.id for u in User.objects.filter(partida_current=p.id)]
            partida = {'id': p.id,
               'classe': p.classe,
               'estat': p.estat,
               'usuaris_registrats': p.usuaris_registrats,
               'dia': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%d") if p.data_creacio else '-',
               'data_creacio': (p.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_creacio else '-',
               'data_inicialitzacio': (p.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_inicialitzacio else '-',
               'data_finalitzacio': (p.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if p.data_finalitzacio else '-',
               'users': users}
            partides.append(partida)
    response_data['partides_actives_sw1'] = partides



    return HttpResponse(json.dumps(response_data), content_type="application/json")

###############################################################################################
##################################         USERS      #########################################
###############################################################################################

@csrf_exempt
def estat_users(request, **kwargs):
    response_data = {}

    users_con_partida_activa = User.objects.filter(~models.Q(partida_current = None)).order_by('partida_current')
    users = []
    for u in users_con_partida_activa:
        jugades = []
        no_jugades = []

        if u.data_finalitzacio_dictator1:
            jugades.append('Water')
        else:
            no_jugades.append('Water')

        if u.data_finalitzacio_dictator2:
            jugades.append(' Bread')
        else:
            no_jugades.append(' Bread')

        if u.data_finalitzacio_snowdrift1:
            jugades.append(' Kiss')
        else:
            no_jugades.append(' Kiss')

        if u.data_finalitzacio_prisoner1:
            jugades.append(' Fruits')
        else:
            no_jugades.append(' Fruits')

        if u.session_game == "prisoner1": u.session_game="Water"
        elif u.session_game == "prisoner2": u.session_game="Bread"
        elif u.session_game == "snowdrift1": u.session_game="Kiss"
        elif u.session_game == "dictator1": u.session_game="Fruits"

        if u.partida_current.classe == "prisoner1": u.partida_current.classe ="Water"
        elif u.partida_current.classe == "prisoner2": u.partida_current.classe ="Bread"
        elif u.partida_current.classe == "snowdrift1": u.partida_current.classe ="Kiss"
        elif u.partida_current.classe == "dictator1": u.partida_current.classe ="Fruits"

        user = {'id': u.id,
                'estat_user': u.status,
                'session_game': u.session_game,
                'partida': u.partida_current.id,
                'classe': u.partida_current.classe,
                'estat': u.partida_current.estat,
                'jugades': jugades,
                'no_jugades': no_jugades}
        users.append(user)
    response_data['users'] = users


    users_all = User.objects.order_by('-data_last_action')
    users_all_array = []

    for u in users_all:

        if u.session_game == "prisoner1": u.session_game="Water"
        elif u.session_game == "prisoner2": u.session_game="Bread"
        elif u.session_game == "snowdrift1": u.session_game="Kiss"
        elif u.session_game == "dictator1": u.session_game="Fruits"


        # Partida activa
        if u.partida_current:
            partida_activa = u.partida_current.id
            estat = u.partida_current.estat
        else:
            partida_activa = '-'
            estat = 'INACTIVE'

        # Jocs registrats
        jr_count = 0
        if u.data_registre_dictator1: jr_count += 1
        if u.data_registre_dictator2: jr_count += 1
        if u.data_registre_prisoner1:jr_count += 1
        if u.data_registre_prisoner2: jr_count += 1
        if u.data_registre_snowdrift1: jr_count += 1

        # Jocs finalitzats
        jf_count = 0
        if u.data_finalitzacio_dictator1: jf_count += 1
        if u.data_finalitzacio_dictator2: jf_count += 1
        if u.data_finalitzacio_prisoner1:jf_count += 1
        if u.data_finalitzacio_prisoner2: jf_count += 1
        if u.data_finalitzacio_snowdrift1: jf_count += 1

        # Diners guanyats
        if u.partida_prisoner1: pr1 = str(u.partida_prisoner1.id)+' ('+str(int(u.diners_prisoner1))+')'
        else: pr1='-'
        if u.partida_prisoner2: pr2 = str(u.partida_prisoner2.id)+' ('+str(int(u.diners_prisoner2))+')'
        else: pr2='-'
        if u.partida_dictator1: dg1 = str(u.partida_dictator1.id)+' ('+str(int(u.diners_dictator1))+')'
        else: dg1='-'
        if u.partida_dictator2: dg2 = str(u.partida_dictator2.id)+' ('+str(int(u.diners_dictator2))+')'
        else: dg2='-'
        if u.partida_snowdrift1: sw1 = str(u.partida_snowdrift1.id)+' ('+str(int(u.diners_snowdrift1))+')'
        else: sw1='-'

        #Diners totals
        if u.punts_totals: total = u.punts_totals
        else: total = '-'

        user = {'id': u.id,
                'name': u.nickname,
                'estat_user': u.status,
                'session_game': u.session_game,
                'estat': estat,
                'partida_activa': partida_activa,
                'jocs_registrats': jr_count,
                'jocs_finalitzats': jf_count,
                'pr1': pr1,
                'pr2': pr2,
                'dg1': dg1,
                'dg2': dg2,
                'sw1': sw1,
                'total': u.punts_totals
                }
        users_all_array.append(user)
    response_data['users_all'] = users_all_array

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def stats_partida(request, **kwargs):
    print 'Stats'

@csrf_exempt
def stats_partida_detail(request, **kwargs):

    id = kwargs.get('num_partida', None)

    partida = Partida.objects.filter(id=id)[0]


    users = []
    if partida.classe == 'prisoner1':
        users = User.objects.filter(partida_prisoner1=partida)

    if partida.classe == 'prisoner2':
        users = User.objects.filter(partida_prisoner2=partida)

    if partida.classe == 'dictator1':
        users = User.objects.filter(partida_dictator1=partida)

    if partida.classe == 'dictator2':
        users = User.objects.filter(partida_dictator2=partida)

    if partida.classe == 'snowdrift1':
        users = User.objects.filter(partida_snowdrift1=partida)

    error = ""
    if partida.estat == 'ACABADA' or partida.estat == 'ACABADA_MANUAL':
        if partida.data_creacio is None:
            error = error + 'ERROR 301: La partida no sha creat.'
            error = error + '\n'
        if partida.data_inicialitzacio is None:
            error = error + 'ERROR 302: La partida no sha iniciat.'
            error = error + '\n'
        if partida.data_finalitzacio is None:
            error = error + 'ERROR 303: La partida no sha acabat.'
            error = error + '\n'
    elif partida.estat == 'REGISTRANT':
        if partida.usuaris_registrats == 0:
            error = error + 'ERROR 304: No hi ha cap usuari a la partida'
            error = error + '\n'
        if partida.usuaris_registrats == 2:
            error = error + 'ERROR 305: La partida tendria que estar jugant-se'
            error = error + '\n'
    elif partida.estat == 'JUGANT':
        if partida.usuaris_registrats == 0:
            error = error + 'ERROR 306: No hi ha jugadors a la partida'
            error = error + '\n'
        if partida.usuaris_registrats == 1:
            error = error + 'ERROR 307: Falta un jugador a la partida'
            error = error + '\n'

    print error

    response_data = {
        "id": partida.id,
        "num_partida": partida.num_partida,
        "creacio": (partida.data_creacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if partida.data_creacio else '-',
        "inici": (partida.data_inicialitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if partida.data_inicialitzacio else '-',
        "fin": (partida.data_finalitzacio + datetime.timedelta(hours=2)).strftime("%a, %H:%M:%S") if partida.data_finalitzacio else '-',
        "estat": partida.estat,
        "classe": partida.classe,
        "users": [u.id for u in users] if len(users) > 0 else '-',
        "error": error
    }


    return HttpResponse(json.dumps(response_data), content_type="application/json")


###############################################################################################
##################################         ANALYSIS      ######################################
###############################################################################################

@csrf_exempt
def basic_analysis(request, **kwargs):
    participants = User.objects.filter()
    prisoners = Prisoner.objects.filter()
    snowdrift = Snowdrift.objects.filter()
    dictator = Dictator.objects.filter()

    participants_from_tarrega = [p for p in participants if p.on_vius == 'r1']
    participants_from_outside_tarrega = [p for p in participants if p.on_vius == 'r2']


    response_participants = {
        "number_of_participants": len(participants) if participants else 0,
        "number_of_participants_from_tarrega" : len(participants_from_tarrega) if participants_from_tarrega else 0,
        "number_of_participants_from_outside_tarrega" : len(participants_from_outside_tarrega) if participants_from_outside_tarrega else 0,
    }

    participants_bot_right_to_water = [p for p in participants if p.bot_pr1_prisoner1 == 'Y']
    participants_bot_not_right_to_water = [p for p in participants if p.bot_pr1_prisoner1 == 'N']
    participants_worried_about_water = [p for p in participants if p.interest_prisoner1 == 'Y']
    participants_not_worried_about_water = [p for p in participants if p.interest_prisoner1 == 'N']


    c_exp_water = [p for p in prisoners if p.partida.classe == 'prisoner1' and p.guess1 == 'C']
    d_exp_water = [p for p in prisoners if p.partida.classe == 'prisoner1' and p.guess1 == 'D']
    c_water = [p for p in prisoners if p.partida.classe == 'prisoner1' and p.seleccio1 == 'C']
    d_water = [p for p in prisoners if p.partida.classe == 'prisoner1' and p.seleccio1 == 'D']


    response_water = {
        "right_to_water": len(participants_bot_right_to_water) if participants_bot_right_to_water else 0,
        "not_right_to_water": len(participants_bot_not_right_to_water) if participants_bot_not_right_to_water else 0,
        "worried_about_water": len(participants_worried_about_water) if participants_worried_about_water else 0,
        "not_worried_about_water": len(participants_not_worried_about_water) if participants_not_worried_about_water else 0,
        "cooperation_expected_water" : len(c_exp_water) if c_exp_water else 0,
        "defection_expected_water" : len(d_exp_water) if d_exp_water else 0,
        "cooperation_water" : len(c_water) if c_water else 0,
        "defection_water" : len(d_water) if d_water else 0,
    }

    participants_bot_cook_is_love = [p for p in participants if p.bot_pr1_prisoner2 == 'Y']
    participants_bot_cook_is_not_love = [p for p in participants if p.bot_pr1_prisoner2 == 'N']
    participants_staring_eyes = [p for p in participants if p.feeling_prisoner2 == 'Y']
    participants_not_staring_eyes = [p for p in participants if p.feeling_prisoner2 == 'N']
    participants_worried_about_food = [p for p in participants if p.interest_prisoner2 == 'Y']
    participants_not_worried_about_food = [p for p in participants if p.interest_prisoner2 == 'N']
    
    c_exp_food = [p for p in prisoners if p.partida.classe == 'prisoner2' and p.guess1 == 'C']
    d_exp_food = [p for p in prisoners if p.partida.classe == 'prisoner2' and p.guess1 == 'D']
    c_food = [p for p in prisoners if p.partida.classe == 'prisoner2' and p.seleccio1 == 'C']
    d_food = [p for p in prisoners if p.partida.classe == 'prisoner2' and p.seleccio1 == 'D']

    response_food = {
        "staring_eyes": len(participants_staring_eyes) if participants_staring_eyes else 0,
        "not_staring_eyes": len(participants_not_staring_eyes) if participants_not_staring_eyes else 0,
        "cook_is_love": len(participants_bot_cook_is_love) if participants_bot_cook_is_love else 0,
        "cook_is_not_love": len(participants_bot_cook_is_not_love) if participants_bot_cook_is_not_love else 0,
        "worried_about_food": len(participants_worried_about_food) if participants_worried_about_food else 0,
        "not_worried_about_food": len(participants_not_worried_about_food) if participants_not_worried_about_food else 0,
        "cooperation_expected_food" : len(c_exp_food) if c_exp_food else 0,
        "defection_expected_food" : len(d_exp_food) if d_exp_food else 0,
        "cooperation_food" : len(c_food) if c_food else 0,
        "defection_food" : len(d_food) if d_food else 0,
    }

    participants_bot_take_care = [p for p in participants if p.bot_pr1_snowdrift1 == 'Y']
    participants_bot_not_take_care = [p for p in participants if p.bot_pr1_snowdrift1 == 'N']

    kiss = [p for p in snowdrift if p.partida.classe == 'snowdrift1' and p.seleccio1 == 'P']
    cheek = [p for p in snowdrift if p.partida.classe == 'snowdrift1' and p.seleccio1 == 'G']


    response_kiss = {
        "take_care": len(participants_bot_take_care) if participants_bot_take_care else 0,
        "not_take_care": len(participants_bot_not_take_care) if participants_bot_not_take_care else 0,
        "kiss": len(kiss) if kiss else 0,
        "cheek": len(cheek) if cheek else 0,
    }

    give_all = [p for p in dictator if p.partida.classe == 'dictator1' and p.seleccio1 == 2]
    split = [p for p in dictator if p.partida.classe == 'dictator1' and p.seleccio1 == 1]
    give_nothing = [p for p in dictator if p.partida.classe == 'dictator1' and p.seleccio1 == 0]

    participants_bot_homeless = [p for p in participants if p.bot_pr1_dictator1 == 'Y']
    participants_bot_not_homeless= [p for p in participants if p.bot_pr1_dictator1 == 'N']
    participants_want_fruit = [p for p in participants if p.interest_dictator1 == 'Y']
    participants_not_want_fruit = [p for p in participants if p.interest_dictator1 == 'N']



    response_fruit = {
        "give_all": len(give_all) if give_all else 0,
        "splits": len(split) if split else 0,
        "give_nothing": len(give_nothing) if give_nothing else 0,
        "homeless": len(participants_bot_homeless) if participants_bot_homeless else 0,
        "not_homeless": len(participants_bot_not_homeless) if participants_bot_not_homeless else 0,
        "want_fruit": len(participants_want_fruit) if participants_want_fruit else 0,
        "not_want_fruit": len(participants_not_want_fruit) if participants_not_want_fruit else 0,
    }

    response_data = {
        "participants": response_participants,
        "water": response_water,
        "food": response_food,
        "kiss": response_kiss,
        "fruit": response_fruit,
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


