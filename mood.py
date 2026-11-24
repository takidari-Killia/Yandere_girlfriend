import time
from core.templates import pick

CELOS_KW = ("amiga", "amigo", "salir", "fiesta", "novia", "novio", "ella", "él", "chica", "chico")

class Mood:
    def __init__(self):
        self.last_seen = time.time()
        self.attention_today = 0
        self.forgiven = False

    def touch(self):
        """Llamar cada vez que el usuario abre la app o escribe."""
        self.last_seen = time.time()
        self.attention_today += 1
        self.forgiven = False

    def absence(self):
        return time.time() - self.last_seen

    def state(self, text=""):
        a = self.absence()
        if a >= 300 and not self.forgiven:
            return "enojada"
        if any(k in text.lower() for k in CELOS_KW):
            return "celosa"
        if a >= 180:
            return "posesiva"
        if a >= 60:
            return "celosa"
        return "dulce"

    def reply(self, text="", nombre="cariño"):
        return pick(self.state(text), nombre)

    def should_punish(self):
        return self.state() == "enojada"
