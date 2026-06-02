create table if not exists explorer_outputs (
  id uuid primary key default gen_random_uuid(),

  created_at timestamptz not null default now(),

  backend text not null,
  model text not null,
  user_query text not null,

  explorer_name text not null,
  explorer_description text,
  explorer_code_body text not null,

  col_definitions jsonb not null default '[]'::jsonb,
  full_output_json jsonb not null,

  validation_passed boolean not null default false,
  validation_errors jsonb not null default '[]'::jsonb,

  status text not null default 'generated',

  automator_started_at timestamptz,
  automator_finished_at timestamptz,
  automator_error text
);

create index if not exists idx_explorer_outputs_created_at
on explorer_outputs (created_at desc);

create index if not exists idx_explorer_outputs_status
on explorer_outputs (status);