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