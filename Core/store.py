"""Estado compartido app <-> servicio (procesos distintos): un archivo con la última vez que te vio."""
import os, time

try:
    from core.punish import _ctx, ANDROID
except Exception:
    ANDROID = False


def data_dir():
    return _ctx().getFilesDir().getAbsolutePath() if ANDROID else "/tmp"


def _f():
    return os.path.join(data_dir(), "last_seen.txt")


def mark_seen():
    """La app la llama al abrirse y cada vez que escribes."""
    with open(_f(), "w") as f:
        f.write(str(time.time()))


def read_seen():
    try:
        return float(open(_f()).read())
    except Exception:
        return time.time()   # sin archivo: no castigar de golpe
