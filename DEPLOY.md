# Publicar Receater en GitHub Pages

Son unos 10 minutos. Hay que hacerlo con tu cuenta, porque son cosas que solo vos podés tocar.

## 1. Crear el repo

1. Entrá a github.com → **New repository**.
2. Nombre: `receater`. Público (GitHub Pages gratis necesita repo público).
3. Crealo vacío, sin README.

## 2. Subir los archivos

1. En el repo nuevo, tocá **uploading an existing file**.
2. Arrastrá los 5 archivos: `index.html`, `manifest.webmanifest`, `icon.svg`, `README.md`, `DEPLOY.md`.
3. **Commit changes**.

## 3. Activar GitHub Pages

1. **Settings → Pages**.
2. Source: **Deploy from a branch**. Branch: `main`, carpeta `/ (root)`. **Save**.
3. En un minuto queda en `https://TU-USUARIO.github.io/receater/`.

## 4. Habilitar el login de Google (el mismo cliente de Artdeas)

1. Entrá a [console.cloud.google.com](https://console.cloud.google.com) con la cuenta de Artdeas, al mismo proyecto.
2. **APIs y servicios → Credenciales** → abrí el cliente OAuth que usa Artdeas.
3. En **Orígenes autorizados de JavaScript**, agregá: `https://TU-USUARIO.github.io` (sin `/receater` y sin barra al final).
4. **Guardar**. Puede tardar unos minutos en aplicarse.

## 5. Dejar que otras personas entren

Si la pantalla de consentimiento está en modo **Prueba**, solo pueden entrar los mails que agregues como usuarios de prueba.

- Para probar vos: agregate en **Pantalla de consentimiento → Usuarios de prueba**.
- Para que la use cualquiera: **Publicar app**. Como solo usa el permiso `drive.file`, no suele pedir verificación, pero Google puede pedirte una política de privacidad y el dominio.

Si preferís que Receater tenga su propio nombre en la pantalla de login, creá un cliente OAuth nuevo y reemplazá `GOOGLE_CLIENT_ID` en `index.html`.

## 6. Probar

1. Abrí la URL, tocá **Entrar con Google** y aceptá.
2. Cargá un gasto y fijate que arriba diga **En tu Drive ✓**.
3. Abrí la URL en otro dispositivo, entrá con la misma cuenta y deberías ver lo mismo.

## Si algo falla

- **"redirect_uri_mismatch" o "origin not allowed"**: el origen del paso 4 no coincide exacto. Revisá https y que no tenga barra final.
- **"Access blocked" / app no verificada**: estás fuera de los usuarios de prueba (paso 5).
- **Dice "Reconectar"**: se venció la sesión de Google (dura una hora). Tocalo y listo.
