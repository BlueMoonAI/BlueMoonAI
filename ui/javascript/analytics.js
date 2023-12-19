// analytics.js

// Google tag (gtag.js)
(function() {
  var script = document.createElement('script');
  script.async = true;
  // for performance and seo testing
  script.src = 'https://www.googletagmanager.com/gtag/js?id=G-MND4E5TGVG';
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-MND4E5TGVG');
})();
