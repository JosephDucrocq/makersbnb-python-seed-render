DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS spaces CASCADE;
DROP SEQUENCE IF EXISTS spaces_id_seq;

CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    encrypted_password TEXT
);

CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name TEXT,
    availability BOOLEAN,
    location TEXT,
    description TEXT,
    price_per_night FLOAT,
    image_content TEXT,
    user_id int,
        constraint fk_user foreign key(user_id)
        references users(id)
        on delete cascade
);

INSERT INTO users (username, encrypted_password) VALUES ('Luis', 'f5d44b29add0d1a87b9edc82e7c5a9fd'); -- Password: IloveTaylorSwift
INSERT INTO users (username, encrypted_password) VALUES ('Joseph', '6380dcbb2728aa384ed16fc1cf98b1f0'); -- Password: Idoto

INSERT INTO spaces (name, location, description, availability, price_per_night, image_content, user_id) VALUES ('Makers Villa', 'London', 'Beautiful refurbished industrial warehouse', True, 150, 'https://as-images.imgix.net/e0e91fbfcbda875d65ccfc75fcc8d60a-DRC_9449.jpg', 1);
INSERT INTO spaces (name, location, description, availability, price_per_night, image_content, user_id) VALUES ('Josephs farm', 'Gorenflos', 'Traditional French potato farm. Perfect for couple retreat', True, 90, 'https://i.redd.it/1z3atrfp76d01.jpg', 2);