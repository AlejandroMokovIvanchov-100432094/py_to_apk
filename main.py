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

from pagina_consultas import SeccionConsultas
from pagina_ratios import SeccionRatios
from pagina_recetas import SeccionRecetas



class Alimento:
    def __init__(self, nombre, calorias, hc, azucares, proteinas, grasas, grupo):
        self.nombre = nombre
        self.calorias = calorias
        self.hc = hc
        self.azucares = azucares
        self.proteinas = proteinas
        self.grasas = grasas
        self.grupo = grupo


class MiApp(App):
    def build(self):
        Window.size = (420, 720)
        # Crea una caja vertical (BoxLayout)
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.main_page = BoxLayout(orientation='vertical', spacing=10, padding=10)
        with self.main_layout.canvas.before:
            Color(0.65, 0.65, 0.65, 0.6)  # RGBA (valores entre 0 y 1)
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self.update_rect)
        self.menu_principal()
        return self.main_layout

    def menu_principal(self):
        self.btn_infnut = Button(text='Consultar información de un alimento', on_press=self.pagina_informacion_nutricional)
        self.btn_recetas = Button(text='Hacer recetas', on_press=self.pagina_recetas)
        self.btn_ratios = Button(text='Definir ratios de insulina', on_press=self.ratios_button_press)
        self.main_page.add_widget(self.btn_infnut)
        self.main_page.add_widget(self.btn_recetas)
        self.main_page.add_widget(self.btn_ratios)
        self.main_layout.add_widget(self.main_page)

    def pagina_recetas(self, instance):
        self.main_layout.remove_widget(self.main_page)
        layout_totales = GridLayout(cols=2)
        seccion = SeccionRecetas(self.main_layout, self.main_page, layout_totales)
        seccion.pagina_principal()

    def pagina_informacion_nutricional(self, instance):
        self.main_layout.remove_widget(self.main_page)
        seccion_in = SeccionConsultas(self.main_layout, self.main_page)
        seccion_in.pagina_principal()

    def leer_alimentos(self):
        self.alimentos = []
        with open("alimentos.csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                alimento = Alimento(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                self.alimentos.append(alimento)

    def update_rect(self, instance, value):
        # Actualiza el tamaño y la posición del Rectangle al cambiar el tamaño de la ventana
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def ratios_button_press(self, instance):
        self.main_layout.remove_widget(self.main_page)
        seccion_r = SeccionRatios(self.main_layout, self.main_page)
        seccion_r.pagina_principal()



if __name__ == '__main__':
    MiApp().run()


