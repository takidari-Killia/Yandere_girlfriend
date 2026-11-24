"""Castigo reversible: brillo, volumen de llamada y notificación.
Solo funciona en Android; fuera de él simula (para poder probar la lógica)."""
import json, os

try:
    from jnius import autoclass
    PS = autoclass("org.kivy.android.PythonService")
    PA = autoclass("org.kivy.android.PythonActivity")
    ANDROID = True
except Exception:
    ANDROID = False

CHANNEL = "yandere_ch"


def _ctx():
    # En el servicio existe mService; en la app, mActivity.
    return PS.mService or PA.mActivity


class Punisher:
    def __init__(self, store="/tmp/yandere_orig.json"):
        self.store = store
        self.log = []

    # ---- aplicar ----
    def apply(self):
        if os.path.exists(self.store):   # ya castigado: no pisar originales
            return self.log
        if not ANDROID:
            self.log.append("simulado: brillo=0, volumen_llamada=0")
            json.dump({"b": 120, "v": 5}, open(self.store, "w"))
            return self.log
        ctx = _ctx()
        S = autoclass("android.provider.Settings$System")
        res = ctx.getContentResolver()
        orig = {}
        if autoclass("android.provider.Settings").System.canWrite(ctx):
            orig["b"] = S.getInt(res, "screen_brightness", 120)
            orig["m"] = S.getInt(res, "screen_brightness_mode", 1)
            S.putInt(res, "screen_brightness_mode", 0)
            S.putInt(res, "screen_brightness", 1)
            self.log.append("brillo bajado")
        else:
            self.log.append("falta permiso WRITE_SETTINGS")
        am = ctx.getSystemService("audio")
        try:
            orig["v"] = am.getStreamVolume(0)   # 0 = STREAM_VOICE_CALL
            am.setStreamVolume(0, 0, 0)
            self.log.append("volumen de llamada a 0")
        except Exception as e:
            self.log.append("volumen falló: %s" % e)
        json.dump(orig, open(self.store, "w"))
        return self.log

    # ---- revertir (botón "perdonar") ----
    def restore(self):
        if not os.path.exists(self.store):
            return
        orig = json.load(open(self.store))
        if ANDROID:
            ctx = _ctx()
            S = autoclass("android.provider.Settings$System")
            res = ctx.getContentResolver()
            if "b" in orig:
                S.putInt(res, "screen_brightness", orig["b"])
                S.putInt(res, "screen_brightness_mode", orig.get("m", 1))
            if "v" in orig:
                ctx.getSystemService("audio").setStreamVolume(0, orig["v"], 0)
        os.remove(self.store)

    # ---- notificación ----
    def notify(self, text, title="💔", nid=1):
        if not ANDROID:
            self.log.append("notif: " + text)
            return
        ctx = _ctx()
        NM = autoclass("android.app.NotificationManager")
        mgr = ctx.getSystemService("notification")
        Build = autoclass("android.os.Build$VERSION")
        if Build.SDK_INT >= 26:
            Ch = autoclass("android.app.NotificationChannel")
            mgr.createNotificationChannel(Ch(CHANNEL, "Ella", NM.IMPORTANCE_HIGH))
            b = autoclass("android.app.Notification$Builder")(ctx, CHANNEL)
        else:
            b = autoclass("android.app.Notification$Builder")(ctx)
        b.setSmallIcon(ctx.getApplicationInfo().icon)
        b.setContentTitle(title).setContentText(text).setAutoCancel(True)
        mgr.notify(nid, b.build())
