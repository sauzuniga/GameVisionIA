

-- 1) Activar la extensión (ya viene disponible en el plan gratuito)

create extension if not exists pg_cron with schema extensions;



-- 2) Programar el borrado diario de filas con más de 30 días

select cron.schedule(

    'purge_request_logs_30d',

    '0 3 * * *',

    $$ delete from public.request_logs where created_at < now() - interval '30 days'; $$

);



-- 3) Verificar que quedó programado

select jobid, jobname, schedule, active

from cron.job

where jobname = 'purge_request_logs_30d';




