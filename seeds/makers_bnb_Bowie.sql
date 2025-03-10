DROP TABLE IF EXISTS test_table;
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255));
INSERT INTO test_table (name) VALUES ('first_record');

DROP TABLE IF EXISTS spaces;
DROP SEQUENCE IF EXISTS spaces_id_seq;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;

-- Table creation below --

CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
);

CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    availability BOOLEAN,
    location VARCHAR(255),
    description VARCHAR(255),
    price_per_night FLOAT,

user_id int,
constraint fk_user foreign key(user_id)
    references users(id)
    on delete cascade
);

INSERT INTO users (username, password) VALUES ('Luis', 'IloveTaylorSwift');
INSERT INTO users (username, password) VALUES ('Joseph', 'Idoto');

INSERT INTO spaces (name, location, description, availability, price_per_night, user_id) VALUES ('Makers Villa', 'London', 'Beautiful refurbished industrial warehouse', True, 150, 1);
INSERT INTO spaces (name, location, description, availability, price_per_night, user_id) VALUES ('Josephs farm', 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', True, 90, 2);
