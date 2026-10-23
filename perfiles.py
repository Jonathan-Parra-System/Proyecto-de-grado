from xml.sax.saxutils import escape


_AVATARES = (
    ("avatar-hombre-1", "Hombre · piel clara", "#f1c7a5", "#50362d", "#233c68", "short"),
    ("avatar-hombre-2", "Hombre · piel media", "#c6865b", "#211b18", "#4b7b5c", "curly"),
    ("avatar-hombre-3", "Hombre · piel oscura", "#74452f", "#171514", "#684d83", "short"),
    ("avatar-hombre-4", "Hombre · piel oliva", "#d3a17c", "#8b542e", "#467b83", "wavy"),
    ("avatar-hombre-5", "Hombre · piel morena", "#a76b4a", "#30251f", "#526d37", "curly"),
    ("avatar-hombre-6", "Hombre · piel clara", "#e0b48d", "#b88945", "#45698a", "wavy"),
    ("avatar-mujer-1", "Mujer · piel clara", "#f1c7a5", "#50362d", "#233c68", "long"),
    ("avatar-mujer-2", "Mujer · piel media", "#c6865b", "#211b18", "#4b7b5c", "curly-long"),
    ("avatar-mujer-3", "Mujer · piel oscura", "#74452f", "#171514", "#684d83", "long"),
    ("avatar-mujer-4", "Mujer · piel oliva", "#d3a17c", "#8b542e", "#467b83", "wavy"),
    ("avatar-mujer-5", "Mujer · piel morena", "#a76b4a", "#30251f", "#526d37", "curly-long"),
    ("avatar-mujer-6", "Mujer · piel clara", "#e0b48d", "#b88945", "#45698a", "long"),
)

AVATARES = tuple(
    {"id": avatar[0], "nombre": avatar[1]}
    for avatar in _AVATARES
)
_AVATARES_POR_ID = {avatar[0]: avatar for avatar in _AVATARES}
AVATAR_PREDETERMINADO = AVATARES[0]["id"]


def avatar_valido(avatar_id):
    return avatar_id in _AVATARES_POR_ID


def obtener_avatar(avatar_id):
    return _AVATARES_POR_ID.get(avatar_id, _AVATARES_POR_ID[AVATAR_PREDETERMINADO])


def generar_avatar_svg(avatar_id):
    avatar_id, etiqueta, piel, cabello, ojos, estilo = obtener_avatar(avatar_id)
    if estilo == "short":
        pelo = f'<path d="M25 42c0-20 12-31 27-31s27 11 27 31l-8 8H33z" fill="{cabello}"/>'
    elif estilo == "curly":
        pelo = "".join(
            f'<circle cx="{x}" cy="{y}" r="10" fill="{cabello}"/>'
            for x, y in ((34, 31), (45, 20), (59, 18), (72, 25), (78, 38))
        )
    elif estilo in {"long", "curly-long"}:
        pelo = f'<path d="M23 44c0-24 13-35 29-35s29 11 29 35v48l-13-9-5-32H41l-5 32-13 9z" fill="{cabello}"/>'
        if estilo == "curly-long":
            pelo += "".join(
                f'<circle cx="{x}" cy="{y}" r="8" fill="{cabello}"/>'
                for x, y in ((31, 28), (41, 13), (57, 10), (72, 17), (80, 31))
            )
    else:
        pelo = f'<path d="M23 43c2-24 15-34 30-34 18 0 30 14 29 35-8-2-12-8-17-14-8 10-23 16-42 17z" fill="{cabello}"/>'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" role="img" aria-label="{escape(etiqueta)}">
<rect width="100" height="120" rx="16" fill="#e7efe7"/>
<path d="M12 120c2-25 16-37 38-37s36 12 38 37" fill="#397568"/>
{pelo}
<path d="M30 46c0-19 9-29 20-29s20 10 20 29v13c0 17-9 28-20 28S30 76 30 59z" fill="{piel}"/>
<path d="M37 51h8m10 0h8" stroke="{cabello}" stroke-width="3" stroke-linecap="round"/>
<circle cx="41" cy="55" r="2.5" fill="{ojos}"/><circle cx="59" cy="55" r="2.5" fill="{ojos}"/>
<path d="M45 69c3 3 7 3 10 0" fill="none" stroke="#8f4e4b" stroke-width="2.5" stroke-linecap="round"/>
<path d="M50 58v6" stroke="#bd8668" stroke-width="2" stroke-linecap="round"/>
</svg>"""
