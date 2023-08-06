from PLManfred.audio import *
import os
import playsound
from PLManfred.say import  *
from PLManfred.logo import *
from PLManfred.czy import *
from PLManfred.pogoda import *
from PLManfred.skript import *

def Manfred():
    logo()
    say("Witaj, Jestem Manfred")
    while True:
        print(" ")
        audio = get_audio()
        if audio != None:
            if len(czy(audio, KLUCZ_COMMAND)): #klucz
                if len(czy(audio, zart)): #żart
                    lossay(zartycommand)








#############################komendy############################################
KLUCZ_COMMAND = ["ok", "manfred", "bot", "okej", "żulu",  "manfredi"]


#############################żarty##############################################

zartycommand = ["nauczyciel języka polskiego pyta się uczniów jak brzmi liczba mnoga do rzeczownika niedziela? Wakacje proszę pani", "Jak się nazywa lekarz, który leczy pandy? Pandoktor", "Dlaczego duchy nie kłamią? Bo wiedzą, że możesz je przejrzeć na wylot", " koniec roku szkolnego. tato, ty to masz szczęście do pieniędzy, Dlaczego? nie  musisz kupować książek na przyszły rok zostaje w tej samej klasie", "panie doktoże wczyscy mnie ignowują. Następny proczę"]
zart = ["żart"]
