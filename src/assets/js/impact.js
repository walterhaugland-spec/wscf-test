// Impact graphic: numbers count up and the dotted trails draw in as the visitor scrolls.
// Without JavaScript, or with reduced motion, the graphic simply shows complete.
(function () {
  var root = document.querySelector('.impact');
  if (!root) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;

  var steps = Array.prototype.slice.call(root.querySelectorAll('[data-step]'));
  root.querySelectorAll('.impact-reveal').forEach(function (p) {
    var len = Math.ceil(p.getTotalLength ? p.getTotalLength() : 400) + 4;
    p.style.strokeDasharray = len + ' ' + len;
    p.style.strokeDashoffset = len;
  });
  root.querySelectorAll('[data-count]').forEach(function (el) { el.textContent = '0'; });
  root.classList.add('armed');

  function countUp(el) {
    var target = +el.dataset.count, dur = target > 100 ? 1800 : 1100, t0 = null;
    function fmt(n) { return Math.round(n).toLocaleString('en-US'); }
    function tick(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * e);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  function run(step) {
    step.classList.add('is-in');
    if (step.classList.contains('impact-stat')) countUp(step.querySelector('[data-count]'));
    else step.querySelectorAll('.impact-reveal').forEach(function (p) { p.style.strokeDashoffset = 0; });
  }

  // Each step waits until it is on screen and the one before it has played.
  var ready = steps.map(function () { return false; }), next = 0, busy = false;
  function advance() {
    if (busy || next >= steps.length || !ready[next]) return;
    busy = true;
    var s = steps[next];
    run(s);
    setTimeout(function () { busy = false; next++; advance(); }, s.classList.contains('impact-stat') ? 650 : 900);
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { ready[steps.indexOf(en.target)] = true; io.unobserve(en.target); }
    });
    advance();
  }, { threshold: 0.6 });
  steps.forEach(function (s) { io.observe(s); });
})();
