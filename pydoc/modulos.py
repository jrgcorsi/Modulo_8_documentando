import re
# import sqlite3
import tempfile
import win32api
import win32print
from tkinter import messagebox
from os import system
import sys
import os
import datetime

from peewee import *

db = SqliteDatabase("comidas.db")


class BaseModel(Model):
    class Meta:
        database = db

# Esta clase esta destinada a los titulos de la tabla


class pedidos(BaseModel):
    mesa = IntegerField(unique=False)
    paso = CharField()
    menu = CharField()
    cantidad = IntegerField()


db.connect()

# Creamos la table de la base de datos
db.create_tables([pedidos])


class RegistroError(Exception):

    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "log.txt")

    def __init__(self, accion, archivo, fecha):
        self.accion = accion
        self.archivo = archivo
        self.fecha = fecha

    def registrar_err(self):
        log = open(self.ruta, "a")
        print("se ha dado un error en la accion:",
              self.archivo, self.accion, self.fecha, file=log)


def err_alta():
    raise RegistroError("crear", "funcion_g", datetime.datetime.now())


def err_modificar():
    raise RegistroError("modificar", "modificar", datetime.datetime.now())


class MiModelo:

    def __init__(self, ): pass  # constructor

    # Alta de registro
    def funcion_g(self, var_mesa, var_paso, var_menu, var_cantidad, tree, mesa_com, paso_com, entry_menu, entry_cantidad):  # OK
        cad_menu = var_menu
        cad_cantidad = var_cantidad
        # patron de validacion
        patron = "^[a-zA-Z0-9\s]+" "+[a-zA-Z0-9]*$"
        patron_cantidad = "[0-9]"

        assert_mesa = str(var_mesa)

        # Usando el assert como excepcion
        assert assert_mesa != "", "Debe ingresar una mesa valida"

        # Usando try para evaluar una condicion
        try:
            if var_paso != "":
                print("pass")
            else:
                raise TypeError
        except TypeError:
            messagebox.showinfo(
                message="No puede crear un pedido sin PASO", title="PASO incorrecto")
            try:
                err_alta()
            except RegistroError as log:
                log.registrar_err()

        else:
            if (re.match(patron, cad_menu) and
                    re.match(patron_cantidad, cad_cantidad)):
                messagebox.showinfo(
                    message="El codigo fue creado correctamente", title="Nuevo Codigo")

                # Nueva alta con peewee
                pedido = pedidos()
                pedido.mesa = var_mesa
                pedido.paso = var_paso
                pedido.menu = var_menu
                pedido.cantidad = var_cantidad
                pedido.save()

                # borra el contenido del text luego de guardar
                mesa_com.delete(0, "end"),
                paso_com.delete(0, "end"),
                entry_menu.delete(0, "end"),
                entry_cantidad.delete(0, "end")
                # actualizo el treeview luego de guardar el elemento
                self.consulta(tree, mesa_com, paso_com,
                              entry_menu, entry_cantidad)
                # posieciono para tomar nuevo pedido
                mesa_com.focus()
            else:

                messagebox.showinfo(
                    message="los datos cargados son incorrectos, por favor intente nuevamente", title="Error")
                # validacion de patron por consolelog
                raise Exception("Patron no valido")

        # Consultar de pedidos totales

    def consulta(self, tree, mesa_com, paso_com, entry_menu, entry_cantidad):  # revisar posicionales
        system("cls")
        registros = tree.get_children()

        for elemento in registros:
            tree.delete(elemento)

        for fila in pedidos.select():
            print(["Mesa", fila.mesa, "Paso", fila.paso,
                  "Menu", fila.menu, "Cantidad", fila.cantidad])
            tree.insert('', 0, text=fila.id, values=(
                fila.mesa, fila.paso, fila.menu, fila.cantidad))

        # borra el contenido del text luego de guardar
        mesa_com.delete(0, "end"),
        paso_com.delete(0, "end"),
        entry_menu.delete(0, "end"),
        entry_cantidad.delete(0, "end")
        # posiciono para tomar nuevo pedido
        mesa_com.focus()

    # Borrar pedido
    def borrar(self, var_mesa, var_paso, var_menu, var_cantidad, tree, mesa_com, paso_com, entry_menu, entry_cantidad):  # OK funciona
        # Obtenemos el ID

        if len(var_mesa) != 0 and len(var_paso) != 0 and len(var_menu) != 0 and len(var_cantidad) != 0:
            item = tree.selection()
            id = tree.item(item)

            borrar = pedidos.get(pedidos.id == id['text'])

            respuesta = messagebox.askyesno(
                'IMPORTANTE', "Usted esta a punto de borrar un registro, desea continuar?")
            if respuesta == True:
                borrar.delete_instance()

                # borra el contenido del text luego de guardar
                mesa_com.delete(0, "end")
                paso_com.delete(0, "end")
                entry_menu.delete(0, "end")
                entry_cantidad.delete(0, "end")
                # actualizo el treeview luego de guardar el elemento
                self.consulta(tree, mesa_com, paso_com,
                              entry_menu, entry_cantidad)
                mesa_com.focus()

            elif respuesta == False:
                messagebox.showinfo(
                    message="La operacion se ha cancelado", title="Error")
        else:
            self.consulta(tree, mesa_com, paso_com, entry_menu, entry_cantidad)
            messagebox.showinfo(
                message="puede que le falte seleccionar algun valor, intente nuevamente", title="Cancelacion")

    # Modificar registro seleccionado
    def modificar(self, var_menu, var_cantidad, var_mesa, var_paso, tree, mesa_com, paso_com, entry_menu, entry_cantidad):  # OK funciona
        cad_menu = var_menu
        cad_cantidad = var_cantidad
        # patron de validacion
        patron = "^[a-zA-Z0-9\s]+" "+[a-zA-Z0-9\s]*$"
        patron_cantidad = "[0-9]"

        # Usando try para evaluar una condicion
        try:
            if var_paso != "" and var_mesa != "":
                print("pass")
            else:
                raise TypeError
        except TypeError:
            messagebox.showinfo(
                message="Puede que le falte completar algun valor", title="PASO incorrecto")
            try:
                err_modificar()
            except RegistroError as log:
                log.registrar_err()

        else:
            if (re.match(patron, cad_menu) and re.match(patron_cantidad, cad_cantidad)):

                item = tree.focus()
                id = tree.item(item)
                actualizar = pedidos.update(
                    mesa=var_mesa, paso=var_paso, menu=var_menu, cantidad=var_cantidad).where(pedidos.id == id['text'])
                actualizar.execute()

                messagebox.showinfo(
                    message="El codigo fue actualizado correctamente", title="Actualizacion")

                # borra el contenido del text luego de guardar
                mesa_com.delete(0, "end")
                paso_com.delete(0, "end")
                entry_menu.delete(0, "end")
                entry_cantidad.delete(0, "end")
                # actualizo el treeview luego de guardar el elemento
                self.consulta(tree, mesa_com, paso_com,
                              entry_menu, entry_cantidad)
                mesa_com.focus()
            else:
                messagebox.showinfo(
                    message="El menu o la cantidad ingresado son incorrectos, por favor intente nuevamente", title="Error")

        # imprimir
    # Esto iria junto al crear item para que se imprima el ticket en el mostrador
    def imprimir(self, var_mesa, var_paso, var_menu, var_cantidad, tree):
        if len(var_mesa) != 0 and len(var_paso) != 0 and len(var_menu) != 0 and len(var_cantidad) != 0:
            archivo = tempfile.mktemp(".txt")
            open(archivo, "w").write("NUEVO PEDIDO" + "\n\n" + "mesa= "+var_mesa + "\n" + "Paso="+var_paso + "\n" + "Menu= "+var_menu +
                                     "\n" + "Cantidad= "+var_cantidad)  # aqui puedes agregar los valores de tu listbox (o puedes crear un documento .docx)
            win32api.ShellExecute(
                0,
                "printto",
                archivo,
                '"%s"' % win32print.GetDefaultPrinter(),
                ".",
                0
            )
        else:
            messagebox.showinfo(
                message="Debe seleccionar un dato, intente nuevamente", title="Error")
