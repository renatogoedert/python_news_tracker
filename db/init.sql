CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    published_date TIMESTAMP,
    summary TEXT,
    content TEXT,
    source TEXT,
    category TEXT,
    keywords TEXT[],
    language TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
