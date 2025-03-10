DROP TABLE IF EXISTS test_table;
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255));
INSERT INTO test_table (name) VALUES ('first_record');

DROP TABLE IF EXISTS space;
DROP SEQUENCE IF EXISTS space_id_seq;
DROP TABLE IF EXISTS user;
DROP SEQUENCE IF EXISTS user_id_seq;

-- Table creation below --

CREATE SEQUENCE IF NOT EXISTS user_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
);

CREATE SEQUENCE IF NOT EXISTS space_id_seq;
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    availability BOOLEAN,
    location VARCHAR(255),
    description VARCHAR(255),
    price_per_night FLOAT,

user_id int,
constraint fk_user foreign key(user_id)
    references user(id)
    on delete cascade

);

INSERT INTO user (username, password) VALUES ('Luis', 'IloveTaylorSwift');
INSERT INTO user (username, password) VALUES ('Joseph', 'Idoto');

INSERT INTO space (name, availability, location, description, price_per_night, user_id) VALUES ('Makers Villa', True, 'London', 'Beautiful refurbished industrial warehouse', 150, 1);
INSERT INTO space (name, availability, location, description, price_per_night, user_id) VALUES ('Josephs farm', True, 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', 90, 2);
