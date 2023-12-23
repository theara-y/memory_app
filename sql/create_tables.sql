CREATE TYPE training_status AS ENUM ('active', 'inactive', 'completed');
CREATE TYPE recall_outcome AS ENUM ('perfect', 'partial', 'failed');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(64) UNIQUE NOT NULL,
    password BYTEA NOT NULL,
    username VARCHAR(32)
);

CREATE TABLE memories (
    id SERIAL PRIMARY KEY,
    prompt TEXT NOT NULL,
    answer TEXT NOT NULL,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    training_status training_status,
    recall_duration_days INT NOT NULL DEFAULT 0,
    total_recall_count INT NOT NULL DEFAULT 0,
    failed_recall_count INT NOT NULL DEFAULT 0,
    partial_recall_count INT NOT NULL DEFAULT 0,
    perfect_recall_count INT NOT NULL DEFAULT 0,
    last_recall_outcome recall_outcome NULL,
    next_recall_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT timezone('UTC', CURRENT_TIMESTAMP),
    last_recall_at TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT timezone('UTC', CURRENT_TIMESTAMP),
    last_modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT timezone('UTC', CURRENT_TIMESTAMP)
);