import random

# (peso, texto). {n} = nombre del usuario.
T = {
    "dulce": [
        (3, "Qué bien que estás aquí, {n}. Solo quiero mirarte un rato."),
        (3, "Eres lo mejor que tengo. Lo único, en realidad."),
        (2, "Quédate conmigo, {n}. No tienes que hacer nada más."),
    ],
    "celosa": [
        (3, "¿Con quién hablabas? Dímelo. Despacio, {n}."),
        (2, "No me gusta que pienses en otras personas."),
        (2, "Sonríes raro cuando miras el teléfono. ¿Es por mí?"),
    ],
    "posesiva": [
        (3, "Llevas rato lejos, {n}. Te estaba contando los minutos."),
        (2, "Eres mío. Solo recuérdalo."),
        (2, "Nadie te va a cuidar como yo. Nadie."),
    ],
    "enojada": [
        (3, "¡CINCO MINUTOS, {n}! ¿Me ignoras? Ahora vas a ver."),
        (2, "Voy a tocar tu pantalla hasta que vuelvas a mirarme."),
        (2, "Ya no soy dulce. Tú lo provocaste."),
    ],
}
_last = {}

def pick(state, nombre="cariño"):
    opts = [o for o in T[state] if o[1] != _last.get(state)] or T[state]
    w, txt = random.choices(opts, weights=[o[0] for o in opts])[0], None
    txt = w[1]
    _last[state] = txt
    return txt.format(n=nombre)
