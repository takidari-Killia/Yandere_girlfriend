import os
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.utils import platform
from core.mood import Mood
from core.punish import Punisher
from core.store import mark_seen, data_dir

EMOJI = {"dulce": "🥰", "celosa": "👀", "posesiva": "🖤", "enojada": "😡"}


def pedir_permisos():
    if platform != "android":
        return
    from android.permissions import request_permissions
    request_permissions(["android.permission.POST_NOTIFICATIONS"])
    from jnius import autoclass
    PA = autoclass("org.kivy.android.PythonActivity")
    act = PA.mActivity
    Settings = autoclass("android.provider.Settings")
    if not Settings.System.canWrite(act):   # permiso de brillo: se concede a mano
        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")
        i = Intent(Settings.ACTION_MANAGE_WRITE_SETTINGS)
        i.setData(Uri.parse("package:" + act.getPackageName()))
        act.startActivity(i)


def lanzar_servicio():
    if platform != "android":
        return
    from jnius import autoclass
    PA = autoclass("org.kivy.android.PythonActivity")
    act = PA.mActivity
    # nombre del servicio en buildozer.spec: guardian -> ServiceGuardian
    autoclass(act.getPackageName() + ".ServiceGuardian").start(act, "")


class Root(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", **kw)
        self.mood = Mood()
        self.punisher = Punisher(os.path.join(data_dir(), "orig.json"))

        self.avatar = Image(size_hint_y=0.35)
        self.emoji = Label(text="🥰", font_size="80sp", size_hint_y=0.35)
        self.add_widget(self.emoji)

        self.counter = Label(text="Atención hoy: 0", size_hint_y=0.07)
        self.add_widget(self.counter)

        sv = ScrollView()
        self.chat = Label(text="", size_hint_y=None, halign="left", valign="top",
                          markup=True, padding=(10, 10))
        self.chat.bind(width=lambda *a: setattr(self.chat, "text_size", (self.chat.width, None)),
                       texture_size=lambda *a: setattr(self.chat, "height", self.chat.texture_size[1]))
        sv.add_widget(self.chat)
        self.sv = sv
        self.add_widget(sv)

        row = BoxLayout(size_hint_y=0.1)
        self.inp = TextInput(multiline=False, hint_text="Escríbele...")
        self.inp.bind(on_text_validate=self.enviar)
        row.add_widget(self.inp)
        row.add_widget(Button(text="Enviar", size_hint_x=0.25, on_release=self.enviar))
        self.add_widget(row)
        self.add_widget(Button(text="Perdonar (restaurar todo)", size_hint_y=0.08,
                               on_release=self.perdonar))

        self.decir(self.mood.reply())
        Clock.schedule_interval(self.refrescar, 2)

    def decir(self, txt, quien="Ella"):
        self.chat.text += "\n[b]%s:[/b] %s" % (quien, txt)
        Clock.schedule_once(lambda dt: setattr(self.sv, "scroll_y", 0), 0.1)

    def tocar(self):
        self.mood.touch()
        mark_seen()
        self.counter.text = "Atención hoy: %d" % self.mood.attention_today

    def enviar(self, *a):
        t = self.inp.text.strip()
        if not t:
            return
        self.inp.text = ""
        self.tocar()
        self.decir(t, "Tú")
        self.decir(self.mood.reply(t))
        self.refrescar()

    def perdonar(self, *a):
        self.mood.forgiven = True
        self.punisher.restore()
        mark_seen()
        self.decir("...Está bien. Pero no lo vuelvas a hacer.")

    def refrescar(self, *a):
        s = self.mood.state()
        self.emoji.text = EMOJI[s]   # luego: cambiar por sprites en assets/avatar/


class YandereApp(App):
    def build(self):
        pedir_permisos()
        lanzar_servicio()
        r = Root()
        r.tocar()
        self.root_w = r
        return r

    def on_pause(self):
        return True

    def on_resume(self):
        self.root_w.tocar()


YandereApp().run()
