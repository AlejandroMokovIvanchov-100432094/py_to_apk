from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

from functools import partial
import csv
import json

class Alimento:
    def __init__(self, nombre, calorias, hc, azucares, proteinas, grasas, grupo):
        self.nombre = nombre
        self.calorias = calorias
        self.hc = hc
        self.azucares = azucares
        self.proteinas = proteinas
        self.grasas = grasas
        self.grupo = grupo

class SeccionRatios:
    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page

    def pagina_principal(self):
        self.ratios_page = GridLayout(cols=1, spacing=10)
        self.main_layout.add_widget(self.ratios_page)
        back_btn_size = (self.main_layout.size[0] * 0.5, self.main_layout.size[1] * 0.1)
        back_btn = Button(text='Volver', height=back_btn_size[1], size_hint_y=None, on_press = partial(self.boton_volver, self))
        self.ratios_page.add_widget(back_btn)
        self.leer_ratios(back_btn_size)
        self.definir_ratios_nuevos(back_btn_size)

    def definir_ratios_nuevos(self, back_btn_size):
        ratios_nuevos = Label(text="Introducir ratios nuevos", height=back_btn_size[1] * 0.5, size_hint_y=None,font_size=25)
        self.ratio_desayuno_nuevo = TextInput(hint_text='Ratio desayuno', multiline=False,height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.ratio_comida_nuevo = TextInput(hint_text='Ratio comida', multiline=False,height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.ratio_cena_nuevo = TextInput(hint_text='Ratio cena', multiline=False,height=back_btn_size[1] * 0.5, size_hint_y=None)
        btn_save_ratios = Button(text='Guardar ratios nuevos', on_press=partial(self.guardar_ratios_nuevos, self), height=back_btn_size[1], size_hint_y=None)
        self.ratios_page.add_widget(ratios_nuevos)
        self.ratios_page.add_widget(self.ratio_desayuno_nuevo)
        self.ratios_page.add_widget(self.ratio_comida_nuevo)
        self.ratios_page.add_widget(self.ratio_cena_nuevo)
        self.ratios_page.add_widget(btn_save_ratios)

    def guardar_ratios_nuevos(self, instance, *args):
        ratio_desayuno = self.ratio_desayuno_nuevo.text
        ratio_comida = self.ratio_comida_nuevo.text
        ratio_cena = self.ratio_cena_nuevo.text
        datos = {"desayuno": ratio_desayuno,"comida": ratio_comida,"cena": ratio_cena}
        with open("ratios.json", 'w') as archivo:
            json.dump(datos, archivo)

    def boton_volver(self, instance, *args):
        self.main_layout.remove_widget(self.ratios_page)
        self.main_layout.add_widget(self.main_page)

    def leer_ratios(self, back_btn_size):
        with open("ratios.json", 'r') as archivo:
            try:
                ratios_cargados = json.load(archivo)
            except json.JSONDecodeError:
                ratios_cargados = {}
            if len(ratios_cargados) > 0:
                layout_ratio_desayuno = BoxLayout(orientation="horizontal",height=back_btn_size[1] * 0.3, size_hint_y=None)
                ratio_desayuno = Label(text="Ratio del desayuno")
                ratio_desayuno_valor = Label(text=ratios_cargados["desayuno"])
                layout_ratio_desayuno.add_widget(ratio_desayuno)
                layout_ratio_desayuno.add_widget(ratio_desayuno_valor)
                layout_ratio_comida = BoxLayout(orientation="horizontal",height=back_btn_size[1] * 0.3, size_hint_y=None)
                ratio_comida = Label(text="Ratio de la comida")
                ratio_comida_valor = Label(text=ratios_cargados["comida"])
                layout_ratio_comida.add_widget(ratio_comida)
                layout_ratio_comida.add_widget(ratio_comida_valor)
                layout_ratio_cena = BoxLayout(orientation="horizontal", height=back_btn_size[1] * 0.3, size_hint_y=None)
                ratio_cena = Label(text="Ratio de la cena")
                ratio_cena_valor = Label(text=ratios_cargados["cena"])
                layout_ratio_cena.add_widget(ratio_cena)
                layout_ratio_cena.add_widget(ratio_cena_valor)

                self.ratios_page.add_widget(layout_ratio_desayuno)
                self.ratios_page.add_widget(layout_ratio_comida)
                self.ratios_page.add_widget(layout_ratio_cena)
