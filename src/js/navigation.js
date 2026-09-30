/* Menu mobile (drawer) — acessibilidade: aria-expanded, Escape, foco. */
(function () {
  "use strict";

  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("main-nav");
  var backdrop = document.querySelector(".nav-backdrop");

  if (!toggle || !nav) return;

  var desktop = window.matchMedia("(min-width: 1024px)");
  var lastFocused = null;

  function isOpen() {
    return nav.classList.contains("is-open");
  }

  function focusables() {
    return [toggle].concat(
      Array.prototype.slice.call(
        nav.querySelectorAll("a[href], button:not([disabled])")
      )
    );
  }

  function open() {
    lastFocused = document.activeElement;
    nav.classList.add("is-open");
    if (backdrop) backdrop.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Fechar menu");
    document.body.style.overflow = "hidden";

    var first = nav.querySelector("a[href]");
    if (first) first.focus();
  }

  function close(restoreFocus) {
    nav.classList.remove("is-open");
    if (backdrop) backdrop.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Abrir menu");
    document.body.style.overflow = "";

    if (restoreFocus !== false && lastFocused && lastFocused.focus) {
      lastFocused.focus();
    }
  }

  toggle.addEventListener("click", function () {
    isOpen() ? close() : open();
  });

  if (backdrop) {
    backdrop.addEventListener("click", function () {
      close();
    });
  }

  nav.addEventListener("click", function (event) {
    if (event.target.closest("a[href]") && !desktop.matches) close(false);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && isOpen()) {
      close();
      return;
    }

    if (event.key !== "Tab" || !isOpen()) return;

    var items = focusables();
    var first = items[0];
    var last = items[items.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  var onChange = function (event) {
    if (event.matches && isOpen()) close(false);
  };

  if (typeof desktop.addEventListener === "function") {
    desktop.addEventListener("change", onChange);
  } else {
    desktop.addListener(onChange);
  }
})();
