// Service Worker para Codex Vitae PWA & Native Push Notifications (Modo Sentinela)

const CACHE_NAME = 'codex-vitae-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/dashboard',
  '/static/css/custom.css',
  '/static/manifest.json'
];

// Install Event
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Instalando Codex Vitae Service Worker...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Ativando Codex Vitae Service Worker...');
  event.waitUntil(self.clients.claim());
});

// Push Event Listener - Recebe a notificação disparada pelo Modo Sentinela / Celery
self.addEventListener('push', (event) => {
  console.log('[Service Worker] Notificação Push recebida:', event);
  
  let payload = {
    title: '🛡️ Alerta do Modo Sentinela',
    body: 'Anomalia biométrica detectada. Inicie o protocolo de imunidade.',
    icon: 'https://cdn-icons-png.flaticon.com/512/3062/3062319.png',
    url: '/dashboard',
    data: {}
  };

  if (event.data) {
    try {
      const dataJson = event.data.json();
      payload.title = dataJson.title || payload.title;
      payload.body = dataJson.body || payload.body;
      payload.icon = dataJson.icon || payload.icon;
      payload.url = dataJson.url || payload.url;
      payload.data = dataJson.data || {};
    } catch (e) {
      payload.body = event.data.text();
    }
  }

  const options = {
    body: payload.body,
    icon: payload.icon,
    badge: payload.icon,
    vibrate: [200, 100, 200, 100, 200],
    data: {
      url: payload.url,
      ...payload.data
    },
    actions: [
      { action: 'open', title: 'Ver Mentoria IA' },
      { action: 'dismiss', title: 'Fechar' }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(payload.title, options)
  );
});

// Notification Click Event Listener
self.addEventListener('notificationclick', (event) => {
  console.log('[Service Worker] Clique na notificação:', event);
  event.notification.close();

  if (event.action === 'dismiss') {
    return;
  }

  const targetUrl = (event.notification.data && event.notification.data.url) ? event.notification.data.url : '/dashboard';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      for (let client of windowClients) {
        if (client.url.includes(targetUrl) && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
