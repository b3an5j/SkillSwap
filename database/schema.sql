CREATE TABLE IF NOT EXISTS users (
	id integer PRIMARY KEY AUTOINCREMENT,
	username text UNIQUE NOT NULL,
	email text UNIQUE NOT NULL,
	password text NOT NULL,
	location text NOT NULL
);

CREATE TABLE IF NOT EXISTS post_category (
	id integer PRIMARY KEY,
	typename text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
	id integer PRIMARY KEY AUTOINCREMENT,
	owner integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	title text NOT NULL,
	description text NOT NULL,
	category_id integer NOT NULL REFERENCES post_category(id) ON DELETE CASCADE,
	is_open integer NOT NULL DEFAULT 1 CHECK (is_open IN (0, 1))
);

-- FTS4 keeps a searchable projection of a post and its owner's location.
-- post_id is retained for joins, but is not itself full-text indexed.
CREATE VIRTUAL TABLE IF NOT EXISTS posts_search USING fts4(
	post_id UNINDEXED,
	title,
	category,
	location,
	description
);

-- Rebuild on startup so databases created before the FTS index are populated.
DELETE FROM posts_search;
INSERT INTO posts_search (docid, post_id, title, category, location, description)
SELECT posts.id, posts.id, posts.title, post_category.category, users.location, posts.description
FROM posts
JOIN users ON users.id = posts.owner
JOIN post_category ON post_category.id = posts.category_id;

CREATE TRIGGER IF NOT EXISTS posts_search_after_insert
AFTER INSERT ON posts
BEGIN
	INSERT INTO posts_search (docid, post_id, title, category, location, description)
	SELECT NEW.id, NEW.id, NEW.title, NEW.category, users.location, NEW.description
	FROM users WHERE users.id = NEW.owner;
END;

CREATE TRIGGER IF NOT EXISTS posts_search_after_update
AFTER UPDATE ON posts
BEGIN
	DELETE FROM posts_search WHERE docid = OLD.id;
	INSERT INTO posts_search (docid, post_id, title, category, location, description)
	SELECT NEW.id, NEW.id, NEW.title, NEW.category, users.location, NEW.description
	FROM users WHERE users.id = NEW.owner;
END;

CREATE TRIGGER IF NOT EXISTS posts_search_after_delete
AFTER DELETE ON posts
BEGIN
	DELETE FROM posts_search WHERE docid = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS posts_search_after_location_update
AFTER UPDATE OF location ON users
BEGIN
	DELETE FROM posts_search
	WHERE docid IN (SELECT id FROM posts WHERE owner = OLD.id);
	INSERT INTO posts_search (docid, post_id, title, category, location, description)
	SELECT posts.id, posts.id, posts.title, post_category.category, NEW.location, posts.description
	FROM posts WHERE posts.owner = NEW.id
	JOIN post_category ON post_category.id = posts.category_id;
END;
