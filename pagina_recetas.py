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

class SeccionRecetas:

    def __init__(self, main_layout, main_page, layout_totales):
        self.main_page = main_page
        self.main_layout = main_layout
        self.layout_totales = layout_totales
        self.layout_recetas = None
        self.alimentos_seleccionados = []

    def pagina_principal(self):
        back_btn_size = (self.main_layout.size[0] * 0.5, self.main_layout.size[1] * 0.1)
        self.leer_alimentos()
        self.main_layout.remove_widget(self.main_page)
        self.layout_recetas = GridLayout(cols=1, spacing=10, height=len(self.alimentos) * back_btn_size[1],size_hint_y=None)
        self.back_btn = Button(text='Volver', on_press=partial(self.back_btn_recetas, self), height=back_btn_size[1], size_hint_y=None)
        self.main_layout.add_widget(self.back_btn)
        self.scroll_view = ScrollView()

        for alimento in self.alimentos:
            self.button_text = alimento.nombre
            self.button = Button(text=self.button_text, height=back_btn_size[1] * 0.5, size_hint_y=None)
            self.layout_recetas.add_widget(self.button)
            self.button.bind(on_press=lambda instance, a=alimento: self.seleccionar_alimento(a))
        self.btn_cantidades = Button(text="Seleccionar cantidades", height=back_btn_size[1], size_hint_y=None,on_press=self.pagina_cantidades)
        self.layout_recetas.add_widget(self.btn_cantidades)
        self.scroll_view.add_widget(self.layout_recetas)
        self.main_layout.add_widget(self.scroll_view)

    def leer_alimentos(self):
        self.alimentos = []
        with open("alimentos.csv", newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                alimento = Alimento(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                self.alimentos.append(alimento)

    def pagina_cantidades(self, instance):
        if self.layout_totales:
            self.main_layout.remove_widget(self.layout_totales)
        self.main_layout.remove_widget(self.back_btn)
        self.main_layout.remove_widget(self.scroll_view)
        back_btn_size = (self.main_layout.size[0] * 0.5, self.main_layout.size[1] * 0.1)
        self.back_btn_cant = Button(text='Volver', on_press=partial(self.back_btn_cantidades, self), height=back_btn_size[1],
                               size_hint_y=None)
        self.main_layout.add_widget(self.back_btn_cant)
        self.btn_insulina = Button(text='Calcular insulina', on_press=self.calcular_insulina,
                                   height=back_btn_size[1]*0.5,
                                   size_hint_y=None)
        self.main_layout.add_widget(self.btn_insulina)
        self.layout_seleccion = GridLayout(cols=2, height = len(self.alimentos_seleccionados)*back_btn_size[1]*0.5,size_hint_y=None)
        for alimento in self.alimentos_seleccionados:
            self.label_text = alimento.nombre
            self.label = Label(text=self.label_text, height=back_btn_size[1]*0.5,size_hint_y=None)
            cantidad = TextInput(hint_text = "Cantidad", height=back_btn_size[1]*0.5,size_hint_y=None, width=back_btn_size[0]*0.3,size_hint_x=None, font_size = 12)
            self.layout_seleccion.add_widget(self.label)
            self.layout_seleccion.add_widget(cantidad)

        self.btn_calcular_totales = Button(text = "Calcular cantidades totales", height=back_btn_size[1]*0.5,size_hint_y=None, on_press = self.calcular_totales)
        self.config_layout_totales(back_btn_size)
        self.main_layout.add_widget(self.btn_calcular_totales)
        self.main_layout.add_widget(self.layout_seleccion)
        self.main_layout.add_widget(self.layout_totales)

    def calcular_insulina(self, instance):
        back_btn_size = (self.main_layout.size[0] * 0.5, self.main_layout.size[1] * 0.1)


        self.layout_insulina = GridLayout(cols = 2)



        insulina_desayuno = Label(text = "Insulina desayuno: ", height=back_btn_size[1]*0.5,size_hint_y=None)
        insulina_desayuno_boton = Button(text= "Unidades desayuno", height=back_btn_size[1]*0.5,size_hint_y=None)
        insulina_comida = Label(text="Insulina comida: ", height=back_btn_size[1]*0.5,size_hint_y=None)
        insulina_comida_boton = Button(text= "Unidades comida", height=back_btn_size[1]*0.5,size_hint_y=None)
        insulina_cena = Label(text="Insulina cena: ", height=back_btn_size[1]*0.5,size_hint_y=None)
        insulina_cena_boton = Button(text="Unidades cena", height=back_btn_size[1]*0.5,size_hint_y=None, on_press = self.add_widget_cena)



        self.layout_insulina.add_widget(insulina_desayuno)
        self.layout_insulina.add_widget(insulina_desayuno_boton)

        self.layout_insulina.add_widget(insulina_comida)
        self.layout_insulina.add_widget(insulina_comida_boton)

        self.layout_insulina.add_widget(insulina_cena)
        self.layout_insulina.add_widget(insulina_cena_boton)

        self.main_layout.add_widget(self.layout_insulina)

    def add_widget_cena(self, instance):
        back_btn_size = (self.main_layout.size[0] * 0.5, self.main_layout.size[1] * 0.1)

        calorias, hc, azucares, proteinas, grasas = self.calcular_totales(instance)
        ratio_desayuno, ratio_comida, ratio_cena = self.leer_ratios()

        unidades_necesarias_desayuno = round(hc / 10 * ratio_desayuno, 2)
        unidades_necesarias_comida = round(hc / 10 * ratio_comida, 2)
        unidades_necesarias_cena = round(hc / 10 * ratio_cena, 2)
        insulina_desayuno_valor = Label(text=str(unidades_necesarias_desayuno) + " unidades",
                                        height=back_btn_size[1] * 0.5, size_hint_y=None)
        insulina_comida_valor = Label(text=str(unidades_necesarias_comida) + " unidades", height=back_btn_size[1] * 0.5,
                                      size_hint_y=None)
        self.insulina_cena_valor = Label(text=str(unidades_necesarias_cena) + " unidades", height=back_btn_size[1] * 0.5,
                                    size_hint_y=None)

        self.main_layout.add_widget(self.insulina_cena_valor)


    def leer_ratios(self):
        with open("ratios.json", 'r') as archivo:
            try:
                ratios_cargados = json.load(archivo)
            except json.JSONDecodeError:
                ratios_cargados = {}
            if ratios_cargados:
                ratio_desayuno = ratios_cargados["desayuno"]
                ratio_comida = ratios_cargados["comida"]
                ratio_cena = ratios_cargados["cena"]

        return round(float(ratio_desayuno),2), round(float(ratio_comida),2), round(float(ratio_cena),2)

    def config_layout_totales(self, back_btn_size):
        self.calorias = Label(text="Calorias totales:", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.calorias_value = Label(text="0", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.layout_totales.add_widget(self.calorias)
        self.layout_totales.add_widget(self.calorias_value)
        self.hc = Label(text="Hidratos de carbono totales:", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.hc_value = Label(text="0", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.layout_totales.add_widget(self.hc)
        self.layout_totales.add_widget(self.hc_value)
        self.azucares = Label(text="de los cuales azúcares:", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.azucares_value = Label(text="0", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.layout_totales.add_widget(self.azucares)
        self.layout_totales.add_widget(self.azucares_value)
        self.proteinas = Label(text="Proteinas totales:", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.proteinas_value = Label(text="0", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.layout_totales.add_widget(self.proteinas)
        self.layout_totales.add_widget(self.proteinas_value)
        self.grasas = Label(text="Grasas totales:", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.grasas_value = Label(text="0", height=back_btn_size[1] * 0.5, size_hint_y=None)
        self.layout_totales.add_widget(self.grasas)
        self.layout_totales.add_widget(self.grasas_value)



    def calcular_totales(self,instance):

        self.cantidades_receta = []

        for child in self.layout_seleccion.children:
            if type(child) == TextInput:
                self.cantidades_receta.append(float(child.text))

        calorias_count, hc_count, azucares_count, proteinas_count, grasas_count = 0,0,0,0,0
        for i in range(len(self.alimentos_seleccionados)):
            calorias_count += float(self.alimentos_seleccionados[i].calorias)*self.cantidades_receta[i]/100
            hc_count += float(self.alimentos_seleccionados[i].hc)*self.cantidades_receta[i]/100
            azucares_count += float(self.alimentos_seleccionados[i].azucares)*self.cantidades_receta[i]/100
            proteinas_count += float(self.alimentos_seleccionados[i].proteinas)*self.cantidades_receta[i]/100
            grasas_count += float(self.alimentos_seleccionados[i].grasas)*self.cantidades_receta[i]/100

        self.calorias_value.text = str(round(calorias_count, 2))
        self.hc_value.text = str(round(hc_count, 2))
        self.azucares_value.text = str(round(azucares_count,2))
        self.proteinas_value.text = str(round(proteinas_count,2))
        self.grasas_value.text = str(round(grasas_count,2))

        return calorias_count, hc_count, azucares_count, proteinas_count, grasas_count

    def seleccionar_alimento(self, alimento):
        self.alimentos_seleccionados.append(alimento)

    def back_btn_recetas(self, instance, *args):
        self.alimentos_seleccionados = []
        self.main_layout.remove_widget(self.back_btn)
        self.main_layout.remove_widget(self.layout_totales)
        self.main_layout.remove_widget(self.scroll_view)
        self.main_layout.add_widget(self.main_page)

    def back_btn_cantidades(self, instance, *args):
        self.main_layout.remove_widget(self.insulina_cena_valor)
        self.main_layout.remove_widget(self.btn_insulina)
        self.main_layout.remove_widget(self.layout_insulina)
        self.main_layout.remove_widget(self.back_btn_cant)
        self.main_layout.remove_widget(self.btn_calcular_totales)
        self.main_layout.remove_widget(self.layout_seleccion)
        self.main_layout.remove_widget(self.layout_totales)
        self.main_layout.add_widget(self.back_btn)
        self.main_layout.add_widget(self.scroll_view)