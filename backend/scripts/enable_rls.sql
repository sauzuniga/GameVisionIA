-- Corrige las alertas CRITICAL del Security Advisor de Supabase (Semana 6)
-- Corre esto UNA VEZ en el SQL Editor de Supabase.

alter table public.predictions enable row level security;
alter table public.chat_sessions enable row level security;
alter table public.chat_messages enable row level security;
alter table public.request_logs enable row level security;

-- Verificar que las 4 quedaron activas:
select tablename, rowsecurity
from pg_tables
where schemaname = 'public'
  and tablename in ('predictions', 'chat_sessions', 'chat_messages', 'request_logs');
