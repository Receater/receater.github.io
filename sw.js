/* Receater: service worker solo para avisos (no guarda la app en caché, así siempre ves la última versión) */
const STORE = "receater-alerts", KEY = "alerts.json";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
async function readAlerts(){
  try { const c = await caches.open(STORE), r = await c.match(KEY); return r ? await r.json() : { list: [], shown: [] }; }
  catch { return { list: [], shown: [] }; }
}
async function saveAlerts(d){ try { const c = await caches.open(STORE); await c.put(KEY, new Response(JSON.stringify(d), { headers: { "Content-Type": "application/json" } })); } catch {} }
/* Muestra los avisos que ya tocaban y todavía no se mostraron */
async function fireDue(){
  const d = await readAlerts(), now = Date.now(), shown = new Set(d.shown || []);
  for (const a of d.list || []){
    if (a.at <= now && a.at > now - 2 * 864e5 && !shown.has(a.id)){
      await self.registration.showNotification(a.title, { body: a.body, tag: a.id, icon: "icon.svg", badge: "icon.svg", data: { url: "./" } });
      shown.add(a.id);
    }
  }
  d.shown = [...shown].slice(-300); await saveAlerts(d);
}
self.addEventListener("periodicsync", e => { if (e.tag === "receater-alerts") e.waitUntil(fireDue()); });
self.addEventListener("message", e => { if (e.data && e.data.type === "fire") e.waitUntil(fireDue()); });
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(ws => {
    const w = ws.find(x => "focus" in x); return w ? w.focus() : self.clients.openWindow("./");
  }));
});
