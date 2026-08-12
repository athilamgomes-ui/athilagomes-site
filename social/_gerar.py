#!/usr/bin/env python3
"""
Gera as artes do Instagram em HTML e exporta PNG via Chrome headless.
Rodar:  python3 social/_gerar.py     (a partir da pasta curso-investimentos)

Feed  = 1080x1350 (4:5, o formato que ocupa mais tela no feed)
Story = 1080x1920
"""
import subprocess, pathlib, sys

RAIZ = pathlib.Path(__file__).resolve().parent
SITE = RAIZ.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BASE = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Nunito';font-weight:400 800;font-display:block;
  src:url('../fonts/nunito-latin.woff2') format('woff2');}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
body{{font-family:'Nunito',sans-serif;background:#080e1c;color:#e9eff8;
  position:relative;display:flex;flex-direction:column;justify-content:{just};
  padding:{pad}px;}}
.glow{{position:absolute;inset:0;background:
  radial-gradient(105% 70% at 78% 30%, rgba(53,99,255,.38) 0%, rgba(8,14,28,0) 62%);}}
.ct{{position:relative;z-index:2;padding-bottom:{pb}px}}
.marca{{font-size:{s_marca}px;font-weight:800;letter-spacing:{ls_marca}px;text-transform:uppercase;
  color:#7ea2ff;margin-bottom:{mb_marca}px}}
h1{{font-size:{s_h1}px;font-weight:800;line-height:1.0;letter-spacing:-{lsh}px;color:#fff}}
h1 em{{font-style:normal;color:#7ea2ff}}
.sub{{font-size:{s_sub}px;color:#a9bdd6;line-height:1.4;margin-top:{mt_sub}px;font-weight:600}}
.barra{{border-left:{bw}px solid #3563ff;padding-left:{bp}px;margin:{bm}px 0}}
.barra p{{font-size:{s_barra}px;line-height:1.35;color:#dce6f5;font-weight:700}}
.chips{{display:grid;grid-template-columns:1fr 1fr;gap:{g_chip}px;margin-top:{mt_chip}px}}
.chip{{background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.16);
  border-radius:{r_chip}px;padding:{p_chip}px;font-size:{s_chip}px;font-weight:700;color:#fff;
  text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.cta{{background:#3563ff;color:#fff;font-size:{s_cta}px;font-weight:800;border-radius:{r_cta}px;
  padding:{p_cta}px;text-align:center;margin-top:{mt_cta}px;
  box-shadow:0 18px 50px rgba(53,99,255,.4)}}
.rodape{{position:absolute;left:{pad}px;right:{pad}px;bottom:{pad}px;z-index:2;
  display:flex;align-items:center;gap:{g_rod}px}}
.rodape img{{width:{s_foto}px;height:{s_foto}px;border-radius:{r_foto}px;object-fit:cover;
  object-position:50% 15%}}
.rodape b{{display:block;font-size:{s_nome}px;color:#fff;font-weight:800}}
.rodape span{{font-size:{s_cred}px;color:#8fa3bd;font-weight:600}}
.lista{{margin-top:{mt_lista}px}}
.lista div{{font-size:{s_lista}px;font-weight:700;color:#dce6f5;padding:{p_lista}px 0;
  border-bottom:2px solid rgba(255,255,255,.10);display:flex;gap:{g_lista}px}}
.lista div:last-child{{border-bottom:0}}
.lista i{{font-style:normal;color:#3563ff;font-weight:800}}
{extra}
</style></head><body><div class="glow"></div>{corpo}</body></html>"""

FEED = dict(w=1080, h=1350, pad=88, just="center", s_marca=26, ls_marca=4, mb_marca=26,
            s_h1=104, lsh=3, s_sub=34, mt_sub=26, bw=7, bp=30, bm=40, s_barra=38,
            g_chip=14, mt_chip=34, r_chip=16, p_chip="18px 24px", s_chip=25,
            s_cta=36, r_cta=20, p_cta="30px", mt_cta=44, g_rod=24, s_foto=104, r_foto=20,
            s_nome=34, s_cred=25, mt_lista=34, s_lista=36, p_lista=22, g_lista=20, pb=170, extra="")

STORY = dict(FEED, w=1080, h=1920, pad=96, s_h1=112, s_sub=36, s_barra=40, mt_cta=54, pb=200)


def art(nome, cfg, corpo, extra=""):
    cfg = {**cfg, "extra": extra or cfg.get("extra", "")}
    html = BASE.format(corpo=corpo, **cfg)
    f = RAIZ / f"{nome}.html"
    f.write_text(html, encoding="utf-8")
    png = RAIZ / f"{nome}.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={png}", f"--window-size={cfg['w']},{cfg['h']}",
                    "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"file://{f}"], capture_output=True, timeout=90)
    ok = png.exists()
    print(f"  {'OK ' if ok else 'FALHOU'} {nome}.png  {cfg['w']}x{cfg['h']}")
    return ok


RODAPE = """<div class="rodape"><img src="../img/athila-retrato.jpg" alt="">
  <div><b>Áthila Gomes</b><span>Pastor, empresário e investidor</span></div></div>"""

# ─────────────────────────── FEED 1 — o anúncio
art("feed-1-anuncio", FEED, f"""<div class="ct">
  <div class="marca">Imersão presencial · Altamira</div>
  <h1>Investindo<br>com <em>Sabedoria</em></h1>
  <div class="barra"><p>Um sábado. Seis horas. Você sai com a sua primeira
    carteira de investimentos montada.</p></div>
  <div class="chips">
    <div class="chip">📅 sábado, 17 de outubro</div>
    <div class="chip">🕓 16h às 22h</div>
    <div class="chip">📍 Vineyard Central</div>
    <div class="chip">👥 50 vagas</div>
  </div>
  <div class="cta">Inscrições no link da bio</div>
</div>{RODAPE}""")

# ─────────────────────────── FEED 2 — autoridade
art("feed-2-autoridade", FEED, f"""<div class="ct">
  <div class="marca">Por que confiar</div>
  <div class="barra"><p>Eu ensino o que eu faço com o meu próprio dinheiro há 15 anos.</p></div>
  <h1 style="font-size:76px">Não é fórmula.<br><em>É o que funciona<br>na vida real.</em></h1>
  <p class="sub">Nenhuma promessa de rentabilidade. Nenhum print de lucro.<br>
     Eu não digo onde investir — eu ensino você a decidir.</p>
</div>{RODAPE}""")

# ─────────────────────────── FEED 3 — identificação
art("feed-3-identificacao", FEED, f"""<div class="ct">
  <div class="marca">Talvez seja você</div>
  <h1 style="font-size:74px">Alguma dessas<br>frases é <em>sua?</em></h1>
  <div class="lista">
    <div><i>—</i> "Deixo tudo na poupança"</div>
    <div><i>—</i> "Tenho medo de perder"</div>
    <div><i>—</i> "Não sei por onde começar"</div>
    <div><i>—</i> "Preciso de muito dinheiro"</div>
    <div><i>—</i> "Já me deram um golpe"</div>
    <div><i>—</i> "Invisto, mas por indicação"</div>
  </div>
  <p class="sub">São as seis que mais escuto em 20 anos de sala.</p>
</div>{RODAPE}""")

# ─────────────────────────── STORY 1 — anúncio
art("story-1-anuncio", STORY, f"""<div class="ct">
  <div class="marca">Imersão presencial · Altamira</div>
  <h1>Investindo<br>com <em>Sabedoria</em></h1>
  <div class="barra"><p>Um sábado. Seis horas.<br>Você sai com a sua primeira
    carteira de investimentos montada.</p></div>
  <div class="chips">
    <div class="chip">📅 sáb, 17 de outubro</div>
    <div class="chip">🕓 16h às 22h</div>
    <div class="chip">📍 Vineyard Central</div>
  </div>
  <div class="cta">👆 Link aqui em cima</div>
</div>{RODAPE}""")

# ─────────────────────────── STORY 2 — escassez
art("story-2-vagas", STORY, f"""<div class="ct" style="text-align:center">
  <div class="marca" style="text-align:center">Investindo com Sabedoria</div>
  <div style="font-size:300px;font-weight:800;color:#3563ff;line-height:.9">50</div>
  <h1 style="font-size:88px">vagas.<br><em>Só isso.</em></h1>
  <p class="sub">A sala tem o tamanho que tem. Quando encher, encerra.<br>
     17 de outubro · Vineyard Central · Altamira</p>
  <div class="cta">👆 Garanta a sua no link</div>
</div>""")

# ─────────────────────────── STORY 3 — a objeção
art("story-3-objecao", STORY, f"""<div class="ct">
  <div class="marca">A dúvida mais comum</div>
  <div class="barra"><p>"Áthila, mas eu não tenho<br>dinheiro pra investir ainda."</p></div>
  <h1 style="font-size:80px">Esse é<br><em>justamente</em><br>o motivo<br>pra ir.</h1>
  <p class="sub">O curso não é pra quem já tem dinheiro aplicado.<br>
     É pra quem quer começar e não sabe como.</p>
  <div class="cta">👆 Link aqui em cima</div>
</div>{RODAPE}""")

print("\nPronto. PNGs em social/")
