# CONTEXTO — Receater

**Última actualización:** 18 de octubre de 2026 (build `2026-10-20.1330`)

Este archivo explica Receater para quien no estuvo en las charlas donde se armó. Cada vez que se cambie algo de la app, se actualiza acá en el mismo commit.

---

## 1. Qué es y qué hace

Receater es una app web (PWA, un solo `index.html`) para anotar gastos, ingresos y ahorros en Argentina (pesos y dólares). La mascota es **Recy**, una trituradora de papel azul que "se come" los tickets. Está toda en castellano rioplatense, sin servidor propio: los datos quedan en el celu y, si el usuario quiere, en su propio Google Drive.

**Funciones actuales**
- **Movimientos**:
  - Cargar gastos e ingresos a mano, contándole a Recy con palabras o con foto del ticket (IA).
  - Gastos con productos del ticket (`items`), cada producto con su categoría.
  - Medios de pago: efectivo, débito, transferencia y tarjeta de crédito (con cuotas y cuotas ya pagadas).
  - Gastos divididos con otras personas ("me deben"), préstamos dados y recibidos.
  - Compra de dólares (con cotización) y pago de tarjetas en pesos y/o dólares.
  - "Lo de siempre": atajos con los gastos que se repiten (3 o más veces en 3 meses).
  - Recy sugiere la categoría según lo que se cargó antes con ese nombre. El usuario confirma.
- **Mes de cobro a cobro**: el período va de un cobro al siguiente (día fijo, último día hábil o sin día fijo), no del 1 al 30.
- **Resumen** ("El Diario de Recy"):
  - Torta por categoría y topes por categoría.
  - "Datos del mes" y "Qué días gastás más" (por día de la semana).
  - Tarjetas: lo que vence, el resumen del banco (subir PDF/foto, Recy lo lee) y "Cuotas que vienen" para los próximos 6 meses.
  - Gráfico de los últimos 6 meses.
  - Cierre del mes, inflación (INDEC) vs. sueldo e imagen del mes para compartir o descargar.
  - Secciones plegables.
- **Fijos**: gastos mensuales (manual, débito automático o con tarjeta, en $ o US$) con estado pagado, por pagar, vencido o en tarjeta. Torta "Fijos vs. sueldo".
- **Ahorros**:
  - Frascos en $ o US$, cada uno con color, meta y fecha objetivo.
  - Historial de movimientos y valor en pesos al dólar del día.
  - Frascos en pesos vs. inflación.
  - **"¿Cuánto puedo ahorrar?"**: sueldo − tarjeta que vence − fijos sin tarjeta − gastos varios del mes, más los próximos 3 meses, una meta mensual (en $ o US$), el botón "separar en un frasco" con el monto ya puesto y el simulador "¿y si…?".
- **Dólar siempre visible** arriba (blue y oficial; al tocarlo muestra todas las cotizaciones).
- **Avisos en el celu sin servidor**: vencimientos de tarjeta y fijos, día de cobro, préstamos y un recordatorio a las 21 si ese día no se cargó nada.
- **Guía de inicio (onboarding)**: explica la app y carga sueldo, cuándo cobra, gastos varios, fijos, tarjetas y Drive.
- **Exportar** a Excel y backup JSON. Importar backup.
- **Páginas legales**: `privacidad.html` y `terminos.html`.

## 2. Cómo se usa

- **Tabs** (un estante de madera arriba): **Movimientos**, **Resumen**, **Fijos** y **Ahorros**. Debajo hay un calendario rojo para cambiar de mes (en Ahorros: Total, mes o día).
- **Pizarra de Recy**: arriba de cada tab hay una pizarra con el número principal y renglones de colores. Recy está al lado con un globito de diálogo.
  - **Estados de Recy**: contento, preocupado o asustado según cómo vas. Al cargar un gasto hace la animación de "triturar" el ticket.
  - **Tamaño**: todas las pizarras miden lo mismo (toman la más alta vista, guardada en `receater.lcdH.*`).
- **Botón principal de cada tab**:
  - Movimientos y Resumen: **"Darle a Recy"** (un ticket), que abre la hoja de carga.
  - Fijos: "+ Nuevo gasto fijo" (un post-it).
  - Ahorros: "+ Nuevo frasco" (una tapa de frasco).
- **Hoja de carga**: pestañas **Gasto / Ingreso / Dólares / Pagué tarjeta**.
  - Arriba: "Lo de siempre" y "Contale a Recy" (texto + **Sacar foto** / **Subir imagen** del ticket).
  - Después: monto, categoría, medio de pago, fecha y hora, dividir, préstamo, frasco y nota.
  - Lo que completa la IA siempre se revisa antes de guardar. Nunca se guarda solo.
- **Resumen**: los botones "Preguntale a Recy" (chat con IA sobre tus gastos) y "¿Me lo puedo comprar?" (simula una compra en cuotas a futuro).
- **Ajustes** (engranaje): cuenta de Google, cuándo cobrás, Recy inteligente (key de Gemini), avisos y recordatorio, personas, categorías, topes, exportar/importar, guía de inicio, privacidad y términos.

## 3. Diseño (respetar)

- **REGLA DE TOMAS: privacidad y términos siempre al día.** Cada vez que un cambio toque qué datos se usan, a qué servicio se conecta la app o qué se calcula, evaluar si `privacidad.html` y `terminos.html` necesitan agregarlo y actualizarlos en el mismo commit. La app nunca manda datos del usuario a servicios de terceros (salvo Google Drive y Gemini con su propia key, ya declarados); a los servicios públicos solo se les piden datos.

- **REGLA DE TOMAS: todo lo nuevo va con la interfaz de la app.** Nunca una tarjeta blanca "normal", un formulario genérico o un diálogo del navegador. Antes de agregar algo, copiá el estilo de lo que ya existe en esa pestaña (libreta con espiral como el Historial, post-it, ticket, frasco, `miniDialog`). Ejemplo: "Plata que rinde" usa las mismas reglas que `#jarGrowthCard`.

- **Estética**: objetos físicos ilustrados, planos y cálidos.
  - Las tabs son un estante de madera con cosas apoyadas.
  - Las hojas son de libreta: Courier Prime, renglones y bordes punteados.
  - Fijos es un post-it amarillo. Los frascos son de vidrio con tapa de color.
  - Resumen es un diario ("El Diario de Recy").
  - Las pizarras son de marcador.
- **Fondos ilustrados por tab** (SVG generado en JS, función `SCENES`):
  - Movimientos: almacén de barrio.
  - Resumen: calle tipo Nueva York.
  - Fijos: cocina con heladera llena de facturas.
  - Ahorros: biblioteca de madera chocolate con frascos.
  - Todos van apagados (opacidad ~.55–.7) para no competir con la interfaz.
- **Tipografías** (Google Fonts):
  - Bricolage Grotesque (display) e Instrument Sans (texto).
  - Courier Prime (libreta), IBM Plex Mono / VT323 (pizarra) y Playfair Display / Source Serif 4 (diario).
- **Paleta base**:
  - Tinta `#1B2430`, acento azul `#2F5BEA`, verde dólar `#1E7A50`/`#1E8A5B`, peligro `#C9374B`.
  - Papel `#FBF8F1`, crema `#F7F2E8`/`#EADFCB`, madera `#D7AE7E`/`#B4844F`.
  - Coral `#EE8A73`, amarillo `#F4C24E`, verde `#76C29B`, celeste `#8DB4E6`.
  - Los ✓ siempre van en verde `#1E7A50`.
- **Íconos**: **sin emojis en ninguna parte.** Solo Font Awesome Free, estilo solid, como sprite SVG embebido (`<symbol id="i-...">`, helper `ico(name)`). Toman el color y el tamaño del texto donde están.
- **Modo oscuro**: existe, pero los fondos ilustrados se mantienen claros (paletas fijas por escena).
- **Responsive**: todo tiene que entrar sin desbordar en 320, 360, 390, 430, 768, 820, 1024, 1100, 1280 y 1440 px.
- **Versión de escritorio (≥1100 px)**: mismo contenido en dos columnas (el JS arma `.vcol-l`/`.vcol-r` en cada tab y `.pcol-a`/`.pcol-b` en el diario; en el celu son `display:contents`). Izquierda (queda fija al scrollear solo si entra entera en la pantalla, `fitLeftCol()`): pizarra de Recy y extras. Derecha: lista principal (movimientos, diario en 2 columnas, fijos, frascos). Arriba, una barra fija con logo, dólar y Ajustes. El botón principal (Darle a Recy / Nuevo fijo / Nuevo frasco) queda abajo, como en el celu (Tomas no lo quiere arriba). Ancho máx. 1240 px.
- **Textos**: cortos, claros, en voseo rioplatense, sin tono de IA.

## 4. Datos

**Dónde se guarda**
- **localStorage**: clave `gastos.v1`, todo el objeto de datos.
- **Google Drive** (opcional, al "Entrar con Google"): archivo **`receater-data.json`** en la **raíz de "Mi unidad"** del usuario, sin carpeta. Si hay varios, se usa el más reciente. Se sincroniza comparando `updatedAt`.
- **Scope**: `https://www.googleapis.com/auth/drive.file`. La app solo ve los archivos que creó ella.
- **Client ID OAuth**: `691647478531-gcdud7lg66o2su8v3mbmmu7if96449st.apps.googleusercontent.com`.
  - Es el mismo proyecto de Google Cloud que se usó para Artdeas/Ideary.
  - No es secreto, pero solo funciona desde orígenes autorizados. Hoy está autorizado `https://receater.github.io`.
  - Para otra app con el mismo Client ID hay que agregar su origen en *APIs y servicios → Credenciales → Orígenes autorizados de JavaScript*.
- **Login**: Google Identity Services (token client). El token dura ~1 hora. Si vence, la app se bloquea con el cartel "Reconectar" hasta que el usuario toca (sin servidor no hay refresh token).

**Estructura del JSON** (datos de mentira; hay más campos opcionales)
```json
{
  "updatedAt": 1760670000000,
  "payRule": "lb",
  "expenses": [{
    "id": "a1b2c3", "type": "expense", "amount": 48250.5, "currency": "ARS",
    "category": "super", "date": "2026-10-15T18:42", "note": "Coto",
    "source": "ticket", "method": "debit", "cardId": null,
    "installments": 1, "paidInstallments": 0, "split": null, "loan": false, "jarId": null,
    "items": [
      { "name": "Leche La Serenísima 1L", "price": 1850, "category": "super" },
      { "name": "Pan lactal Bimbo", "price": 3200, "category": "super" },
      { "name": "Detergente Magistral", "price": 2900, "category": "casa" }
    ]
  }],
  "incomes": [{ "id": "i1", "type": "income", "amount": 1500000, "currency": "ARS", "category": "sueldo", "date": "2026-09-30T09:00", "note": "Sueldo" }],
  "fixed": [{ "id": "f1", "name": "Alquiler", "category": "casa", "currency": "ARS", "amount": 350000, "day": 10, "how": "manual", "start": "2026-01", "end": null, "history": [], "monthAmounts": {} }],
  "cards": [{ "id": "c1", "name": "Visa Galicia", "color": "#2F5BEA", "closeDay": 24, "rule": "due", "day": 5 }],
  "cardPayments": [{ "cardId": "c1", "date": "2026-10-05", "amount": 498061.47, "usd": 18.75 }],
  "jars": [{ "id": "j1", "name": "Viaje", "currency": "ARS", "goal": 5000000, "goalBy": "2027-06", "color": "#E08A2C" }],
  "jarMoves": [{ "id": "m1", "jarId": "j1", "date": "2026-10-01", "amount": 100000, "kind": "deposit", "note": "" }],
  "customCats": [], "budgets": { "super": 800000 }, "merchantCats": { "COTO": "super" },
  "dailyBudget": 400000, "saveGoal": 300000, "saveGoalCur": "ARS",
  "aiKey": "AIza…(key de Gemini del usuario)"
}
```
- **Fechas**: `date` va en hora local `YYYY-MM-DDTHH:mm`, sin zona horaria.
- **Gasto de súper**: `category: "super"`.
- **Productos del ticket**: van en `items` (`name`, `price` final y `category`). Solo existen si el gasto vino de un ticket o se cargaron a mano; si no, `items: []`.
- **Origen del gasto** (`source`): `manual`, `ticket` o `statement` (resumen de tarjeta).
- **Ingresos**: `type: "income"` y `category` puede ser `sueldo`, `extra`, `otro_ing` o `prestamo`.
- **Otros campos posibles**:
  - `cardStmt`, `payOverrides`, `people`, `settles`, `lastRate`, `closeSeen`, `budgetWarned`, `remindDaily`.
  - `lastMethod`, `lastCardId`, `lastJar`, `lastFixedDay`, `peopleOff`.
  - Los fijos también pueden tener `cardId` y `currency: "USD"`.

**Claves de localStorage** (además de `gastos.v1`)
- **Cuenta de Google y sincronización**:
  - `receater.gtoken`: token de Google y su vencimiento.
  - `receater.linked`: este navegador ya está vinculado a un Drive.
  - `receater.user`: nombre del usuario.
  - `receater.email`: email del usuario.
  - `receater.autoFail`: el navegador no deja reconectar sin un toque.
  - `receater.localAntesDeEntrar`: copia de lo local antes de entrar con Google.
- **IA y cotizaciones**:
  - `receater.gkey`: key de Gemini.
  - `receater.aiInviteOff`: el usuario ocultó la invitación a activar la IA.
  - `receater.quotes`: cache del dólar, 30 minutos.
  - `receater.infl`: cache de la inflación, 1 día.
  - `receater.fxCasa`: casa de cambio elegida para compras de dólares.
  - `receater.cpkCasa`: casa de cambio elegida para el pago de tarjeta.
- **Pantalla y preferencias**:
  - `receater.tab`: última tab abierta.
  - `receater.folds`: secciones plegadas del Resumen.
  - `receater.lcdH.s` / `.m` / `.l`: alto de las pizarras.
  - `receater.onb`: ya vio la guía de inicio.
  - `receater.bannerDismissed`: cerró el cartel de Google.
  - `receater.notify`: avisos prendidos.
- **Avisos**: se guardan en Cache Storage (`receater-alerts` / `alerts.json`) y los muestra `sw.js`.

## 5. IA

- **Modelo**: Google **Gemini**, con la key **del propio usuario** (gratis en Google AI Studio). Se llama directo desde el navegador, sin servidor. Usa `gemini-2.5-flash` con fallback a otros modelos flash.
- **Dónde está la key**: en `localStorage` como `receater.gkey` **y** dentro del JSON de Drive como `aiKey` (raíz del objeto). Así se sincroniza entre dispositivos. No se incluye en los backups exportados.
- **Para qué se usa**:
  - Entender un gasto contado con palabras.
  - Leer fotos de tickets.
  - Leer resúmenes de tarjeta (PDF o foto). Si la IA no está o falla, los PDF del banco con texto se leen sin IA.
  - "Preguntale a Recy" (preguntas sobre tus datos).
- **Qué devuelve la lectura de un ticket**: `tipo`, `monto` (total), `moneda`, `fecha`, `hora`, `nota` (nombre del comercio), `categoria`, `medio` e `items: [{ nombre, precio, categoria }]`.
  - **No devuelve cantidad**: "2 x Leche" queda como un producto con el precio de la línea.
  - Al guardar se transforma a `items: [{ name, price, category }]`.

## 6. Publicación

- **Repo**: `github.com/Receater/receater.github.io`, organización **Receater**, rama `main`. Se mudó de `receater/receater.github.io`; el remoto viejo redirige.
- **Hosting**: GitHub Pages desde `main` / raíz, en **https://receater.github.io/**. Publicar es hacer push a `main`: se actualiza en 1–2 minutos.
- **Archivos**:
  - `index.html`: toda la app.
  - `sw.js`: service worker, solo para notificaciones.
  - `manifest.webmanifest` e `icon.svg`.
  - `privacidad.html` y `terminos.html`.
  - `README.md`, `DEPLOY.md` y este `CONTEXTO.md`.
- **Versiones**: cada cambio sube `const BUILD = "AAAA-MM-DD.HHMM"` en `index.html`. La app compara su BUILD con el publicado y avisa "hay una versión nueva".
- **Autor de los commits**: Tomas `<tomaspcarballes@gmail.com>`.

## 7. Decisiones tomadas (no deshacer sin hablarlo)

- **Sin servidor**: todo corre en el navegador. Por eso:
  - El login de Drive vence cada hora.
  - Los avisos dependen del service worker.
  - Mercado Pago no se puede conectar en automático.
- **Drive con `drive.file`**: lo más privado posible. El creador nunca ve datos de nadie.
- **La IA nunca guarda sola**: completa el formulario y el usuario revisa.
- **Key de Gemini propia del usuario**: costo cero para el proyecto y privacidad.
- **Con Drive vinculado y token vencido, la app se bloquea hasta reconectar**: para no perder sincronización. Excepción: sin internet deja seguir.
- **El mes va de cobro a cobro.** Las cuotas y la tarjeta cuentan el día que se pagan, no el de la compra.
- **"Pagué tarjeta" existe en dos lugares a propósito**: en la hoja de carga y en cada tarjeta del Resumen. El usuario lo quiere así.
- **"Gastos varios del mes"**: es el total de un mes entero (no lo de un día). Si no se carga, se calcula con el promedio sin tarjeta ni fijos.
- **Diseño**:
  - Sin emojis, solo íconos Font Awesome solid. Checks en verde.
  - Fondos ilustrados apagados.
  - Las pizarras miden lo mismo en todas las tabs.
  - En touch no hay auto-focus.
- **Guía de inicio**: con "Atrás" y "Saltear" en cada paso. "No tengo día fijo" va como opción separada.

## 7a. Dónde está tu plata (cuentas)

- Botón "¿Dónde está tu plata?" debajo de la pizarra de Movimientos (la pizarra no cambia). Abre la libreta `#accSheet` con cada cuenta, su saldo estimado, lo que rinde por día y en el mes, y el total.
- `data.accounts`: `{ id, prov, name, color, main, tna (null = automática), anchor:{amount, date} }`. `ACC_PROVS` lista billeteras, bancos digitales, bancos y efectivo de Argentina (con color).
- Al cargar un gasto, los chips de pago son: Efectivo, una por cuenta ("Débito Galicia", "Mercado Pago"…) y las tarjetas. No se pregunta de nuevo de dónde salió la plata. Se guarda `accountId`. Ingresos: "¿Dónde entró?" (por defecto la principal). Tarjetas de crédito: `card.payFrom` (de qué cuenta se pagan; por defecto la principal). Gastos viejos sin cuenta: débito/transferencia → principal, efectivo → efectivo.
- Saldo: desde el último "¿Cuánto tenés hoy?" (`anchor`) se suman ingresos y se restan gastos y cuotas de tarjeta el día que se pagan; si la cuenta rinde, se suma el interés de cada día (compuesto diario, solo con saldo positivo).
- Tasa automática cuando hay dato público: fondos de las billeteras (ArgentinaDatos FCI, por nombre: Mercado Fondo, Ualá, Delta Pesos para Personal Pay, Cocos Ahorro, Prex) y `/v1/finanzas/rendimientos` (Lemon, Belo, Ripio, Fiwind, Letsbit; APY → TNA). Naranja X, Brubank y otras cuentas remuneradas no tienen dato público: la tasa se pone a mano. Bancos: caja de ahorro sin interés salvo que se ponga a mano. Los nombres de fondo de cada billetera no están confirmados; si no aparece, cae a manual.
- **Lápiz en la pizarra** (Movimientos, mes actual, cuando dice "Te queda"): `openFixLeft()` pregunta cuánto te queda de verdad (con atajo "Usar lo de mis cuentas") y carga la diferencia como gasto/ingreso sin anotar (`adjust: true`, sin cuenta: no pregunta de dónde salió ni toca las cuentas; tiene que funcionar aunque el usuario no cargue cuentas). El lápiz va al final del renglón del monto, del mismo color que el número. Si la suma de las cuentas no coincide con "Te queda", la pizarra lo avisa.
- **Lápiz en la pizarra de Ahorros** (vista total): `openFixJars()` corrige todos los frascos juntos con movimientos `kind:"adjust"`. Fijos y Resumen no llevan lápiz.
- Botón "volver arriba" (`#goTop`, estilo libreta; en compu pegado a la esquina inferior derecha de la ventana, a 24 px; en celu arriba de "Darle a Recy") aparece al bajar más de 700 px; se oculta con hojas o diálogos abiertos.
- "Te da para $X por día" lleva un ícono de info (`explainPerDay`) que muestra la cuenta: cobrado − gastado (sin hoy) − fijos pendientes − a devolver, dividido los días hasta el próximo cobro. Las líneas de `setBoardLines` aceptan `{ t, info }`.
- Los gastos/ingresos `adjust` no mueven los saldos de las cuentas (solo hacen cerrar la pizarra con la realidad).
- En la libreta: "Pasé plata de una cuenta a otra" (`data.accMoves`: `{ id, from, to, amount, date }`; ej: cajero = banco → efectivo; no es gasto) y "Actualizar saldos" (todas las cuentas juntas; vacío = no cambia). Si el saldo real no coincide con el calculado, `reconcileDiffs` ofrece cargar la diferencia como "Gasto sin anotar" (categoría otros) o "Ingreso sin anotar" (`adjust: true`, con su `accountId`, el día de hoy; no se descuenta dos veces porque el ancla es de hoy), así cierra también la pizarra.
- Solo pesos por ahora (los dólares siguen en los frascos).

## 7g. Corregir lo que te debe una persona

- En la hoja de una persona (cuánto te debe / le debés), cada renglón tiene un lápiz (`pbEdit`): en gastos divididos y préstamos que hiciste se corrige ahí mismo la parte de esa persona (no puede pasar el total del gasto, salvo en préstamos); en pagos que anotaste ("Te dio"/"Le diste") se corrige el monto; lo demás (lo pagó otra persona, te prestó, fijo compartido) abre el gasto, ingreso o fijo donde se cargó.

## 7f. Importar resumen de Mercado Pago (PDF)

- Botón en la libreta "¿Dónde está tu plata?": "Importar resumen de Mercado Pago (PDF)". Se lee en el dispositivo con pdf.js (`mpParse`): cada renglón se arma alrededor del "ID de la operación" (la descripción puede ir en 2 líneas). La parte "Resumen de tenencias en dólares" se saltea.
- `mpClassify`: "Rendimientos" → un solo ingreso por mes; "Ingreso de dinero" → pase banco → MP (`accMoves`); "Transferencia enviada/recibida" a vos mismo (nombre del titular del resumen) → pase entre cuentas; a otros → gasto / ingreso; "Pago …" / "Pago con QR …" → gasto con categoría sugerida (aprendida o por palabras); "Débito por deuda Créditos…" → Intereses. Lo ya cargado (mismo día y monto, o mismo `mpId`) viene destildado.
- Pantalla de revisión (`#mpSheet`): tildar/destildar y cambiar categoría; al sumar se guardan con `source:"mp"`, `mpId` y la cuenta Mercado Pago (se crea si no existe). Pendiente: resumen de Galicia y otros bancos.

## 7e. Categorías editables

- Todas las categorías se pueden editar (nombre y color), también las que vienen con la app: "Editar categorías" en la carga de un gasto, o "Editar esta categoría" en la hoja de un fijo. Las de la app guardan el cambio en `data.catEdits` `{ id: { name, color } }` (no se borran); las propias (`data.customCats`) se pueden borrar (sus gastos y fijos pasan a Otros).
- Al guardar un fijo, todos los pagos ya cargados de ese fijo (`fixedId`) toman la categoría del fijo.

## 7d. Datos para pagar un fijo

- Cada fijo puede guardar `payTo` (link de pago, alias o CBU/CVU) y `payWho` (a nombre de quién, ej: Mamá). Se carga en la hoja del fijo ("Datos para pagarlo").
- En el calendario de fijos pendientes y al abrir un fijo en la pestaña Fijos aparece un renglón con "Abrir link ›" (si empieza con http/www o tiene una barra) o "Copiar" (alias/CBU). Ojo: los alias llevan puntos, por eso no se toman como link.

## 7c. La escuelita de Recy

- Es **otra sección**, separada de los gastos. El botón "Aprender" (gorro) de la barra de arriba, a la izquierda del dólar, entra al **modo escuelita** (`enterLearn`): se ocultan las pestañas, el mes y "Darle a Recy", y se muestra `#viewLearn` con su propio fondo (escena `learn`: un estudio con biblioteca, ventana, cuadro con gráfico, escritorio). El botón pasa a "Volver a mis gastos"; tocar el logo también vuelve (`exitLearn`). `render()` no hace nada mientras `learnOn`.
- Dashboard: pizarra con Recy y el progreso, tarjeta "Para hoy" (próxima lección) y capítulos como libretas con espiral (mismo estilo que el Historial). En compu, dos columnas como el resto.
- Lección: dentro de la página (no en una hoja): texto, dibujito (`LEARN_FIG`: tres partes del sueldo con tus fijos, frascos del colchón, deuda pagando el mínimo, triángulo, crecimiento al 30% TNA, una empresa vs. muchas), "Lo que te llevás", "En tu caso" con link a la parte de la app (`learnGo`: dash, list, fixed, accounts), preguntita y "Leída · siguiente".
- Contenido en `LEARN` (JS). Progreso en `data.learned` `{ idLeccion: "YYYY-MM-DD" }`.
- Hechos los 6 capítulos (27 lecciones): 1 Ordenar la plata · 2 Gastar menos sin sufrir (arranca con "Darte gustos también es parte del plan": tono sano, sin culpa) · 3 Inflación y tasas · 4 Dónde poner la plata · 5 Acciones desde cero (broker/ALyC/CNV, cómo comprar, diversificar, miedo, estafas) · 6 Impuestos (dólar tarjeta y percepciones, monotributo, Ganancias y Bienes Personales; siempre aclarando que las reglas cambian y a chequear en ARCA). El aviso de "no es recomendación" va en rojo con ícono de alerta, al pie del índice y en cada lección de los capítulos 4 y 5.
- Siempre educación, nunca "comprá esto"; aviso al pie y sección en `terminos.html`. Pensado para alguien que no sabe nada.

## 7b. Plata que rinde

- Libreta "Plata que rinde" (mismo estilo que el Historial) en Ahorros (después de los frascos; en escritorio, columna derecha). Guarda `data.yields`: `{ id, kind:"fund"|"rate", name, amount, start, fund, units, vcp0, usd, tna, cur }`.
- **Fondo común**: se elige de la lista de ArgentinaDatos (`/v1/finanzas/fci/{mercadoDinero,rentaFija}/{ultimo,penultimo}`, sin key). Se guardan las cuotapartes (`units = monto / vcp`); el valor es `units × vcp` del día, lo de hoy sale de la diferencia con el valor anterior y la TNA se estima con esos dos valores. Cache diaria en `receater.fci`.
- **Cuenta con tasa** (Naranja X, etc.): TNA a mano, interés compuesto diario desde `start`.
- "¿Cuánto tenés hoy?" reinicia el cálculo con el monto real de la app. Es estimación; no se suma a gastos ni ingresos todavía.
- Falta confirmar en el navegador real que ArgentinaDatos responda (CORS); si falla, se ofrece "Cuenta con tasa".

## 8. Pendientes e ideas

- **Escuelita, próximos pasos**: glosario tocable y "No entendí, explicámelo de otra forma" / preguntar con Gemini. Revisar cada tanto los datos de impuestos (cambian).
- **Recy dibujado por Tomas (lo hace él)**: guía y plantilla en `recy/` (`recy-guia.png`, `recy-plantilla-1024.png`). 10 emociones + 8 animaciones = 50 PNG de 1024×1024 transparentes, patitas en y=872, centrado en x=512. Diseño nuevo de Tomas: Recy con lentes, boca con borde violeta oscuro (paleta violeta); sin brazo a la vista (solo lo saca en saludo, festejo y señalar); el papelito no es parte de Recy: va solo en Comer 1-3 y además suelto como `recy_papel.png` (y `recy_tiritas.png`). Tutorial completo en el doc "Cómo animar a Recy en Procreate" (claude.ai). Cuando Tomas pase los PNG: achicarlos, armar tiras (sprites WebP) por animación y reemplazar `recySVG()`.
- **Separar `index.html` en archivos** (propuesto, a confirmar con Tomas): CSS y JS en archivos aparte con `?v=BUILD` para el caché.

- **Pulir la versión de escritorio**: la primera versión en columnas ya está; falta ajustar detalles con el uso.
- **Importar movimientos del banco** (Galicia y otros): Mercado Pago ya está; falta un resumen de ejemplo de cada banco.
- **Reconexión de Drive sin cartel**: necesita un servidor mínimo para el refresh token (por ejemplo, un Cloudflare Worker). Postergado.
- **Cuenta compartida**: descartada por ahora.
- **Asistente de IA para aprender y ahorrar**: chat con Gemini (key del usuario) para pedir consejos con los datos propios del usuario, más una sección educativa sobre inversiones (acciones, CEDEARs, FCI, plazo fijo, bonos) explicadas sin tecnicismos: riesgo, horizonte, diversificación. Siempre como educación, no como recomendación de compra. A definir con Tomas.
- **Probar en iPhone/iPad**: campos de fecha, que no se mueva la pantalla al abrir hojas, avisos, compartir la imagen del mes y la reconexión con Google desde la guía.
- **Google Cloud (lo hace Tomas)**: cargar los links de privacidad y términos y el mail de soporte en la pantalla de consentimiento, y agregar el dominio de Despensa como origen autorizado.
- **Verificación de la app en Google**: para sacar el aviso de "app no verificada". Requiere cargar privacidad y términos en la pantalla de consentimiento.

## 9. Conexiones con otras apps

- **Despensa** (nombre provisorio, inventario de casa: heladera, freezer, alacena, limpieza y baño; qué falta y qué vence; recetas con IA) se conecta a Receater **solo en modo lectura**:
  - Lee `receater-data.json` del Drive del usuario y toma los `items` de los gastos de ticket (sobre todo `category: "super"`) para ofrecer sumarlos al inventario.
  - Usa la misma key de Gemini (`aiKey` del JSON) para no pedirla de nuevo.
  - Usa **el mismo Client ID de Google** que Receater (con `drive.file` solo así puede ver ese archivo). Lo único necesario es agregar el dominio de Despensa como origen autorizado en Google Cloud.
  - **Despensa nunca escribe en `receater-data.json`.** Receater no cambia nada por esta conexión.
- **Ecosistema a futuro**: Receater, Ideary y Despensa unidas por un hub común. Cada repo tiene su `CONTEXTO.md` para darle contexto a los chats de cada app y del hub.
