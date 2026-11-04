#!/usr/bin/env python3
"""Pruebas de las cuentas de plata de Receater.

Carga tests/fixture.json (datos inventados que reproducen errores que ya pasaron), congela la hora
y compara lo que calcula la app con lo esperado. Correr antes de publicar:

    python3 tests/run.py          (levanta un servidor local solo)
"""
import json, pathlib, subprocess, sys, time, socket
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIX = json.loads((ROOT / "tests/fixture.json").read_text())
NOW = "2026-10-30T11:00:00-03:00"   # día de cobro, a la mañana

# (nombre, expresión JS, esperado, por qué importa)
CHECKS = [
  ("Saldo en cuentas", "teQuedaReal(viewYear, viewMonth).real", 2955000, "saldo + sueldo de hoy − gasto de la mañana − débito de la suscripción"),
  ("Tarjeta por pagar", "teQuedaReal(viewYear, viewMonth).card", 95000, "vence hoy, sin pagar: manda el total del resumen del banco, no lo anotado (100.000)"),
  ("Fijos sin pagar", "teQuedaReal(viewYear, viewMonth).fix", 300000, "el fijo en dólares pagado en pesos ya está pagado"),
  ("Te queda", "teQuedaReal(viewYear, viewMonth).left", 2560000, "cuentas − fijos − tarjeta"),
  ("Fijos pagados", "fixInstances(viewYear, viewMonth).filter(i => i.state === 'paid' || i.state === 'cardpaid').length", 1, "un fijo pagado en otra moneda cuenta como pagado"),
  ("Total de fijos", "Math.round(fixSummary(viewYear, viewMonth).total)", 340005, "300.000 + lo que pagaste de verdad por la suscripción en dólares (≈ $40.000; antes daba millones)"),
  ("Pagó el fijo en dólares", "fixInstance(data.fixed.find(f => f.id === 'f_usd'), viewYear, viewMonth).state", "paid", "pagado en pesos"),
  ("Compra después del cierre no vence hoy", "entries().filter(x => x.cardId && x.date.slice(0,10) === '2026-10-30').reduce((a,x) => a + x.amount, 0)", 100000, "la compra del 25 va al resumen siguiente"),
  ("Tarjeta en la lista: total del banco", "document.querySelector('#viewList').innerText.includes('95.000')", True, "Movimientos muestra lo que cobra el banco"),
]

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

def main():
    port = free_port()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8); bad = 0
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route("**/*", lambda r: r.abort() if not r.request.url.startswith(f"http://localhost:{port}") else r.continue_())
            pg.clock.install(time=NOW)
            pg.add_init_script("localStorage.clear();localStorage.setItem('gastos.v1',%s);localStorage.setItem('receater.lang','es');localStorage.setItem('receater.onb','1');localStorage.setItem('receater.setup','1');localStorage.setItem('receater.banner','1');localStorage.setItem('receater.newsSeen','999');" % json.dumps(json.dumps(FIX)))
            pg.goto(f"http://localhost:{port}/index.html"); pg.wait_for_timeout(1500)
            for name, js, want, why in CHECKS:
                try: got = pg.evaluate(js)
                except Exception as e: got = f"ERROR {e}".splitlines()[0]
                ok = (abs(got - want) < 0.5) if isinstance(want, (int, float)) and not isinstance(want, bool) and isinstance(got, (int, float)) else got == want
                bad += not ok
                print(("OK   " if ok else "FALLA"), name, "" if ok else f"→ dio {got}, tenía que dar {want} ({why})")
            if errs: bad += 1; print("FALLA errores de la página:", errs[:3])
            b.close()
    finally:
        srv.terminate()
    print("\n" + ("Todo bien." if not bad else f"{bad} cosas fallaron: no publicar."))
    sys.exit(1 if bad else 0)

if __name__ == "__main__": main()
