PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS url_store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url text NOT NULL,
    short_url text NOT NULL UNIQUE,
    domain text DEFAULT 'bit.ly',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by text,
    updated_by text,
    group_guid text,
    tags text,
    deeplinks text,
    title text
);
CREATE TABLE IF NOT EXISTS clicks (
    short_url text REFERENCES url_store(short_url) ON DELETE CASCADE,
    domain text REFERENCES url_store(domain) ON DELETE CASCADE,
    click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    minute INTEGER,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER
);