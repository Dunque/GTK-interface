import urllib.request
import urllib.error
import json
import vista
import random
import gettext

_ = gettext.gettext
N_ = gettext.ngettext

# list of tuples for each software, containing the software name, initial release, and main programming languages used
class Modelo:

    def __init__(self):

        self.lista_intervalos = []
        self.notas = [_('Do'), _('Do♯/Re♭'), _('Re'), _('Re♯/Mi♭'), _('Mi'), _('Fa'), _('Fa♯/Sol♭'), _('Sol'), _('Sol♯/La♭'), _('La'), _('La♯/Si♭'), _('Si')]

    #Hace una request al servidor y obtiene la lista de intervalos, y la guarda en su atributo "lista_intervalos"
    def obtener_intervalos(self):
        try:
            intervals_request = urllib.request.urlopen('http://localhost:5000/intervals')
            intervals_read = intervals_request.read()
            intervals = json.loads(intervals_read)
        except urllib.error.HTTPError as e:
            print(e.reason)
            return []
        except urllib.error.URLError as e:
            print(e.reason)
            return []

        for element in intervals["data"]:
            self.lista_intervalos.append(element)
        #time.sleep(2)
        return self.lista_intervalos

    #Realiza la peticion al server del intervalo deseado, y devuelve una lista con las canciones obtenidas
    def obtener_canciones_con_intervalo(self, intervalo, asc_or_des):
        try:
            songs_request = urllib.request.urlopen('http://localhost:5000/songs/' + intervalo + '/' + asc_or_des)
            songs_read = songs_request.read()
            songs = json.loads(songs_read)
        except urllib.error.HTTPError as e:
            print(e.reason)
        except urllib.error.URLError as e:
            print(e.reason)
        
        return songs["data"]

    #Getter del atributo lista_intervalos
    def get_lista_intervalos(self):
        return self.lista_intervalos

    #Calcula un par de notas aleatorias que cumplan el intervalo introducido
    def calcular_nota(self, intervalo, asc_or_desc):
        if (asc_or_desc == "asc"):
            intervalo_ = self.parsear_intervalo(intervalo)
            pos_first = random.randint(0,11)
            pos_last = (pos_first + intervalo_)%12
            
            notasFinales = (intervalo + " " + asc_or_desc + " ---> " + self.notas[pos_first] + ' - ' + self.notas[pos_last] )
            print(notasFinales)
            
            return notasFinales
        else:
            intervalo_ = self.parsear_intervalo(intervalo)
            pos_first = random.randint(0,11)
            pos_last = (pos_first - intervalo_)%12

            notasFinales = (intervalo + " " + asc_or_desc + " ---> " + self.notas[pos_first] + ' - ' + self.notas[pos_last] )
            print(notasFinales)
            
            return notasFinales

    #Transforma los intervalos en los semitonos que representan, para hacer el cálculo de las notas
    def parsear_intervalo(self, intervalo):
        if (intervalo == '2m'):
            return 1
        elif (intervalo == '2M'):
            return 2
        elif (intervalo == '3m'):
            return 3
        elif (intervalo =='3M'):
            return 4
        elif (intervalo == '4j'):
            return 5
        elif (intervalo == '4aum'):
            return 6
        elif (intervalo == '5j'):
            return 7
        elif (intervalo == '6m'):
            return 8
        elif (intervalo == '6M'):
            return 9
        elif (intervalo == '7m'):
            return 10
        elif (intervalo == '7M'):
            return 11
        elif (intervalo == '8a'):
            return 12