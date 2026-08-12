-- ============================================================================
-- config_curso — o painel de controle da página, editável sem publicar nada
-- Projeto: valhewbvjwdkkvuejrxa · rodar uma vez no SQL Editor · idempotente
-- ============================================================================
--
-- POR QUÊ: virar o lote ou marcar esgotado exigia editar o index.html e publicar
-- no GitHub. Isso trava o dono numa dependência do agente justamente na hora em
-- que ele precisa agir rápido (esgotar acontece à noite, no fim de semana).
-- Com esta tabela, ele troca o valor no Table Editor e a página obedece na hora.
--
-- SEGURANÇA: aqui só existe estado de exibição — nada sensível. `anon` pode LER
-- (a página precisa), mas NÃO pode escrever: quem altera é o dono, pelo painel.
-- ============================================================================

create table if not exists public.config_curso (
  id            int primary key default 1,
  esgotado      boolean not null default false,
  lote_atual    smallint not null default 1
                check (lote_atual between 1 and 3),
  atualizado_em timestamptz not null default now(),
  constraint apenas_uma_linha check (id = 1)
);

insert into public.config_curso (id, esgotado, lote_atual)
values (1, false, 1)
on conflict (id) do nothing;

-- carimba a data sozinho, para você saber quando foi a última virada
create or replace function public.config_curso_touch()
returns trigger language plpgsql as $$
begin new.atualizado_em = now(); return new; end $$;

drop trigger if exists trg_config_curso_touch on public.config_curso;
create trigger trg_config_curso_touch before update on public.config_curso
  for each row execute function public.config_curso_touch();

-- ---------------------------------------------------------------- permissões
alter table public.config_curso enable row level security;

drop policy if exists "todos podem ler a config" on public.config_curso;
create policy "todos podem ler a config"
  on public.config_curso for select to anon, authenticated using (true);

revoke all on public.config_curso from anon, authenticated;
grant select on public.config_curso to anon, authenticated;

-- ---------------------------------------------------------------- conferência
select
  c.relname as tabela,
  case when c.relrowsecurity then 'RLS ligado' else 'RLS DESLIGADO' end as protecao,
  coalesce((select string_agg(distinct g.privilege_type, ', ' order by g.privilege_type)
            from information_schema.role_table_grants g
            where g.table_schema='public' and g.table_name=c.relname
              and g.grantee in ('anon','authenticated')), '—') as permissoes_publicas
from pg_class c join pg_namespace n on n.oid=c.relnamespace
where n.nspname='public' and c.relname in ('config_curso','leads_cursos');

-- Esperado:  config_curso -> RLS ligado, SELECT
--            leads_cursos -> RLS ligado, INSERT

select * from public.config_curso;
