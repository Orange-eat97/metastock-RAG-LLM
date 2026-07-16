-- Required by RagExplorerUpdateService optimistic locking.
-- Run once against the Supabase project that owns public.explorer_outputs.

alter table public.explorer_outputs
    add column if not exists updated_at timestamptz not null default now(),
    add column if not exists manual_edit_version bigint not null default 0;

create index if not exists explorer_outputs_manual_edit_version_idx
    on public.explorer_outputs (id, manual_edit_version);
