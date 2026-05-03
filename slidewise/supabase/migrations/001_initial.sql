-- Slidewise: initial schema

-- API keys for paid service access
create table api_keys (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete cascade,
    key_hash text not null unique,
    name text not null default 'default',
    revoked boolean not null default false,
    last_used_at timestamptz,
    created_at timestamptz not null default now()
);

create index idx_api_keys_hash on api_keys(key_hash) where not revoked;

-- Extraction jobs
create table extraction_jobs (
    id text primary key,  -- short hex job id
    api_key_id uuid references api_keys(id),
    user_id uuid references auth.users(id),
    video_url text,
    video_title text,
    status text not null default 'processing',  -- processing, completed, failed
    result_json jsonb,
    error_message text,
    processing_time_seconds real,
    created_at timestamptz not null default now(),
    completed_at timestamptz
);

create index idx_jobs_user on extraction_jobs(user_id, created_at desc);
create index idx_jobs_status on extraction_jobs(status);

-- Usage log for billing/analytics
create table usage_log (
    id uuid primary key default gen_random_uuid(),
    api_key_id uuid references api_keys(id),
    job_id text references extraction_jobs(id),
    processing_time_seconds real not null default 0,
    created_at timestamptz not null default now()
);

create index idx_usage_key on usage_log(api_key_id, created_at desc);

-- Storage bucket for keyframe images
insert into storage.buckets (id, name, public)
values ('keyframes', 'keyframes', false)
on conflict do nothing;

-- RLS policies
alter table api_keys enable row level security;
alter table extraction_jobs enable row level security;
alter table usage_log enable row level security;

-- Users can read their own API keys
create policy "Users read own keys" on api_keys
    for select using (auth.uid() = user_id);

-- Users can read their own jobs
create policy "Users read own jobs" on extraction_jobs
    for select using (auth.uid() = user_id);

-- Service role can do everything (API server uses service role key)
create policy "Service role full access api_keys" on api_keys
    for all using (auth.role() = 'service_role');

create policy "Service role full access jobs" on extraction_jobs
    for all using (auth.role() = 'service_role');

create policy "Service role full access usage" on usage_log
    for all using (auth.role() = 'service_role');
