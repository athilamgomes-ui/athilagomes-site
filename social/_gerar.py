#!/usr/bin/env python3
"""
Gera as artes do Instagram em HTML e exporta PNG via Chrome headless.
Rodar:  python3 social/_gerar.py     (a partir da pasta curso-investimentos)

Feed  = 1080x1350 (4:5, o formato que ocupa mais tela no feed)
Story = 1080x1920
"""
import subprocess, pathlib, sys, json

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


# O screenshot NÃO é feito aqui. `Google Chrome --headless --screenshot` trava
# quando o Chrome do usuário está aberto (14/08/2026). Cada art() só escreve o
# HTML e enfileira; no fim, _shot.mjs renderiza tudo com o Chromium do
# Playwright, abrindo o navegador uma única vez.
JOBS = []

def art(nome, cfg, corpo, extra=""):
    cfg = {**cfg, "extra": extra or cfg.get("extra", "")}
    (RAIZ / f"{nome}.html").write_text(BASE.format(corpo=corpo, **cfg), encoding="utf-8")
    JOBS.append({"nome": nome, "w": cfg["w"], "h": cfg["h"]})
    return True


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
  <p class="sub">São as seis que mais escuto em 20 anos ensinando.</p>
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
  <p class="sub">Quando encher, encerra.<br>
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

# ═══════════════════════════════════════════════════════════════════════════
# VERSÕES SEM LINK — para a fase de exclusividade dos ex-alunos.
# Enquanto o 1º lote (15 lugares, R$ 347) estiver aberto, o Instagram não pode
# mandar ninguém pro checkout: o público pegaria um preço prometido ao grupo.
# Estas artes anunciam sem oferecer. Quando a Sympla virar pro 2º lote, voltam
# a valer as originais, com link.
# ═══════════════════════════════════════════════════════════════════════════

art("story-1-anuncio-sem-link", STORY, f"""<div class="ct">
  <div class="marca">Imersão presencial · Altamira</div>
  <h1>Investindo<br>com <em>Sabedoria</em></h1>
  <div class="barra"><p>Um sábado. Seis horas.<br>Você sai com a sua primeira
    carteira de investimentos montada.</p></div>
  <div class="chips">
    <div class="chip">📅 sáb, 17 de outubro</div>
    <div class="chip">🕓 16h às 22h</div>
    <div class="chip">📍 Vineyard Central</div>
  </div>
  <div class="cta">Inscrições abrem em breve</div>
</div>{RODAPE}""")

art("story-3-objecao-sem-link", STORY, f"""<div class="ct">
  <div class="marca">A dúvida mais comum</div>
  <div class="barra"><p>"Áthila, mas eu não tenho<br>dinheiro pra investir ainda."</p></div>
  <h1 style="font-size:80px">Esse é<br><em>justamente</em><br>o motivo<br>pra ir.</h1>
  <p class="sub">O curso não é pra quem já tem dinheiro aplicado.<br>
     É pra quem quer começar e não sabe como.</p>
  <div class="cta" style="background:transparent;color:#7ea2ff;border:3px solid rgba(126,162,255,.45);
       box-shadow:none">17 de outubro · Altamira</div>
</div>{RODAPE}""")

# ═══════════════════════════════════════════════════════════════════════════
# STATUS DO WHATSAPP — 1080x1920, mas NÃO é igual ao story:
#   · não existe figurinha de link (o link, quando houver, vai na legenda)
#   · o WhatsApp cobre o topo com o cabeçalho e o rodapé com a barra de resposta
#     → conteúdo recuado para a faixa central segura
#   · quem vê é a agenda dele: ex-aluno, irmão de igreja, cliente. Tom mais seco.
# ═══════════════════════════════════════════════════════════════════════════

# Zona segura do status: o miolo de 1080x1350 (285px de folga em cima e embaixo
# no canvas de 1920). Fora disso o WhatsApp cobre com cabeçalho e barra de resposta.
SAFE = """.ct{padding-bottom:0}
.rodape{bottom:300px}
body{justify-content:center;padding-top:300px;padding-bottom:420px}"""

STATUS = dict(STORY, pad=100, s_h1=104, s_sub=34, s_barra=38)

art("status-1-anuncio", STATUS, f"""<div class="ct">
  <div class="marca">Imersão presencial · Altamira</div>
  <h1>Investindo<br>com <em>Sabedoria</em></h1>
  <div class="barra"><p>Um sábado. Seis horas.<br>Você sai com a sua primeira
    carteira de investimentos montada.</p></div>
  <div class="chips">
    <div class="chip">📅 sáb, 17 de outubro</div>
    <div class="chip">🕓 16h às 22h</div>
    <div class="chip">📍 Vineyard Central</div>
    <div class="chip">👥 50 vagas</div>
  </div>
</div>{RODAPE}""", extra=SAFE)

art("status-2-vagas", STATUS, f"""<div class="ct" style="text-align:center">
  <div class="marca" style="text-align:center">Investindo com Sabedoria</div>
  <div style="font-size:270px;font-weight:800;color:#3563ff;line-height:.9">50</div>
  <h1 style="font-size:84px">vagas.<br><em>Só isso.</em></h1>
  <p class="sub">Quando encher, encerra.<br>
     17 de outubro · Vineyard Central · Altamira</p>
</div>""", extra=SAFE)

art("status-3-objecao", STATUS, f"""<div class="ct">
  <div class="marca">A dúvida mais comum</div>
  <div class="barra"><p>"Áthila, mas eu não tenho<br>dinheiro pra investir ainda."</p></div>
  <h1 style="font-size:78px">Esse é<br><em>justamente</em><br>o motivo<br>pra ir.</h1>
  <p class="sub">O curso não é pra quem já tem dinheiro aplicado.<br>
     É pra quem quer começar e não sabe como.</p>
</div>{RODAPE}""", extra=SAFE)

# ═══════════════════════════════════════════════════════════════════════════
# CARROSSEL "O PREÇO DA SUA HORA" — 6 slides, feed 1080x1350
#
# A ideia (medir dinheiro em horas de vida) é um clássico da educação
# financeira, não invenção de ninguém. O que NÃO se copia é a execução alheia
# — e principalmente não se copia o que quebra as regras dele:
#   · nada de print de rendimento     · nada de ativo citado
#   · nada de "ganhe X sem trabalhar" · nada de promessa de retorno
#
# A conta usa 220h/mês, que é o divisor padrão de jornada no Brasil (44h
# semanais), e um salário de EXEMPLO — o leitor refaz com o dele, que é onde
# mora a força: a conta vira sobre a vida da própria pessoa.
#
# Confs: 3000/220 = 13,64 · 20/13,64 = 1,47h · 10h = 136 · 50h = 682
# ═══════════════════════════════════════════════════════════════════════════

CARR_CSS = """
.seta{position:absolute;right:88px;bottom:76px;font-size:52px;color:#7ea2ff;font-weight:800;z-index:3}
.big{font-size:172px;font-weight:800;color:#7ea2ff;line-height:.95;letter-spacing:-6px;margin:14px 0}
.conta{font-size:56px;font-weight:800;color:#fff;line-height:1.34}
.conta em{font-style:normal;color:#7ea2ff}
.nota{font-size:31px;color:#8fa3bd;font-weight:600;margin-top:32px;line-height:1.42}
.ct{padding-bottom:0}
"""
CARR = dict(FEED, just="center", s_h1=96, s_sub=32, s_barra=40, extra=CARR_CSS)
SETA = '<div class="seta">→</div>'

art("carrossel-1-hora", CARR, f"""<div class="ct">
  <div class="marca">Uma conta que muda tudo</div>
  <h1>Quanto vale<br><em>uma hora</em><br>da sua vida?</h1>
  <p class="sub">Quase ninguém sabe responder. E é o número<br>
     mais importante da sua vida financeira.</p>
</div>{SETA}{RODAPE}""")

art("carrossel-2-jornada", CARR, f"""<div class="ct">
  <div class="marca">Primeiro, a jornada</div>
  <p class="conta">A jornada padrão no Brasil é de<br><em>220 horas por mês.</em></p>
  <p class="nota">É esse o número que a sua empresa usa para calcular
     quanto vale o seu salário por hora.</p>
</div>{SETA}""")

art("carrossel-3-divisao", CARR, f"""<div class="ct">
  <div class="marca">Agora, a divisão</div>
  <p class="conta">Um salário de R$ 3.000<br>dividido por 220 horas:</p>
  <div class="big">R$ 13,64</div>
  <p class="nota">É o que custa <strong style="color:#dce6f5">uma hora da sua vida</strong>.
     Refaça com o seu salário. Guarda esse número.</p>
</div>{SETA}""")

art("carrossel-4-virada", CARR, f"""<div class="ct">
  <div class="marca">Agora inverta</div>
  <p class="conta">Se um dinheiro seu render<br><em>R$ 20 num mês</em>,<br>
     ele te devolveu quase<br><em>uma hora e meia.</em></p>
  <p class="nota">Uma hora e meia que você não precisou trabalhar.</p>
</div>{SETA}""")

art("carrossel-5-escala", CARR, f"""<div class="ct">
  <div class="marca">E a conta cresce</div>
  <p class="conta"><em>R$ 136</em> é um dia inteiro.<br>
     <em>R$ 682</em> é uma semana.</p>
  <p class="nota">Todo real que você guarda e coloca para trabalhar
     compra de volta um pedaço do seu tempo. E tempo é a única coisa
     que você não recupera trabalhando mais.</p>
</div>{SETA}""")

art("carrossel-6-convite", CARR, f"""<div class="ct">
  <div class="marca">Investindo com Sabedoria</div>
  <h1 style="font-size:72px">Um sábado para<br>aprender a fazer<br><em>essa conta virar.</em></h1>
  <div class="chips" style="margin-top:38px">
    <div class="chip">📅 sábado, 17 de outubro</div>
    <div class="chip">🕓 16h às 22h</div>
    <div class="chip">📍 Vineyard Central</div>
    <div class="chip">👥 50 vagas</div>
  </div>
  <div class="cta">Inscrições no link da bio</div>
</div>{RODAPE}""")

# ═══════════════════════════════════════════════════════════════════════════
# TABELA "ACHE O SEU" — story + status, 14/08/2026
#
# Continua a conta do carrossel em vez de repetir: a pessoa acha o próprio
# salário e lê o valor da hora dela sem fazer conta nenhuma. Zero atrito.
#
# ⚠️ Nenhum valor é rotulado como "salário mínimo" — o valor de 2026 não foi
# verificado, e número errado numa arte de finanças destrói a autoridade dele.
# São faixas redondas, e o rodapé ensina a fazer com o salário real.
# Conferido: 1500/220=6,82 · 2000=9,09 · 3000=13,64 · 5000=22,73 · 8000=36,36
# ═══════════════════════════════════════════════════════════════════════════

TAB_CSS = """
.cab{display:flex;justify-content:space-between;padding:0 30px 14px;
  font-size:22px;font-weight:800;letter-spacing:2.4px;text-transform:uppercase;color:#6f83a0}
.tab{display:grid;gap:15px}
.lin{display:flex;align-items:center;justify-content:space-between;
  background:rgba(255,255,255,.055);border:2px solid rgba(255,255,255,.11);
  border-radius:20px;padding:26px 30px}
.lin b{font-size:50px;font-weight:800;color:#dce6f5}
.lin i{font-style:normal;font-size:50px;font-weight:800;color:#7ea2ff}
.lin.dest{background:rgba(53,99,255,.20);border-color:rgba(53,99,255,.6)}
.lin.dest b{color:#fff}
.rod{font-size:31px;color:#a9bdd6;font-weight:700;line-height:1.4;margin-top:36px}
.rod em{font-style:normal;color:#fff}
"""

LINHAS = """
  <div class="cab"><span>Salário</span><span>Uma hora sua</span></div>
  <div class="tab">
    <div class="lin"><b>R$ 1.500</b><i>R$ 6,82</i></div>
    <div class="lin"><b>R$ 2.000</b><i>R$ 9,09</i></div>
    <div class="lin dest"><b>R$ 3.000</b><i>R$ 13,64</i></div>
    <div class="lin"><b>R$ 5.000</b><i>R$ 22,73</i></div>
    <div class="lin"><b>R$ 8.000</b><i>R$ 36,36</i></div>
  </div>"""

TAB = dict(STORY, just="center", s_h1=84, extra=TAB_CSS)

art("story-hora-tabela", TAB, f"""<div class="ct">
  <div class="marca">Ache o seu</div>
  <h1>Quanto custa<br><em>uma hora</em> da sua vida?</h1>
  <div style="height:34px"></div>
  {LINHAS}
  <p class="rod">O seu não está aí? <em>Divide por 220.</em><br>
     É a jornada padrão de um mês.</p>
  <div class="cta" style="margin-top:38px">👆 A conta inteira no meu perfil</div>
</div>""")

art("status-hora-tabela", TAB, f"""<div class="ct">
  <div class="marca">Ache o seu</div>
  <h1>Quanto custa<br><em>uma hora</em> da sua vida?</h1>
  <div style="height:34px"></div>
  {LINHAS}
  <p class="rod">O seu não está aí? <em>Divide por 220.</em><br>
     É a jornada padrão de um mês.</p>
</div>{RODAPE}""", extra=TAB_CSS + SAFE)

# ═══════════════════════════════════════════════════════════════════════════
# "A PERGUNTA ERRADA" — feed + story + status, 14/08/2026
#
# Pedido original: mostrar o preço de 1 ação de 3 empresas bem-sucedidas.
# NÃO FEITO ASSIM, de propósito:
#   · citar ativo em post que convida a começar a investir = indicação,
#     atividade regulada pela CVM. É a regra que ele mesmo definiu.
#   · preço de ação desatualiza em dias e a arte continua circulando.
#
# A mensagem ("dá pra começar com pouco") não precisa de nome de empresa —
# e fica mais forte pela negativa: derruba os valores que a pessoa imagina,
# e move a barreira de dinheiro para conhecimento, que é o que ele vende.
# Nenhum número de cotação, nenhuma promessa de retorno.
# ═══════════════════════════════════════════════════════════════════════════

ERR_CSS = """
.errados{display:flex;flex-direction:column;gap:10px;margin:34px 0 30px}
.err{font-size:58px;font-weight:800;color:#55657d;text-decoration:line-through;
  text-decoration-thickness:6px;text-decoration-color:#3563ff;line-height:1.18}
.certo{border-left:7px solid #3563ff;padding-left:30px;margin-top:10px}
.certo b{display:block;font-size:44px;font-weight:800;color:#fff;line-height:1.3}
.certo b em{font-style:normal;color:#7ea2ff}
.punch{font-size:40px;font-weight:800;color:#dce6f5;line-height:1.35;margin-top:38px}
.punch em{font-style:normal;color:#7ea2ff}
"""

CORPO_ERR = """
  <div class="marca">A pergunta errada</div>
  <h1>Quanto eu preciso ter<br>pra <em>começar</em> a investir?</h1>
  <div class="errados">
    <div class="err">R$ 50.000</div>
    <div class="err">R$ 10.000</div>
    <div class="err">R$ 1.000</div>
  </div>
  <div class="certo"><b>Na bolsa você compra <em>uma ação</em>. Uma unidade —
    e muita empresa grande custa menos que um delivery de sábado.</b></div>
  <p class="punch">O que trava não é o valor.<br><em>É não saber escolher.</em></p>"""

art("feed-4-pergunta-errada", dict(FEED, just="center", s_h1=68, extra=ERR_CSS),
    f'<div class="ct">{CORPO_ERR}</div>{RODAPE}')

art("story-pergunta-errada", dict(STORY, just="center", s_h1=72, extra=ERR_CSS),
    f'<div class="ct">{CORPO_ERR}\n  <div class="cta" style="margin-top:44px">'
    f'👆 O curso inteiro é sobre isso</div></div>')

art("status-pergunta-errada", dict(STORY, just="center", s_h1=68, extra=ERR_CSS + SAFE),
    f'<div class="ct">{CORPO_ERR}</div>{RODAPE}')


# ═══════════════════════════════════════════════════════════════════════════
# "ÚLTIMO DIA" — 20/08/2026, dia do prazo do 1º lote
#
# Dia de prazo não é dia de conteúdo esperto. A arte não explica nada, não
# ensina nada: mostra o que muda à meia-noite e sai da frente. Urgência aqui
# é VERDADE (a Sympla vira sozinha), então pode ser dita sem rodeio.
# ═══════════════════════════════════════════════════════════════════════════

HOJE_CSS = """
.selo{display:inline-block;background:#3563ff;color:#fff;font-size:26px;font-weight:800;
  letter-spacing:3px;text-transform:uppercase;padding:14px 26px;border-radius:12px;
  margin-bottom:30px;box-shadow:0 14px 40px rgba(53,99,255,.45)}
.precos{display:flex;align-items:flex-end;gap:34px;margin:38px 0 6px;flex-wrap:wrap}
.pr{display:flex;flex-direction:column}
.pr span{font-size:26px;font-weight:800;letter-spacing:2.4px;text-transform:uppercase;
  color:#6f83a0;margin-bottom:10px}
.pr b{font-size:104px;font-weight:800;line-height:.95;letter-spacing:-4px}
.pr.hoje b{color:#fff}
.pr.dep b{color:#7ea2ff}
.seta2{font-size:76px;color:#3563ff;font-weight:800;padding-bottom:12px}
.obs{font-size:32px;color:#a9bdd6;font-weight:700;line-height:1.4;margin-top:34px}
.obs em{font-style:normal;color:#fff}
"""

CORPO_HOJE = """
  <div class="selo">Último dia</div>
  <h1>O 1º lote fecha<br><em>hoje à meia-noite.</em></h1>
  <div class="precos">
    <div class="pr hoje"><span>Até hoje</span><b>R$ 347</b></div>
    <div class="seta2">&rarr;</div>
    <div class="pr dep"><span>A partir de amanhã</span><b>R$ 447</b></div>
  </div>
  <p class="obs">Mesmo sábado, mesmo conteúdo, mesma vaga.<br>
     <em>Só o preço muda.</em> 17 de outubro · Altamira.</p>"""

art("feed-5-ultimo-dia", dict(FEED, just="center", s_h1=72, extra=HOJE_CSS),
    f'<div class="ct">{CORPO_HOJE}</div>{RODAPE}')

art("story-ultimo-dia", dict(STORY, just="center", s_h1=76, extra=HOJE_CSS),
    f'<div class="ct">{CORPO_HOJE}\n  <div class="cta" style="margin-top:46px">'
    f'👆 Garanta a sua hoje</div></div>')

art("status-ultimo-dia", dict(STORY, just="center", s_h1=72, extra=HOJE_CSS + SAFE),
    f'<div class="ct">{CORPO_HOJE}</div>{RODAPE}')

(RAIZ / "_jobs.json").write_text(json.dumps(JOBS, ensure_ascii=False), encoding="utf-8")
print(f"{len(JOBS)} artes escritas em HTML. Renderizando com o Playwright:\n")
sys.exit(subprocess.run(["node", str(RAIZ / "_shot.mjs")], cwd=RAIZ).returncode)
