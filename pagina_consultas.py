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

class SeccionConsultas:

    def __init__(self, main_layout, main_page):
        self.main_layout = main_layout
        self.main_page = main_page

    def pagina_principal(self):
        back_btn_size = (self.main_layout.size[0] * 0.5, self.main_layout.size[1] * 0.1)
        self.leer_alimentos()
        self.layout_lista_alimentos = BoxLayout(orientation="vertical", spacing=10,height=(len(self.alimentos) + 1) * back_btn_size[1], size_hint_y=None)
        self.back_btn = Button(text='Volver', on_press=self.boton_volver_lista_alimentos, height=back_btn_size[1],size_hint_y=None)
        self.layout_lista_alimentos.add_widget(self.back_btn)
        self.scroll_view_lista_alimentos = ScrollView()
        for alimento in self.alimentos:
            self.button_text = alimento.nombre
            self.button = Button(text=self.button_text)
            self.button.bind(on_press=lambda instance, a=alimento: self.consultar_info(a), height=back_btn_size[1]*0.5,size_hint_y=None)
            self.layout_lista_alimentos.add_widget(self.button)
        self.scroll_view_lista_alimentos.add_widget(self.layout_lista_alimentos)
        self.main_layout.add_widget(self.scroll_view_lista_alimentos)

    def leer_alimentos(self):
        self.alimentos = []
        with open("alimentos.csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                alimento = Alimento(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                self.alimentos.append(alimento)

    def consultar_info(self, alimento):
        back_btn_size = (self.main_layout.size[0] * 0.5, self.main_layout.size[1] * 0.1)
        self.main_layout.remove_widget(self.scroll_view_lista_alimentos)

        self.layout_informacion_nutricional = GridLayout(cols = 1, rows = 3, spacing = 10)
        self.propiedades = GridLayout(cols=2, rows=10, spacing=10)
        self.back_btn = Button(text='Volver', on_press=self.boton_volver_informacion, height=back_btn_size[1],
                               size_hint_y=None, size_hint_x = 1)
        self.layout_informacion_nutricional.add_widget(self.back_btn)

        nombre = Label(text="Nombre:")
        calorias = Label(text="Calorias:")
        hc = Label(text="Hidratos de carbono:")
        azucares = Label(text="de los cuales azúcares:")
        proteinas = Label(text="Proteinas:")
        grasas = Label(text="Grasas:")
        grupo = Label(text="Grupo:")

        nombre_valor = Label(text = alimento.nombre)
        calorias_valor = Label(text=alimento.calorias + " kcal")
        hc_valor = Label(text=alimento.hc + " g")
        azucares_valor = Label(text=alimento.azucares + " g")
        proteinas_valor = Label(text=alimento.proteinas + " g")
        grasas_valor = Label(text=alimento.grasas + " g")
        grupo_valor = Label(text=alimento.grupo)

        self.propiedades.add_widget(nombre)
        self.propiedades.add_widget(nombre_valor)

        self.propiedades.add_widget(calorias)
        self.propiedades.add_widget(calorias_valor)

        self.propiedades.add_widget(hc)
        self.propiedades.add_widget(hc_valor)

        self.propiedades.add_widget(azucares)
        self.propiedades.add_widget(azucares_valor)

        self.propiedades.add_widget(proteinas)
        self.propiedades.add_widget(proteinas_valor)

        self.propiedades.add_widget(grasas)
        self.propiedades.add_widget(grasas_valor)

        self.propiedades.add_widget(grupo)
        self.propiedades.add_widget(grupo_valor)

        self.layout_informacion_nutricional.add_widget(self.propiedades)
        self.main_layout.add_widget(self.layout_informacion_nutricional)

    def boton_volver_lista_alimentos(self, instance):
        self.main_layout.remove_widget(self.scroll_view_lista_alimentos)
        self.main_layout.add_widget(self.main_page)

    def boton_volver_informacion(self, instance):
        self.main_layout.remove_widget(self.layout_informacion_nutricional)
        self.main_layout.add_widget(self.scroll_view_lista_alimentos)