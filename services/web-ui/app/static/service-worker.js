// Minimalny SW – bez precache, tylko szybka aktywacja
self.addEventListener('install', (event) => {
  self.skipWaiting();
});
self.addEventListener('activate', (event) => {
  self.clients.claim();
});
// (Na razie bez 'fetch' – wszystko idzie do sieci)
