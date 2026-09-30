/* Utilidades da página: ano, newsletter (demo) e calculadora (demo). */
(function () {
  "use strict";

  /* Ano do copyright ----------------------------------------------------- */
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  /* Newsletter — apenas demonstração, sem backend ------------------------ */
  function isEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  Array.prototype.forEach.call(
    document.querySelectorAll(".newsletter-form"),
    function (form) {
      var input = form.querySelector('input[type="email"]');
      var note = form.parentNode.querySelector(".newsletter-note");

      form.addEventListener("submit", function (event) {
        event.preventDefault();
        if (!input || !note) return;

        if (!isEmail(input.value.trim())) {
          input.setAttribute("aria-invalid", "true");
          note.className = "newsletter-note is-error";
          note.textContent = "Introduza um e-mail válido.";
          input.focus();
          return;
        }

        input.removeAttribute("aria-invalid");
        note.className = "newsletter-note is-success";
        note.textContent = "Obrigado! Registo simulado (demonstração).";
        form.reset();
      });
    }
  );

  /* Calculadora de demonstração (juros compostos) ------------------------ */
  var calcForm = document.getElementById("calc-demo-form");
  if (calcForm) {
    var output = document.getElementById("calc-demo-result");
    var brl = new Intl.NumberFormat("pt-PT", {
      style: "currency",
      currency: "EUR",
    });

    calcForm.addEventListener("submit", function (event) {
      event.preventDefault();

      var start = parseFloat(calcForm.elements.start.value) || 0;
      var monthly = parseFloat(calcForm.elements.monthly.value) || 0;
      var rate = (parseFloat(calcForm.elements.rate.value) || 0) / 100 / 12;
      var months = (parseFloat(calcForm.elements.years.value) || 0) * 12;

      var balance = start;
      for (var i = 0; i < months; i++) {
        balance = balance * (1 + rate) + monthly;
      }

      var contributed = start + monthly * months;
      output.textContent =
        brl.format(balance) +
        " (depositado: " +
        brl.format(contributed) +
        ")";
    });
  }
})();
