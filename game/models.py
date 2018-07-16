from django.db import models


class AdminUser(models.Model):
    email = models.CharField(max_length=300)
    passwd = models.CharField(max_length=300) # guardar md5

class Game(models.Model):
    name = models.CharField(max_length=10)
    timestamp = models.DateTimeField(null=True)

class Partida(models.Model):
    num_partida = models.IntegerField()
    data_creacio = models.DateTimeField()
    data_inicialitzacio = models.DateTimeField(null=True)
    data_finalitzacio = models.DateTimeField(null=True)
    estat = models.CharField(max_length=20, default="INACTIVA") # INACTIVA, REGISTRANT, COMPLETA, ENJOC, ACABADA
    classe = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides
    usuaris_registrats = models.IntegerField(default=0)
    comentari = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides



class User(models.Model):
    is_robot = models.BooleanField(default=False)
    check1 = models.BooleanField(default=False)

    # Enquesta inicial
    nickname = models.CharField(max_length=100, default="")
    on_vius = models.CharField(max_length=6, default="")
    genere = models.CharField(max_length=1, default="")
    rang_edat = models.CharField(max_length=100, default="")

    interest_prisoner1 = models.CharField(max_length=100, default="")
    interest_prisoner2 = models.CharField(max_length=100, default="")
    interest_dictator1 = models.CharField(max_length=100, default="")
    interest_dictator2 = models.CharField(max_length=100, default="")

    feeling_prisoner2 = models.CharField(max_length=100, default="")

    bot_pr1_prisoner1 = models.CharField(max_length=100, default="")
    bot_pr1_prisoner2 = models.CharField(max_length=100, default="")
    bot_pr1_dictator1 = models.CharField(max_length=100, default="")
    bot_pr1_snowdrift1 = models.CharField(max_length=100, default="")

    ####################

    num_jugador = models.IntegerField(null=True)

    data_creacio = models.DateTimeField()

    acabat = models.BooleanField(default=False)

    status = models.CharField(max_length=100, default="")
    session_game = models.CharField(max_length=100, default="")

    num_seleccions = models.IntegerField(default=0)
    guany_final = models.IntegerField(default=0)

    # Partides
    partida_prisoner1 = models.ForeignKey(Partida, null=True, related_name='prisoner1') #aigua
    partida_prisoner2 = models.ForeignKey(Partida, null=True, related_name='prisoner2') #vi
    partida_dictator1 = models.ForeignKey(Partida, null=True, related_name='dictator1') #pa
    partida_dictator2 = models.ForeignKey(Partida, null=True, related_name='dictator2') #fruita
    partida_snowdrift1 = models.ForeignKey(Partida, null=True, related_name='snowdrift1') #peto

    # Registre
    data_registre_prisoner1 = models.DateTimeField(null=True)
    data_registre_prisoner2 = models.DateTimeField(null=True)
    data_registre_dictator1 = models.DateTimeField(null=True)
    data_registre_dictator2 = models.DateTimeField(null=True)
    data_registre_snowdrift1 = models.DateTimeField(null=True)

    # Finalitzacio
    data_finalitzacio_prisoner1 = models.DateTimeField(null=True)
    data_finalitzacio_prisoner2 = models.DateTimeField(null=True)
    data_finalitzacio_dictator1 = models.DateTimeField(null=True)
    data_finalitzacio_dictator2 = models.DateTimeField(null=True)
    data_finalitzacio_snowdrift1 = models.DateTimeField(null=True)

    data_last_action = models.DateTimeField(null=True) # last register and ended


    # partida actual que esta jugant
    partida_current =  models.ForeignKey(Partida, null=True, related_name='current')

    #Variables diners
    diners_prisoner1 = models.FloatField(default=0)
    diners_prisoner2 = models.FloatField(default=0)
    diners_dictator1 = models.FloatField(default=0)
    diners_dictator2 = models.FloatField(default=0)
    diners_snowdrift1 = models.FloatField(default=0)

    punts_totals = models.FloatField(default=0)

class Dictator(models.Model):
    user = models.ForeignKey(User)

    # Primera tirada
    rival1 = models.ForeignKey(User,null=True,blank=True, related_name='rival_dictator1')
    rol1 = models.CharField(max_length=100)
    seleccio1 = models.FloatField(default=-1)
    is_robot1 = models.BooleanField(default=True)
    data_seleccio1 = models.DateTimeField(null=True)
    diners_guanyats1 = models.FloatField(default=0)

    partida = models.ForeignKey(Partida, null=True)

class Prisoner(models.Model):
    user = models.ForeignKey(User)

    # Primera tirada
    rival1 = models.ForeignKey(User,null=True,blank=True, related_name='rival_prisoner1')
    guess1 = models.CharField(max_length=1, default="")
    rol1 = models.CharField(max_length=100, default="") # ADVANTAGE OR DISVANTAGE
    seleccio1 = models.CharField(max_length=1, default="")
    is_robot1 = models.BooleanField(default=True)
    data_seleccio1 = models.DateTimeField(null=True)
    data_guess1 = models.DateTimeField(null=True)
    diners_guanyats1 = models.FloatField(default=0)

    partida = models.ForeignKey(Partida, null=True)

class Snowdrift(models.Model):
    user = models.ForeignKey(User)

    rival1 = models.ForeignKey(User,null=True,blank=True, related_name='rival_snowdrift1')
    seleccio1 = models.CharField(max_length=1, default="")
    is_robot1 = models.BooleanField(default=True)
    data_seleccio1 = models.DateTimeField(null=True)
    diners_guanyats1 = models.FloatField(default=0)

    partida = models.ForeignKey(Partida, null=True)




