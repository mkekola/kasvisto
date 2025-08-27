CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE plants (
    id INTEGER PRIMARY KEY,
    plant_name TEXT,
    light TEXT,
    care_info TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    plant_id INTEGER REFERENCES plants,
    user_id INTEGER REFERENCES users,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    category TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    plant_id INTEGER REFERENCES plants,
    image BLOB
);

CREATE TABLE plant_categories (
    id INTEGER PRIMARY KEY,
    plant_id INTEGER REFERENCES plants,
    category TEXT
);