self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('offline-media').then(function(cache) {
            return cache.addAll([/*
                'https://unpkg.com/vue@next',
                '/static/index.html',
                '/static/manifest.json',
                '/static/style.css',
                '/static/sw.js',
                '/static/main.js',
                '/static/icon192.png',
                '/static/icon512.png'*/
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
