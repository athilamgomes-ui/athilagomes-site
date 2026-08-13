-- ============================================================================
-- visitas — quantas pessoas abrem a página por dia. Sem dado pessoal.
-- Projeto: valhewbvjwdkkvuejrxa · rodar uma vez no SQL Editor · idempotente
-- ============================================================================
--
-- POR QUÊ: hoje o site não registra nada. Quem entra e não compra é invisível,
-- e sem isso não dá para saber se o problema é alcance (pouca gente entrando)
-- ou é a página (muita gente entrando e ninguém comprando). São dois problemas
-- opostos, com soluções opostas.
--
-- O QUE NÃO ENTRA AQUI: nada que identifique a pessoa. Sem IP, sem navegador,
-- sem identificador. Só o dia, de onde veio e nada mais. A página é pública e
-- o público é a cidade dele — vigiar visitante seria traição de confiança, além
-- de problema de LGPD sem necessidade nenhuma.
-- ============================================================================

create table if not exists public.visitas (
  id         bigserial primary key,
  dia        date        not null default current_date,
  origem     text        check (origem is null or length(origem) <= 60),
  referer    text        check (referer is null or length(referer) <= 120),
  criado_em  timestamptz not null default now()
);

create index if not exists visitas_dia_idx on public.visitas (dia);

-- ---------------------------------------------------------------- permissões
-- anon INSERE (a página precisa), mas não lê nem apaga. O relatório sai pela
-- chave de administrador, do Keychain — nunca pela chave pública do site.
alter table public.visitas enable row level security;

drop policy if exists "qualquer um registra a própria visita" on public.visitas;
create policy "qualquer um registra a própria visita"
  on public.visitas for insert to anon, authenticated with check (true);

revoke all on public.visitas from anon, authenticated;
grant insert on public.visitas to anon, authenticated;
grant usage, select on sequence public.visitas_id_seq to anon, authenticated;

-- ---------------------------------------------------------------- conferência
select
  c.relname as tabela,
  case when c.relrowsecurity then 'RLS ligado' else 'RLS DESLIGADO' end as protecao,
  coalesce((select string_agg(distinct g.privilege_type, ', ' order by g.privilege_type)
            from information_schema.role_table_grants g
            where g.table_schema='public' and g.table_name=c.relname
              and g.grantee in ('anon','authenticated')), '—') as permissoes_publicas
from pg_class c join pg_namespace n on n.oid=c.relnamespace
where n.nspname='public' and c.relname in ('visitas','config_curso','leads_cursos');

-- Esperado:  visitas      -> RLS ligado, INSERT
--            config_curso -> RLS ligado, SELECT
--            leads_cursos -> RLS ligado, INSERT
