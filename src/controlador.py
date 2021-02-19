import vista
import modelo
import locale
import gettext

_ = gettext.gettext
N_ = gettext.ngettext

import threading
import time

class Controlador:

	def __init__(self):

		self.modelo = modelo.Modelo()
		self.vista = vista.Vista()
		self.vista.boton_pulsado(self.on_asc_des_clicked)
		self.vista.reintentar_pulsado(self.reintentar_intervalos)

		#Creamos ya una thread para pedir los intervalos al servidor, y de funcionar bien,
		#la interfaz se creará ya con las páginas de la notebook.
		#Si no llega a funcionar por cualquier motivo, aparecerá el botón Reintentar conexión.
		threading.Thread(target = self.actualizar_intervalos, daemon = True).start()

	#Esta función se llama al pulsar los botones Ascendente o Descendente de la vista, y llama a las
	#funciones de modelo para obtener la lista de canciones y crear un ejemplo de notas del intervalo
	def on_asc_des_clicked(self, boton):
		pagina = self.vista.obtener_pagina()
		threading.Thread(target = self.actualizar_vista, daemon = True, args = (boton, pagina)).start()
		
	#Esta funcion se llama tras pulsar los botones ascendente o descendente, y le dice al modelo
	#la request que debe hacer, para luego actualizar la vista con la lista de canciones obtenida
	def actualizar_vista(self, boton, pagina):
		self.vista.spinner.start()

		asc_des = boton.get_label()
		if (asc_des == _("Ascendente")):
			asc_des = "asc"
		elif (asc_des == _("Descendente")):
			asc_des = "des"

		canciones = self.modelo.obtener_canciones_con_intervalo(pagina[0], asc_des)
		notas = self.modelo.calcular_nota(pagina[0], asc_des)
		time.sleep(0.5)
		self.vista.actualizar_treeview(canciones, pagina)
		self.vista.actualizar_notas_ejemplo(notas, pagina)
		self.vista.spinner.stop()

	#Esta funcion pide al modelo que haga la peticion de intervalos, y hace que la vista se actualize
	#conforme a los intervalos recibidos
	def actualizar_intervalos(self):
		self.vista.spinner.start()
		self.vista.bot_rein.hide()
		self.vista.actualizar_paginas(self.modelo.obtener_intervalos())

	#Esta función se llama al hacr click en el botón Reintentar conexión, que solo aparece
	#si se ha recibido una lista de intervalos vacía, es decir, no se realizó correctamente
	#la petición al servidor
	def reintentar_intervalos(self, boton):
		threading.Thread(target = self.actualizar_intervalos, daemon = True).start()

	
	def run(self):
		vista.run()