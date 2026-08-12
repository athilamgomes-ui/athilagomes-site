-- ============================================================
-- Cursos de Finanças — Athila M. Gomes
-- Banco de leads (lista de espera + compradores)
-- Projeto Supabase: valhewbvjwdkkvuejrxa ("digitacao de pedido on line")
--   O projeto "Curso on line" (ewclhvelikxqjjnnbnfw) não coube: plano grátis dá 2 projetos
--   ativos e os dois já são o ERP e o dashboard de estudos. Decisão de 11/08/2026.
--   Esta tabela é segura mesmo nesse projeto: RLS insert-only + SELECT revogado.
--   A leitura aberta das OUTRAS tabelas do projeto é problema à parte, em correção.
-- Rodar no SQL Editor do Supabase. Idempotente.
-- ============================================================

create table if not exists public.leads_cursos (
  id            bigint generated always as identity primary key,
  criado_em     timestamptz not null default now(),

  -- identificação
  nome          text not null,
  whatsapp      text not null,          -- guardado só com dígitos: 5593999998888
  email         text,
  cidade        text,

  -- qualificação (o que separa quem compra de quem só olha)
  perfil        text,                   -- 'nao_invisto' | 'poupanca' | 'ja_invisto'
  objetivo      text,                   -- texto livre, opcional

  -- origem / atribuição
  curso         text not null default 'investindo-com-sabedoria',
  turma         text,                   -- ex: 'outubro-2026-altamira'
  origem        text,                   -- utm_source: instagram, whatsapp, indicacao, meta_ads...
  campanha      text,                   -- utm_campaign
  referer       text,

  -- LGPD
  consentimento boolean not null default false,

  -- funil (atualizado depois, pelo webhook da Eduzz ou na mão)
  status        text not null default 'lead',  -- lead | contatado | inscrito | comprou | recusou
  valor_pago    numeric(10,2),
  pago_em       timestamptz,
  eduzz_id      text,
  observacoes   text
);

-- Um mesmo WhatsApp não entra duas vezes na mesma turma
create unique index if not exists leads_cursos_whats_turma_uk
  on public.leads_cursos (whatsapp, curso, coalesce(turma, ''));

create index if not exists leads_cursos_criado_idx  on public.leads_cursos (criado_em desc);
create index if not exists leads_cursos_status_idx  on public.leads_cursos (status);

-- ============================================================
-- RLS: o anon key é PÚBLICO (vai no HTML). A segurança é aqui.
-- O visitante pode INSERIR. Não pode ler, editar nem apagar nada.
-- ============================================================
alter table public.leads_cursos enable row level security;

drop policy if exists "anon pode inserir lead" on public.leads_cursos;
create policy "anon pode inserir lead"
  on public.leads_cursos
  for insert
  to anon
  with check (
    consentimento = true
    and length(nome) between 2 and 120
    and length(whatsapp) between 10 and 15
  );

-- NENHUMA policy de select/update/delete para anon = ninguém baixa sua lista.
-- Você lê pelo painel do Supabase ou pelo dashboard (que usa service_role no servidor).

-- Cinto e suspensório: além do RLS, tira na unha qualquer permissão de leitura/alteração
-- que o Supabase conceda por padrão aos papéis públicos. Assim, se alguém um dia rodar de novo
-- um script tipo "supabase_sem_login.sql" que abre o RLS geral, esta tabela continua fechada.
revoke all on public.leads_cursos from anon, authenticated;
grant insert on public.leads_cursos to anon;

-- ============================================================
-- Visão rápida do funil (usar no SQL Editor ou no dashboard)
-- ============================================================
create or replace view public.leads_cursos_funil as
select
  curso,
  coalesce(turma, '(sem turma)')            as turma,
  count(*)                                  as leads,
  count(*) filter (where status = 'comprou') as compraram,
  round(100.0 * count(*) filter (where status = 'comprou')
        / nullif(count(*), 0), 1)           as conversao_pct,
  coalesce(sum(valor_pago), 0)              as receita,
  max(criado_em)                            as ultimo_lead
from public.leads_cursos
group by 1, 2
order by 3 desc;

-- View no Postgres roda com o privilégio do DONO por padrão, o que fura o RLS.
-- security_invoker = true faz a view respeitar as regras de quem consulta, e o revoke
-- garante que os papéis públicos nem enxerguem a view.
alter view public.leads_cursos_funil set (security_invoker = true);
revoke all on public.leads_cursos_funil from anon, authenticated;
