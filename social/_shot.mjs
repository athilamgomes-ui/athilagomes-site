// Renderiza os .html das artes em PNG usando o Chromium do Playwright.
//
// POR QUÊ NÃO O CHROME DO SISTEMA: `Google Chrome --headless --screenshot`
// passou a travar indefinidamente quando o Chrome normal do usuário está
// aberto (14/08/2026) — nem `--user-data-dir` isolado resolveu. O Chromium do
// Playwright é outro binário, com perfil próprio, e não disputa nada.
//
// Bônus: abre o navegador UMA vez para todas as artes, em vez de um processo
// por PNG. Ficou muito mais rápido.
//
// Lê _jobs.json (escrito pelo _gerar.py): [{nome, w, h}, ...]

import { chromium } from "playwright";
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const jobs = JSON.parse(readFileSync(resolve(AQUI, "_jobs.json"), "utf8"));

const navegador = await chromium.launch();
let ok = 0;
for (const j of jobs) {
  const html = resolve(AQUI, `${j.nome}.html`);
  const png  = resolve(AQUI, `${j.nome}.png`);
  const pag  = await navegador.newPage({
    viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1
  });
  await pag.goto("file://" + html, { waitUntil: "load" });
  await pag.evaluate(() => document.fonts.ready);   // sem isso a Nunito sai como fallback
  await pag.screenshot({ path: png });
  await pag.close();
  const bom = existsSync(png);
  if (bom) ok++;
  console.log(`  ${bom ? "OK " : "FALHOU"} ${j.nome}.png  ${j.w}x${j.h}`);
}
await navegador.close();
console.log(`\n${ok}/${jobs.length} artes geradas.`);
process.exit(ok === jobs.length ? 0 : 1);
