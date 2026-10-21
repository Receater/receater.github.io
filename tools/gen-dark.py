#!/usr/bin/env python3
"""Genera el modo oscuro de Receater.

Lee el CSS de index.html (sin el bloque oscuro anterior), y por cada regla con colores
escribe la misma regla bajo :root[data-theme="dark"] con los colores pasados a oscuro
(en OKLab: los claros se oscurecen, la tinta se aclara, los colores vivos quedan).
Lo escribe entre /*DARK-START*/ y /*DARK-END*/. Correr después de tocar estilos:

    python3 tools/gen-dark.py
"""
import re, sys, math, pathlib
import tinycss2

P = pathlib.Path(__file__).resolve().parent.parent / "index.html"
SRC = P.read_text()
START, END = "/*DARK-START*/", "/*DARK-END*/"
css_open = SRC.index("<style>") + len("<style>")
css_close = SRC.index("</style>")
CSS = SRC[css_open:css_close]
CSS_NO_DARK = re.sub(re.escape(START) + r".*?" + re.escape(END), "", CSS, flags=re.S)

# ---------- color ----------
def srgb2lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def lin2srgb(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def to_oklab(r, g, b):
    r, g, b = srgb2lin(r), srgb2lin(g), srgb2lin(b)
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l, m, s = l ** (1/3), m ** (1/3), s ** (1/3)
    return (0.2104542553*l + 0.7936617850*m - 0.0040720468*s,
            1.9779984951*l - 2.4285922050*m + 0.4505937099*s,
            0.0259040371*l + 0.7827717662*m - 0.8086757660*s)
def from_oklab(L, a, b):
    l = (L + 0.3963377774*a + 0.2158037573*b) ** 3
    m = (L - 0.1055613458*a - 0.0638541728*b) ** 3
    s = (L - 0.0894841775*a - 1.2914855480*b) ** 3
    return (lin2srgb(4.0767416621*l - 3.3077115913*m + 0.2309699292*s),
            lin2srgb(-1.2684380046*l + 2.6097574011*m - 0.3413193965*s),
            lin2srgb(-0.0041960863*l - 0.7034186147*m + 1.7076147010*s))

def darken(r, g, b, shadow=False, text=False, bg=False):
    L, A, B = to_oklab(r, g, b)
    C = math.hypot(A, B)
    if shadow and L < 0.6: return (r, g, b)          # sombras oscuras: quedan
    if text and L > 0.80: return (r, g, b)             # texto claro: va sobre color, queda
    if L > 0.80:   L2, k = 0.21 + (1 - L) * 0.85, 0.55   # papel / fondos claros
    elif L < 0.42 and C >= 0.04 and not text: return (r, g, b)   # madera y oscuros con color: quedan
    elif L < 0.42 and bg: L2, k = 0.36, 0.6                 # botones negros: gris oscuro levantado
    elif L < 0.42: L2, k = 0.93 - L * 0.35, 0.8         # tinta
    elif C < 0.05: L2, k = 1.12 - L, 0.8                # grises medios (bordes, texto suave)
    else:          L2, k = (max(L, 0.66) if text else L * 0.92), 0.95  # vivos: texto más claro, fondos igual
    return from_oklab(L2, A * k, B * k)

def hx(v): return int(v, 16) / 255
def fmt(rgb, a=None):
    r, g, b = (round(max(0, min(1, x)) * 255) for x in rgb)
    if a is None or a >= 1: return "#%02X%02X%02X" % (r, g, b)
    return "rgba(%d,%d,%d,%s)" % (r, g, b, ("%.3f" % a).rstrip("0").rstrip("."))

def lum(tok):
    t = tok.lower()
    if t == "white": return 1
    if t == "black": return 0
    if t.startswith("#"):
        h = t[1:]
        if len(h) in (3, 4): h = "".join(c * 2 for c in h)
        return to_oklab(hx(h[0:2]), hx(h[2:4]), hx(h[4:6]))[0]
    n = re.findall(r"[\d.]+", t)
    return to_oklab(*(float(x) / 255 for x in n[:3]))[0] if len(n) >= 3 else 0
COLOR_RE = re.compile(r"#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3,4}\b|rgba?\([^)]*\)|\b(?:white|black)\b")
def conv_color(tok, shadow, text=False, bg=False):
    t = tok.lower()
    a = None
    if t == "white": rgb = (1, 1, 1)
    elif t == "black": rgb = (0, 0, 0)
    elif t.startswith("#"):
        h = t[1:]
        if len(h) in (3, 4): h = "".join(c * 2 for c in h)
        rgb = (hx(h[0:2]), hx(h[2:4]), hx(h[4:6]))
        if len(h) == 8: a = int(h[6:8], 16) / 255
    else:
        nums = re.findall(r"[\d.]+%?", t)
        if len(nums) < 3: return tok
        rgb = tuple(float(n) / 255 for n in nums[:3])
        if len(nums) > 3: a = float(nums[3].rstrip("%")) / (100 if nums[3].endswith("%") else 1)
    if a is not None and a < 1 and not text and to_oklab(*rgb)[0] < 0.42: return tok   # velos/sombras oscuras: quedan
    return fmt(darken(*rgb, shadow=shadow, text=text, bg=bg), a)

COLOR_PROPS = ("color", "background", "background-color", "background-image", "border", "border-color",
    "border-top", "border-bottom", "border-left", "border-right", "border-top-color", "border-bottom-color",
    "border-left-color", "border-right-color", "outline", "outline-color", "box-shadow", "text-shadow",
    "fill", "stroke", "caret-color", "text-decoration-color", "accent-color", "filter", "column-rule",
    "-webkit-text-fill-color", "scrollbar-color")
SHADOWY = ("box-shadow", "text-shadow", "filter")
TEXTY = ("color", "fill", "-webkit-text-fill-color", "caret-color", "text-decoration-color")

def conv_decl(name, value):
    name_l = name.lower()
    if name_l == "color-scheme": return "dark" if "light" in value else None
    if not (name_l.startswith("--") or name_l in COLOR_PROPS): return None
    if "url(" in value and not COLOR_RE.search(value.split("url(")[0]): return None
    out = COLOR_RE.sub(lambda m: conv_color(m.group(0), name_l in SHADOWY, name_l in TEXTY, name_l.startswith("background")), value)
    return out if out != value else None

SKIP_SEL = re.compile(r'data-theme|#scene|(?:^|[\s>,])\.recy\b|recy-svg|\.lt-bar i|\.cat-dot|\.dot\b|::selection')
def prefix(sel):
    out = []
    for s in sel.split(","):
        s = s.strip()
        if not s: continue
        if s in (":root", "html"): out.append(':root[data-theme="dark"]')
        elif s.startswith(":root"): out.append(':root[data-theme="dark"]' + s[5:])
        elif s.startswith("html"): out.append(':root[data-theme="dark"]' + s[4:])
        else: out.append(':root[data-theme="dark"] ' + s)
    return ",".join(out)

def walk(rules, out, in_dark_media=False):
    for r in rules:
        if r.type == "at-rule" and r.lower_at_keyword == "media":
            pre = tinycss2.serialize(r.prelude).strip()
            if "prefers-color-scheme" in pre: continue
            if r.content is None: continue
            inner = []
            walk(tinycss2.parse_rule_list(r.content, skip_comments=True, skip_whitespace=True), inner)
            if inner: out.append("@media " + pre + "{" + "".join(inner) + "}")
        elif r.type == "qualified-rule":
            sel = tinycss2.serialize(r.prelude).strip()
            if SKIP_SEL.search(sel) or sel == ":root": continue
            decls = tinycss2.parse_declaration_list(r.content, skip_comments=True, skip_whitespace=True)
            body, light_bg = [], False
            for d in decls:
                if d.type != "declaration": continue
                v = tinycss2.serialize(d.value).strip()
                nv = conv_decl(d.name, v)
                if d.name.lower() in ("background", "background-color") and nv:
                    cs = COLOR_RE.findall(nv)
                    if cs and lum(cs[-1]) > 0.6: light_bg = True
                if nv is not None: body.append([d.name, nv])
            body = [f"{n}:{v} !important" for n, v in body]
            if body: out.append(prefix(sel) + "{" + ";".join(body) + "}")

out = []
walk(tinycss2.parse_stylesheet(CSS_NO_DARK, skip_comments=True, skip_whitespace=True), out)
block = START + "\n" + "\n".join(out) + "\n" + END
if START in CSS:
    NEW = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, CSS, flags=re.S)
else:
    NEW = CSS.rstrip() + "\n" + block + "\n"
P.write_text(SRC[:css_open] + NEW + SRC[css_close:])
print(f"{len(out)} reglas oscuras")
