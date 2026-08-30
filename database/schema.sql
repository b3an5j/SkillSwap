CREATE TABLE IF NOT EXISTS users (
	id integer PRIMARY KEY AUTOINCREMENT,
	username text UNIQUE NOT NULL,
	email text UNIQUE NOT NULL,
	password text NOT NULL,
	location text NOT NULL
);

CREATE TABLE IF NOT EXISTS post_category (
	id integer PRIMARY KEY,
	category text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
	id integer PRIMARY KEY AUTOINCREMENT,
	owner integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	title text NOT NULL,
	description text NOT NULL,
	category_id integer NOT NULL REFERENCES post_category(id) ON DELETE CASCADE,
	is_open integer NOT NULL DEFAULT 1 CHECK (is_open IN (0, 1)),
	receive_accepted integer NOT NULL DEFAULT 0 CHECK (receive_accepted >= 0)
);

CREATE TABLE IF NOT EXISTS trade_offers (
	post_send integer NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
	post_receive integer NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
	status integer NOT NULL DEFAULT 0,
	PRIMARY KEY (post_send, post_receive),
	CHECK (post_send != post_receive)
);

CREATE VIRTUAL TABLE IF NOT EXISTS posts_fts USING fts5(
    title,
    description,
    category,
    location,
    tokenize='trigram'
);

-- Keep FTS table in sync when posts change
CREATE TRIGGER IF NOT EXISTS posts_ai AFTER INSERT ON posts BEGIN
    INSERT INTO posts_fts (rowid, title, description, category, location)
    SELECT NEW.id, NEW.title, NEW.description, pc.category, u.location
    FROM post_category pc, users u
    WHERE pc.id = NEW.category_id AND u.id = NEW.owner;
END;

CREATE TRIGGER IF NOT EXISTS posts_ad AFTER DELETE ON posts BEGIN
    DELETE FROM posts_fts WHERE rowid = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS posts_au AFTER UPDATE ON posts BEGIN
    DELETE FROM posts_fts WHERE rowid = OLD.id;
    INSERT INTO posts_fts (rowid, title, description, category, location)
    SELECT NEW.id, NEW.title, NEW.description, pc.category, u.location
    FROM post_category pc, users u
    WHERE pc.id = NEW.category_id AND u.id = NEW.owner;
END;
