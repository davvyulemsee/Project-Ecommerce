// static/js/cart.js
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('form.add-to-cart-form[data-ajax="true"]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var url = form.action;
      var data = new FormData(form);
      fetch(url, {
        method: 'POST',
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        body: data,
        credentials: 'same-origin'
      }).then(function (res) { return res.json(); })
        .then(function (json) {
          // update header badge if present
          var badge = document.querySelector('.cart-badge');
          if (badge) badge.textContent = json.items_count;
          // optionally show a small toast using your site's UI
          console.log('Cart updated', json);
        }).catch(function (err) {
          console.error('Add to cart failed', err);
          // fall back to normal submit if desired
          form.submit();
        });
    });
  });
});