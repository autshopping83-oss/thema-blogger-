// Verifica a regra da sidebar: escondida sem .main-layout, visível com ele.
// Uso: NODE_PATH=<fvtest>/node_modules node tools/sidebar-rule.test.js
const puppeteer = require("puppeteer-core");
const BASE = "http://127.0.0.1:8080";

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "/data/data/com.termux/files/usr/bin/chromium-browser",
    protocolTimeout: 120000,
    args: ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto(BASE + "/category.html", { waitUntil: "networkidle0" });

  const state = () =>
    page.evaluate(() => {
      const c = Array.from(document.querySelectorAll(".container")).find(
        (el) => el.querySelector(":scope > .sidebar")
      );
      const aside = c.querySelector(":scope > .sidebar");
      const main = c.querySelector(":scope > .main-content, :scope > main");
      return {
        hasLayout: c.classList.contains("main-layout"),
        sidebar: getComputedStyle(aside).display,
        mainWidth: Math.round(main.getBoundingClientRect().width),
        containerWidth: Math.round(c.getBoundingClientRect().width),
        widgets: aside.querySelectorAll(".widget").length,
      };
    });

  const com = await state();

  // simula a página do tema SEM sidebar (home/artigo/pesquisa)
  await page.evaluate(() =>
    Array.from(document.querySelectorAll(".container")).find((el) => el.querySelector(":scope > .sidebar")).classList.remove("main-layout")
  );
  const sem = await state();

  await page.screenshot({
    path: __dirname + "/../preview/sidebar-sem-layout.png",
    fullPage: false,
  });

  const fails = [];
  if (!com.hasLayout || com.sidebar !== "flex")
    fails.push("com .main-layout: sidebar devia estar visível (" + com.sidebar + ")");
  if (sem.hasLayout || sem.sidebar !== "none")
    fails.push("sem .main-layout: sidebar devia estar escondida (" + sem.sidebar + ")");
  if (sem.mainWidth <= com.mainWidth)
    fails.push("sem .main-layout o conteúdo devia ficar mais largo");
  if (com.widgets < 1) fails.push("sem widgets nativos na sidebar");

  console.log("com .main-layout :", JSON.stringify(com));
  console.log("sem .main-layout :", JSON.stringify(sem));
  await browser.close();

  if (fails.length) {
    console.log("FALHOU:");
    fails.forEach((f) => console.log(" -", f));
    process.exit(1);
  }
  console.log("REGRAS DA SIDEBAR OK");
})();
