import gi
import webbrowser
import locale
import gettext

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

_ = gettext.gettext
N_ = gettext.ngettext

class ListaCanciones(Gtk.Grid):
    def __init__(self, lista_canciones):
        Gtk.Grid.__init__(self)

        #Creando un grid para colocar los elementos
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        #Creando la ListStore para colocar bien desde el json los nombres, urls y favs
        self.list = Gtk.ListStore(str, str, str)
        for software_ref in lista_canciones:
            self.list.append(list(software_ref))

        #Creando el treeview y sus columnas, luego añadiéndoselas
        self.treeview = Gtk.TreeView(model=self.list)
        
        self.renderer_text = Gtk.CellRendererText()

        self.column_nombre = Gtk.TreeViewColumn(_("Nombre"), self.renderer_text, text=0)
        self.column_nombre.set_resizable(True)
        self.column_nombre.set_min_width(250)

        self.column_url = Gtk.TreeViewColumn("URL", self.renderer_text, text=1)
        self.column_url.set_resizable(True)
        self.column_url.set_min_width(420)

        self.column_fav = Gtk.TreeViewColumn("Fav", self.renderer_text, text=2)
        self.column_fav.set_resizable(True)
        self.column_fav.set_min_width(5)
        self.column_fav.set_max_width(10)

        #Haciendo doble click sobre una fila se abre el link en el navegador
        self.treeview.connect('row-activated', self.abrir_enlace)

        self.treeview.append_column(self.column_nombre)
        self.treeview.append_column(self.column_url)
        self.treeview.append_column(self.column_fav)

        #Creando una caja para el ejemplo de notas del intervalo
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.title = Gtk.Label()
        self.title.set_markup(_("<big>Ejemplo de notas</big>"))
        self.box.pack_start(self.title,expand=False,fill=False,padding=8)

        self.box_notas=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.notas=Gtk.Label(label="")
        self.box_notas.pack_start(self.notas,expand=False,fill=False,padding=8)

        #Colocando el treeview en una ventana con scroll
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 5, 12)
        self.grid.attach_next_to(self.box, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.box_notas, self.box, Gtk.PositionType.BOTTOM, 1, 1)
        
        self.scrollable_treelist.add(self.treeview)

    #Limpia la lista de canciones e introduce la nueva obtenida de la petición
    def actuaizar_lista(self, lista):
        self.list.clear()
        for software_ref in lista:
            self.list.append(list(software_ref))

    #Hace que se actualicen las notas del intervalo de ejemplo
    def actualizar_ejemplo(self, ejemplo):
        self.notas.set_text(ejemplo)

    #Abre el enlace seleccionado al hacer doble click sobre el
    def abrir_enlace(self, treeview, path, view_column):
        #Comprobamos primero si hay enlace
        if(self.list[path][1]!=""):
            webbrowser.open(self.list[path][1])

#Clase principal
class Vista(Gtk.Window):

    def __init__(self):

        #creando la ventana y estableciendo sus parámetros
        self.win = Gtk.Window(title=_("Cliente Musical"))
        self.win.connect("destroy", Gtk.main_quit)
        self.win.set_default_size(300, 400)

        self.win.set_size_request(800, 500)
        self.win.set_position(Gtk.WindowPosition.CENTER)
        self.win.set_resizable(True)
        self.win.set_border_width(10)

        #lista de los intervalos
        self.lista_intervalos = []
        #creando la estructura base donde colocar la libreta y los dos botones
        self.grid = Gtk.Grid()
        self.win.add(self.grid)

        #creando la libreta de paginas de intervalos
        self.notebook = Gtk.Notebook()
        self.grid.attach(self.notebook, 0, 0, 8, 10)
        self.notebook.set_scrollable(True)
        self.notebook.popup_enable()
        
        #creando el botón de intervalo ascendente
        self.bot_asc = Gtk.Button(label=_("Ascendente"))

        #creando el botón de intervalo ascendente
        self.bot_des = Gtk.Button(label=_("Descendente"))

        #creando el botón de reintentar conexión
        self.bot_rein = Gtk.Button(label=_("Reintentar conexión"))

        #creando un spinner para cuando tarden los datos
        self.spinner = Gtk.Spinner()

        #colocando los botones arriba de la libreta
        self.grid.attach_next_to(self.bot_asc, self.notebook, Gtk.PositionType.TOP, 1, 1)
        self.grid.attach_next_to(self.bot_des, self.bot_asc, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.spinner, self.bot_des, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.bot_rein, self.spinner, Gtk.PositionType.RIGHT, 1, 1)

        #creando lista de páginas
        self.paginas = list()

        #creando tlista de treeviews
        self.treeviews = list()

        #mostrando la ventana con solo el spinner, hasta que se ejecute "actualizar_paginas"
        #con tantas paginas en la libreta como intervalos
        self.win.show_all()
        self.bot_asc.hide()
        self.bot_des.hide()
        self.bot_rein.hide()

    #Esta funcion se llama al inicio y cuando se pulsa reintentar conexion
    def actualizar_paginas(self, intervalos):

        if (intervalos != []):
            self.lista_intervalos = intervalos

            #creando tantas paginas como intervalos
            for pagina in self.lista_intervalos:
                pagina = Gtk.Grid()
                self.paginas.append(pagina)

            #creando tantos treeviews como paginas (intervalos)
            for treev in self.lista_intervalos:
                treev = ListaCanciones([])
                self.treeviews.append(treev)

            #insertando todas las páginas y añadiéndoles un treeview
            for i, pagina in enumerate(self.paginas):
                pagina.add(self.treeviews[i])
                self.notebook.append_page(pagina, Gtk.Label(label=self.lista_intervalos[i]))

            self.win.show_all()
            self.bot_rein.hide()
            self.spinner.stop()

        else:
            self.spinner.stop()
            self.bot_rein.show()

    #Avisa al controller cuando se pulsa el botón Ascendente o Descendente
    def boton_pulsado(self, handler): 
        self.bot_asc.connect('clicked', handler)
        self.bot_des.connect('clicked', handler)

    #Avisa al controller cuando se pulsa el botón Reintentar conexión
    def reintentar_pulsado(self, handler):
        self.bot_rein.connect('clicked', handler)

    #obtener el nombre de la pagina en la que nos encontramos
    def obtener_pagina(self):
        page_number = self.notebook.get_current_page()
        page = self.notebook.get_nth_page(page_number)
        return (self.notebook.get_tab_label_text(page),page_number)

    #obtenemos el numero de la pagina en la que nos encontramos
    def obtener_num_pagina(self):
        return self.notebook.get_current_page()

    #actualizar el treeview con la lista de canciones del intervalo
    def actualizar_treeview(self,lista, page):
        page_number = page[1]
        self.treeviews[page_number].actuaizar_lista(lista)

    #Actualiza las notas de ejemplo del intervalo, generando unas nuevas aleatorias
    def actualizar_notas_ejemplo(self, ejemplo, page):
        page_number = page[1]
        self.treeviews[page_number].actualizar_ejemplo(ejemplo)


def run():
    Gtk.main()