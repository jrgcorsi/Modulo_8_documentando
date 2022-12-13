"""
vista.py
    creamos la vista de nuestra aplicacion
"""

from tkinter import StringVar
from tkinter import CENTER
from tkinter import Label
from tkinter import W
from tkinter import S
from tkinter import Entry
from tkinter import Button
from tkinter import ttk
from modulos import MiModelo
"""
importamos los modulos necesarios para nuestra ejecucion
"""

class MiVista():
    def __init__(self, window):

        """
        definimos los valores y formato de los campos que completaremos.
        """
        self.var_mesa = StringVar()
        self.var_paso = StringVar()
        self.var_menu = StringVar()
        self.var_cantidad = StringVar()

        # Formato de ventana
        self.root = window
        self.obj = MiModelo()

        self.root.title("RESTO - Alta de pedido")
        self.root.geometry("720x330")
        self.root.resizable(0, 0)

        # Creando la tabla
        self.tree = ttk.Treeview(self.root)
        self.tree.grid(row=0, column=0, pady=10,
                       padx=5, columnspan=5, rowspan=5)
        self.tree["columns"] = ("col1", "col2", "col3", "col4")
        self.tree.column("#0", width=50, minwidth=50, anchor=S)
        self.tree.column("col1", width=50, minwidth=80, anchor=S)
        self.tree.column("col2", width=80, minwidth=80, anchor=S)
        self.tree.column("col3", width=350, minwidth=80, anchor=S)
        self.tree.column("col4", width=50, minwidth=80, anchor=S)
        # Titulos de la tabla
        self.tree.heading("#0", text="ID", anchor=CENTER)
        self.tree.heading("col1", text="MESA #", anchor=CENTER)
        self.tree.heading("col2", text="PASO #", anchor=CENTER)
        self.tree.heading("col3", text="MENU", anchor=CENTER)
        self.tree.heading("col4", text="CANTIDAD", anchor=CENTER)
        # evento de seleccion para consulta / Eliminacion
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

        # Campos para ingresar
        self.mesa = Label(self.root, text="Mesa")
        self.mesa.grid(row=6, column=0, sticky=W, padx=10, pady=5)  # centrado
        self.mesa_com = ttk.Combobox(self.root, textvariable=self.var_mesa)
        self.mesa_com['values'] = (
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13')
        self.mesa_com.grid(row=6, column=1)
        self.mesa_com.focus()

        self.paso = Label(self.root, text="Paso")
        self.paso.grid(row=6, column=2, sticky=W, padx=10, pady=5)  # centrado
        self.paso_com = ttk.Combobox(self.root, textvariable=self.var_paso)
        self.paso_com['values'] = ('entrada', 'principal', 'postre', 'otros')
        self.paso_com.grid(row=6, column=3)

        self.menu = Label(self.root, text="Menu")
        self.menu.grid(row=7, column=0, sticky=W, padx=10, pady=5)  # centrado
        self.entry_menu = Entry(
            self.root, textvariable=self.var_menu, width=30)
        self.entry_menu.grid(row=7, column=1)
        # Cantidad a pedir
        self.cantidad = Label(self.root, text="Cantidad")
        self.cantidad.grid(row=7, column=2, sticky=W,
                           padx=10, pady=5)  # centrado
        self.entry_cantidad = Entry(
            self.root, textvariable=self.var_cantidad, width=30)
        self.entry_cantidad.grid(row=7, column=3)

        # Botonera
        self.boton_g = Button(self.root, text="Guardar",
                              command=lambda: self.obj.funcion_g(
                                  self.var_mesa.get(),
                                  self.var_paso.get(),
                                  self.var_menu.get(),
                                  self.var_cantidad.get(),
                                  self.tree,
                                  self.mesa_com,
                                  self.paso_com,
                                  self.entry_menu,
                                  self.entry_cantidad), width=15)
        self.boton_g.grid(row=0, column=7, pady=2, padx=2)
        self.boton_color = Button(self.root, text="Consulta",
                                  command=lambda: self.obj.consulta(
                                      self.tree,
                                      self.mesa_com,
                                      self.paso_com,
                                      self.entry_menu,
                                      self.entry_cantidad),  width=15)
        self.boton_color.grid(row=1, column=7, pady=2, padx=2)
        self.boton_color = Button(self.root, text="Modificar",
                                  command=lambda: self.obj.modificar(
                                      self.var_menu.get(),
                                      self.var_cantidad.get(),
                                      self.var_mesa.get(),
                                      self.var_paso.get(),
                                      self.tree,
                                      self.mesa_com,
                                      self.paso_com,
                                      self.entry_menu,
                                      self.entry_cantidad),  width=15)
        self.boton_color.grid(row=2, column=7, pady=2, padx=2)
        self.boton_Eliminar = Button(self.root, text="Eliminar",
                                     command=lambda: self.obj.borrar(
                                         self.var_mesa.get(),
                                         self.var_paso.get(),
                                         self.var_menu.get(),
                                         self.var_cantidad.get(),
                                         self.tree,
                                         self.mesa_com,
                                         self.paso_com,
                                         self.entry_menu,
                                         self.entry_cantidad),  width=15)
        self.boton_Eliminar.grid(row=3, column=7, pady=2, padx=2)
        self.boton_imprimir = Button(self.root, text="Imprimir",
                                     command=lambda: self.obj.imprimir(
                                         self.var_mesa.get(),
                                         self.var_paso.get(),
                                         self.var_menu.get(),
                                         self.var_cantidad.get(),
                                         self.tree),  width=15)
        self.boton_imprimir.grid(row=4, column=7, pady=2, padx=2)

       # Seleccionar pedido para Edicion / Destroy
    def seleccionar(self, event):
        try:
            id = self.tree.selection()[0]
            self.var_mesa.set(self.tree.item(id, "values")[0])
            self.var_paso.set(self.tree.item(id, "values")[1])
            self.var_menu.set(self.tree.item(id, "values")[2])
            self.var_cantidad.set(self.tree.item(id, "values")[3])

        except IndexError:
            pass
