const CACHE_NAME = 'nicegui-blog-cache-v1';
const OFFLINE_URLS = [
  '/',
  '/static/blog.min.css'
];
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(OFFLINE_URLS))
  );
});
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
