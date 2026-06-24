from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar

from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation


Window.size = (360, 640)


class LoadingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation="vertical",
            padding=30,
            spacing=18,
            md_bg_color=(0.05, 0.05, 0.08, 1)
        )

        layout.add_widget(MDLabel(size_hint_y=0.10))

        self.logo = AsyncImage(
            source="https://cdn-icons-png.flaticon.com/512/4727/4727424.png",
            size_hint=(0.80, 0.40),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            opacity=0
        )
        layout.add_widget(self.logo)

        layout.add_widget(MDLabel(
            text="CALCULADORA PRO",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=0.13
        ))

        layout.add_widget(MDLabel(
            text="Desarrollado por Alan Martinez",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0.75, 0.65, 1, 1),
            size_hint_y=0.08
        ))

        self.barra = MDProgressBar(
            value=0,
            max=100,
            size_hint_y=None,
            height=8
        )
        layout.add_widget(self.barra)

        self.texto_carga = MDLabel(
            text="Cargando... 0%",
            halign="center",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.8, 0.8, 0.9, 1),
            size_hint_y=0.08
        )
        layout.add_widget(self.texto_carga)

        self.add_widget(layout)
        self.progreso = 0

    def on_enter(self):
        self.animar_logo()
        Clock.schedule_interval(self.cargar, 0.1)

    def animar_logo(self):
        anim = (
            Animation(opacity=1, size_hint=(0.88, 0.46), duration=1) +
            Animation(size_hint=(0.78, 0.38), duration=1)
        )
        anim.repeat = True
        anim.start(self.logo)

    def cargar(self, dt):
        if self.progreso < 30:
            self.progreso += 1.5
        elif self.progreso < 70:
            self.progreso += 0.8
        else:
            self.progreso += 0.3

        if self.progreso >= 100:
            self.progreso = 100

        self.barra.value = self.progreso
        self.texto_carga.text = f"Cargando... {int(self.progreso)}%"

        if self.progreso >= 100:
            Clock.unschedule(self.cargar)
            self.manager.current = "calculadora"


class CalculadoraScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.operacion = ""

        main = MDBoxLayout(
            orientation="vertical",
            padding=15,
            spacing=12,
            md_bg_color=(0.05, 0.05, 0.08, 1)
        )

        self.pantalla = MDLabel(
            text="0",
            halign="right",
            font_style="H2",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=0.30
        )
        main.add_widget(self.pantalla)

        botones = [
            ["C", "DEL", "÷", "×"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "="],
            ["0", "."]
        ]

        for fila in botones:
            row = MDBoxLayout(spacing=10, size_hint_y=0.14)

            for texto in fila:
                btn = MDRaisedButton(
                    text=texto,
                    font_size=26,
                    size_hint=(1, 1),
                    md_bg_color=self.color_boton(texto),
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    elevation=8
                )
                btn.bind(on_release=self.click)
                row.add_widget(btn)

            main.add_widget(row)

        self.add_widget(main)

    def color_boton(self, texto):
        if texto in ["+", "-", "×", "÷", "="]:
            return (0.45, 0.20, 0.90, 1)
        if texto in ["C", "DEL"]:
            return (0.90, 0.20, 0.35, 1)
        return (0.15, 0.15, 0.22, 1)

    def click(self, boton):
        texto = boton.text

        if texto == "C":
            self.operacion = ""
            self.pantalla.text = "0"

        elif texto == "DEL":
            self.operacion = self.operacion[:-1]
            self.pantalla.text = self.operacion if self.operacion else "0"

        elif texto == "=":
            try:
                cuenta = self.operacion.replace("×", "*").replace("÷", "/")
                resultado = str(eval(cuenta))
                self.pantalla.text = resultado
                self.operacion = resultado
            except:
                self.pantalla.text = "Error"
                self.operacion = ""

        else:
            self.operacion += texto
            self.pantalla.text = self.operacion


class CalculadoraApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"

        sm = MDScreenManager()
        sm.add_widget(LoadingScreen(name="loading"))
        sm.add_widget(CalculadoraScreen(name="calculadora"))
        return sm


CalculadoraApp().run()