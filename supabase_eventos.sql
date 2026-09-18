-- ============================================================================
-- eventos_site — ONDE o visitante desiste. Sem dado pessoal.
-- Projeto: valhewbvjwdkkvuejrxa · rodar uma vez no SQL Editor · idempotente
-- ============================================================================
--
-- POR QUÊ (18/09/2026): o anúncio trouxe 73 pessoas pagas (R$ 0,50 cada) e
-- saiu 1 venda na Sympla em 3 dias. A tabela `visitas` só diz que a pessoa
-- ENTROU. Não dá para saber se ela chegou no preço, clicou em comprar ou
-- desistiu antes — e cada resposta pede uma correção diferente.
--
-- Tabela separada de `visitas` DE PROPÓSITO: evento não é visita. Misturar
-- inflaria toda contagem de visitas que já existe (relatórios, runbook).
-- ============================================================================

create table if not exists public.eventos_site (
  id         bigserial primary key,
  tipo       text not null check (tipo in ('viu_preco','clique_comprar','viu_form','clique_whatsapp')),
  origem     text check (origem is null or length(origem) <= 60),
  criado_em  timestamptz not null default now()
);
create index if not exists eventos_site_tipo_idx on public.eventos_site (tipo, criado_em);

-- anon só INSERE; ler é só com a chave de administrador (Keychain).
alter table public.eventos_site enable row level security;
drop policy if exists "qualquer um registra evento" on public.eventos_site;
create policy "qualquer um registra evento"
  on public.eventos_site for insert to anon, authenticated with check (true);
revoke all on public.eventos_site from anon, authenticated;
grant insert on public.eventos_site to anon, authenticated;
grant usage, select on sequence public.eventos_site_id_seq to anon, authenticated;

select c.relname as tabela,
       case when c.relrowsecurity then 'RLS ligado' else 'RLS DESLIGADO' end as protecao
from pg_class c join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relname = 'eventos_site';
-- Esperado: eventos_site -> RLS ligado
