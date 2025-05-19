CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create table index_test (
    id serial uuid default uuid_generate_v4() primary key,
    external_id uuid not null,
    title varchar not null,
    embedding jsonb,
    content text,
    reference jsonb,
    metadata jsonb,
    chunck_number integer,
    total_chunks integer,
    created_at timestamp default now(),
    updated_at timestamp default now(),
);

CREATE INDEX idx_index_test_metadata ON index_test USING GIN (metadata);