# Receater

App para cargar gastos, sueldo, tarjetas y ahorro, y ver en qué se te va la plata. La mascota es **Recy**, una trituradora que se come tus tickets.

## Qué hace

- Gastos con categoría, fecha, hora, nota y medio de pago (efectivo, débito, transferencia o tarjeta).
- Gastos compartidos: dividís entre amigos y marcás quién te devolvió.
- Sueldo con día fijo, último día hábil o sin día fijo, y ajustes por mes.
- Tarjetas de crédito con cierre, forma de pago y cuotas. Cada cuota cuenta el día que se paga.
- Compra de dólares y categoría Ahorro.
- Resumen con torta sobre el sueldo, barras de 6 meses y gráfico por tarjeta.

## Cómo se guardan los datos

- Sin iniciar sesión: en el navegador (localStorage).
- Con **Entrar con Google**: en un archivo `receater-data.json` en el Google Drive de cada usuario. La app usa el permiso `drive.file`, así que solo ve ese archivo, nada más del Drive.

## Estructura

- `index.html`: toda la app (HTML, CSS y JS en un archivo, sin build).
- `manifest.webmanifest` e `icon.svg`: para instalarla en el celu como app.

## Correr local

Abrí `index.html` en el navegador. El login de Google solo funciona desde `https` o `localhost`, por ejemplo con:

```
npx serve .
```

## Publicar

Ver [DEPLOY.md](DEPLOY.md).

## Pendiente

- Leer tickets con foto (necesita un pequeño servidor para no exponer la API key).
- Préstamos sueltos.
- Cotización del dólar automática.
