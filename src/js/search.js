/* Pesquisa local de demonstração — dados fictícios, sem backend. */
(function () {
  "use strict";

  var POSTS = [
    {
      title: "Como montar um orçamento pessoal que funciona de verdade",
      url: "article.html",
      category: "Finanças",
      date: "12 mar 2026",
      summary:
        "Um método simples em quatro passos para distribuir salário, despesas e metas sem planilhas complicadas.",
      image: "assets/images/ph-a.svg",
    },
    {
      title: "Precificação por valor: como definir preços sem competir por preço",
      url: "article.html",
      category: "Precificação",
      date: "08 mar 2026",
      summary:
        "Aprenda a calcular margem, custo de aquisição e disposição de pagamento do cliente.",
      image: "assets/images/ph-b.svg",
    },
    {
      title: "Fluxo de caixa para pequenos negócios: o guia essencial",
      url: "article.html",
      category: "Pequenos Negócios",
      date: "02 mar 2026",
      summary:
        "Contas a pagar, recebimentos em atraso e reserva de segurança em um único quadro mensal.",
      image: "assets/images/ph-c.svg",
    },
    {
      title: "Reserva de emergência: quanto guardar e onde deixar o dinheiro",
      url: "article.html",
      category: "Finanças",
      date: "26 fev 2026",
      summary:
        "Critérios objetivos para definir o tamanho da reserva e o nível de liquidez ideal.",
      image: "assets/images/ph-d.svg",
    },
    {
      title: "Calculadora de juros compostos: veja o poder do tempo",
      url: "article.html",
      category: "Calculadoras",
      date: "20 fev 2026",
      summary:
        "Demonstração prática de como aportes mensais consistentes alteram o resultado final.",
      image: "assets/images/ph-hero.svg",
    },
    {
      title: "Margem de contribuição explicada em cinco minutos",
      url: "article.html",
      category: "Pequenos Negócios",
      date: "14 fev 2026",
      summary:
        "O indicador que mostra quanto cada venda realmente sobra para cobrir custos fixos.",
      image: "assets/images/ph-a.svg",
    },
    {
      title: "Guia de precificação para freelancers iniciantes",
      url: "article.html",
      category: "Guias",
      date: "07 fev 2026",
      summary:
        "Como sair da hora-venda e construir propostas com base em resultado entregue.",
      image: "assets/images/ph-b.svg",
    },
    {
      title: "Dívidas no cartão: rolar, quitar ou renegociar?",
      url: "article.html",
      category: "Finanças",
      date: "31 jan 2026",
      summary:
        "Comparação de custos entre as três saídas com um exemplo numérico realista.",
      image: "assets/images/ph-c.svg",
    },
  ];

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (char) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      }[char];
    });
  }

  function card(post) {
    return (
      '<article class="card card--row">' +
      '<a class="card-media" href="' +
      escapeHtml(post.url) +
      '" tabindex="-1" aria-hidden="true">' +
      '<img src="' +
      escapeHtml(post.image) +
      '" alt="" width="160" height="120" loading="lazy">' +
      "</a>" +
      '<div class="card-body">' +
      '<span class="eyebrow">' +
      escapeHtml(post.category) +
      "</span>" +
      '<h2 class="card-title"><a href="' +
      escapeHtml(post.url) +
      '">' +
      escapeHtml(post.title) +
      "</a></h2>" +
      '<p class="card-summary">' +
      escapeHtml(post.summary) +
      "</p>" +
      '<p class="card-meta">' +
      escapeHtml(post.date) +
      "</p>" +
      "</div></article>"
    );
  }

  var list = document.getElementById("search-results");
  if (!list) return;

  var params = new URLSearchParams(window.location.search);
  var query = (params.get("q") || "").trim();

  var term = document.getElementById("results-term");
  var count = document.getElementById("results-count");
  var input = document.querySelector('.search-page-form input[name="q"]');

  if (input) input.value = query;

  if (!query) {
    if (term) term.textContent = "—";
    if (count)
      count.textContent = "Escreva um termo para pesquisar nos artigos.";
    list.innerHTML =
      '<div class="empty-state">Use a pesquisa acima para encontrar artigos, guias e calculadoras.</div>';
    return;
  }

  var needle = query.toLowerCase();
  var results = POSTS.filter(function (post) {
    return (
      post.title.toLowerCase().indexOf(needle) !== -1 ||
      post.summary.toLowerCase().indexOf(needle) !== -1 ||
      post.category.toLowerCase().indexOf(needle) !== -1
    );
  });

  if (term) term.textContent = '"' + query + '"';

  if (!results.length) {
    if (count) count.textContent = "Nenhum resultado encontrado.";
    list.innerHTML =
      '<div class="empty-state">Nenhum artigo corresponde a <strong>' +
      escapeHtml(query) +
      "</strong>. Tente termos como “orçamento”, “preço” ou “juros”.</div>";
    return;
  }

  if (count) {
    count.textContent =
      results.length +
      (results.length === 1 ? " resultado" : " resultados") +
      " encontrados.";
  }

  list.innerHTML = results.map(card).join("");
})();
