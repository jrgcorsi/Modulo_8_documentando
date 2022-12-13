"""
controlador.py
    creamos el modulo que ejecutara nuestra vista
"""

import vista
from tkinter import Tk


class Controller:

    def __init__(self, root):
        self.root_controler = root
        self.objeto_vista = vista.MiVista(self.root_controler)


if __name__ == "__main__":
    root_tk = Tk()
    Controller(root_tk)  # accion
    root_tk.mainloop()
