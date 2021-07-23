CREATE TABLE show_stats_cache(
    show_stats_cache_id SERIAL PRIMARY KEY,
    stat_id INT UNIQUE NOT NULL,
    url VARCHAR NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);