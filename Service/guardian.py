import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.mood import Mood
from core.punish import Punisher
from core.store import data_dir, read_seen

COOLDOWN = 120   # segundos entre notificaciones
PERIODO = 10     # cada cuánto revisa


def tick(m, p, st):
    m.last_seen = read_seen()
    s = m.state()
    now = time.time()
    if s == "enojada":
        p.apply()                      # idempotente: no repite si ya castigó
    if s != "dulce" and now - st["t"] >= COOLDOWN:
        p.notify(m.reply())
        st["t"] = now
    return s


def main():
    m = Mood()
    p = Punisher(os.path.join(data_dir(), "orig.json"))
    st = {"t": 0}
    while True:
        try:
            tick(m, p, st)
        except Exception:
            pass                        # el servicio nunca debe morir por un fallo
        time.sleep(PERIODO)


main()
